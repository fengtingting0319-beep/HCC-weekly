#!/usr/bin/env python3
"""肝癌研究周报 · 一键周更入口

用法:
    python3 run_weekly.py                    # 默认窗口 = 最近7天
    python3 run_weekly.py 2026-10-03 2026-10-10   # 指定窗口

流程: PubMed/bioRxiv/medRxiv/ClinicalTrials.gov/指南 抓取 → 清洗分级 → 渲染当期HTML → 更新总目录页

说明:
- annotations.py 是当周 AI 精读标注层（中文标题/要点/分级/Top10精读/热点述评）。
  每周在 Biomni 会话中由 AI 更新；未标注条目自动回退为规则评分（C级、无中文标题）。
- 输出: /mnt/results/肝癌研究周报_<窗口>_第N期.html + 肝癌研究周报_总目录.html
"""
import subprocess, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))
env = {**os.environ, "HCC_BASE": BASE}
if len(sys.argv) == 3:
    env["HCC_START"], env["HCC_END"] = sys.argv[1], sys.argv[2]

for f in ["fetch_data.py", "fetch_preprints.py", "clean_data.py", "render.py"]:
    print(f"\n=== {f} ===")
    r = subprocess.run([sys.executable, os.path.join(BASE, f)], env=env)
    if r.returncode:
        sys.exit(f"{f} 失败, 中止")
print("\n本周周报生成完毕。")
