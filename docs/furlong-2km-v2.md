# Furlong Street 2 公里版本：准备与运行

2026-11-04，按用户新授权准备。此时未发出新的付费模型请求。

## 文件与版本

- 新任务：[task.md](../tasks/furlong-2km-v2/task.md)。
- 本机快照：`.local-runs/furlong-2km-20261104/frozen/`，含 task.md、corpus.json、manifest.json。
- 本机资料索引：`.local-runs/furlong-2km-20261104/source-index.md`。
- 原始 HTTP 响应、提取文本、政府 PDF 与抓取状态：同级 `raw/`；网络沙箱失败单独保存在 `sandbox-fetch-failures/`。
- 位置计算：同级 `distance-evidence.json`；提取/冻结程序 `build_snapshot.py`。
- 原 `.local-runs/frozen-20261101`、两次用户运行和审查重试保持原样。

2 公里是围绕固定道路代表点的圆，不是整条道路的缓冲区。10 个案例均有平台坐标并在圈内；这不是完整成交库或库存普查。门牌标点不等于测绘成果。
18 条模型资料包含房源、当前列表、郊区页面及页面内结构化历史数据、官方规划摘录、距离派生记录与采集缺口。页面 JSON、金额标准化、程序距离均明确标明转换，不伪装为网页自然语言原句。保存原 HTML 校验和，superscript² 保留。

## 已补充与仍缺

补充了门牌平台坐标、圈内成交/当前挂牌案例、土地面积原始上标、郊区历史价格及样本量、政府开发规划。
仍缺两个时点的圈内完整 house 库存、圈内完整年度成交总体及当期批准/开工/完工的完整序列。规划预计量不能替代这些数据。价格年度字段的精确起止未明确时也须披露。
快照采用直接 HTTP 保存内容，不能混用搜索缓存的旧日期/旧值。

## 本轮代码修复

1. 检查器增加 fully_supported、unsupported_parts，以及主体、数值单位、时间、范围、句意五项检查。任何一项缺失、冲突或契约不完整，即使模型顶层写 supported，也由程序改为 missing。原模型判断保留在 model_verdict。
2. 计算采用带单位 Decimal：同币种相减、同单位相除；20% 按比例0.2运算。裸$与AUD不互换，不能通过去掉货币单位绕过绑定。只允许数学恒等常数0/1；其他输入必须绑定原文。显式 decimal_places 才允许 ROUND_HALF_UP 舍入。
3. 程序保存来源 URL 与抓取时间，检查器不能把抓取时间误当发布日期；报告必须保留已核验陈述的范围限制。
4. 审查只把真实阻断问题列入 issues；非阻断建议列 warnings。没有放松真实事实错误、引用或人工复核门。
5. 新增 --task 和离线 check，避免新任务误用旧 task；protocol 记录是否与原作业同任务。

这仍是同模型不同上下文检查，不能保证语义审查永不误判。测试证明程序约束，不证明模型质量提升。新旧任务/资料/代码都不同，不能称单因素对照。

## 自己执行

在仓库目录运行（密钥仍在本地，勿提交）：

```sh
python3 scripts/run_live.py check --task tasks/furlong-2km-v2/task.md --frozen .local-runs/furlong-2km-20261104/frozen
new_run=".local-runs/furlong-2km-run-$(date +%Y%m%d-%H%M%S)"
python3 scripts/run_live.py run --key-file .local-runs/deepseek.env --task tasks/furlong-2km-v2/task.md --frozen .local-runs/furlong-2km-20261104/frozen --out "$new_run" --max-cny 5
```

最多9次API，不自动重试；按客户端价格估算在请求前检查5元额度，不是服务商账户级硬限额。已有输出目录会拒绝覆盖。

```sh
python3 -m json.tool --no-ensure-ascii "$new_run/run.json"
python3 -m json.tool --no-ensure-ascii "$new_run/report-audit.json"
open -a TextEdit "$new_run/report.md"
```

审查通过时当前代码输出 report_generated，同时 human_review=pending、deliverable=false；不是擅自改 done。审查不通过则 blocked_review，保留原因。明确披露资料缺口可满足报告覆盖要求，但不能声称研究资料已齐全。

报告及完整 trace.jsonl、所有请求/返回均在新的输出目录。原历史比较和失败文件不被覆盖。正式 RACE/FACT 仍未运行。
