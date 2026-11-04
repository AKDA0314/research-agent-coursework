# Furlong Street 周边 2 公里 house 市场证据调查报告（V2）

信息截止：2026-11-04 Australia/Perth。本报告仅使用冻结任务与冻结资料快照，运行时不联网补抓。以下所有实质结论均就近标注 checked_claims 中核验通过（supported）的 claim_key；未通过（missing）候选与 gaps 仅用于描述限制，不作为事实结论。

## 一、范围与对象说明

- 工作中心：此前保存的 Furlong Street 道路代表点（纬度 -32.1158872，经度 115.8494353），半径 2000 米直线距离；该点不是 11 号门牌中心，本次不采用沿整条道路外扩的缓冲区。
- 房源坐标为平台地图标点，不是测绘或产权边界证明；距离为程序 Haversine 派生值，属派生数据，不是页面逐字原文。
- 房型主对象为 house；平台标 House 但正文称 townhouse 的保留双重标签、单列展示，不称独立住宅。unit/apartment/空地/开发地块不混入同类 house 对比。
- 坐标样本为主动选取的公开案例，不是全量成交或完整库存；即使多条在圈内，也不据此宣称圈内总体样本已齐全。
- suburb 整体与 Perth 数据只作单列背景，不升级为 2 公里范围统计。

## 二、三事项证据表

### 事项 1：价格变化与成交样本

**结论状态：核心证据缺失。** 冻结资料中，圈内成交样本候选（Q1C1–Q1C7）与两个已完成年度 house 中位价候选（Q1C8）均未通过核验（missing），因此本报告不能给出任何经核验的圈内成交价、成交日期、土地面积、卧室/卫浴配置或年度中位价与样本量作为证据性结论。

| 项目 | 状态 | 说明 |
|---|---|---|
| 圈内 house 成交样本（地址/成交价/日期/面积/卧室卫浴/房型） | missing | Q1C1–Q1C7 均因房型标签、卧室/卫浴/车位、经度或 within_2000m 等部分无绑定证据而未通过；不得作为事实引用 |
| 两个已完成可比年度 house 中位价与样本量 | missing | Q1C8 存在未绑定数值锚点（AUD 750000、AUD 845000）及地理范围/指标句意未支持，未通过 |
| 2026 年当前滚动 12 个月值 | 缺口 | 属未结束年度/滚动口径，不能称完整 2026 日历年；与 CalendarYear 字段对应关系未核实 |

缺口（gaps，仅描述限制）：
- 圈内成交样本为主动选取的公开案例，非全量成交；不同房屋成交价差不等于同房涨幅，不能据两宗推断区域价格趋势。
- 31 Equitation Terrace、4 Equitation Terrace、12 Lodge Court、29 Paddock Parade 为在售挂牌（无成交日期），不属成交样本。
- 郊区中位价与样本量仅覆盖 Cockburn Central suburb，不能升级为 2 公里圈统计；CalendarYear 准确起止与首次发布日期未核实。
- 所有距离为程序 Haversine 派生值，坐标为平台地图标点。

### 事项 2：在售库存与开发供应

**当前挂牌（逐条核验通过）：**

| 地址 | 报价 | 状态 | 平台房型 | 卧室/卫浴/车位 | 土地 | ListDate | 访问时间 | claim_key |
|---|---|---|---|---|---|---|---|---|
| 12 Lodge Court, Cockburn Central | Offers Over $1,150,000 | 在售（无成交日期） | House | 5卧2卫6车位 | 518m² | 2026-10-11 | 2026-11-04T10:23:07.390222+00:00 | Q2C3 |
| 31 Equitation Terrace, Cockburn Central | From $895,000 | 在售（无成交日期） | House | 4卧2卫2车位 | 159m² | 2026-08-31 | 2026-11-04T10:23:07.389642+00:00 | Q2C4 |
| 4 Equitation Terrace, Cockburn Central | Price Guide on Request | 在售（无成交日期） | House | 3卧2卫2车位 | 130m² | 2026-10-09 | 2026-11-04T10:23:07.390039+00:00 | Q2C5 |
| 29 Paddock Parade, Cockburn Central | From $1,000,000 | 在售（无成交日期） | House | 3卧3卫2车位 | 192m² | 2026-09-09 | 2026-11-04T10:23:07.390342+00:00 | Q2C6 |

