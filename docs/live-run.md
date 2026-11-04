# 真实模型六步运行

如果最后一步出现 `Output not complete: length`，见 [仅重跑审查的命令](audit-retry.md)，不必从头重跑。

## 课堂演示：按顺序执行

先在 macOS 终端进入本作业仓库。以下命令在同一个终端窗口执行；Python 3.9+ 标准库即可，不需要启用 HyperResearch 虚拟环境。

1. 展示原始任务与六步代码：本仓库的 `evidence/task.md`、`src/six_step.py`。API 通信在 `src/deepseek_client.py`，命令入口在 `scripts/run_live.py`。
2. 检查模型连接（不生成报告）：

```sh
python3 scripts/run_live.py models --key-file .local-runs/deepseek.env
```

看到 `available: true` 表示指定模型可用。不要投屏打开密钥文件。

3. 如只展示已经真实跑过的记录，不发起收费生成：

```sh
python3 -m json.tool .local-runs/deepseek-flash-01/run.json
open .local-runs/deepseek-flash-01
```

打开 report.md 展示报告、claims.json 展示核验，再打开 report-audit.json 解释为什么没有通过。

4. 如需要现场重新运行，以下命令会发起一次新的收费实验；最多 9 次生成调用，客户端预算上限 5 元。第一次历史运行估费约 0.73 元，不保证新运行费用和输出相同。

```sh
demo_run=".local-runs/classroom-$(date +%Y%m%d-%H%M%S)"
python3 scripts/run_live.py run --key-file .local-runs/deepseek.env --frozen .local-runs/frozen-20261101 --out "$demo_run" --max-cny 5
```

输出将依次出现 plan、proposal、check、report、report_audit 等阶段。若返回 blocked_review 与退出码 1，应展示失败原因；不要为“演示成功”反复重跑。原冻结资料与原结果不覆盖。

5. 新运行结束后，在同一终端执行以下两行，生成对照并打开结果文件夹。这不会再调用模型：

```sh
python3 scripts/compare_live.py "$demo_run"
open "$demo_run"
```

口头说明：“现场这次是真实模型读冻结资料生成报告；Python 检查引用、记录预算并控制停止。模型检查器也可能错，所以保留原始返回和拒绝交付状态。重复展示旧文件不算重复实验，现场新跑一次也还不足以证明稳定性。”

## 已有运行与详细说明

第一次真实运行已结束，见 [结果与失败对照](live-comparison-01.md)。当前目录已经存在，不要重复执行运行命令来覆盖它。

正式入口是 `scripts/run_live.py`，模型由 DeepSeek API 调用产生实际结果。
旧 `offline_rules.py` 和 `fixtures/*.json` 仅服务历史课堂演示，正式入口不导入它们。
“固定”的是研究委托、来源快照、提示结构与预算，不是模型要给出的答案。

## 密钥与模型

在仓库本机的 `.local-runs/deepseek.env` 第 1 行填写 `DEEPSEEK_API_KEY=`，等号后紧接自己的密钥，保持纯文本。
该目录被 Git 忽略，密钥文件权限应为 600。不要把密钥放进 task、源码、截图或聊天。
也可不用文件，改从同名环境变量读取。程序不执行 `.env` 中的 shell 代码。

```sh
python3 scripts/run_live.py models --key-file .local-runs/deepseek.env
```

