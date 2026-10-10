#!/usr/bin/env python3
"""数据清洗: IF规范化匹配 + 相关性过滤 + 规则预分类 + 生成标注工作表"""
import json, re, os

BASE = os.environ.get("HCC_BASE", os.path.dirname(os.path.abspath(__file__)))

data = json.load(open(os.path.join(BASE, "data/raw.json"), encoding="utf-8"))

# JCR2024 IF 静态对照表 (best-effort)
IF_TABLE = {
    "ca cancer j clin": 254.7, "lancet oncol": 56.7, "jama oncol": 28.5, "ann oncol": 39.5,
    "signal transduct target ther": 40.8, "nat rev clin oncol": 81.1, "lancet": 98.4,
    "n engl j med": 158.5, "jama": 63.1, "bmj": 93.6, "nat med": 58.7, "nature": 64.8,
    "science": 44.7, "cell": 64.5, "cancer cell": 48.8, "nat rev gastroenterol hepatol": 65.1,
    "gastroenterology": 25.7, "j hepatol": 30.1, "hepatology": 17.4, "gut": 23.0,
    "ann surg": 9.5, "j clin oncol": 42.1, "lancet gastroenterol hepatol": 30.9,
    "nat commun": 14.7, "cancer discov": 29.5, "j natl cancer inst": 9.9,
    "clin cancer res": 11.5, "oncogene": 6.9, "mol cancer": 27.7, "immunity": 32.4,
    "cancer": 6.0, "eur j cancer": 8.4, "liver cancer": 6.5,
    "front oncol": 3.5, "world j gastroenterol": 4.3, "ann surg oncol": 5.4,
    "int j cancer": 6.4, "cancers": 4.5, "oncologist": 5.1, "hepatol res": 4.6,
    "j gastroenterol": 6.9, "liver transpl": 3.0, "transplantation": 3.9,
    "radiother oncol": 7.0, "int j radiat oncol biol phys": 7.4, "radiology": 12.1,
    "cell res": 28.1, "sci transl med": 17.6, "cancer lett": 9.1, "theranostics": 12.4,
    "j immunother cancer": 10.9, "nat rev drug discov": 68.5, "trends cancer": 17.8,
    "genome med": 12.3, "ebiomedicine": 11.1, "cell mol immunol": 24.2, "j exp med": 15.3,
    "am j gastroenterol": 8.0, "aliment pharmacol ther": 6.7, "mod pathol": 5.7,
    "histopathology": 5.0, "adv sci": 14.1, "adv mater": 27.4, "biomaterials": 12.8,
    "acta biomater": 9.4, "bioact mater": 18.0, "j nanobiotechnology": 10.7,
    "acs nano": 15.3, "nat biotechnol": 33.1, "nat genet": 36.3, "genome biol": 22.5,
    "hepatol int": 6.0, "clin mol hepatol": 14.6, "gut liver": 4.0, "liver int": 6.0,
    "j viral hepat": 3.0, "dig dis": 3.0, "j gastroenterol hepatol": 3.2,
    "eur radiol": 4.7, "acad radiol": 4.0, "eur j surg oncol": 3.8, "surgery": 3.6,
    "surg endosc": 3.0, "j surg oncol": 3.3, "hpb": 3.0, "world j surg": 2.8,
    "j hepatocell carcinom": 3.0, "j hepatocell carcinoma": 3.0, "target oncol": 4.4,
    "cancer med": 3.0, "cancer res": 12.9, "cancer treat rev": 15.3, "sem oncol": 4.0,
    "semin oncol": 4.0, "oncol lett": 2.2, "oncol rep": 3.2, "biomed pharmacother": 6.8,
    "metabolism": 9.6, "cell rep": 7.5, "pnas": 9.4, "proc natl acad sci": 9.4,
    "mol cell proteomics": 6.7, "biochem pharmacol": 5.3, "br j cancer": 6.8,
    "mol biomed": 8.7, "medcomm": 9.9, "j exp clin cancer res": 11.4,
    "exp hematol oncol": 12.0, "j big data": 0, "npj digit med": 12.4,
    "radiographics": 5.2, "j magn reson imaging": 4.4, "eur j radiol": 3.2,
    "med phys": 3.5, "j med imaging": 2.0, "quant imaging med surg": 2.9,
    "front immunol": 5.7, "front pharmacol": 4.4, "front med": 3.1, "front nutr": 4.0,
    "j clin med": 2.9, "biomedicines": 3.9, "pharmaceuticals": 4.3, "int j mol sci": 4.5,
    "nutrients": 4.8, "j clin transl hepatol": 0, "j clin transl res": 0,
    "clin transl gastroenterol": 2.6, "scand j gastroentero": 0, "scand j gastroenterol": 2.2,
    "united european gastroenterol": 3.0, "jgh open": 1.8, "medicine": 1.3,
    "cureus": 1.2, "ploS one": 2.6, "plos one": 2.6, "sci rep": 3.8,
    "am j clin nutr": 6.5, "int j epidemiol": 5.3, "am j epidemiol": 3.8,
    "j natl compr canc netw": 4.2, "ann transl med": 1.9, "j cancer": 3.5,
    "transl oncol": 4.9, "cancer sci": 3.0, "cancer res treat": 3.6,
    "invest new drugs": 3.0, "esmo open": 6.5, "clin colorectal cancer": 3.0,
    "jco gastrointest oncol": 0, "ann surg open": 0, "j am coll surg": 3.6,
}

