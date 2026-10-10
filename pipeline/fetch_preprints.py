#!/usr/bin/env python3
"""补抓 bioRxiv/medRxiv 预印本并过滤肝癌关键词, 合并进 raw.json"""
import json, time, urllib.request

import os
BASE = os.environ.get("HCC_BASE", os.path.dirname(os.path.abspath(__file__)))
_raw = json.load(open(os.path.join(BASE, "data/raw.json"), encoding="utf-8"))
D0, D1 = _raw["window_start"], _raw["window_end"]
KW = ["hepatocellular", "liver cancer", "liver tumor", "liver tumour",
      "liver neoplasm", "intrahepatic cholangiocarcinoma", "liver metastasis",
      "liver carcinoma", "liver malignan", "hepatic carcinoma", "hepatic tumor",
      "hepatic malignan", "hcc "]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "hcc-weekly/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))

preprints, raw_total = [], 0
for server in ["biorxiv", "medrxiv"]:
    cursor = 0
    while True:
        js = get(f"https://api.{server}.org/details/{server}/{D0}/{D1}/{cursor}")
        if js.get("messages", [{}])[0].get("status") != "ok":
            print(f"{server} cursor={cursor}: 异常, 停止"); break
        rows = js.get("collection", [])
        raw_total += len(rows)
        for r in rows:
            text = ((r.get("title") or "") + " " + (r.get("abstract") or "")).lower()
            if any(k in text for k in KW):
                preprints.append({
                    "uid": f"doi:{r.get('doi','')}", "source": "preprint", "server": server,
                    "title": (r.get("title") or "").rstrip("."),
                    "journal": f"{server} (预印本)",
                    "date": (r.get("date") or D0)[:10],
                    "authors": ", ".join((r.get("authors") or "").split(";")[:3]),
                    "abstract": r.get("abstract") or "",
                    "doi": r.get("doi", ""), "url": f"https://doi.org/{r.get('doi','')}",
                    "if_value": None, "citations": None,
                })
        total = int(js["messages"][0].get("total", 0))
        cursor += 30
        if cursor >= total or not rows:
            break
        time.sleep(0.3)
    print(f"{server}: 完成, 累计预印本 {len(preprints)}")

data = _raw
data["preprints"] = preprints
data["funnel"]["preprint_raw"] = raw_total
data["funnel"]["preprint_kept"] = len(preprints)
data["funnel"]["preprint_excluded"] = raw_total - len(preprints)
json.dump(data, open(os.path.join(BASE, "data/raw.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"预印本: 拉取{raw_total}, 保留{len(preprints)}; 已合并进 raw.json")