这个命令调用官方 `GET /models`，只显示模型 ID/名称，不生成文本。
Key 用于账户鉴权；实际模型由请求的 `model` 字段选择。
2026-11-01 查阅的官方映射为 `deepseek-flash` → DeepSeek-V4.1-Flash-1017；别名以后可能更新，运行协议及响应会留档。
参考：[模型列表](https://api-docs.deepseek.com/api/list-models/)、[人民币价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing/)。

## 本次固定输入与执行命令

已准备的本地冻结目录是 `.local-runs/frozen-20261101/`。
其中 `task.md` 是原始任务的逐字节副本，SHA-256 为
`5203bace7a264be8dbdfc8b8ea1aa4a9bd47510300eb2ec961d1133b0f8d01e8`。
`corpus.json` 保存原研究的 15 条来源正文及原文件/正文哈希，排除旧报告与 YAML 中 AI 编写的摘要和标签。
保留来源 URL、笔记 ID、访问时间；访问时间不等于发布日期或数据期间。
这份事后保存的资料不能证明旧研究的每一步接触到完全相同的资料。

准备新快照的通用命令（已有目录会拒绝覆盖）：

```sh
python3 scripts/run_live.py freeze --task ../hyperresearch-lab/task.md --notes ../hyperresearch-lab/research/notes --out .local-runs/frozen-20261101
```

只运行一次的命令：

```sh
python3 scripts/run_live.py run --key-file .local-runs/deepseek.env --frozen .local-runs/frozen-20261101 --out .local-runs/deepseek-flash-01 --max-cny 5
```

同名运行目录存在即停止，防止覆盖失败证据。执行后不要为了得到好结果重复运行；需要新实验时另行登记。
结果返回 `blocked_review` 或失败不代表可以删掉本次记录重新选一份。

运行结束后生成对照表和描述性计数（不额外调用模型）：

```sh
python3 scripts/compare_live.py .local-runs/deepseek-flash-01
```

它会产生 `comparison.md` 与 `comparison-metrics.json`；报告质量需要另外逐项阅读核验，计数本身不是质量评分。

## 六步落实在哪里

| 职责 | 实际输入/动作 | 可查看的输出 |
|---|---|---|
| 拆主张 | 模型读取完整 task 与来源目录，分成最多三个问题 | `plan.json`：question、claim_key、completion_condition、scope_requirements |
| 拟查询 | 模型生成 query 与 source_type | `plan_query` 事件；本地搜索按 query 排序 |
| 写回观察 | Python 读取全部冻结来源，逐轮交给模型；不联网补抓 | `trace.jsonl` 的 search_frozen / read_frozen，含空匹配、正文与来源 ID |
| 绑定核验 | 模型提议原子陈述，程序查逐字引用，再由独立上下文的同模型查语义、范围、时间及算术 | `claims.json`：candidate、bindings、literal_errors、model_verdict、最终 verdict |
| 记账 | 一轮提议一单位，一轮检查一单位，最多三对；其他模型调用另计费用 | budget 事件、API usage、run.json 的 spent / remaining_budget / estimated_cost_cny |
| 停止交付 | 计划轮次结束后写报告，再审查任务覆盖与引用；API/解析失败立刻停，不重试 | report.md、report-audit.json、run.json：stop_reason 与 review_status 分开 |

每轮读取全部冻结来源，仅按查询排序，不截断为前几条。因此检索环节是固定资料阅读实验，不是自主联网搜索。
只有核验为 supported 的陈述才能进入证据结论；引用格式为 `[[Q1C1]]`，通过 `claims.json` 追到来源 ID、URL 与逐字片段。
仅仅逐字引用存在不会自动变成 supported。语义检查仍可能错，所以 `human_review=pending`、`deliverable=false` 保留，不能把程序状态写成已通过人工验收。

## 调用与预算

最多 9 次生成调用：1 次规划 + 最多 3 对提议/检查 + 1 次写报告 + 1 次报告审查。
课堂的六操作单位按批次计数，并非 6 次全部 API 调用，也不是 6 元。
本次 temperature=0、thinking=disabled；温度为零不保证服务端重复输出一致。

按官方人民币高峰、未命中缓存的费率保守估算：输入每百万 token 2 元，输出 8 元。
每次发送前按 UTF-8 字节数加协议余量及最大输出预留，返回后用实际 token 用量重新记账。
未知用量的失败保留该次预留费用，停止，不自动重试。
5 元是客户端预算检查，非服务商账户的硬性扣款设置；最终收费以 DeepSeek 账单为准。

## 证据和比较边界

运行目录保留 protocol.json、plan.json、claims.json、gaps.json、report.md、report-audit.json、run.json、trace.jsonl，
以及每次完整的请求/响应/错误文件。鉴权头不写入日志，密钥值在落盘文本中替换。
来源全文与原始调用放在本地忽略目录，公开提交需要另外选取脱敏短片段。

旧 HyperResearch 报告只在调用外保存为 baseline-report.md 用于对照，绝不传给生成器或检查器。
比较固定的是完整任务和现存来源；旧模型、联网过程、预算与本次不同，属于一次观察性对照，
不满足 task.md 中“同模型同预算单因素”的另一项实验要求，也不替代已有的离线单因素实验。
可以比较任务覆盖、引用支持、范围错误和缺口披露，不能据此证明哪套框架更强或多次运行稳定。
本次正式 RACE/FACT 仍是未运行、未提交。
