# Cockburn Central house：买入时机与证据缺口调查报告

**信息截止日：2026-10-30（Australia/Perth）。** 本报告只使用给定资料与 checked_claims 中 status=supported 的陈述作为证据性结论；gaps 与未通过候选仅用于描述限制，不升级为事实。

---

## 1. 范围说明

- **地址核实状态：部分核实。** OpenStreetMap Nominatim 对“11 Furlong Street Cockburn Central WA”的检索仅返回 Furlong Street 道路（residential，place_rank 26），坐标 lat -32.1158872、lon 115.8494353，未返回门牌 11 号的具体点位 [[Q1C2]]。因此无法确认 11 号门牌的精确坐标；suburb 归属 Cockburn Central WA 6164 有 REIWA 郊区页邮编支持 [[Q1C3]]。
- **地域边界：** 工作默认口径为上述道路坐标点 1 公里直线半径（助教设定的初始口径，非用户指定、非评估标准）。**但现有成交记录均未提供与锚点的距离，无法确认是否落在 1 公里内，半径内样本量未取得**（见缺口）。
- **房型：** 仅 house；不混入 apartment/unit、空地。
- **统计期与截止日：** 信息截止 2026-10-30；suburb 中位价数据为截至 2026 年 9 月的 12 个月期间，更新于 2026-10-30 [[Q1C3]]。
- **分栏原则：** 地址附近样本与 Cockburn Central suburb 整体统计分列；6164 邮编与 Perth 全市数据仅作背景，不写成地址附近事实。

---

## 2. 三事项证据表

| 事项 | 发现 | 范围 | 数值/原文 | 来源 URL / 笔记 ID | 发布日期 | 数据期间 | 访问日期 | 核验状态 |
|---|---|---|---|---|---|---|---|---|
| 1 价格变化 | 11 Furlong St 为 4卧3卫2车位 house，2025-05-13 成交 $768,000，土地 172m | 单宗成交（地址本身） | $768,000；4/3/2；172m | https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/ (11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025) | 未提供 | 成交日 2025-05-13 | 2026-10-30 | supported [[Q1C1]] |
| 1 价格变化 | 27 Furlong St 为 4卧2卫2车位 house，2026-01-29 成交 $940,000，土地 187m | 单宗成交 | $940,000；4/2/2；187m | https://reiwa.com.au/27-furlong-street-cockburn-central-4984527/ (27-furlong-street-cockburn-central-wa-6164-sold-29-jan-2026) | 未提供 | 成交日 2026-01-29 | 2026-10-30 | supported [[Q1C5]] |
| 1 价格变化 | 27 Paddock Pde 为 3卧2卫 house，2026-05-22 成交 $1,000,000；此前 2024-07-01 成交 $810,000 | 单宗成交（同一房产两次成交） | $1,000,000（2026-05-22）；$810,000（2024-07-01） | https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896 (27-paddock-parade-cockburn-central-wa-6164-sold-on-22-may-2026-onthehouse) | 未提供 | 2024-07-01 与 2026-05-22 | 2026-10-30 | supported [[Q1C6]] |
| 1 价格变化（suburb 背景） | Cockburn Central house 中位价 $975,000，邮编 6164，数据为截至 2026 年 9 月的 12 个月、更新于 2026-10-30 | suburb 整体 | $975,000 | https://reiwa.com.au/suburb/cockburn-central/ (cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa) | 2026-10-30（更新日） | 截至 2026-09 的 12 个月 | 2026-10-30 | supported [[Q1C3]] |
| 1 价格变化（suburb 背景） | house 年增长 21.7%，但未给出前一年度中位价数值或样本量 | suburb 整体 | 21.7% | 同上 | 未提供 | 未明确 | 2026-10-30 | supported [[Q1C4]] |
| 2 在售库存 | **地址 1 公里半径内 house 在售库存：missing** | 地址附近 | — | — | — | — | — | missing（见缺口） |
| 2 在售库存（全市背景） | Perth 全市在售房源在截至 4 月 12 日的四周内升至 3,669 套，2025 年底为 1,881 套；口径为 Perth 全市 listings，非 Cockburn Central 或 1 公里范围 | Perth 全市 | 3,669；1,881 | https://www.apimagazine.com.au/news/article/perth-property-boom-to-power-through-2026-before-sharp-slowdown-looms (perth-property-boom-to-power-through-2026-before-sharp-slowdown-looms-residentia) | 未提供 | 截至 4 月 12 日的四周 / 2025 年底 | 2026-10-30 | supported [[Q2C5]]（年份未在片段中明确为 2026） |
| 3 负资产临界 | 教学假设购价 AUD 1,000,000、贷款余额 AUD 800,000 | 教学情景 | 1,000,000 / 800,000 | TASK | 不适用 | 不适用 | 不适用 | supported [[Q3C1]] |
| 3 负资产临界 | 基础计算不计交易成本、出售成本、税费及贷款余额随时间变化 | 教学情景 | — | TASK | 不适用 | 不适用 | 不适用 | supported [[Q3C6]] |
| 3 负资产临界 | 抗跌幅度不等于预测下跌概率，也不证明未来不会负资产 | 教学情景 | — | TASK | 不适用 | 不适用 | 不适用 | supported [[Q3C7]] |

