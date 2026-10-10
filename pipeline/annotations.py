#!/usr/bin/env python3
"""肝癌研究周报 · LLM标注层 (人工/大模型撰写, 供渲染脚本合并)
所有中文标题、要点启示、分级与评分为本期编辑判断, 供课题组复核。
"""

PAPERS = {
    # ============ S 级 ============
    "42838226": dict(
        cn_title="SIERRA研究：STRIDE方案用于不良预后不可切除肝癌的IIIb期单臂研究",
        insight="首个专门纳入Child-Pugh B7/B8、ECOG 1-2及门静脉主干癌栓（Vp4）等不良预后人群的STRIDE IIIb期研究，填补了关键试验长期排除该类患者的证据空白；安全性可管理，支持STRIDE向肝功能受损人群拓展。",
        grade="S", design=24, validation=12, mechanism=6, fit=20,
        grade_rationale="IIIb期前瞻研究、直击真实世界最常见却长期被试验排除的人群，可能改变一线治疗选择与说明书人群界定",
        top=True,
        reading=dict(
            background="STRIDE（单次替西木单抗+度伐利尤单抗）是不可切除肝癌（uHCC）一线标准方案之一，但III期HIMALAYA等关键试验排除了Child-Pugh B、ECOG 1-2及门静脉主干癌栓（Vp4）患者，而这类患者在临床中占比很高。",
            results="SIERRA（NCT05883644）为IIIb期单臂研究，专门纳入上述不良预后人群。主要分析显示STRIDE在该人群中安全性可管理，疗效信号与总体人群方向一致，为不良预后人群使用STRIDE提供了前瞻性证据。",
            significance="不良预后uHCC人群的一线免疫治疗证据长期空白，SIERRA以专门设计填补该空白；对临床实践而言，肝功能受损与癌栓患者的一线选择有了更直接的支持，也提示后续试验应减少对该人群的系统性排除。")),
    # ============ A 级 ============
    "42843419": dict(
        cn_title="CHANCE2504：免疫+靶向±肝动脉灌注化疗治疗门静脉癌栓肝癌的全国目标试验仿真研究",
        insight="36家中国中心、目标试验仿真框架+克隆删失加权，比较HAIC+免疫+靶向三联与免疫+靶向双联一线治疗合并PVTT的肝癌；为癌栓人群联合HAIC的价值提供迄今规模最大的真实世界证据。",
        grade="A", design=20, validation=11, mechanism=5, fit=20,
        grade_rationale="全国36中心目标试验仿真、方法学严谨，直接回答PVTT人群是否加用HAIC这一高争议临床问题",
        top=True,
        reading=dict(
            background="合并门静脉癌栓（PVTT）的肝癌预后极差，治疗策略长期存在争议。免疫+靶向已成为一线标准，但在此基础上是否联合肝动脉灌注化疗（HAIC）缺乏高级别证据。",
            results="CHANCE2504采用目标试验仿真（target trial emulation）与克隆删失加权（CCW）框架，整合全国36个中心的回顾性队列，比较HAIC+ICI+MTA三联与ICI+MTA双联的疗效与安全性。",
            significance="在RCT难以覆盖的癌栓人群，目标试验仿真提供了接近随机的比较证据；若三联获益确立，将推动PVTT人群一线方案从'双联系统治疗'向'系统+局部'联合范式演进。")),
    "42829912": dict(
        cn_title="多中心大样本血清代谢标志物谱用于肝癌早诊（1924例发现队列）",
        insight="11个中心1924例发现队列+225例独立外验，9-代谢物标志物联合AFP的AUC达0.92-0.93，对早期及AFP阴性肝癌均有提升；为影像学之外提供了可及性高的血液早诊路径。",
        grade="A", design=22, validation=13, mechanism=6, fit=20,
        grade_rationale="大规模多中心、独立外验、检测平台可及（纳米增强LDI-MS），早诊转化路径清晰",
        top=True,
        reading=dict(
            background="肝癌预后差的核心原因是早诊率低，现有监测手段（AFP+超声）敏感性不足，亟需新的血液标志物组合。",
            results="研究采用高通量纳米增强激光解吸/电离质谱对11个中心1924名参与者的血清代谢物建模，并在另2个中心225人独立外验；9-代谢物标志物联合AFP的判别AUC达0.92（发现）与0.93（外验）。",
            significance="代谢组学标志物与AFP互补，有望纳入高危人群分层监测；若前瞻验证成立，将推动肝癌早诊从'影像+AFP'向多组学组合演进。")),
    "42843362": dict(
        cn_title="TRIPLET-HCC研究的经验与教训（Lancet Gastro Hep述评）",
        insight="对三联免疫治疗HCC的TRIPLET-HCC研究发表述评，讨论三联方案的毒性-疗效平衡、试验设计与结果解读，对后续HCC免疫联合试验设计有直接参考价值。",
        grade="A", design=8, validation=6, mechanism=4, fit=18,
        grade_rationale="顶刊述评，虽非原创研究但对联合方案试验设计具有领域指导意义",
        top=True,
        reading=dict(
            background="TRIPLET-HCC评估三联免疫检查点抑制剂组合在肝癌中的价值，其结果对'更多靶点叠加是否更好'这一领域核心问题给出了否定或谨慎信号。",
            results="述评系统梳理该试验的设计选择、毒性谱与疗效边界，指出三联方案在HCC中获益-风险比不佳的深层原因。",
            significance="为后续HCC免疫联合策略（双联优化、局部+系统、生物标志物指导人群选择）提供了设计层面的教训，值得试验研究者与申办方精读。")),
    "42829153": dict(
        cn_title="SETDB1：肝癌抗肿瘤免疫组织的表观遗传守门人",
        insight="揭示SETDB1通过表观沉默机制组织HCC免疫微环境（抗原呈递/干扰素应答），提示'表观遗传靶向+免疫治疗'的联合窗口。",
        grade="A", design=12, validation=6, mechanism=14, fit=18,
        grade_rationale="J Hepatol机制研究，机制链条完整，直接指向免疫治疗增敏新靶点",
        top=True,
        reading=dict(
            background="HCC对免疫检查点抑制剂的原发/继发耐药与肿瘤内在表观遗传状态密切相关，但'谁在守门'尚不清晰。",
            results="研究确立SETDB1为HCC抗肿瘤免疫组织的表观遗传守门人，其沉默肿瘤抗原呈递与IFN应答程序，塑造免疫冷微环境。",
            significance="表观遗传'守门人'靶点为免疫冷型HCC提供了可药物化的增敏路径，SETDB1抑制剂或可与ICI联合开展转化研究。")),
    "42842338": dict(
        cn_title="CPEB3连接遗传变异与选择性多聚腺苷酸化驱动肝癌进展",
        insight="Hepatology研究解码肿瘤进展的转录后调控代码，将'遗传变异—APA—肿瘤进展'串联，为HCC的RNA加工层面调控提供新机制与潜在标志物。",
        grade="A", design=12, validation=6, mechanism=14, fit=18,
        grade_rationale="顶刊机制研究，开辟RNA加工层面新维度",
        top=True,
        reading=dict(
            background="选择性多聚腺苷酸化（APA）是转录后调控的关键层面，但其在肝癌遗传易感与进展中的作用不清。",
            results="研究鉴定CPEB3为连接遗传变异与APA的关键因子，阐明其如何通过改变3'UTR landscape影响肿瘤表型。",
            significance="将GWAS信号与RNA加工调控打通，提示APA图谱可作为HCC分层标志物，CPEB3通路或成治疗靶点。")),
    "42843897": dict(
        cn_title="免疫治疗时代肝癌患者的快速肌肉丢失：超越移植等待名单的意义",
        insight="Gut研究提示免疫治疗HCC患者肌少症快速进展与结局相关，将肌肉丢失的评估意义从移植等待名单拓展至系统治疗全程；支持营养-体能动态监测纳入免疫治疗管理。",
        grade="A", design=14, validation=8, mechanism=5, fit=18,
        grade_rationale="Gut原创研究，临床管理启示直接",
        top=True,
        reading=dict(
            background="肌少症是肝硬化与肝癌患者的重要共病，既往证据集中于移植等待名单；免疫治疗时代其动态变化与疗效/预后的关系尚不明确。",
            results="研究显示接受免疫治疗的HCC患者中快速肌肉丢失普遍存在，并与不良结局相关，其意义超越等待名单场景。",
            significance="提示在免疫治疗全程动态监测肌肉量（影像/生物电阻抗），营养与运动干预或可改善免疫治疗人群结局，值得前瞻验证。")),
    "42843561": dict(
        cn_title="高炎症重编程标记MASH向肝癌（无肝硬化）的转化",
        insight="整合病理、单细胞、细胞因子与多重免疫组化，定义非肝硬化MASH相关HCC的促炎转变特征并在人体队列验证；提示MASH-HCC一级预防与监测的炎症靶点。",
        grade="A", design=14, validation=8, mechanism=13, fit=18,
        grade_rationale="多平台整合+人体验证，直指代谢性肝癌（非肝硬化）这一快速增长人群",
        top=True,
        reading=dict(
            background="高达40%的MASH相关肝癌发生于无肝硬化肝脏，其癌变机制与病毒性/酒精性肝癌不同，监测策略也难以覆盖。",
            results="在Gubra-Amylin NASH饮食小鼠模型中整合多组学，鉴定出从MASH到HCC转变的'高炎症重编程'特征，并在独立人体队列验证。",
            significance="为非肝硬化MASH-HCC的早诊标志物与抗炎预防策略提供机制锚点，呼应代谢性肝癌监测指南的更新需求。")),
    # ============ B 级 ============
    "42835116": dict(
        cn_title="初始不可切除肝癌转化治疗后手术时机：整合主要病理缓解与治疗时长的多中心研究",
        insight="7家中心数据提示以主要病理缓解（残留存活肿瘤≤15%）联合术前治疗时长共同决定手术窗口，为'转化后何时手术'这一临床难题提供量化参考。",
        grade="B", design=16, validation=8, mechanism=4, fit=20,
        grade_rationale="多中心、直击转化治疗决策痛点，但为回顾性设计",
        top=True,
        reading=dict(
            background="转化治疗使初始不可切除肝癌获得根治性切除机会，但最佳手术时机缺乏客观标准：过早肿瘤未充分降期，过晚耐药与进展风险增加。",
            results="多中心回顾研究（7家三级医院，2020-2025）以限制性立方样条确定MPR（残留存活肿瘤≤15%）预后切点，将患者按治疗时长与病理缓解分组比较术后生存。",
            significance="首次将MPR与治疗时长整合为手术时机决策框架，若前瞻验证成立，将改变'固定周期后手术'的经验做法。")),
    "42851630": dict(
        cn_title="阿替利珠单抗+贝伐 vs 度伐利尤+替西木单抗真实世界疗效比较：76项观察性研究荟萃分析",
        insight="汇总76项报告、10243例真实世界数据，协变量校正后比较两大一线免疫方案的ORR/DCR与生存；为缺乏头对头RCT的一线选择提供参考，但异质性与选择偏倚需警惕。",
        grade="B", design=12, validation=9, mechanism=2, fit=20,
        grade_rationale="迄今最大规模的真实世界比较汇总，但观察性数据固有局限",
        top=True,
        reading=dict(
            background="阿替利珠单抗+贝伐珠单抗（T+A）与度伐利尤单抗+替西木单抗（STRIDE）均为uHCC一线标准，但无头对头RCT，临床选择依赖间接比较。",
            results="系统评价纳入76项观察性报告共10243例患者；ORR/DCR采用随机效应模型合并，协变量校正meta回归为主要分析，并辅以无泄漏嵌套交叉验证的探索性ML预测。",
            significance="为一线方案间选择提供了迄今最全面的真实世界汇总证据；结论仍受适应证混杂限制，个体化选择需结合肝功能、出血风险与给药便利性。")),
    "42845031": dict(
        cn_title="局部高剂量自体NK细胞联合HAIC治疗局部晚期肝癌的多中心IIa期试验",
        insight="HAIC后序贯肝动脉输注高剂量自体NK细胞可行且初步疗效积极，为'细胞治疗+局部灌注'在局部晚期肝癌的联合模式提供临床证据。",
        grade="B", design=16, validation=6, mechanism=6, fit=20,
        grade_rationale="多中心前瞻IIa期、给药途径创新（肝动脉局部输注）",
        top=True,
        reading=dict(
            background="局部治疗失败的局部晚期肝癌缺乏有效方案；NK细胞治疗全身输注疗效有限，局部高剂量递送或可突破。",
            results="开放标签多中心IIa期：标准治疗难治患者经2周期HAIC（5-FU+顺铂）后疾病稳定及以上者行肝动脉高剂量自体NK细胞输注，评估疗效与安全性。",
            significance="局部区域给药策略为细胞治疗在实体瘤中的应用提供了剂量与安全性优势，值得III期推进。")),
    "42828122": dict(
        cn_title="CyberKnife SBRT联合仑伐替尼+替雷利珠单抗治疗合并大血管侵犯肝癌的真实世界研究",
        insight="IPTW校正后SBRT三联较双联系统治疗改善合并大血管侵犯（MVI）肝癌的生存，支持'局部控制癌栓+系统治疗'策略在该极差预后人群的探索。",
        grade="B", design=14, validation=7, mechanism=3, fit=20,
        grade_rationale="真实世界IPTW校正、116例，针对MVI这一未满足需求人群",
        reading=dict(background="合并大血管侵犯的肝癌预后极差，系统治疗局部控制不足。", results="116例真实世界数据IPTW校正比较SBRT+仑伐替尼+替雷利珠单抗与双联系统治疗。", significance="支持放疗在癌栓人群的免疫增敏与局部控制价值，需前瞻验证。")),
    "42841937": dict(
        cn_title="超米兰标准可切除肝癌：术前TARE vs TACE vs 直接切除的比较",
        insight="回顾性比较提示术前TARE在超米兰标准人群的复发时间/RFS优势，为TARE进入围术期治疗提供依据，仍需前瞻验证。",
        grade="B", design=13, validation=7, mechanism=3, fit=19,
        grade_rationale="回顾性三臂比较、样本量有限但问题重要"),
    "42849888": dict(
        cn_title="TARE vs TACE治疗不可切除大肝癌（≥6cm单灶）的肿瘤学结局比较",
        insight="单灶大肝癌中TARE显示更优局部控制与肝功能保留趋势，支持其作为TACE替代的定位。",
        grade="B", design=13, validation=7, mechanism=3, fit=19,
        grade_rationale="14年单中心对照队列，样本充分、随访长"),
    "42829106": dict(
        cn_title="超Up-to-Seven标准肝癌TARE的单中心队列结局",
        insight="94例超肿瘤负荷标准患者TARE后报告局部进展生存与安全性，拓展TARE适用边界。",
        grade="B", design=12, validation=6, mechanism=3, fit=19,
        grade_rationale="单中心回顾、但针对超标准人群的空白"),
    "42833659": dict(
        cn_title="度伐利尤+替西木单抗治疗中早期淋巴细胞计数变化预测晚期肝癌结局",
        insight="299例多中心研究：治疗2周外周血淋巴细胞动态变化与生存相关，为廉价的动态预后标志物。",
        grade="B", design=13, validation=7, mechanism=4, fit=18,
        grade_rationale="多中心、样本量较大、标志物易得"),
    "42845114": dict(
        cn_title="层粘连蛋白γ2单体联合PAGE-B评分用于慢乙肝肝癌监测",
        insight="抗病毒时代仍残存HCC风险，基线血清LG2m加入PAGE-B可再分层监测强度，优化监测资源配置。",
        grade="B", design=13, validation=7, mechanism=4, fit=18,
        grade_rationale="1016例前瞻测量、监测算法可直接落地"),
    "42840712": dict(
        cn_title="根治性切除后极早期复发（≤12月）作为动态预后分层：地标分析",
        insight="以地标分析规避保证时间偏倚，确认极早期复发对术后复发后生存的分层价值，支持术后12个月内强化随访。",
        grade="B", design=13, validation=6, mechanism=3, fit=18,
        grade_rationale="方法学严谨（地标分析+ML基准）"),
    "42855130": dict(
        cn_title="肝移植后肝癌复发14年全国队列：选择标准演变与AFP模型的影响",
        insight="法国15家中心388例复发患者分析复发模式与复发后生存的时间趋势，为移植选择标准的动态优化提供数据。",
        grade="B", design=14, validation=8, mechanism=3, fit=19,
        grade_rationale="全国性14年队列、回应ILTS-ILCA共识的数据需求"),
    "42839774": dict(
        cn_title="ALT正常慢乙肝患者早期抗病毒治疗与肝癌发生率：前瞻性II期研究",
        insight="115例非肝硬化患者5年病毒应答92.4%、HCC累计发生率低，支持'ALT正常也治疗'的适应证扩大方向。",
        grade="B", design=15, validation=7, mechanism=3, fit=17,
        grade_rationale="前瞻多中心II期、但样本量与终点限制"),
    "42834828": dict(
        cn_title="体力活动与肝癌风险：26万人竞争风险分析",
        insight="NIH-AARP队列（263184人、870例肝癌）以竞争风险框架量化≥4h/周体力活动的肝癌风险绝对差，量化可干预生活方式的预防价值。",
        grade="B", design=14, validation=9, mechanism=2, fit=17,
        grade_rationale="大样本、方法学（竞争风险因果框架）严谨"),
    "42834792": dict(
        cn_title="人肝癌类器官整合表征及其HBV相关生物学",
        insight="20例PDO+12株PDCL多组学与药筛，分两大分子亚型并关联治疗应答，为HBV-HCC精准模型平台。",
        grade="B", design=13, validation=6, mechanism=10, fit=18,
        grade_rationale="模型平台研究、多组学整合充分"),
    "42848956": dict(
        cn_title="ANXA1通过内质网-线粒体钙偶联维持肝癌仑伐替尼耐药",
        insight="揭示ERMCS钙信号为仑伐替尼耐药机制，ANXA1或为逆转耐药靶点；活细胞超分辨成像+钙动力学证据链完整。",
        grade="B", design=12, validation=6, mechanism=12, fit=19,
        grade_rationale="Cancer Research机制研究、直击一线TKI耐药"),
    "42833294": dict(
        cn_title="FGFR2/3变异肝内胆管癌：独立临床病理与分子亚型（预后更好）",
        insight="90例WES/WTS分析显示FGFR2/3变异iCCA为预后较好的独立亚型，支持iCCA常规基因检测与分层。",
        grade="B", design=13, validation=7, mechanism=8, fit=18,
        grade_rationale="基因组+转录组双测序、直接指导检测实践"),
    "42829798": dict(
        cn_title="工程化IFN-γ血小板样微粒重塑肝免疫微环境清除肝转移瘤",
        insight="肝靶向递送IFN-γ驱动M1极化与CXCL9/10趋化轴，逆转肝脏免疫耐受；为结直肠癌肝转移免疫治疗提供新递送策略。",
        grade="B", design=12, validation=5, mechanism=12, fit=16,
        grade_rationale="Advanced Materials、递送工程+机制双创新（CRLM亚方向）"),
    "42837177": dict(
        cn_title="核Prohibitin 1缺失驱动酒精性肝损伤并易感结肠癌肝转移",
        insight="PHB1核输出阻断肽同时改善ALD并降低CRLM易感，连接肝病背景与转移微环境（CRLM亚方向）。",
        grade="B", design=12, validation=6, mechanism=11, fit=15,
        grade_rationale="JCI机制研究、肝病-转移交叉视角"),
    "42848958": dict(
        cn_title="配对单细胞测序揭示乳腺癌肝转移谷胱甘肽依赖的免疫逃逸",
        insight="BCLM高免疫浸润却功能逃逸的'悖论'解析，谷胱甘肽代谢为治疗靶点（肝转移亚方向）。",
        grade="B", design=12, validation=6, mechanism=11, fit=14,
        grade_rationale="Cancer Research、配对原发-转移单细胞设计"),
    "42830367": dict(
        cn_title="SPP1+巨噬细胞与结直肠癌肝转移新辅助化疗耐药相关",
        insight="scRNA+空间转录组定位耐药相关巨噬亚群，为CRLM新辅助方案优化提供靶点（肝转移亚方向）。",
        grade="B", design=12, validation=5, mechanism=11, fit=15,
        grade_rationale="单细胞+空间双技术、临床耐药问题导向"),
    "42843420": dict(
        cn_title="表观遗传与表观转录调控肝癌免疫检查点应答：机制、靶向与转化挑战（综述）",
        insight="系统梳理HCC特异性表观/表观转录调控与ICI应答的证据，提出可转化靶点清单，适合作为免疫耐药方向的研究地图。",
        grade="B", design=8, validation=5, mechanism=10, fit=18,
        grade_rationale="高质量机制综述、领域地图价值"),
    "42854784": dict(
        cn_title="MASLD对肝癌发生发展的影响（Ann Hepatol）",
        insight="量化MASLD背景下肝癌发生风险与结局差异，呼应代谢性肝病人群的监测需求。",
        grade="C", design=10, validation=5, mechanism=3, fit=16,
        grade_rationale="回顾性队列、主题重要但增量有限"),
    # ============ C 级（重点文献中的一般性研究） ============
    "42843363": dict(cn_title="TRIPLET-HCC研究的经验与教训：作者回复", insight="TRIPLET-HCC研究作者对述评的回复，补充三联方案设计考量。", grade="C", design=5, validation=3, mechanism=2, fit=15, grade_rationale="述评回复"),
    "42850232": dict(cn_title="GPC3靶向原位自由基生成纳米系统精准治疗肝癌", insight="空间分隔LNP原位产生靶向癌蛋白自由基，兼顾效率与特异性。", grade="C", design=9, validation=4, mechanism=9, fit=17, grade_rationale="临床前纳米医学"),
    "42850702": dict(cn_title="仿生cRGDyk血小板纳米平台递送ACAD11触发肝癌焦亡", insight="鉴定ACAD11-ROS/NLRP3/GSDMD焦亡轴并构建靶向递送。", grade="C", design=9, validation=4, mechanism=9, fit=16, grade_rationale="临床前研究"),
    "42851518": dict(cn_title="微波消融联合纳米免疫反应器协同治疗肝癌", insight="17-AAG-MnO2纳米反应器利用消融后免疫 cues 诱导免疫原性死亡，消融+免疫协同。", grade="C", design=9, validation=4, mechanism=8, fit=17, grade_rationale="临床前研究"),
    "42846631": dict(cn_title="PD-L1纳米体工程化RNA病毒干扰PCSK9上调MHC-I增强肝癌免疫治疗", insight="PCSK9抑制恢复MHC-I呈递+PD-L1靶向双功能VLP，机制新颖。", grade="C", design=9, validation=4, mechanism=9, fit=16, grade_rationale="临床前研究"),
    "42855228": dict(cn_title="XIAP抑制增强个体化新抗原疫苗抗肝癌免疫", insight="原位HCC模型中XIAP抑制剂与新抗原疫苗协同，为疫苗联合策略提供依据。", grade="C", design=9, validation=4, mechanism=9, fit=16, grade_rationale="临床前研究"),
    "42844863": dict(cn_title="A20结合STAT1抑制IFN-γ信号削弱肝癌抗肿瘤免疫", insight="揭示HCC细胞IFN-γ通路负调新机制，与ICB原发耐药相关。", grade="C", design=8, validation=4, mechanism=9, fit=16, grade_rationale="机制研究"),
    "42832095": dict(cn_title="GLUT1抑制剂BAY-876通过破坏GLUT1-SLC7A11-NADPH轴逆转仑伐替尼耐药", insight="代谢-氧化还原轴为仑伐替尼耐药提供联合逆转思路。", grade="C", design=8, validation=4, mechanism=8, fit=16, grade_rationale="体外机制研究"),
    "42854556": dict(cn_title="小檗碱通过HIF-1α介导能量危象增敏索拉非尼", insight="天然产物代谢干预增敏TKI，临床转化距离尚远。", grade="C", design=8, validation=4, mechanism=8, fit=15, grade_rationale="临床前研究"),
    "42844287": dict(cn_title="深度学习CT特征预测胰腺癌早期肝转移（多中心1063例）", insight="Mamba模型AUC 0.81-0.89并指导新辅助治疗选择；肝转移预测的影像AI范式（胰腺癌肝转移亚方向）。", grade="C", design=12, validation=8, mechanism=3, fit=12, grade_rationale="非原发性肝癌、方法学可借鉴"),
    "42834048": dict(cn_title="多模态放射-病理组学预测胃癌术后异时性肝转移", insight="影像组学+病理组学+临床三源融合可解释模型（胃癌肝转移亚方向）。", grade="C", design=11, validation=7, mechanism=3, fit=12, grade_rationale="非原发性肝癌"),
    "42830873": dict(cn_title="结直肠癌肝转移：从发病机制到当前治疗（综述）", insight="CRLM微环境与治疗全景综述（肝转移亚方向）。", grade="C", design=6, validation=4, mechanism=6, fit=13, grade_rationale="综述"),
    "42828719": dict(cn_title="纤维板层样肝癌的分子时代：DNAJB1::PRKACA生物学与精准治疗（综述）", insight="罕见亚型分子分型与精准治疗全景。", grade="C", design=6, validation=4, mechanism=6, fit=15, grade_rationale="综述"),
    "42836161": dict(cn_title="聚合物纳米药物递送siRNA治疗肝癌：策略与转化展望（综述）", insight="siRNA递送平台在HCC的系统梳理。", grade="C", design=6, validation=4, mechanism=6, fit=15, grade_rationale="综述"),
    "42830470": dict(cn_title="超越抗体：GPC3靶向肽用于肝癌诊疗（综述）", insight="GPC3靶向肽作为抗体替代/补充的诊疗展望。", grade="C", design=6, validation=4, mechanism=6, fit=15, grade_rationale="综述"),
    "42840955": dict(cn_title="HBV相关肝癌基线低水平病毒血症的预后意义与风险分层", insight="921例提示基线低水平病毒血症与生存相关，支持抗病毒指征前移。", grade="C", design=11, validation=6, mechanism=3, fit=17, grade_rationale="回顾性、但样本较大"),
    "42834629": dict(cn_title="残余肝硬度补充动态变化用于肝癌风险预测", insight="肝硬度动态监测或补充现有HCC风险模型。", grade="C", design=9, validation=5, mechanism=3, fit=16, grade_rationale="回顾性"),
    "42829200": dict(cn_title="五十年之际：metALD成为肝病新前沿（述评）", insight="代谢与酒精相关肝损伤（metALD）概念演进的领域述评。", grade="C", design=5, validation=3, mechanism=3, fit=14, grade_rationale="述评"),
    "42831089": dict(cn_title="单细胞RNA测序解析HBV与HCV阳性肝癌的不同调控机制", insight="病毒病因差异的单细胞层面解析。", grade="C", design=8, validation=4, mechanism=8, fit=16, grade_rationale="基础研究"),
    "42827845": dict(cn_title="HBV整合入KMT2B经表观重编程增强肝癌恶性表型", insight="HBV整合事件的功能验证与机制。", grade="C", design=8, validation=4, mechanism=8, fit=16, grade_rationale="基础研究"),
    "42851002": dict(cn_title="多族裔肝硬化人群肝癌多基因风险评分评估", insight="11-SNP加权PRS在美国多族裔肝硬化队列的分层价值有限，跨人群外推需谨慎。", grade="C", design=10, validation=6, mechanism=2, fit=16, grade_rationale="回顾性评估"),
    "42843350": dict(cn_title="抗病毒治疗下胰岛素抵抗与慢乙肝肝癌发生（多中心前瞻队列）", insight="HOMA2-IR可细分抗病毒应答后残存HCC风险，代谢共病管理进入肝癌一级预防。", grade="C", design=11, validation=6, mechanism=3, fit=17, grade_rationale="前瞻多中心、样本量中等"),
    "42833306": dict(cn_title="血清蛋白组学panel辅助BCLC-B肝癌手术决策", insight="DIA-MS+Lasso-Cox构建术后预后模型，为BCLC-B异质性下的手术选择提供蛋白组依据。", grade="C", design=10, validation=5, mechanism=5, fit=17, grade_rationale="回顾性、训练样本小"),
    "42832300": dict(cn_title="整合功能肝储备与肿瘤负荷的BCLC-B专用预后指数", insight="1843例四中心构建mMDN/mUS等新指数，弥补通用分期对BCLC-B内部异质性刻画不足。", grade="C", design=11, validation=6, mechanism=2, fit=17, grade_rationale="回顾性、工具类研究"),
    "42839680": dict(cn_title="T+A治疗肝癌患者心血管风险分层：ESC vs CARDIOSOR评分比较", insight="免疫治疗延长生存背景下贝伐相关心血管毒性管理前移，肝硬化人群需专用分层工具。", grade="C", design=10, validation=5, mechanism=2, fit=16, grade_rationale="多中心回顾、支持性证据"),
    "42841025": dict(cn_title="术前CT影像组学+临床病理特征预测肝癌切除后早期肝外复发", insight="多模态ML模型外验提示可识别肝外复发高危人群，指导术后个体化监测。", grade="C", design=10, validation=6, mechanism=3, fit=16, grade_rationale="回顾性、样本量中等"),
    "42836110": dict(cn_title="HepaKineticNet：CT动力学深度学习预测BCLC B-C肝癌综合治疗生存", insight="多期CT肿瘤内异质性建模，外验改善OS预测；AI影像在系统治疗时代预后评估的新尝试。", grade="C", design=10, validation=6, mechanism=4, fit=16, grade_rationale="回顾性双中心"),
    "42838878": dict(cn_title="Gd-EOB-DTPA MRI可解释机器学习模型鉴别≤2cm小肝癌（多中心）", insight="多中心296灶外验，辅助小病灶良恶性鉴别，降低误诊/漏诊。", grade="C", design=11, validation=7, mechanism=3, fit=17, grade_rationale="多中心、诊断场景实用"),
    "42844316": dict(cn_title="ISTAR-01：大肝癌同日Y-90树脂微球放射栓塞的前瞻性多中心注册研究方案", insight="基于影像预测低肺分流的同日治疗流程可缩短住院、提高可及性；方案发布供领域关注。", grade="C", design=8, validation=4, mechanism=2, fit=17, grade_rationale="研究方案"),
}