def norm(j):
    j = (j or "").lower()
    j = re.sub(r"\(.*?\)", "", j)          # 去括号
    j = re.sub(r"[^a-z ]", " ", j)
    j = re.sub(r"\s+", " ", j).strip()
    return j

# 规范化期刊全名 → JCR2024 IF (精确匹配, best-effort 静态表)
JOURNAL_IF = {
    "gut": 23.0, "radiology": 12.1, "nature communications": 14.7,
    "the lancet gastroenterology hepatology": 30.9, "lancet gastroenterology hepatology": 30.9,
    "hepatology": 17.4, "journal of hepatology": 30.1, "cancer research": 12.9,
    "advanced science": 14.1, "advanced materials": 27.4,
    "clinical and molecular hepatology": 14.6, "hepatology international": 6.0,
    "liver international official journal of the international association for the study of the liver": 6.0,
    "liver international": 6.0, "journal of hepatocellular carcinoma": 3.0,
    "frontiers in immunology": 5.7, "european radiology": 4.7, "cancer medicine": 3.0,
    "alimentary pharmacology therapeutics": 6.7, "annals of surgical oncology": 5.4,
    "international journal of cancer": 6.4, "biomedicine pharmacotherapy biomedecine pharmacotherapie": 6.8,
    "journal of nanobiotechnology": 10.7, "journal for immunotherapy of cancer": 10.9,
    "clinical and translational medicine": 10.6, "molecular biomedicine": 8.7,
    "medcomm": 9.9, "acta biomaterialia": 9.4, "biomaterials research": 14.5,
    "exploration": 8.9, "biochemical pharmacology": 5.3, "modern pathology an official journal of the united states and canadian academy of pathology inc": 5.7,
    "molecular cellular proteomics mcp": 6.7, "the journal of clinical investigation": 13.3,
    "targeted oncology": 4.4, "the oncologist": 5.1, "seminars in oncology": 4.0,
    "surgery": 3.6, "surgical endoscopy": 3.0,
    "european journal of surgical oncology the journal of the european society of surgical oncology and the british association of surgical oncology": 3.8,
    "cardiovascular and interventional radiology": 2.6,
    "journal of vascular and interventional radiology jvir": 3.9,
    "korean journal of radiology": 4.4,
    "radiographics a review publication of the radiological society of north america inc": 5.2,
    "academic radiology": 4.0, "journal of medical imaging and radiation oncology": 2.0,
    "medical physics": 3.5, "radiation oncology": 2.9, "journal of viral hepatitis": 3.0,
    "journal of gastroenterology and hepatology": 3.2, "gut and liver": 4.0,
    "annals of hepatology": 3.0, "jhep reports innovation in hepatology": 6.1,
    "hepatobiliary pancreatic diseases international hbpd int": 5.2,
    "international journal of nanomedicine": 6.6, "immunotherapy": 2.9,
    "american journal of clinical oncology": 3.2, "cancer research and treatment": 3.6,
    "cancer science": 3.0, "cellular and molecular gastroenterology and hepatology": 7.4,
    "clinical and experimental medicine": 3.9,
    "european journal of gastroenterology hepatology": 2.6, "human pathology": 4.0,
    "international immunopharmacology": 4.2, "journal of clinical and experimental hepatology": 3.9,
    "oncology letters": 2.2, "phytomedicine international journal of phytotherapy and phytopharmacology": 7.9,
    "plos one": 2.6, "cureus": 1.2, "cell death disease": 8.1, "cell insight": 3.5,
    "genes diseases": 6.4, "iliver": 2.0, "health care science": 1.5,
    "transplantation proceedings": 1.0, "updates in surgery": 2.5, "tissue cell": 2.7,
    "toxicology and applied pharmacology": 3.3, "virus research": 2.8, "daru journal of faculty of pharmacy tehran university of medical sciences": 3.0,
    "analytica chimica acta": 5.7, "analytical biochemistry": 2.9,
    "biochemical and biophysical research communications": 2.7, "biofactors": 4.5,
    "biotechnology letters": 2.0, "cancer reports": 1.5, "current medical imaging": 1.2,
    "current pharmaceutical design": 2.6, "current topics in medicinal chemistry": 2.9,
    "experimental and therapeutic medicine": 2.1, "immunity inflammation and disease": 2.9,
    "international journal of computer assisted radiology and surgery": 2.9,
    "jmir research protocols": 3.0, "journal of applied clinical medical physics": 2.9,
    "journal of gastrointestinal cancer": 2.0,
    "journal of the egyptian national cancer institute": 2.5,
    "applied radiation and isotopes including data instrumentation and methods for use in agriculture industry and medicine": 1.5,
    "asia-pacific journal of clinical oncology": 1.8, "clinical journal of gastroenterology": 1.5,
    "clinical laboratory": 1.5, "rsc advances": 3.9,
    "technology in cancer research treatment": 2.4, "omics a journal of integrative biology": 2.2,
    "iju case reports": 0.8, "clinical and translational radiation oncology": 2.4,
    "acs applied bio materials": 5.3, "journal of peptide science an official publication of the european peptide society": 3.0,
    "journal of korean medical science": 2.6, "frontiers in medicine": 3.1,
    "frontiers in nutrition": 4.0, "frontiers in pharmacology": 4.4,
    "international journal of cancer": 6.4,
}

