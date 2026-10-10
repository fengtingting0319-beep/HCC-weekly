#!/usr/bin/env python3
"""肝癌研究周报数据抓取脚本（参照肠癌周报 update.py 口径）
数据源: PubMed (EDAT窗口) / bioRxiv+medRxiv API / ClinicalTrials.gov API v2 / PubMed指南检索
输出: /workspace/hcc_report/data/*.json
"""
import json, os, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import date, timedelta

BASE = os.environ.get("HCC_BASE", os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "data")
os.makedirs(OUT, exist_ok=True)

# 周报窗口: 默认最近7天, 可用 HCC_START/HCC_END 覆盖 (ISO格式)
WINDOW_END = date.fromisoformat(os.environ["HCC_END"]) if os.environ.get("HCC_END") else date.today()
WINDOW_START = date.fromisoformat(os.environ["HCC_START"]) if os.environ.get("HCC_START") else WINDOW_END - timedelta(days=7)
D0, D1 = WINDOW_START.isoformat(), WINDOW_END.isoformat()
print(f"窗口: {D0} 至 {D1}")

def http_get(url, retries=3, wait=2):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "hcc-weekly/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception as e:
            print(f"  retry {i+1}: {e}")
            time.sleep(wait)
    return None

# ---------- ① PubMed ----------
# 肝癌主题: 肝细胞癌为主, 含肝内胆管细胞癌/肝母细胞瘤等肝脏恶性肿瘤
HCC_TERM = ('("carcinoma, hepatocellular"[MeSH] OR "liver neoplasms"[MeSH] '
            'OR "hepatocellular carcinoma"[tiab] OR "liver cancer"[tiab] '
            'OR "liver tumour"[tiab] OR "liver tumor"[tiab] '
            'OR "intrahepatic cholangiocarcinoma"[tiab] OR "liver metastasis"[tiab] OR HCC[tiab])')
pubmed_query = (f'({HCC_TERM}) AND (english[lang] OR lang[lang]) '
                f'AND ("2026/{WINDOW_START.month:02d}/{WINDOW_START.day:02d}"[EDAT] : "2026/{WINDOW_END.month:02d}/{WINDOW_END.day:02d}"[EDAT])'
                .replace("(english[lang] OR lang[lang])", "english[lang]"))
# 简化: 语言限定
pubmed_query = f'({HCC_TERM}) AND english[lang] AND "2026/{WINDOW_START.month:02d}/{WINDOW_START.day:02d}"[EDAT] : "2026/{WINDOW_END.month:02d}/{WINDOW_END.day:02d}"[EDAT]'
print("PubMed检索式:", pubmed_query)

base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
u = f"{base}/esearch.fcgi?db=pubmed&retmode=json&retmax=2000&term={urllib.parse.quote(pubmed_query)}"
js = json.loads(http_get(u))
pmids = js["esearchresult"]["idlist"]
pubmed_raw = int(js["esearchresult"]["count"])
print(f"PubMed命中: {pubmed_raw}, 取回 {len(pmids)} 个PMID")

papers = []
# 分批 esummary (期刊/日期/DOI) + efetch (摘要/类型)
def batch(lst, n=200):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

summaries = {}
for chunk in batch(pmids):
    u = f"{base}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(chunk)}"
    js = json.loads(http_get(u))
    for r in js.get("result", {}).get("uids", []):
        summaries[r] = js["result"][r]
    time.sleep(0.4)

abstracts = {}
for chunk in batch(pmids):
    u = f"{base}/efetch.fcgi?db=pubmed&retmode=xml&id={','.join(chunk)}"
    xml_text = http_get(u)
    if not xml_text:
        continue
    try:
        root = ET.fromstring(xml_text)
        for art in root.findall(".//PubmedArticle"):
            pmid = art.findtext(".//PMID")
            abst = " ".join(t.text or "" for t in art.findall(".//Abstract/AbstractText"))
            abst += " " + " ".join(t.text or "" for t in art.findall(".//Abstract/AbstractText/i"))
            pubtypes = [pt.text for pt in art.findall(".//PublicationType")]
            abstracts[pmid] = {"abstract": abst.strip(), "pubtypes": pubtypes}
    except Exception as e:
        print("  efetch parse error:", e)
    time.sleep(0.4)

