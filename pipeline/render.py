#!/usr/bin/env python3
"""渲染肝癌研究周报 HTML (合并数据+LLM标注 → Jinja2)"""
import json, re, sys, hashlib, os, glob
from datetime import datetime, timezone
BASE = os.environ.get("HCC_BASE", os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.environ.get("HCC_OUT", "/mnt/results")
sys.path.insert(0, BASE)
from annotations import PAPERS, PREPRINTS, TRIALS, GUIDELINES, HOTSPOTS, GRADE_DEFS, CATEGORIES, STUDY_TYPES

from jinja2 import Environment, FileSystemLoader

data = json.load(open(os.path.join(BASE, "data/clean.json"), encoding="utf-8"))
D0, D1 = data["window_start"], data["window_end"]

MONTHS = {m: i for i, m in enumerate(
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], 1)}

def parse_date(s):
    if not s:
        return None
    m = re.match(r"^(\d{4})\s+([A-Za-z]{3})(?:\s+(\d{1,2}))?", s.strip())
    if m:
        y, mon, d = int(m.group(1)), MONTHS.get(m.group(2)), m.group(3)
        if mon:
            return datetime(y, mon, int(d or 1)).date()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s.strip())
    if m:
        return datetime.strptime(m.group(0)[:10], "%Y-%m-%d").date()
    m = re.match(r"^(\d{4})$", s.strip())
    if m:
        return datetime(int(m.group(1)), 1, 1).date()
    return None

def label_display(week_key):
    m = re.match(r"^(\d{4})-W(\d{1,2})$", week_key)
    if m:
        return f"{m.group(1)}年第{int(m.group(2))}周"
    return week_key

# ---------- 组装期刊论文 ----------
papers = []
for p in data["papers"]:
    pmid = p["pmid"]
    ann = PAPERS.get(pmid, {})
    ifv = p.get("if_value")
    impact = min(20, round(ifv / 2)) if ifv else 0
    design = ann.get("design", 6)
    validation = ann.get("validation", 3)
    mechanism = ann.get("mechanism", 3)
    fit = ann.get("fit", 12)
    score = design + validation + mechanism + impact + fit
    d = parse_date(p.get("date"))
    # 其他肿瘤肝转移 → topic 标记
    title_abs = (p["title"] + " " + (p.get("abstract") or "")).lower()
    is_liver_mets = ("metastas" in title_abs and not
                     any(k in title_abs for k in ["hepatocellular carcinoma", "intrahepatic cholangio", "liver cancer", "hepatoblastoma", "fibrolamellar"]))
    papers.append({
        **p,
        "cn_title": ann.get("cn_title"),
        "insight": ann.get("insight"),
        "grade": ann.get("grade", "C"),
        "grade_rationale": ann.get("grade_rationale"),
        "category": ann.get("category", p.get("topic", "其他")),
        "topic": "肝转移" if is_liver_mets else None,
        "study_type": ann.get("study_type", p.get("study_type", "其他")),
        "design": design, "validation": validation, "mechanism": mechanism,
        "impact": impact, "fit": fit, "score": score,
        "top": ann.get("top", False),
        "reading": ann.get("reading"),
        "practice_changing": ann.get("grade") == "S",
        "cas": None,
        "_date": d,
    })

# rank: 本期IF前10
by_if = sorted([p for p in papers if p["if_value"]], key=lambda x: -x["if_value"])
for i, p in enumerate(by_if[:10]):
    p["rank"] = i + 1

# 无摘要且未精标注的排除 (述评/通信类保留)
annotated = set(PAPERS.keys())
kept, no_abs_excluded = [], 0
for p in papers:
    if not (p.get("abstract") or "").strip() and p["pmid"] not in annotated:
        no_abs_excluded += 1
        continue
    kept.append(p)
papers = kept

# 周分组: 周报窗口统一为一组 (EDAT窗口口径, 出版日期可能早于窗口)
_wd = parse_date(D0)
_iso = _wd.isocalendar()
_week_key = f"{_iso[0]}-W{_iso[1]:02d}"
week_groups = [(_week_key, sorted(papers, key=lambda x: (x["_date"] or datetime(1970, 1, 1).date()), reverse=True))]

top10 = sorted([p for p in papers if p.get("top")], key=lambda x: -x["score"])[:10]