def match_if(journal):
    nj = norm(journal)
    if not nj:
        return None
    if nj in JOURNAL_IF:
        return JOURNAL_IF[nj]
    # 去掉 "official journal of ..." 尾缀再试
    nj2 = re.sub(r"\s*official journal.*$", "", nj).strip()
    return JOURNAL_IF.get(nj2)

# 无关期刊黑名单 (与肝癌研究无关的误命中)
BLACKLIST = ["nursing outlook", "arts & health", "case reports in dentistry",
             "veterinary medicine", "australian health review", "medical care",
             "general hospital psychiatry", "respirology case reports",
             "prague medical report", "ijU case reports", "heart ", "aids "]

def relevant(p):
    text = (p["title"] + " " + (p.get("abstract") or "")).lower()
    core = ["hepatocellular", "liver cancer", "liver tumor", "liver tumour",
            "liver neoplasm", "intrahepatic cholangiocarcinoma", "liver metastasis",
            "liver metastases", "hcc", "liver transplantation", "liver resection",
            "hepatectomy", "liver cirrhosis", "hepatic carcinoma", "liver lesion",
            "liver tumour", "liver-directed", "liver function", "hepatoblastoma",
            "fibrolamellar", "cholangiocarcinoma", "liver ablation", "liver disease"]
    hits = sum(1 for k in core if k in text)
    title_hit = any(k in p["title"].lower() for k in core)
    black = any(b in (p["journal"] or "").lower() for b in BLACKLIST)
    return (title_hit or hits >= 3) and not black