以上四条均为平台标 House 的在售挂牌，报价、房型、土地面积与挂牌日期有绑定片段支持 [[Q2C3]][[Q2C4]][[Q2C5]][[Q2C6]]。

**搜索页总数与分页（仅作范围限定，非圈内库存）：**
- REIWA Cockburn Central houses 搜索页在访问时间 2026-11-04T10:22:33.506496+00:00 显示“1,355 properties and houses for sale in Cockburn Central and surrounding suburbs”，该总数含周边 suburbs，不能作为 2 公里圈内 house 库存总量 [[Q2C1]]。
- 同一搜索页显示分页“1 - 20 of 165 results”，并另列“152 results from surrounding suburbs”；分页数与周边结果数均不等于 2 公里圈内 house 在售总量 [[Q2C2]]。

**规划资料（规划容量口径）：**
- 同一结构规划 PDF 第 22 页载明：表列预计住宅数基于拟定密度，且不含 North Lake Road 沿线 Restricted Use-Office/R160 区域可额外容纳最多 459 套住宅；该预计数为规划容量口径，不是当前待售、已批准、已开工或已完工套数 [[Q2C8]]。

**缺口（gaps，仅描述限制）：**
- 库存变化 missing：冻结资料未取得同一 2 公里范围、同一 house 定义下两个时点的完整在售快照。
- 当前挂牌仅逐条覆盖 4 宗；搜索页另列 190/2 Signal Terrace、170 Muriel Court、7 Colt Entrance、28 Horseshoe Promenade、9 Abbey Court 等挂牌，但无各自详情页绑定，报价/状态/访问时间未逐条核验。
- 搜索页 22 Ridge Road 标 Under offer、806 North Lake Road 标 Sold（06 Aug 2026），属不同状态分栏，未作为在售 house 计入。
- Muriel Court 结构规划第 22 页预计住宅数表格为栅格图像，数字未转录；仅能引用“estimated projected dwelling numbers”与“additional maximum of 459 dwellings”文字，无法给出表内总套数。
- 未取得圈内当前批准、开工、完工的完整可比序列；规划容量不能当作已批准、已开工、已完工或当前待售套数。
- 结构规划适用范围为 Muriel Court 结构规划区，不能凭结构图推定某门牌 R-code，也不能升级为 2 公里圈统计。
- 规划文件最初通过时间与到期日候选（Q2C7）因 quoted_span_not_found 未通过，本报告不引用其页码与引用编号。

### 事项 3：静态负资产条件计算

**教学假设（非用户真实财务信息，非目标房屋估值）：**
- 购价 AUD 1,000,000 [[Q3C1]]。
- 固定贷款余额 AUD 800,000 [[Q3C2]]。

**简化定义：**
- 当前市场价值等于固定贷款余额时，房产净权益为零 [[Q3C3]]。
- 当前市场价值小于固定贷款余额时，房产净权益为负 [[Q3C4]]。

**临界市场价值（核验通过）：**
- 净权益为零的临界市场价值等于固定贷款余额 AUD 800,000 [[Q3C5]]。
- 公式：临界市场价值 = 贷款余额；输入：贷款余额 = AUD 800,000；结果：AUD 800,000。

**相对购价的下跌比例：**
- 该比例候选（Q3C6）因未绑定数值锚点 percent:20 未通过核验，本报告不输出其肯定结果。
- 教学公式（仅作方法说明，不输出肯定数值）：下跌比例 = (购价 − 贷款余额) / 购价；输入：购价 AUD 1,000,000、贷款余额 AUD 800,000。该比例结果未通过核验，故不在此给出肯定数值。