PREPRINTS = {
    "10.64898/2026.08.02.742347": dict(
        cn_title="患者来源肝癌类器官反映肿瘤生物学，生长表型与临床结局相关",
        insight="HCC类器官形态多样性与其生物学/临床结局关联，支持类器官作为治疗应答预测平台。"),
    "10.64898/2026.09.28.755065": dict(
        cn_title="TWISTAR平台：肿瘤反应性TCR的功能去孤儿化与共享优势抗原图谱",
        insight="系统性鉴定肿瘤浸润T细胞识别的抗原，为肝癌等实体瘤TCR-T与新抗原治疗提供抗原清单。"),
    "10.64898/2026.10.02.26363145": dict(
        cn_title="血/尿超深度测序无创检测马兜铃酸致突变暴露",
        insight="马兜铃酸与肝癌负担相关，暴露的无创检测或支持肿瘤形成前的风险分层。"),
    "10.64898/2026.10.07.26364402": dict(
        cn_title="本地部署大语言模型从德文肝癌病理报告中结构化提取关键变量",
        insight="病理登记与质控的LLM结构化路径，可迁移至中文病理报告场景。"),
    "10.64898/2026.06.11.26354897": dict(
        cn_title="Delta-HLD：PCR兼容的天然游离DNA多位点甲基化定量平台",
        insight="低输入样本甲基化液体活检的新方法学，与肝癌早诊/MRD监测技术路线相关。"),
    "10.64898/2026.09.29.755355": dict(
        cn_title="患者来源肝类器官高通量形态学 profiling 用于肝毒性识别",
        insight="药物性肝损伤临床前评价平台，与肝癌药物开发的安全性筛选相关。"),
    "10.64898/2026.10.05.756567": dict(
        cn_title="ATF6α-ABCD3动态拴链门控过氧化物酶体质量控制",
        insight="内质网-过氧化物酶体通讯新机制，与肝细胞脂代谢背景相关。"),
}

