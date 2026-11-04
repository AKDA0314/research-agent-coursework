# Cockburn Central house：买入时机与证据缺口调查

**信息截止日：2026-10-30（Australia/Perth）。** 本报告只使用给定资料与 checked_claims 中 status=supported 的陈述作为证据性结论；gaps 与 rejected_claims 只用于描述限制，不升级为事实。

---

## 1. 范围说明

- **地址核实**：11 Furlong Street, Cockburn Central WA 6164 在 REIWA 记录为 House，2025-05-13 成交价 $768,000，4 卧 3 卫 2 车位，地块 172 平方米 [[Q1C1]]。该地址拼写与 suburb 与用户提供一致。
- **定位来源与限制**：OpenStreetMap/Nominatim 检索仅返回 Furlong Street 道路级结果（中心约 -32.1158872, 115.8494353，Cockburn Central WA 6164），未返回 11 号门牌点位 [[Q1C8]]；因此无法据此界定 1 公里直线半径 [[Q2C7]]。
- **地域边界**：任务设定的工作默认范围为地址定位点 1 公里直线半径；由于门牌级坐标缺失，**该半径未能实际界定**，本报告不声称取得“附近”样本集合。
- **房型**：仅 house；suburb 级在售页面混含 unit、apartment、townhouse、house 和 land，未按 house 单列 [[Q2C2]]。
- **统计期**：suburb 中位价数据最后更新 2026-10-30，含截至 2026 年 9 月的 12 个月成交 [[Q1C4]]；OnTheHouse 估值截至 2026-09-30 [[Q1C6]]。
- **分栏原则**：地址附近样本与 Cockburn Central suburb 整体统计分栏；6164 仅作辅助定位。

---

## 2. 三事项证据表

### 事项 1：同一区域、同类住宅的价格变化

| 发现 | 范围 | 数值/原文 | 来源 URL | 发布日期/数据期间 | 访问日期 | 核验状态 |
|---|---|---|---|---|---|---|
| 11 Furlong St 为 House，2025-05-13 成交 $768,000，4卧3卫2车位，地块172㎡ | 单笔成交（该地址） | Sold price: $768,000；Sold: 13 May 2025；Landsize 172m | https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/ | 成交 2025-05-13 | 2026-10-30 | supported [[Q1C1]] |
| 27 Furlong St 为 House，2026-01-29 成交 $940,000，4卧2卫2车位，地块187㎡ | 单笔成交（同街另一房产） | Sold price: $940,000；Sold: 29 Jan 2026；Landsize 187m | https://reiwa.com.au/27-furlong-street-cockburn-central-4984527/ | 成交 2026-01-29 | 2026-10-30 | supported [[Q1C2]] |
| 两笔价差 $172,000，按前者计约 +22.4%；但为不同房产，不能视为同一房产涨跌 | 两笔不同房产 | 940000−768000=172000；172000/768000=22.40% | 同上两源 | 2025-05-13 与 2026-01-29 | 2026-10-30 | supported（计算）[[Q1C3]] |
| suburb 整体 house 中位价 $975,000 | suburb 背景（非1公里） | Median price data last updated 30 October 2026 containing transactions for the 12 month period ending September 2026；Landgate/REIWA | https://reiwa.com.au/suburb/cockburn-central/ | 更新 2026-10-30；截至 2026-09 的12个月 | 2026-10-30 | supported [[Q1C4]] |
| suburb 3卧 house 中位 $930K、4卧 $1.21M，无样本量、无可比上一完整年度区间 | suburb 背景 | 3BR $930K；4BR $1.21M | https://reiwa.com.au/suburb/cockburn-central/ | 未标注 | 2026-10-30 | supported [[Q1C5]] |
| OnTheHouse/Cotality suburb house 中位估值 $939,034，称过去5年上涨90.60% | suburb 级 AVM 估值（非成交价、非1公里） | median value for Houses in Cockburn Central is $939,034；as at 30 September 2026 | https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896 | 截至 2026-09-30 | 2026-10-30 | supported [[Q1C6]] |
| 27 Paddock Parade 同一房产 2024-07-01 成交 $810,000、2026-05-22 成交 $1,000,000；来源未说明与目标地址距离 | 单笔房产历史（距离未知） | Sold on 22 May 2026 for $1,000,000；01 Jul 2024 Sold for $810,000 | 同上 | 2024-07-01 与 2026-05-22 | 2026-10-30 | supported [[Q1C7]] |

**事项 1 缺口**：未取得门牌级坐标，无法界定 1 公里半径；未找到按 1 公里半径统计的 house 成交中位价或样本量；未取得最近两个已发布、完整且可比的年度区间（含起止日期、发布日期、样本量）的 house 成交指标；挂牌价与成交价未系统配对；suburb 级 REIWA 成交中位 $975,000 与 Cotality AVM 估值 $939,034 定义不同，不可互换或拼接成趋势。