IF_TABLE = {
    # JCR 2024 影响因子静态对照表 (主要肿瘤/肝病期刊, best-effort)
    "CA Cancer J Clin": 254.7, "Lancet Oncol": 56.7, "JAMA Oncol": 28.5, "Ann Oncol": 39.5,
    "Signal Transduct Target Ther": 40.8, "Nat Rev Clin Oncol": 81.1, "Lancet": 98.4,
    "N Engl J Med": 158.5, "JAMA": 63.1, "BMJ": 93.6, "Nat Med": 58.7, "Nature": 64.8,
    "Science": 44.7, "Cell": 64.5, "Cancer Cell": 48.8, "Nat Rev Gastroenterol Hepatol": 65.1,
    "Gastroenterology": 25.7, "J Hepatol": 30.1, "Hepatology": 17.4, "Gut": 23.0,
    "Ann Surg": 9.5, "J Clin Oncol": 42.1, "Lancet Gastroenterol Hepatol": 30.9,
    "Nat Commun": 14.7, "Cancer Discov": 29.5, "J Natl Cancer Inst": 9.9,
    "Clin Cancer Res": 11.5, "Oncogene": 6.9, "Mol Cancer": 27.7, "Immunity": 32.4,
    "Cancer": 6.0, "Eur J Cancer": 8.4, "Liver Cancer": 6.5, "J Hepatocell Carcinoma": 3.0,
    "Front Oncol": 3.5, "World J Gastroenterol": 4.3, "J Gastrointest Surg": 2.2,
    "Ann Surg Oncol": 5.4, "Int J Cancer": 6.4, "Cancers": 4.5, "Oncologist": 5.1,
    "Hepatol Res": 4.6, "J Gastroenterol": 6.9, "Dig Dis Sci": 2.8, "Liver Transpl": 3.0,
    "Transplantation": 3.9, "Surg Oncol": 3.3, "HPB": 3.0, "Radiother Oncol": 7.0,
    "Int J Radiat Oncol Biol Phys": 7.4, "Cardiovasc Intervent Radiol": 2.6,
    "J Vasc Interv Radiol": 3.9, "Abdom Radiol": 2.7, "Eur Radiol": 4.7, "Radiology": 12.1,
    "Lancet Gastroenterology Hepatology": 30.9, "Cell Res": 28.1, "Sci Transl Med": 17.6,
    "Cancer Lett": 9.1, "Oncotarget": 2.5, "Theranostics": 12.4, "J Immunother Cancer": 10.9,
    "Nat Rev Drug Discov": 68.5, "Trends Cancer": 17.8, "Genome Med": 12.3, "EBioMedicine": 11.1,
    "Cell Mol Immunol": 24.2, "J Exp Med": 15.3, "Gastrointest Endosc": 7.7,
    "Am J Gastroenterol": 8.0, "Aliment Pharmacol Ther": 6.7, "J Virchows Arch": 0,
    "Virchows Arch": 3.4, "Mod Pathol": 5.7, "Histopathology": 5.0,
}

for pmid in pmids:
    s = summaries.get(pmid)
    if not s:
        continue
    abst_info = abstracts.get(pmid, {})
    pubtypes = abst_info.get("pubtypes", [])
    journal = s.get("source", "")
    # 提取完整期刊名
    full_jname = s.get("fulljournalname", journal)
    doi = ""
    for aid in s.get("articleids", []):
        if aid.get("idtype") == "doi":
            doi = aid.get("value", "")
    date_str = s.get("pubdate", "")
    authors = ", ".join(a.get("name", "") for a in s.get("authors", [])[:3])
    if len(s.get("authors", [])) > 3:
        authors += " 等"
    papers.append({
        "uid": f"pmid:{pmid}",
        "source": "pubmed",
        "title": s.get("title", "").rstrip("."),
        "journal": full_jname,
        "date": date_str,
        "authors": authors,
        "abstract": abst_info.get("abstract", ""),
        "doi": doi,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        "pmid": pmid,
        "pubtypes": pubtypes,
        "if_value": IF_TABLE.get(full_jname),
        "citations": None,
    })

