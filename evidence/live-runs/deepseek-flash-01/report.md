# Cockburn Central house：买入时机与证据缺口调查

**信息截止日：2026-10-30（Australia/Perth）。** 本报告只使用给定资料与 checked_claims 中 status=supported 的陈述作为证据性结论；gaps 与未通过候选只用于描述限制，不升级为事实。

---

## 1. 范围说明

| 项目 | 内容 | 状态 |
|---|---|---|
| 用户地址 | 11 Furlong St, Cockburn Central, WA | 拼写与 REIWA/Nominatim 的“Furlong Street”一致 [[Q1C3]] |
| 定位来源 | Nominatim 地理编码 | 只返回整条 Furlong Street（way 1082972044，约 -32.1158872, 115.8494353），**未返回门牌 11 的精确点位** [[Q1C3]] |
| 地域边界 | 工作默认 1 公里直线半径（助教设定，非用户指定、非评估标准） | **圆心未独立核实**，半径内样本无法确认 |
| 房型 | house | 存在口径冲突：11 Furlong St 被 REIWA 标为 House，但描述为 townhouse [[Q1C2]] |
| 统计期 | 各来源不一，逐项标注 | 见下表 |
| 截止日 | 2026-10-30 | 固定 |

**关键限制：** 由于门牌 11 的精确坐标未核实，本报告**不能声称取得了“11 Furlong St 1 公里半径内”的成交或在售数据**。下文所有成交样本仅能确认位于 Cockburn Central suburb 内，不能确认落在 1 公里内。

---

## 2. 三事项证据表

### 事项 1：同一区域、同类住宅的价格变化

| 发现 | 范围 | 数值/原文 | 来源 URL | 发布日期 | 数据期间 | 访问日期 | 核验状态 |
|---|---|---|---|---|---|---|---|
| 11 Furlong St 成交 | 单幢（suburb 内，半径未确认） | $768,000，2025-05-13 成交；4卧3浴2车位，土地 172m² [[Q1C1]] | https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/ | 页面未给发布日期 | 成交日 2025-05-13 | 2026-10-30 | supported |
| 11 Furlong St 房型口径冲突 | 单幢 | 页面标题“4x3 Townhouse!”、“Built in 2021”，与 House 标签并存 [[Q1C2]] | 同上 | 未给 | — | 2026-10-30 | supported |
| 27 Furlong St 成交 | 单幢（suburb 内，半径未确认） | $940,000，2026-01-29 成交；4卧2浴2车位，土地 187m² [[Q1C4]] | https://reiwa.com.au/27-furlong-street-cockburn-central-4984527/ | 未给 | 成交日 2026-01-29 | 2026-10-30 | supported |
| 27 Paddock Parade 成交 | 单幢（suburb 内，半径未确认） | 2026-05-22 售 $1,000,000；3卧2浴2车位；2024-07-01 曾售 $810,000 [[Q1C5]] | https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896 | 未给 | 成交日 2026-05-22 / 2024-07-01 | 2026-10-30 | supported |
| 其他成交样本 | suburb 内，半径未确认 | 37 Paddock Parade 2026-07-24 $995,000；178 Semple Court 2026-07-14 $1,050,000；3/2 Stockton Bend 2026-07-06 $585,000 [[Q1C6]] | https://reiwa.com.au/sold/cockburn-central/ | 未给 | 各成交日 | 2026-10-30 | supported |
| suburb 中位价（背景） | Cockburn Central 全 suburb | $975,000；数据最后更新 2026-10-30，覆盖截至 2026 年 9 月的 12 个月 [[Q2C1]]；3BR $930K、4BR $1.21M [[Q2C2]] | https://reiwa.com.au/suburb/cockburn-central/ | 2026-10-30（数据更新日） | 12 个月至 2026-09 | 2026-10-30 | supported |
| 无法计算两个年度区间变化 | suburb | 页面只给一个 12 个月期间，无前一完整可比年度数值 [[Q2C3]] | 同上 | — | — | 2026-10-30 | supported（推断） |
| 21.7% 增长不可比 | suburb | 未注明期间、房型、样本量，不能当作两个完整年度区间涨幅 [[Q2C4]] | 同上 | — | — | 2026-10-30 | supported（推断） |