# ---------- 预印本 ----------
preprints = []
for p in data["preprints"]:
    ann = PREPRINTS.get(p.get("doi", ""), {})
    title_abs = (p["title"] + " " + (p.get("abstract") or "")).lower()
    is_liver_mets = "metastas" in title_abs and not any(
        k in title_abs for k in ["hepatocellular", "liver cancer", "cholangio"])
    preprints.append({
        **p,
        "cn_title": ann.get("cn_title"),
        "insight": ann.get("insight"),
        "category": "机制与转化" if "organoid" in title_abs or "methylation" in title_abs or "sequencing" in title_abs else "诊断与标志物",
        "topic": "肝转移" if is_liver_mets else None,
        "study_type": "基础研究",
        "score": 0,
    })

# ---------- 临床试验 ----------
STATUS_CN = {"RECRUITING": "招募中", "NOT_YET_RECRUITING": "尚未招募", "ACTIVE_NOT_RECRUITING": "活跃不招募",
             "COMPLETED": "已完成", "TERMINATED": "终止", "SUSPENDED": "暂停", "WITHDRAWN": "已撤回",
             "ENROLLING_BY_INVITATION": "受邀入组", "UNKNOWN": "未知"}
PHASE_CN = {"PHASE1": "I期", "PHASE2": "II期", "PHASE3": "III期", "PHASE4": "IV期",
            "PHASE1,PHASE2": "I/II期", "PHASE2,PHASE3": "II/III期", "NA": "不适用", "N/A": "不适用"}
trials = []
for t in data["trials"]:
    title_l = (t.get("title") or "").lower()
    kw = ["hepatocellular", "liver cancer", "liver tumor", "liver metast", "intrahepatic",
          "cholangio", "liver lesion", "liver tumour", "hcc", "liver transplantation",
          "liver resection", "hepatectomy", "fibrolamellar", "liver ablation", "liver met"]
    if not any(k in title_l for k in kw):
        continue
    ph = t.get("phase")
    if isinstance(ph, list):
        ph = ",".join(ph)
    trials.append({
        **t,
        "cn_title": TRIALS.get(t["regid"], {}).get("cn_title"),
        "status": STATUS_CN.get(t.get("status"), t.get("status")),
        "phase": PHASE_CN.get(ph, ph or "不适用"),
    })
trials.sort(key=lambda x: x.get("date") or "", reverse=True)

# ---------- 指南 ----------
guidelines = []
for g in data["guidelines"]:
    pmid = g["uid"].split(":")[1]
    if pmid not in GUIDELINES:
        continue
    ann = GUIDELINES[pmid]
    guidelines.append({**g, **ann, "study_type": "指南", "score": 0})
guidelines.sort(key=lambda x: x.get("date") or "", reverse=True)

# ---------- 统计 ----------
if_vals = [p["if_value"] for p in papers if p["if_value"]]
grade_counts = {g: sum(1 for p in papers if p.get("grade") == g) for g in ["S", "A", "B", "C"]}
stats = {
    "n_papers": len(papers), "n_preprints": len(preprints), "n_trials": len(trials),
    "n_guidelines": len(guidelines),
    "avg_if": round(sum(if_vals) / len(if_vals), 1) if if_vals else None,
    "max_if": max(if_vals) if if_vals else None,
    "n_no_if": sum(1 for p in papers if not p["if_value"]),
    "grade_counts": grade_counts,
}
funnel = dict(data["funnel"])
funnel["no_abstract"] = no_abs_excluded
funnel["included"] = len(papers) + len(preprints)

if_verified = []
seen_j = set()
for p in by_if:
    if p["journal"] not in seen_j and p["if_value"]:
        seen_j.add(p["journal"])
        if_verified.append({"journal": p["journal"], "if": p["if_value"]})

context = {
    "window_start": D0, "window_end": D1,
    "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "if_year": 2024, "cas_year": 2024,
    "stats": stats, "funnel": funnel,
    "pubmed_query": data["pubmed_query"],
    "guideline_query": data["guideline_query"],
    "ctg_condition": data["ctg_condition"],
    "preprint_onco": ["hepatocellular", "liver cancer", "liver tumor", "intrahepatic cholangiocarcinoma",
                      "liver metastasis", "HCC", "hepatoblastoma", "fibrolamellar"],
    "grade_defs": GRADE_DEFS, "categories": CATEGORIES, "study_types": STUDY_TYPES,
    "week_groups": week_groups, "top10": top10,
    "preprints": preprints, "trials": trials, "guidelines": guidelines,
    "hotspots": HOTSPOTS, "if_verified": if_verified,
}