print(f"PubMed解析: {len(papers)} 篇")

# ---------- ② bioRxiv / medRxiv ----------
preprint_raw, preprints = 0, []
for server in ["biorxiv", "medrxiv"]:
    u = f"https://api.{server}.org/details/{server}/retrieval/date-range?from={D0}&to={D1}&cursor=0&format=json"
    txt = http_get(u)
    if not txt:
        print(f"{server} API失败, 跳过")
        continue
    try:
        js = json.loads(txt)
    except Exception as e:
        print(f"{server} JSON解析失败: {e}")
        continue
    msgs = js.get("messages", [])
    if msgs and msgs[0].get("status") != "ok":
        print(f"{server}: {msgs[0].get('status')}")
        continue
    rows = js.get("collection", [])
    preprint_raw += len(rows)
    for r in rows:
        ab = r.get("abstract", "") or ""
        ti = r.get("title", "") or ""
        text = (ti + " " + ab).lower()
        kw = ["hepatocellular", "liver cancer", "liver tumor", "liver tumour",
              "liver neoplasm", "intrahepatic cholangiocarcinoma", "liver metastasis",
              "hcc", "liver carcinoma"]
        if any(k in text for k in kw):
            preprints.append({
                "uid": f"doi:{r.get('doi','')}",
                "source": "preprint", "server": server,
                "title": ti, "journal": f"{server} (预印本)",
                "date": r.get("date", D0)[:10],
                "authors": ", ".join((r.get("authors", "") or "").split(";")[:3]),
                "abstract": ab, "doi": r.get("doi", ""),
                "url": f"https://doi.org/{r.get('doi','')}",
                "if_value": None, "citations": None,
            })
    print(f"{server}: 拉取{len(rows)}, 累计预印本{len(preprints)}")

# ---------- ③ ClinicalTrials.gov ----------
ctg_condition = "hepatocellular carcinoma OR liver cancer OR intrahepatic cholangiocarcinoma OR liver tumor"
u = ("https://clinicaltrials.gov/api/v2/studies?query.cond=" + urllib.parse.quote(ctg_condition) +
     f"&filter.advanced=AREA%5BLastUpdatePostDate%5DRANGE%5B{D0}%2C{D1}%5D" +
     "&pageSize=100&countTotal=true&fields=NCTId|BriefTitle|OverallStatus|Phase|EnrollmentCount|" +
     "Condition|InterventionName|LastUpdatePostDate|StudyType|LeadSponsorName|StartDate")
txt = http_get(u)
trials = []
trials_raw = 0
if txt:
    js = json.loads(txt)
    trials_raw = js.get("totalCount", 0)
    for st in js.get("studies", []):
        p = st.get("protocolSection", {})
        ident = p.get("identificationModule", {})
        status = p.get("statusModule", {})
        desc = p.get("descriptionModule", {})
        arms = p.get("armsInterventionsModule", {})
        interv = ", ".join(i.get("name", "") for i in arms.get("interventions", [])[:4])
        trials.append({
            "regid": ident.get("nctId", ""),
            "title": ident.get("briefTitle", ""),
            "status": status.get("overallStatus", ""),
            "phase": (p.get("designModule", {}).get("phases") or ["N/A"]),
            "enrollment": p.get("designModule", {}).get("enrollmentInfo", {}).get("count"),
            "interventions": interv,
            "date": (status.get("lastUpdatePostDateStruct", {}) or {}).get("date", ""),
            "created": (status.get("startDateStruct", {}) or {}).get("date", ""),
            "url": f"https://clinicaltrials.gov/study/{ident.get('nctId','')}",
            "sponsor": (p.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}) or {}).get("name", ""),
        })
    print(f"ClinicalTrials.gov: {trials_raw} 项命中, 取回{len(trials)}")