**说明：** 上述单幢成交价格不能直接拼成“同一房产的涨跌趋势”；27 Paddock Parade 的 $810,000→$1,000,000 是同一地址两次成交，但两次房型/条件是否完全可比未在资料中说明，只能作为个案记录，不能外推为区域趋势。suburb 中位价 $975,000 只是区域背景，**不能代表 11 Furlong St 的估值** [[Q1C7]]。

### 事项 2：同一范围的在售库存变化

| 发现 | 范围 | 数值/原文 | 来源 URL | 发布日期 | 数据期间 | 访问日期 | 核验状态 |
|---|---|---|---|---|---|---|---|
| REIWA 在售数 | Cockburn Central 及周边 suburb | “210 properties and houses for sale”；列表“1-20 of 268 results”；未按 house 或时点拆分 [[Q2C5]] | https://reiwa.com.au/for-sale/cockburn-central/ | 未给 | 单一时点 | 2026-10-30 | supported |
| OnTheHouse 在售数 | Cockburn Central | 当前 37 套在售；未按 house 拆分，无历史时点 [[Q2C6]] | https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896 | 未给 | 单一时点 | 2026-10-30 | supported |
| Perth 全市挂牌数（背景） | Perth 全市 | 2026 年 5 月底 5,137 套，比 4 月高 16.0%，比一年前高 20.7% [[Q2C7]] | https://reiwa.com.au/news/homes-taking-nearly-twice-as-long-to-sell | 未给 | 2026-05 末 | 2026-10-30 | supported |
| Perth 全市价格增长（背景） | Perth 全市 | 年度 house 中位成交价增长：2025-12→2026-03 为 5.3%，2026-03→06 为 5.0%，2026-06→09 为 2.1% [[Q2C8]] | https://reiwa.com.au/news/perth-property-price-growth-slowed-significantly-in-the-september-2026-quarter | 未给 | 各季度区间 | 2026-10-30 | supported |

**库存结论：** 地址附近 1 公里半径内的 house 在售库存**历史时点数据缺失（missing）**；suburb 级只有单一时点、且两个来源口径不同（210/268 vs 37），**不能据此写库存增加或减少**。Perth 全市挂牌数属全市背景，不能升级为 Cockburn Central 或地址附近事实 [[Q2C7]]。

### 事项 3：假设购价与贷款余额下的负资产临界条件

| 项目 | 内容 | 标记 |
|---|---|---|
| 假设 | 购价 AUD 1,000,000，固定贷款余额 AUD 800,000；为教学假设，非用户真实财务信息，也非目标地址估值 [[Q3C6]] | [[Q3C6]] |
| 定义 | 市值 < 贷款余额 ⇒ 净权益为负 | — |
| 临界市值 | = 贷款余额 = **AUD 800,000** [[Q3C1]] | [[Q3C1]] |
| 抗跌幅度 | (1,000,000 − 800,000) / 1,000,000 = **20%** [[Q3C2]] | [[Q3C2]] |
| 等于临界值 | 市值 = 800,000 ⇒ 净权益 = 0，**不构成负资产** [[Q3C3]] | [[Q3C3]] |
| 低于临界值 | 市值 = 799,999 ⇒ 净权益 = −1，构成负资产 [[Q3C3]] | [[Q3C3]] |
| 简化 | 不计交易成本、出售成本、税费及贷款余额随时间变化 [[Q3C4]] | [[Q3C4]] |
| 边界 | 20% 抗跌幅度不等于预测下跌概率，也不证明未来不会负资产 [[Q3C5]] | [[Q3C5]] |

**算术核验：** 1,000,000 − 800,000 = 200,000；200,000 / 1,000,000 = 0.20 = 20%，一致。

---

## 3. 支持材料、反对材料与未解决缺口

### 3.1 对“现在买入风险较低／未来有上涨空间”的支持材料

- 27 Paddock Parade 同一地址 2024-07-01 售 $810,000、2026-05-22 售 $1,000,000，个案显示该地址两年内成交价上升 [[Q1C5]]。**仅支持该单幢个案的价格记录，不能外推为区域或未来趋势。**
- suburb 页显示 house 中位价 $975,000、4BR 中位价 $1.21M [[Q2C1]][[Q2C2]]。**仅为 suburb 背景，不能代表 11 Furlong St 估值。**
- 上述材料**均不足以支持“现在买入风险较低”或“未来必涨”的结论**。