### 事项 2：同一范围的在售库存变化

| 发现 | 范围 | 数值/原文 | 来源 URL | 发布日期/数据期间 | 访问日期 | 核验状态 |
|---|---|---|---|---|---|---|
| REIWA 在售页面为 suburb 级挂牌结果总数，非1公里半径 house 库存 | suburb 级 | 1-20 of 268 results；Displaying 1-20 of 268 properties | https://reiwa.com.au/for-sale/cockburn-central/ | 未标注 | 2026-10-30 | supported [[Q2C1]] |
| 该页面混含 unit、apartment、townhouse、house、land，未按 house 单列 | suburb 级 | 31 Equitation Terrace；51 Muriel Court；Lot 136, Filly Avenue | 同上 | 未标注 | 2026-10-30 | supported [[Q2C2]] |
| Perth 全市活跃挂牌：2025年末低于2,000；2026年5月末5,137 | Perth 全市（非附近） | active listings fall to below 2,000 at the end of December；5,137 at the end of May | https://reiwa.com.au/the-wa-market/resources/articles/affordability--accessibility-and-availability-to-drive-the-market-in-2026/ ；https://reiwa.com.au/news/homes-taking-nearly-twice-as-long-to-sell | 2025年末；2026-05末 | 2026-10-30 | supported [[Q2C5]] |
| 另一来源：截至2026-04-12四周 Perth 挂牌 3,669 套，与5月末5,137不同时点/窗口，不能相减 | Perth 全市（非附近） | the number of properties listed for sale in Perth surged by 20 per cent to 3,669 properties | https://www.apimagazine.com.au/news/article/perth-property-boom-to-power-through-2026-before-sharp-slowdown-looms | 截至 2026-04-12 的四周 | 2026-10-30 | supported [[Q2C6]] |
| 定位仅返回道路级坐标，无法界定1公里半径 | 定位 | Furlong Street, Cockburn Central, Western Australia, 6164, Australia | https://nominatim.openstreetmap.org/search?q=11+Furlong+Street+Cockburn+Central+WA&format=json | 未标注 | 2026-10-30 | supported [[Q2C7]] |

**事项 2 缺口**：**地址附近历史库存标为 missing**——未找到同一地理范围（1公里半径）、house 类型、同一统计定义在两个时点或期间的在售数量。suburb 级在售数存在口径冲突（REIWA 268 条含周边与多房型；OnTheHouse 37 套未分房型，且该候选因引文未逐字匹配被列为 missing，不作证据）。Perth 全市多个时点统计窗口与范围不一致，不能拼接成 Cockburn Central 库存趋势。新房供应、建筑批准量、开工量、完工量未取得，且不能替代在售库存变化。

### 事项 3：假设购价与贷款余额下的负资产临界条件

| 发现 | 范围 | 数值/原文 | 来源 | 数据期间 | 访问日期 | 核验状态 |
|---|---|---|---|---|---|---|
| 教学假设：购价 AUD 1,000,000、固定贷款余额 AUD 800,000，非用户真实财务信息或目标地址估值 | 条件假设 | 购价 AUD 1,000,000；贷款余额 AUD 800,000 | TASK（frozen/task.md） | 不适用 | not_applicable | supported [[Q3C1]] |
| 简化定义：市场价值小于贷款余额时净权益为负 | 条件定义 | 市场价值 < 贷款余额 ⇒ 净权益为负 | TASK | 不适用 | not_applicable | supported [[Q3C2]] |
| 计算式与临界值 | 条件计算 | 净权益 = V − 800,000；V < 800,000 时净权益为负；临界值 V* = AUD 800,000 | TASK | 不适用 | not_applicable | supported（计算）[[Q3C3]] |
| 等于临界值 | 条件计算 | V = 800,000：净权益 = 800,000 − 800,000 = 0，不构成负资产 | TASK | 不适用 | not_applicable | supported（计算）[[Q3C4]] |
| 超过临界值 | 条件计算 | V = 900,000：净权益 = +100,000 > 0 | TASK | 不适用 | not_applicable | supported（计算）[[Q3C5]] |
| 低于临界值 | 条件计算 | V = 700,000：净权益 = −100,000 < 0 | TASK | 不适用 | not_applicable | supported（计算）[[Q3C6]] |
| 抗跌幅度 | 条件计算 | (1,000,000 − 800,000)/1,000,000 = 20%；价值下跌超过 20% 才进入负权益 | TASK | 不适用 | not_applicable | supported（计算）[[Q3C7]] |
| 简化披露 | 条件假设 | 不计交易成本、出售成本、税费及贷款余额随时间变化；抗跌幅度不等于下跌概率预测 | TASK | 不适用 | not_applicable | supported [[Q3C8]] |