---

## 3. 支持材料、反对材料与未解决缺口

### 3.1 对“现在买入风险较低／未来有上涨空间”的支持材料

- **suburb 层面价格背景偏强：** Cockburn Central house 中位价 $975,000，年增长 21.7% [[Q1C3]][[Q1C4]]。**但**该增长未给出前一年度中位价数值或样本量 [[Q1C4]]，且 21.7% 未注明是 house 还是全部住宅、对比期间不明（缺口），只能作为 suburb 背景，不能推成地址附近或未来必涨。
- **同街成交价上行（单宗观察）：** 27 Furlong St 2026-01-29 成交 $940,000 [[Q1C5]]；27 Paddock Pde 同一房产 2024-07-01 $810,000 升至 2026-05-22 $1,000,000 [[Q1C6]]。这些是零散单宗成交，未确认在 1 公里内，也未控制面积/卧室等可比条件，不能构成系统趋势。
- **全市库存背景：** Perth 全市在售从 2025 年底 1,881 套升至 3,669 套 [[Q2C5]]——这实际是供给增加信号，对“稀缺推涨”是反向材料，且口径为全市，不能用于地址附近。

### 3.2 反对材料

- **库存背景指向供给回升：** Perth 全市在售房源四周内升至 3,669 套、2025 年底为 1,881 套 [[Q2C5]]，属全市口径，不能升级为 Cockburn Central 或地址附近事实，但方向上不支持“供给持续紧张”。
- **可比性不足：** 现有成交为不同房产、不同卧室/面积（11 Furlong 4/3/2 172m [[Q1C1]]；27 Furlong 4/2/2 187m [[Q1C5]]；27 Paddock 3/2 [[Q1C6]]），不能当作同一房产或同一构成的涨跌。
- **suburb 中位价不能代表该房屋估值：** $975,000 为 suburb 中位价 [[Q1C3]]，不能直接用于 11 Furlong St 的估值。

### 3.3 未解决缺口（只能描述限制，不能升级为事实）