TOPIC_RULES = [
    ("外科与移植", ["hepatectomy", "resection", "surgical", "transplant", "laparoscop",
                   "robotic", "portal vein embolization", "parenchyma-sparing", "postoperative"]),
    ("局部治疗", ["transarterial", "tace", "radioembolization", "ablation", "yttrium",
                 "y-90", "y90", "sbrt", "radiotherapy", "radiation", "embolization",
                 "histotripsy", "brachytherapy", "hepatic arterial infusion", "hai"]),
    ("系统治疗", ["immunotherapy", "atezolizumab", "durvalumab", "tremelimumab", "pembrolizumab",
                 "lenvatinib", "sorafenib", "bevacizumab", "tislelizumab", "camrelizumab",
                 "systemic therapy", "checkpoint inhibitor", "adc", "antibody-drug",
                 "chemotherapy", "targeted therapy", "tki", "first-line", "second-line"]),
    ("诊断与标志物", ["biomarker", "liquid biopsy", "ctdna", "ctDNA", "diagnosis", "detection",
                     "screening", "surveillance", "afp", "pivka", "radiomics", "imaging",
                     "mri", "ct ", "ultrasound", "pet", "machine learning", "deep learning",
                     "artificial intelligence", "model", "score", "risk prediction"]),
    ("流行病学与预防", ["epidemiology", "incidence", "prevalence", "mortality", "trends",
                       "risk factors", "hepatitis b", "hepatitis c", "hbv", "hcv", "masld",
                       "mash", "steatosis", "alcohol", "diabetes", "statin", "physical activity"]),
    ("机制与转化", ["mechanism", "pathway", "single-cell", "single cell", "spatial", "multi-omic",
                   "multiomic", "organoid", "mouse", "xenograft", "in vitro", "crispr",
                   "nanoparticle", "nano", "ferroptosis", "apoptosis", "pyroptosis", "immune microenvironment",
                   "tumor microenvironment", "macrophage", "t cell", "nk cell", "epigenetic",
                   "methylation", "lactylation", "metabolism", "gut microbiota"]),
]

def classify_topic(p):
    text = (p["title"] + " " + (p.get("abstract") or "")).lower()
    best, bn = "其他", 0
    for topic, kws in TOPIC_RULES:
        n = sum(text.count(k) for k in kws)
        if n > bn:
            best, bn = topic, n
    return best

def classify_type(p):
    pts = p.get("pubtypes") or []
    if "Randomized Controlled Trial" in pts:
        return "RCT"
    if "Meta-Analysis" in pts or "Systematic Review" in pts:
        return "Meta分析"
    if "Practice Guideline" in pts or "Guideline" in pts:
        return "指南"
    if "Review" in pts:
        return "综述"
    if "Multicenter Study" in pts:
        return "多中心研究"
    if "Comparative Study" in pts:
        return "对照研究"
    t = (p["title"] + " " + (p.get("abstract") or "")).lower()
    if "case report" in t or "we report" in t:
        return "病例报告"
    if any(k in t for k in ["single-cell", "single cell", "xenograft", "in vitro", "mice", "mouse"]):
        return "基础研究"
    if any(k in t for k in ["cohort", "registry", "database", "seer", "nationwide"]):
        return "队列研究"
    return "其他"

papers = [p for p in data["papers"] if relevant(p)]
removed = len(data["papers"]) - len(papers)
for p in papers:
    p["if_value"] = match_if(p["journal"])
    p["topic"] = classify_topic(p)
    p["study_type"] = classify_type(p)

papers.sort(key=lambda x: (x["if_value"] if x["if_value"] else 0, 0), reverse=True)
data["papers"] = papers
data["funnel"]["excluded_irrelevant"] = removed
data["funnel"]["included"] = len(papers)

json.dump(data, open(os.path.join(BASE, "data/clean.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# 标注工作表: 需要人工(LLM)精标注的重点文献 (IF>=5 或 RCT/Meta 或 高相关)
key_papers = [p for p in papers if (p["if_value"] and p["if_value"] >= 5)
              or p["study_type"] in ("RCT", "Meta分析", "多中心研究")]
print(f"过滤后: {len(papers)} 篇 (剔除无关 {removed}) | 重点标注对象: {len(key_papers)} 篇")
from collections import Counter
print("主题分布:", dict(Counter(p["topic"] for p in papers)))
print("类型分布:", dict(Counter(p["study_type"] for p in papers)))
print("有IF:", sum(1 for p in papers if p["if_value"]), "/", len(papers))
for p in key_papers:
    print(f"  {p['pmid']}|IF{p['if_value'] or 0}|{p['study_type']}|{p['topic']}|{p['title'][:80]}")