**事项 3 缺口**：本项为静态条件计算，未使用外部市场数据，不能推断目标地址或 Cockburn Central house 的实际负资产概率；未计入交易成本、出售成本、税费及贷款余额随时间变化；未考虑只还息/本息摊还、再融资或房价与贷款余额同时变动。

---

## 3. 支持材料、反对材料与未解决缺口

### 3.1 对“现在买入风险较低／未来有上涨空间”的支持材料（仅限其实际涵盖的窄结论）

- 同一条 Furlong Street 上，2026-01-29 的 house 成交价 $940,000 高于 2025-05-13 的 $768,000，价差 $172,000（约 +22.4%）[[Q1C3]]。**这只说明两笔不同房产的成交价差，不构成同一房产或该区域 house 的涨幅证据。**
- suburb 级背景：REIWA 记录 Cockburn Central house 中位价 $975,000（截至 2026-09 的12个月）[[Q1C4]]；OnTheHouse/Cotality 给出 suburb house 中位估值 $939,034，并称过去5年上涨 90.60% [[Q1C6]]。**这些是 suburb 级背景，不是 1 公里半径数据，也不是目标地址估值；历史上涨不能推成未来必涨。**
- 27 Paddock Parade 同一房产 2024-07-01 成交 $810,000、2026-05-22 成交 $1,000,000 [[Q1C7]]。**该来源未说明其与 11 Furlong St 的距离，不能升级为附近事实。**

### 3.2 反对材料

- 现有成交均为单笔挂牌页记录，未取得按 1 公里半径统计的 house 成交中位价或样本量，无法验证“附近”价格趋势（见事项 1 缺口）。
- suburb 级指标口径冲突：REIWA 成交中位 $975,000 [[Q1C4]] 与 Cotality AVM 估值 $939,034 [[Q1C6]] 定义不同，不可互换或拼接成趋势。
- 在售库存方面，地址附近历史库存为 missing；suburb 级 268 条结果混含多房型 [[Q2C1]][[Q2C2]]，Perth 全市多时点数据窗口不一致 [[Q2C5]][[Q2C6]]，均不能支持“附近库存增加或减少”的结论。
- 负资产情景显示：在购价 $1,000,000、贷款余额 $800,000 假设下，价值下跌超过 20% 即进入负权益 [[Q3C7]]；该计算为静态情景，不等于下跌概率预测 [[Q3C8]]。

### 3.3 未解决缺口

- 门牌级坐标缺失，1 公里半径无法界定 [[Q1C8]][[Q2C7]]。
- 无可比的两个完整年度区间 house 成交指标（含起止日期、发布日期、样本量）。
- 挂牌价与成交价未系统配对。
- 地址附近历史在售库存 missing；新房供应/建筑批准等指标未取得。
- 负资产计算未含交易成本、出售成本、税费及贷款余额随时间变化。

---

## 4. 事实、条件计算与推断的区分

- **观察到的事实**：Q1C1、Q1C2、Q1C4、Q1C5、Q1C6、Q1C7、Q1C8、Q2C1、Q2C2、Q2C5、Q2C6、Q2C7、Q3C1、Q3C2、Q3C8。
- **条件计算**：Q1C3（价差与百分比）、Q3C3–Q3C7（净权益与临界值）。
- **推断**：本报告未将任何历史上涨或 suburb 背景数据推断为未来走势；所有“不能视为”“不能升级”的表述均为范围限制说明，不是事实结论。

---

## 5. 结论边界

- 三个事项不足以完整判断购房风险；未调查的风险不能写成不存在。
- 本报告不输出保证收益或确定买入建议。
- 事项 1 与事项 2 的“附近”口径因门牌级坐标缺失而未能落实，相关结论只能停留在 suburb 背景或单笔成交层面。

---

## 6. 覆盖情况、反对材料与不确定性

- **覆盖情况**：已覆盖地址单笔成交（Q1C1、Q1C2）、suburb 背景中位与估值（Q1C4–Q1C6）、同街价差计算（Q1C3）、suburb 在售页面口径（Q2C1、Q2C2）、Perth 全市库存时点（Q2C5、Q2C6）、定位限制（Q1C8、Q2C7）、负资产静态计算（Q3C1–Q3C8）。
- **未覆盖**：1 公里半径内 house 成交与库存、两个可比完整年度区间、挂牌-成交配对、新房供应/建筑批准指标、扣除出售成本后的净回款。
- **反对材料**：见 3.2。
- **不确定性**：suburb 级指标定义冲突；OnTheHouse 37 套在售数与 REIWA 5,137 等候选因引文未逐字匹配被列为 missing，未作证据；Perth 全市数据不能替代附近数据。
- **执行约束说明**：本报告基于给定 checked_claims 与 source_catalog；未宣称执行 14.5 逐句核验；RACE/FACT 未运行、未提交。