TRIALS = {
    "NCT03847428": dict(cn_title="EMERALD-1：度伐利尤单抗±贝伐珠单抗联合TACE的III期研究（已完成）"),
    "NCT03298451": dict(cn_title="HIMALAYA：度伐利尤+替西木单抗一线治疗晚期肝癌的III期研究"),
    "NCT05185505": dict(cn_title="阿替利珠单抗+贝伐珠单抗新辅助治疗用于肝移植前肝癌的IV期研究"),
    "NCT05062837": dict(cn_title="肝切除联合卡瑞利珠单抗+阿帕替尼治疗CNLC IIIb期肝癌的II期研究"),
    "NCT05171335": dict(cn_title="仑伐替尼+TACE新辅助治疗用于符合移植条件肝癌的II期研究（已完成）"),
    "NCT07866612": dict(cn_title="免疫治疗完全缓解后手术 vs 等待观察策略在肝癌中的比较"),
    "NCT06728410": dict(cn_title="佩米替尼+度伐利尤单抗治疗经治晚期肝内胆管癌的II期研究"),
    "NCT07847710": dict(cn_title="围术期Retlirafusp alfa（抗PD-L1/TGF-β双功能融合蛋白）联合治疗的II期研究"),
    "NCT07612007": dict(cn_title="HRX215（first-in-class MKK4抑制剂）治疗肝癌的I期研究"),
    "NCT07861425": dict(cn_title="ACE723双载荷抗体偶联药物治疗实体瘤（含肝胆肿瘤）的I期研究"),
    "NCT07430202": dict(cn_title="DNAJB1-PRKACA融合激酶肽疫苗联合谷氨酰胺拮抗剂治疗纤维板层样肝癌的I期研究"),
    "NCT07847671": dict(cn_title="粪菌移植联合QL1706（PD-1/CTLA-4双抗）+贝伐珠单抗治疗晚期肝癌的II期研究"),
    "NCT06855225": dict(cn_title="单次替西木单抗+常规间隔度伐利尤单抗联合治疗的II期研究"),
    "NCT03937830": dict(cn_title="度伐利尤+贝伐+替西木单抗联合TACE治疗肝癌的II期研究"),
    "NCT06096779": dict(cn_title="阿替利珠单抗±贝伐珠单抗在肝癌中的II期研究"),
    "NCT05221398": dict(cn_title="肝癌术后辅助免疫检查点抑制剂治疗研究"),
    "NCT07091942": dict(cn_title="T+A治疗有效后根治性治疗策略的观察性研究（已完成）"),
    "NCT07863258": dict(cn_title="STRATHEP：AI驱动的晚期肝癌治疗分层研究"),
    "NCT07428356": dict(cn_title="组织碎裂术（Histotripsy）消融肝肿瘤的亚洲多中心研究"),
    "NCT07110233": dict(cn_title="Y-90放射段切除术治疗肝癌的注册研究"),
    "NCT05588388": dict(cn_title="贝伐珠单抗联合化学免疫治疗+阿替利珠单抗的II期研究"),
    "NCT05971108": dict(cn_title="Elecsys GAAD评分用于肝癌监测的真实世界实施与验证研究（IV期，已完成）"),
    "NCT05482516": dict(cn_title="ctDNA阳性消化道肿瘤新型治疗III期平台研究"),
    "NCT07178093": dict(cn_title="牛樟芝对TACE后肝癌患者影响的研究（已终止）"),
}