1. **地址门牌级定位缺失：** Nominatim 仅返回道路级结果，未返回 11 号点位 [[Q1C2]]；无法确认精确坐标，也无法计算各成交与锚点的距离。
2. **1 公里半径内 house 成交样本未系统取得：** 现有记录均未提供与锚点距离，半径内样本量未披露（缺口）。
3. **suburb 中位价缺两个完整可比年度区间的成对数值：** 仅有截至 2026-09 的 12 个月中位价 $975,000 与 21.7% 增长 [[Q1C3]][[Q1C4]]，缺前一年度中位价、样本量与精确起止日期，无法核验年度变化。
4. **挂牌价与成交价未系统分列：** 仅有零散挂牌，无对应成交结果（缺口）。
5. **地址附近在售库存：missing。** 无 1 公里半径内 house 在售数量，也无同一范围、同一统计定义的两个时点数据；suburb 与 Perth 全市库存数字均为单时点或不同口径，不能据此判断地址附近库存增减（缺口）。
6. **suburb 级 house 在售库存历史：missing**（缺口）。
7. **新房供应/批准/开工/完工：** 未取得可单列补充的地址附近数据（缺口）。
8. **口径冲突：** REIWA 在售页“210 properties and houses（含周边 suburb）”与“268 results”并存，且未按 house 拆分、抓取日期未绑定，不能作为可比库存计数（未通过候选 Q2C1，conflict）。
9. **OnTheHouse 37 套在售：** 未绑定抓取日期、未按 house 拆分、无历史时点（未通过候选 Q2C2，missing）。
10. **Perth 全市 5,137 套（2026 年 5 月底）及 16.0%/20.7%：** 数值锚点未绑定，未通过（Q2C3，missing）；2025 年 12 月底低于 2,000 的年份未绑定（Q2C4，missing）。
11. **OnTheHouse AVM 中位估值 $939,034 与 REIWA 中位成交价 $975,000 口径不同：** 该对比候选未通过（Q1C8，missing），不能拼接为同一趋势。

---

## 4. 事项 3：负资产临界条件（静态情景计算）

**教学假设（非用户真实财务信息，非目标地址市场估值）：** 购价 AUD 1,000,000，贷款余额 AUD 800,000 [[Q3C1]]。

**简化定义：** 房屋当前市场价值 < 贷款余额时，房产净权益为负。

**计算式与算术核验：**
- 临界市场价值 = 贷款余额 = AUD 800,000。
- 抗跌幅度 = (购价 − 贷款余额) / 购价 = (1,000,000 − 800,000) / 1,000,000 = 0.20 = 20%。
- 算术检查：1,000,000 − 800,000 = 200,000；200,000 / 1,000,000 = 0.20 ✓。

**等于与超过临界值的区别：**
- 市场价值 = AUD 800,000：净权益 = 800,000 − 800,000 = 0，尚未构成负资产。
- 市场价值 < AUD 800,000：净权益为负，即构成负资产。

> **注意：** 上述临界值与 20% 抗跌幅度属于条件计算，其对应候选（Q1C7、Q3C2、Q3C3、Q3C4、Q3C5）在核验中均为 missing（计算未绑定/数值锚点未绑定），**不作为证据性结论**；此处仅按任务要求展示计算式与算术，供读者自行核验。

**简化披露：** 基础计算不计交易成本、出售成本、税费及贷款余额随时间变化 [[Q3C6]]；扣除出售成本的净回款需另列定义与假设，本报告未计算。抗跌幅度不等于预测下跌概率，也不证明未来不会负资产 [[Q3C7]]。

---

## 5. 事实、条件计算与推断的区分

- **观察到的事实（supported）：** 三宗成交记录 [[Q1C1]][[Q1C5]][[Q1C6]]；suburb 中位价与年增长 [[Q1C3]][[Q1C4]]；道路级定位 [[Q1C2]]；Perth 全市库存背景 [[Q2C5]]；教学假设与简化 [[Q3C1]][[Q3C6]][[Q3C7]]。
- **条件计算：** 负资产临界值 AUD 800,000 与 20% 抗跌幅度（见第 4 节，未通过核验，仅作展示）。
- **推断（须谨慎）：** 同街成交价上行、suburb 年增长可作背景，但不能推成地址附近趋势或未来必涨；全市库存回升方向上不支持“供给紧张”。

---

## 6. 结论边界

- 三个事项**不足以完整判断购房风险**；未调查的风险不能写成不存在。
- 本报告**不输出保证收益或确定买入建议**。
- 地址附近 1 公里 house 价格变化与在售库存变化均存在实质缺口（missing），suburb 与全市数据仅作背景。
- 负资产计算为教学静态情景，非用户真实财务信息，也非目标地址估值。