**等于/低于临界值的区别：**
- 等于临界值 AUD 800,000 时净权益为零 [[Q3C3]][[Q3C5]]；低于临界值时净权益为负 [[Q3C4]]。

**计算边界：**
- 基础计算不计交易成本、出售成本、税费和贷款余额变化 [[Q3C7]]。
- 条件算术正确不等于市场预测，抗跌比例不等于下跌概率 [[Q3C8]]。

## 三、支持 / 反对 / 缺口汇总

**支持（核验通过）：**
- 搜索页总数含周边 suburbs，不能当圈内库存总量 [[Q2C1]]；分页 165 与周边 152 均不等于圈内总量 [[Q2C2]]。
- 4 宗在售 house 挂牌的报价、房型、土地、挂牌日期与访问时间 [[Q2C3]][[Q2C4]][[Q2C5]][[Q2C6]]。
- 规划容量口径与额外最多 459 套住宅，非当前待售/批准/开工/完工套数 [[Q2C8]]。
- 教学假设购价与贷款余额、简化定义、临界值 AUD 800,000、计算边界 [[Q3C1]][[Q3C2]][[Q3C3]][[Q3C4]][[Q3C5]][[Q3C7]][[Q3C8]]。

**反对材料 / 未通过候选（仅描述限制，不作事实）：**
- Q1C1–Q1C7 成交样本候选均 missing，部分字段无绑定证据，不能作为成交事实。
- Q1C8 年度中位价候选 missing，存在未绑定数值锚点，不能作为中位价事实。
- Q2C7 规划通过时间/到期日候选 missing（quoted_span_not_found），不引用其页码与编号。
- Q3C6 下跌比例候选 missing（未绑定 percent:20），不输出肯定比例。

**缺口：**
- 圈内成交样本与两个已完成年度中位价均无经核验证据。
- 库存变化 missing，缺两个时点完整快照。
- 批准/开工/完工套数不可得。
- 下跌比例数值未通过核验。

## 四、结论边界

1. 本报告不能给出经核验的圈内 house 成交价、成交日期、土地面积、卧室/卫浴配置或年度中位价与样本量；相关候选均未通过核验。
2. 当前在售 house 仅逐条核验 4 宗，不能代表圈内库存总量；搜索页总数与分页数含周边 suburbs，不能当圈内库存。
3. 规划资料仅支持规划容量口径，不能当作当前待售、已批准、已开工或已完工套数。
4. 条件计算仅支持临界市场价值 AUD 800,000 及等于/低于临界值的定性区别；下跌比例数值未通过核验，不输出肯定结果。条件算术不等于市场预测，抗跌比例不等于下跌概率。
5. 不输出保证收益或确定买入建议；房产完整风险评估超出本次三个事项。
6. 审查通过不等于独立人工复核通过；human_review 单独记录。RACE/FACT 未运行、未提交。

## 五、覆盖情况与不确定性

- 覆盖：事项 2 的当前挂牌（4 宗）与搜索页范围限定、规划容量口径、事项 3 的临界值与定性区别已覆盖并有核验通过证据。
- 未覆盖：事项 1 的成交样本与年度中位价、事项 2 的库存变化与批准/开工/完工套数、事项 3 的下跌比例数值。
- 不确定性：所有距离为程序派生值；坐标为平台标点；样本为主动选取非全量；CalendarYear 起止未明确；规划表内总套数未转录。
- 来源类型区分：页面原文（搜索页、挂牌页、规划 PDF 文字）、页面内结构化数据（PropertyType、ListDate、LandsizeHtml 等字段）、程序计算距离（distance-evidence.json 派生）、人工摘录与检索失败记录分别标注，派生数据不称页面逐字原文。

## 程序生成的引用索引

逐字片段和核验理由见同目录 claims.json。TASK 指冻结任务中的教学假设。