GUIDELINES = {
    "42831646": dict(cn_title="ACG临床指南：肝硬化患者的预防保健", category="肝病基础管理",
        insight="涵盖肝硬化人群肝癌监测在内的预防保健要点，是肝癌一级/二级预防的上游指南。"),
    "42810973": dict(cn_title="肝癌立体定向放疗（SBRT）2026专家共识", category="局部治疗",
        insight="更新SBRT在肝癌中的适应证、剂量分割与正常肝约束，与消融/TARE形成互补格局。"),
    "42785981": dict(cn_title="肝癌系统治疗临床试验专家共识（Gut）", category="临床试验设计",
        insight="针对肝癌系统治疗临床试验的关键设计要素（人群、终点、对照）给出共识建议，试验研究者必读。"),
    "42624290": dict(cn_title="Baveno VIII：门静脉高压共识新进展", category="肝病基础管理",
        insight="门脉高压管理共识更新，影响肝癌人群肝功能评估与治疗决策路径。"),
    "42565685": dict(cn_title="BEACON-HCC：北美肝癌治疗分配最佳证据共识", category="综合诊疗",
        insight="按疾病分期与肝功能给出治疗分配算法，是BCLC路径在北美实践语境下的落地版本。"),
    "42660571": dict(cn_title="泛亚洲适配ESMO肝癌临床实践指南", category="综合诊疗",
        insight="ESMO指南的泛亚洲适配版，纳入区域病因谱（HBV）与可及性考量，对中国实践参考价值高。"),
    "42524660": dict(cn_title="肝癌转化治疗与新辅助治疗的定义国际共识", category="围术期治疗",
        insight="统一'转化治疗'与'新辅助治疗'的概念边界与终点定义，为围术期研究可比性奠定基础。"),
    "42600366": dict(cn_title="肝癌后线系统治疗标准化共识", category="系统治疗",
        insight="规范后线治疗的顺序、交叉与终点，回应后线证据碎片化问题。"),
    "42270817": dict(cn_title="EASL-AASLD-ILCA肝癌临床试验设计与终点共识", category="临床试验设计",
        insight="三大国际肝病学会联合发布，规范肝癌试验人群、终点与统计考量。"),
    "42061383": dict(cn_title="国际多学会肝肿瘤热消融Delphi共识：操作规范", category="局部治疗",
        insight="热消融操作流程的国际多学会共识，规范适应证与技术细节。"),
    "42061382": dict(cn_title="国际多学会肝肿瘤热消融Delphi共识：切缘定义", category="局部治疗",
        insight="统一消融切缘的影像评价标准，与本周Radiology'消融 beyond margin'研究形成呼应。"),
    "42273581": dict(cn_title="中国原发性肝癌转化及围术期治疗专家共识", category="围术期治疗", china=True,
        insight="中国版转化/围术期共识，与本周转化手术时机多中心研究直接相关。"),
    "42312290": dict(cn_title="ILTS-ILCA肝癌肝移植选择标准国际共识（2024）", category="肝移植",
        insight="移植选择标准扩展（降期、超米兰）的国际共识，本周移植后复发队列研究为其提供数据反馈。"),
    "41733829": dict(cn_title="台湾肿瘤消融学会（TATA）肝癌消融共识", category="局部治疗",
        insight="区域消融共识，与热消融国际共识互补。"),
    "41849750": dict(cn_title="AASLD纤维板层样肝癌诊疗指南", category="综合诊疗",
        insight="罕见亚型FLC的首部系统指南，覆盖分子诊断与治疗路径。"),
    "41786254": dict(cn_title="肝移植受者免疫检查点抑制剂应用专家共识", category="肝移植",
        insight="移植后肿瘤复发使用ICI的获益-排斥风险平衡共识。"),
    "42615769": dict(cn_title="巴西肝癌预防、监测与早期诊断指南", category="筛查监测",
        insight="中低收入地区肝癌监测路径的区域版本。"),
    "42690308": dict(cn_title="巴西肝癌诊断、临床评估与分期指南", category="综合诊疗",
        insight="诊断与分期的区域实践指南。"),
    "42017860": dict(cn_title="AGA临床实践更新：肝癌风险分层与监测新策略", category="筛查监测",
        insight="更新高危人群界定与监测间隔的证据，与本周代谢标志物/PRS研究形成呼应。"),
    "41624065": dict(cn_title="生物标志物组合在肝癌监测与随访中的应用（Liver Cancer）", category="筛查监测",
        insight="系统比较AFP/PIVKA-II/多标志物组合的监测效能。"),
    "42365189": dict(cn_title="APASL慢性乙型肝炎管理临床实践指南", category="肝病基础管理",
        insight="亚太CHB管理指南更新，抗病毒适应证扩大与肝癌一级预防直接相关。"),
    "42241153": dict(cn_title="机器人放射外科（射波刀）治疗肝癌专家共识", category="局部治疗",
        insight="机器人放射外科在肝癌中的技术共识。"),
    "42095128": dict(cn_title="越南TACE治疗肝癌专家共识", category="局部治疗",
        insight="TACE技术规范的区域共识。"),
    "42754979": dict(cn_title="从实践共识到临床整合：SBRT在肝癌中的定位", category="局部治疗",
        insight="讨论SBRT证据如何整合进肝癌治疗算法。"),
    "42601228": dict(cn_title="马来西亚肝病学会肝癌预防共识", category="筛查监测",
        insight="区域预防共识。"),
}