env = Environment(loader=FileSystemLoader(BASE))
env.filters["label_display"] = label_display
tmpl = env.get_template("index_hcc.html.j2")
html = tmpl.render(**context)

# 自动期号: 同窗口覆盖已有期, 新窗口才递增期号 (幂等, 重复触发不产生重复期)
os.makedirs(OUTDIR, exist_ok=True)
existing = glob.glob(os.path.join(OUTDIR, "肝癌研究周报_*_第*期.html"))
same_window = [f for f in existing if f"{D0}-{D1}" in os.path.basename(f)]
if same_window:
    out = same_window[0]   # 覆盖同窗口旧版
else:
    issue_no = len(existing) + 1
    out = os.path.join(OUTDIR, f"肝癌研究周报_{D0}-{D1}_第{issue_no}期.html")
open(out, "w", encoding="utf-8").write(html)

# ---- 历史总目录页 ----
issues = []
for f in sorted(glob.glob(os.path.join(OUTDIR, "肝癌研究周报_*_第*期.html")), reverse=True):
    m = re.search(r"肝癌研究周报_(\d{4}-\d{2}-\d{2})-(\d{4}-\d{2}-\d{2})_第(\d+)期", os.path.basename(f))
    if m:
        issues.append(dict(start=m.group(1), end=m.group(2), no=int(m.group(3)),
                           file=os.path.basename(f)))
index_html = ["<!DOCTYPE html><html lang=\"zh-CN\"><head><meta charset=\"UTF-8\">",
              "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">",
              "<title>肝癌研究周报 · 总目录</title>",
              "<style>body{font-family:'Liberation Sans','PingFang SC','Microsoft YaHei',sans-serif;",
              "background:#f4f6f9;color:#1e293b;max-width:860px;margin:0 auto;padding:40px 20px}",
              "h1{color:#0b2545;border-left:4px solid #1d6fb8;padding-left:12px}",
              ".iss{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px 22px;",
              "margin:12px 0;display:flex;justify-content:space-between;align-items:center}",
              ".iss:hover{box-shadow:0 4px 16px rgba(19,64,116,.12)}",
              "a{color:#1d6fb8;text-decoration:none;font-weight:600;font-size:16px}",
              ".no{background:#e8f1fa;color:#134074;border-radius:999px;padding:3px 14px;font-size:13px}",
              ".tip{color:#64748b;font-size:13px;margin-top:24px}</style></head><body>",
              "<h1>肝癌研究周报 · 总目录</h1>",
              "<p class='tip'>每周一期 · 覆盖原发性肝癌全域（其他肿瘤肝转移为重点亚方向）· 点击期号进入当期</p>"]
for it in issues:
    index_html.append(f"<div class='iss'><a href='{it['file']}'>第 {it['no']} 期：{it['start']} 至 {it['end']}</a>"
                      f"<span class='no'>第 {it['no']} 期</span></div>")
index_html.append("</body></html>")
open(os.path.join(OUTDIR, "肝癌研究周报_总目录.html"), "w", encoding="utf-8").write("\n".join(index_html))
# 同步输出 index.html 作为 Pages 根路径入口
open(os.path.join(OUTDIR, "index.html"), "w", encoding="utf-8").write("\n".join(index_html))
print(f"总目录已更新: 肝癌研究周报_总目录.html ({len(issues)} 期)")
print(f"渲染完成: {out} ({len(html)//1024} KB)")
print(f"统计: {stats}")
print(f"漏斗: {funnel}")
print(f"校验: {funnel['pubmed_raw']+funnel['preprint_raw']} - {funnel['preprint_excluded']} - {funnel['dedup_removed']} - {funnel['excluded_irrelevant']} - {funnel['no_abstract']} = {funnel['pubmed_raw']+funnel['preprint_raw']-funnel['preprint_excluded']-funnel['dedup_removed']-funnel['excluded_irrelevant']-funnel['no_abstract']} (纳入 {funnel['included']})")
print(f"Top10: {[p['pmid'] for p in top10]}")