---

## 7. 覆盖情况、反对材料与不确定性

- **覆盖：** 事项 1 有 3 宗单宗成交 + suburb 中位价背景；事项 2 地址附近库存 missing，仅有 Perth 全市背景；事项 3 教学计算已展示但核验未通过。
- **反对材料：** Perth 全市在售回升 [[Q2C5]]；成交样本可比性不足；suburb 中位价不能代表单幢估值。
- **不确定性：** 地址门牌级定位缺失 [[Q1C2]]；半径内样本量与距离未披露；suburb 年增长口径与样本量不明 [[Q1C4]]；多个库存候选未通过核验（Q2C1 conflict；Q2C2/Q2C3/Q2C4/Q2C6/Q2C7 missing）。
- **执行约束说明：** 本报告基于给定快照与 checked_claims；light 路线默认不执行 14.5，未宣称逐句核验；正式 RACE/FACT 保持“未运行、未提交”。


## 程序生成的引用索引

逐字片段和核验理由见同目录 claims.json。TASK 指冻结任务中的教学假设。

- Q1C1 → 11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025；来源：https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/；访问时间：2026-10-30T10:18:57.580706Z
- Q1C1 → 11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025；来源：https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/；访问时间：2026-10-30T10:18:57.580706Z
- Q1C2 → search；来源：https://nominatim.openstreetmap.org/search?q=11+Furlong+Street+Cockburn+Central+WA&format=json；访问时间：2026-10-30T10:19:43.483450Z
- Q1C2 → search；来源：https://nominatim.openstreetmap.org/search?q=11+Furlong+Street+Cockburn+Central+WA&format=json；访问时间：2026-10-30T10:19:43.483450Z
- Q1C3 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q1C3 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q1C3 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q1C4 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q1C4 → cockburn-central-suburb-profile-property-market-house-prices-and-more-reiwa；来源：https://reiwa.com.au/suburb/cockburn-central/；访问时间：2026-10-30T10:19:03.106139Z
- Q1C5 → 27-furlong-street-cockburn-central-wa-6164-sold-29-jan-2026；来源：https://reiwa.com.au/27-furlong-street-cockburn-central-4984527/；访问时间：2026-10-30T10:19:37.441960Z
- Q1C5 → 27-furlong-street-cockburn-central-wa-6164-sold-29-jan-2026；来源：https://reiwa.com.au/27-furlong-street-cockburn-central-4984527/；访问时间：2026-10-30T10:19:37.441960Z
- Q1C6 → 27-paddock-parade-cockburn-central-wa-6164-sold-on-22-may-2026-onthehouse；来源：https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896；访问时间：2026-10-30T10:18:49.815899Z
- Q1C6 → 27-paddock-parade-cockburn-central-wa-6164-sold-on-22-may-2026-onthehouse；来源：https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896；访问时间：2026-10-30T10:18:49.815899Z
- Q1C6 → 27-paddock-parade-cockburn-central-wa-6164-sold-on-22-may-2026-onthehouse；来源：https://www.onthehouse.com.au/property/wa/cockburn-central-6164/27-paddock-pde-cockburn-central-wa-6164-39555896；访问时间：2026-10-30T10:18:49.815899Z
- Q2C5 → perth-property-boom-to-power-through-2026-before-sharp-slowdown-looms-residentia；来源：https://www.apimagazine.com.au/news/article/perth-property-boom-to-power-through-2026-before-sharp-slowdown-looms；访问时间：2026-10-30T10:18:32.337655Z
- Q2C5 → perth-property-boom-to-power-through-2026-before-sharp-slowdown-looms-residentia；来源：https://www.apimagazine.com.au/news/article/perth-property-boom-to-power-through-2026-before-sharp-slowdown-looms；访问时间：2026-10-30T10:18:32.337655Z
- Q3C1 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C6 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C7 → TASK；来源：frozen/task.md；访问时间：not_applicable