HOTSPOTS = [
    "不良预后人群成为一线免疫证据拓展的主战场：SIERRA（IIIb期）与CHANCE2504（全国目标试验仿真）同周发布，Child-Pugh B、Vp4癌栓等'试验排除人群'的一线策略正在被系统性补证，建议课题组在真实世界队列中同步积累该人群的前瞻数据。",
    "PVTT/大血管侵犯人群的'局部控制+系统治疗'范式加速成型：HAIC（CHANCE2504）、SBRT（CyberKnife三联真实世界研究）、TARE（多项队列）从不同路径支持局部强化，值得设计跨模态比较或平台研究。",
    "转化治疗后手术时机开始从经验走向量化：MPR（残留存活肿瘤≤15%）+治疗时长的多中心框架首次给出决策参数，建议在转化手术标本中常规执行病理缓解评估并纳入前瞻登记。",
    "早诊标志物从单分子走向多组学组合：9-代谢物panel（AUC 0.93外验）、血清蛋白panel、LG2m+PAGE-B同周出现，血液早诊与影像AI并行；可评估现有随访队列标本的代谢/蛋白panel复现性。",
    "耐药机制聚焦'代谢-钙信号-表观遗传'轴：ANXA1-ERMCS钙偶联、GLUT1-SLC7A11氧化还原、SETDB1表观守门人等研究提示联合逆转策略，仑伐替尼/免疫耐药的机制队列值得布局。",
    "细胞治疗与局部递送平台结合成为局部晚期探索热点：肝动脉输注自体NK细胞（IIa期）、溶瘤病毒-GPC3、新抗原疫苗联合XIAP抑制等，提示'细胞/病毒治疗+局部灌注'是可及性较高的转化研究方向。",
]

GRADE_DEFS = {
    "S": "可能改变临床实践的重大研究",
    "A": "高质量临床研究或重要机制突破",
    "B": "有参考价值的临床/转化研究",
    "C": "一般性研究或早期探索",
}

CATEGORIES = ["流行病学与预防", "诊断与标志物", "系统治疗", "局部治疗", "外科与移植", "机制与转化", "其他"]
STUDY_TYPES = ["RCT", "多中心研究", "队列研究", "基础研究", "Meta分析", "综述", "病例报告", "其他"]