### 3.2 反对材料

- Perth 全市年度 house 中位成交价增长率由 5.3%→5.0%→2.1%，增速明显放缓 [[Q2C8]]。**这是 Perth 全市数据，不是 Cockburn Central 数据，只能作为背景警示。**
- Perth 全市挂牌数同比高 20.7% [[Q2C7]]。**全市背景，不能写成 Cockburn Central 库存增加。**
- 房型口径冲突：11 Furlong St 被标 House 但描述为 townhouse [[Q1C2]]，影响“同类住宅”可比性。

### 3.3 未解决缺口（只描述限制，不作事实）

1. **定位缺口：** 门牌 11 的精确坐标未核实，1 公里半径圆心未定，半径内样本量无法确定 [[Q1C3]]。
2. **价格变化缺口：** suburb 只有截至 2026-09 的一个 12 个月中位价，缺前一完整可比年度，无法计算两个年度区间变化 [[Q2C3]]；21.7% 增长无期间/房型/样本量说明，不可比 [[Q2C4]]。
3. **库存缺口：** 地址附近无历史时点库存；suburb 级仅单一时点且口径不一 [[Q2C5]][[Q2C6]]。
4. **可比条件缺口：** 多数成交缺建筑面积、卧室数或土地面积（如 37 Paddock Parade、178 Semple Court、3/2 Stockton Bend 仅有价格与日期）[[Q1C6]]。
5. **发布日期缺口：** REIWA 单条成交页与 OnTheHouse 页均未给页面发布日期，仅有成交日期与抓取时间 2026-10-30。
6. **挂牌价与成交价：** 在售列表只给挂牌价，无对应成交价，不能混用。
7. **负资产计算缺口：** 若计入出售成本/税费，临界市值会高于 800,000，资料未给任何成本数值；贷款余额随时间变化未涵盖 [[Q3C4]]。

---

## 4. 事实、条件计算与推断的区分

- **观察到的事实：** 各单幢成交记录 [[Q1C1]][[Q1C4]][[Q1C5]][[Q1C6]]；suburb 中位价与分项 [[Q2C1]][[Q2C2]]；在售数 [[Q2C5]][[Q2C6]]；Perth 全市挂牌与增长率 [[Q2C7]][[Q2C8]]；房型口径冲突 [[Q1C2]]；定位结果 [[Q1C3]]。
- **条件计算：** 临界市值 800,000、抗跌幅度 20%、等于/低于临界值区别 [[Q3C1]][[Q3C2]][[Q3C3]]。
- **推断：** 无法计算两个年度区间变化 [[Q2C3]]；21.7% 不可比 [[Q2C4]]；抗跌幅度不等于下跌概率 [[Q3C5]]。

---

## 5. 结论边界

- 三个事项**不足以完整判断购房风险**；未调查的风险不能写成不存在。
- 不输出保证收益或确定买入建议。
- 历史上涨（如 27 Paddock Parade 个案）不能直接推成未来必涨。
- 地址附近 1 公里半径内的价格变化与库存变化均**未取得可核实数据**，相关结论标 missing。

---

## 6. 覆盖情况、反对材料与不确定性

| 项目 | 状态 |
|---|---|
| 事项 1 价格变化 | 部分覆盖：有单幢成交与 suburb 背景；缺两个完整可比年度区间与半径内样本 |
| 事项 2 库存变化 | 部分覆盖：仅单一时点、口径不一；半径内历史库存 missing |
| 事项 3 负资产计算 | 完整覆盖（静态情景），算术已核验 |
| 地址定位 | 部分覆盖：街道级已核实，门牌级未核实 |
| 房型口径 | 存在冲突，未解决 |
| 引用与结论检查 | 仅基于 checked_claims 的 supported 陈述；light 路线默认不执行 14.5，**未逐句核验** |
| RACE/FACT | **未运行、未提交** |

**主要不确定性：** 半径圆心未定导致“附近”样本无法确认；suburb 与全市数据不能替代地址附近事实；房型口径冲突影响同类可比性；页面发布日期缺失影响时效判断。

**来源清单：** 见 source_catalog（REIWA 单条成交页、REIWA suburb 页、REIWA 在售/成交列表页、OnTheHouse、Nominatim、REIWA 新闻页、TASK）。所有访问日期为 2026-10-30。