- Q2C1 → current；来源：https://reiwa.com.au/for-sale/cockburn-central/houses/；访问时间：2026-11-04T10:22:33.506496+00:00
- Q2C2 → current；来源：https://reiwa.com.au/for-sale/cockburn-central/houses/；访问时间：2026-11-04T10:22:33.506496+00:00
- Q2C2 → current；来源：https://reiwa.com.au/for-sale/cockburn-central/houses/；访问时间：2026-11-04T10:22:33.506496+00:00
- Q2C3 → lodge12；来源：https://reiwa.com.au/12-lodge-court-cockburn-central-5070649/；访问时间：2026-11-04T10:23:07.390222+00:00
- Q2C3 → lodge12；来源：https://reiwa.com.au/12-lodge-court-cockburn-central-5070649/；访问时间：2026-11-04T10:23:07.390222+00:00
- Q2C3 → lodge12；来源：https://reiwa.com.au/12-lodge-court-cockburn-central-5070649/；访问时间：2026-11-04T10:23:07.390222+00:00
- Q2C3 → lodge12；来源：https://reiwa.com.au/12-lodge-court-cockburn-central-5070649/；访问时间：2026-11-04T10:23:07.390222+00:00
- Q2C4 → equitation31；来源：https://reiwa.com.au/31-equitation-terrace-cockburn-central-5055619/；访问时间：2026-11-04T10:23:07.389642+00:00
- Q2C4 → equitation31；来源：https://reiwa.com.au/31-equitation-terrace-cockburn-central-5055619/；访问时间：2026-11-04T10:23:07.389642+00:00
- Q2C4 → equitation31；来源：https://reiwa.com.au/31-equitation-terrace-cockburn-central-5055619/；访问时间：2026-11-04T10:23:07.389642+00:00
- Q2C4 → equitation31；来源：https://reiwa.com.au/31-equitation-terrace-cockburn-central-5055619/；访问时间：2026-11-04T10:23:07.389642+00:00
- Q2C5 → equitation4；来源：https://reiwa.com.au/4-equitation-terrace-cockburn-central-5067289/；访问时间：2026-11-04T10:23:07.390039+00:00
- Q2C5 → equitation4；来源：https://reiwa.com.au/4-equitation-terrace-cockburn-central-5067289/；访问时间：2026-11-04T10:23:07.390039+00:00
- Q2C5 → equitation4；来源：https://reiwa.com.au/4-equitation-terrace-cockburn-central-5067289/；访问时间：2026-11-04T10:23:07.390039+00:00
- Q2C5 → equitation4；来源：https://reiwa.com.au/4-equitation-terrace-cockburn-central-5067289/；访问时间：2026-11-04T10:23:07.390039+00:00
- Q2C6 → paddock29；来源：https://reiwa.com.au/29-paddock-parade-cockburn-central-5062709/；访问时间：2026-11-04T10:23:07.390342+00:00
- Q2C6 → paddock29；来源：https://reiwa.com.au/29-paddock-parade-cockburn-central-5062709/；访问时间：2026-11-04T10:23:07.390342+00:00
- Q2C6 → paddock29；来源：https://reiwa.com.au/29-paddock-parade-cockburn-central-5062709/；访问时间：2026-11-04T10:23:07.390342+00:00
- Q2C6 → paddock29；来源：https://reiwa.com.au/29-paddock-parade-cockburn-central-5062709/；访问时间：2026-11-04T10:23:07.390342+00:00
- Q2C8 → muriel-plan；来源：https://www.wa.gov.au/system/files/2024-02/cockburn-central-north-muriel-court-local-structure-plan-wapc-reference-spn-0801m-7.pdf；访问时间：2026-11-04T10:24:16.958531+00:00
- Q2C8 → muriel-plan；来源：https://www.wa.gov.au/system/files/2024-02/cockburn-central-north-muriel-court-local-structure-plan-wapc-reference-spn-0801m-7.pdf；访问时间：2026-11-04T10:24:16.958531+00:00
- Q3C1 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C2 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C3 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C4 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C5 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C7 → TASK；来源：frozen/task.md；访问时间：not_applicable
- Q3C8 → TASK；来源：frozen/task.md；访问时间：not_applicable