## 程序生成的引用索引

逐字片段和核验理由见同目录 claims.json。TASK 指冻结任务中的教学假设。

- Q1C1 → 11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025；来源：https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/；访问时间：2026-10-30T10:18:57.580706Z
- Q1C1 → 11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025；来源：https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/；访问时间：2026-10-30T10:18:57.580706Z
- Q1C2 → 27-furlong-street-cockburn-central-wa-6164-sold-29-jan-2026；来源：https://reiwa.com.au/27-furlong-street-cockburn-central-4984527/；访问时间：2026-10-30T10:19:37.441960Z
- Q1C2 → 27-furlong-street-cockburn-central-wa-6164-sold-29-jan-2026；来源：https://reiwa.com.au/27-furlong-street-cockburn-central-4984527/；访问时间：2026-10-30T10:19:37.441960Z
- Q1C3 → 11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025；来源：https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/；访问时间：2026-10-30T10:18:57.580706Z
- Q1C3 → 27-furlong-street-cockburn-central-wa-6164-sold-29-jan-2026；来源：https://reiwa.com.au/27-furlong-street-cockburn-central-4984527/；访问时间：2026-10-30T10:19:37.441960Z
- Q1C4 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q1C5 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q1C6 → 27-paddock-parade-cockburn-central-wa-6164-sold-on-22-may-2026-onthehouse；来源：https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896；访问时间：2026-10-30T10:18:49.815899Z
- Q1C7 → 27-paddock-parade-cockburn-central-wa-6164-sold-on-22-may-2026-onthehouse；来源：https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896；访问时间：2026-10-30T10:18:49.815899Z
- Q1C7 → 27-paddock-parade-cockburn-central-wa-6164-sold-on-22-may-2026-onthehouse；来源：https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896；访问时间：2026-10-30T10:18:49.815899Z
- Q1C8 → search；来源：https://nominatim.openstreetmap.org/search?q=11+Furlong+Street+Cockburn+Central+WA&format=json；访问时间：2026-10-30T10:19:43.483450Z
- Q2C1 → real-estate-for-sale-cockburn-central-wa-6164-real-estate-listings-cockburn-cent；来源：https://reiwa.com.au/for-sale/cockburn-central/；访问时间：2026-10-30T10:18:25.867680Z
- Q2C1 → real-estate-for-sale-cockburn-central-wa-6164-real-estate-listings-cockburn-cent；来源：https://reiwa.com.au/for-sale/cockburn-central/；访问时间：2026-10-30T10:18:25.867680Z
- Q2C2 → real-estate-for-sale-cockburn-central-wa-6164-real-estate-listings-cockburn-cent；来源：https://reiwa.com.au/for-sale/cockburn-central/；访问时间：2026-10-30T10:18:25.867680Z
- Q2C2 → real-estate-for-sale-cockburn-central-wa-6164-real-estate-listings-cockburn-cent；来源：https://reiwa.com.au/for-sale/cockburn-central/；访问时间：2026-10-30T10:18:25.867680Z
- Q2C2 → real-estate-for-sale-cockburn-central-wa-6164-real-estate-listings-cockburn-cent；来源：https://reiwa.com.au/for-sale/cockburn-central/；访问时间：2026-10-30T10:18:25.867680Z
- Q2C5 → affordability-accessibility-and-availability-to-drive-the-market-in-2026；来源：https://reiwa.com.au/the-wa-market/resources/articles/affordability--accessibility-and-availability-to-drive-the-market-in-2026/；访问时间：2026-10-30T10:19:09.365505Z
- Q2C5 → homes-taking-nearly-twice-as-long-to-sell；来源：https://reiwa.com.au/news/homes-taking-nearly-twice-as-long-to-sell；访问时间：2026-10-30T10:19:01.630237Z
- Q2C6 → perth-property-boom-to-power-through-2026-before-sharp-slowdown-looms-residentia；来源：https://www.apimagazine.com.au/news/article/perth-property-boom-to-power-through-2026-before-sharp-slowdown-looms；访问时间：2026-10-30T10:18:32.337655Z
- Q2C7 → search；来源：https://nominatim.openstreetmap.org/search?q=11+Furlong+Street+Cockburn+Central+WA&format=json；访问时间：2026-10-30T10:19:43.483450Z
- Q3C1 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C2 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C3 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C4 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C5 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C6 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C7 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C8 → TASK；来源：frozen/task.md；访问时间：not_applicable