## 程序生成的引用索引

逐字片段和核验理由见同目录 claims.json。TASK 指冻结任务中的教学假设。

- Q1C1 → 11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025；来源：https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/；访问时间：2026-10-30T10:18:57.580706Z
- Q1C1 → 11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025；来源：https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/；访问时间：2026-10-30T10:18:57.580706Z
- Q1C2 → 11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025；来源：https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/；访问时间：2026-10-30T10:18:57.580706Z
- Q1C2 → 11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025；来源：https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/；访问时间：2026-10-30T10:18:57.580706Z
- Q1C3 → search；来源：https://nominatim.openstreetmap.org/search?q=11+Furlong+Street+Cockburn+Central+WA&format=json；访问时间：2026-10-30T10:19:43.483450Z
- Q1C3 → search；来源：https://nominatim.openstreetmap.org/search?q=11+Furlong+Street+Cockburn+Central+WA&format=json；访问时间：2026-10-30T10:19:43.483450Z
- Q1C4 → 27-furlong-street-cockburn-central-wa-6164-sold-29-jan-2026；来源：https://reiwa.com.au/27-furlong-street-cockburn-central-4984527/；访问时间：2026-10-30T10:19:37.441960Z
- Q1C4 → 27-furlong-street-cockburn-central-wa-6164-sold-29-jan-2026；来源：https://reiwa.com.au/27-furlong-street-cockburn-central-4984527/；访问时间：2026-10-30T10:19:37.441960Z
- Q1C5 → 27-paddock-parade-cockburn-central-wa-6164-sold-on-22-may-2026-onthehouse；来源：https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896；访问时间：2026-10-30T10:18:49.815899Z
- Q1C5 → 27-paddock-parade-cockburn-central-wa-6164-sold-on-22-may-2026-onthehouse；来源：https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896；访问时间：2026-10-30T10:18:49.815899Z
- Q1C5 → 27-paddock-parade-cockburn-central-wa-6164-sold-on-22-may-2026-onthehouse；来源：https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896；访问时间：2026-10-30T10:18:49.815899Z
- Q1C6 → sold-real-estate-in-cockburn-central-wa-6164-sold-house-and-property-prices-reiw；来源：https://reiwa.com.au/sold/cockburn-central/；访问时间：2026-10-30T10:18:31.955173Z
- Q1C6 → sold-real-estate-in-cockburn-central-wa-6164-sold-house-and-property-prices-reiw；来源：https://reiwa.com.au/sold/cockburn-central/；访问时间：2026-10-30T10:18:31.955173Z
- Q1C6 → sold-real-estate-in-cockburn-central-wa-6164-sold-house-and-property-prices-reiw；来源：https://reiwa.com.au/sold/cockburn-central/；访问时间：2026-10-30T10:18:31.955173Z
- Q1C7 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q1C7 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q2C1 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q2C2 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q2C2 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q2C2 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q2C3 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q2C4 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q2C5 → real-estate-for-sale-cockburn-central-wa-6164-real-estate-listings-cockburn-cent；来源：https://reiwa.com.au/for-sale/cockburn-central/；访问时间：2026-10-30T10:18:25.867680Z
- Q2C5 → real-estate-for-sale-cockburn-central-wa-6164-real-estate-listings-cockburn-cent；来源：https://reiwa.com.au/for-sale/cockburn-central/；访问时间：2026-10-30T10:18:25.867680Z
- Q2C6 → 27-paddock-parade-cockburn-central-wa-6164-sold-on-22-may-2026-onthehouse；来源：https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896；访问时间：2026-10-30T10:18:49.815899Z
- Q2C7 → homes-taking-nearly-twice-as-long-to-sell；来源：https://reiwa.com.au/news/homes-taking-nearly-twice-as-long-to-sell；访问时间：2026-10-30T10:19:01.630237Z
- Q2C8 → perth-property-price-growth-slowed-significantly-in-the-september-2026-quarter；来源：https://reiwa.com.au/news/perth-property-price-growth-slowed-significantly-in-the-september-2026-quarter；访问时间：2026-10-30T10:19:23.984490Z
- Q3C1 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C1 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C2 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C3 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C4 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C5 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C6 → TASK；来源：frozen/task.md；访问时间：not_applicable