# ---------- ④ 指南与共识 ----------
guideline_query = (f'({HCC_TERM}) AND (practice guideline[pt] OR guideline[pt] OR consensus[ti] '
                   f'OR guideline[ti] OR "practice guidance"[ti]) AND english[lang] '
                   f'AND "2020/01/01"[EDAT] : "2026/{WINDOW_END.month:02d}/{WINDOW_END.day:02d}"[EDAT]')
u = f"{base}/esearch.fcgi?db=pubmed&retmode=json&retmax=100&term={urllib.parse.quote(guideline_query)}"
js = json.loads(http_get(u))
gpmids = js["esearchresult"]["idlist"]
guidelines_raw = int(js["esearchresult"]["count"])
print(f"指南命中: {guidelines_raw}")

guidelines = []
if gpmids:
    u = f"{base}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(gpmids)}"
    js = json.loads(http_get(u))
    gsumm = {r: js["result"][r] for r in js.get("result", {}).get("uids", [])}
    u = f"{base}/efetch.fcgi?db=pubmed&retmode=xml&id={','.join(gpmids)}"
    xml_text = http_get(u)
    gabs = {}
    if xml_text:
        try:
            root = ET.fromstring(xml_text)
            for art in root.findall(".//PubmedArticle"):
                pmid = art.findtext(".//PMID")
                abst = " ".join(t.text or "" for t in art.findall(".//Abstract/AbstractText"))
                gabs[pmid] = abst.strip()
        except Exception as e:
            print("  指南efetch解析失败:", e)
    for pmid in gpmids:
        s = gsumm.get(pmid)
        if not s:
            continue
        doi = ""
        for aid in s.get("articleids", []):
            if aid.get("idtype") == "doi":
                doi = aid.get("value", "")
        guidelines.append({
            "uid": f"pmid:{pmid}",
            "title": s.get("title", "").rstrip("."),
            "journal": s.get("fulljournalname", ""),
            "date": s.get("pubdate", ""),
            "authors": ", ".join(a.get("name", "") for a in s.get("authors", [])[:3]),
            "abstract": gabs.get(pmid, ""),
            "doi": doi,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "china": any(k in (s.get("title", "") + s.get("fulljournalname", "")).lower()
                         for k in ["china", "chinese", "caca", "csco"]),
            "category": "指南/共识",
        })

# ---------- 汇总 ----------
# 去重 (DOI)
seen, dedup_removed = set(), 0
deduped = []
for p in papers:
    key = p.get("doi", "").lower() or p["uid"]
    if p.get("doi") and key in seen:
        dedup_removed += 1
        continue
    seen.add(key)
    deduped.append(p)

no_abstract = sum(1 for p in deduped if not p.get("abstract"))
funnel = {
    "pubmed_raw": pubmed_raw, "preprint_raw": preprint_raw,
    "preprint_kept": len(preprints), "preprint_excluded": preprint_raw - len(preprints),
    "trials_raw": trials_raw, "guidelines_raw": guidelines_raw,
    "dedup_removed": dedup_removed, "no_abstract": no_abstract,
    "included": len(deduped),
}

os.makedirs(OUT, exist_ok=True)
json.dump({"window_start": D0, "window_end": D1, "funnel": funnel,
           "pubmed_query": pubmed_query, "guideline_query": guideline_query,
           "ctg_condition": ctg_condition,
           "papers": deduped, "preprints": preprints,
           "trials": trials, "guidelines": guidelines},
          open(f"{OUT}/raw.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n汇总: 期刊论文{len(deduped)} (去重{dedup_removed}, 无摘要{no_abstract}) | "
      f"预印本{len(preprints)} | 试验{len(trials)} | 指南{len(guidelines)}")
print(f"输出: {OUT}/raw.json")
