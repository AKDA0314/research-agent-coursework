# 从代码到产物：六步框架逐段讲解

本说明对应 2026-11-01 的 [six_step.py](../src/six_step.py)，共 224 行。没有修改研究代码或重新调用 DeepSeek。
先读第 130 行开始的主流程，再回头读辅助函数。六步是六项职责，不是六个独立函数，也不是正好六次 API 调用。

## 先分清三个 Python 文件

| 文件 | 初学者可以怎么理解 | 实际职责 |
|---|---|---|
| [scripts/run_live.py](../scripts/run_live.py) | 开机按钮 | 解析终端参数、读密钥、加载冻结输入、创建模型和记录器、调用主流程、最后写 run.json |
| [src/six_step.py](../src/six_step.py) | 研究流程 | 冻结/检查输入、规划、读材料、提议、核验、写报告、审查 |
| [src/deepseek_client.py](../src/deepseek_client.py) | 模型电话与记录本 | 真正发 API 请求；保存请求响应；估算费用；Journal 类负责写文件和事件 |

直接执行 six_step.py 只会定义函数，不会自动启动研究，因为文件没有命令行主入口。课堂运行的是 `python3 scripts/run_live.py run ...`。

## 从这一行开始读

```python
def run_framework(task, sources, model, journal):
```

第 130 行的 `def` 是定义函数。括号内四个参数来自 run_live.py，不是从天上出现的：

- `task`：字符串，原 task.md 的完整文字。
- `sources`：列表，每个元素是一个字典，包含 source_id、url、fetched_at、text 和哈希等。
- `model`：DeepSeek 客户端对象；`model.ask(...)` 才会发起真实模型调用。
- `journal`：Journal 记录器对象；`write` 写 JSON，`event` 追加一条 JSONL 事件，`write_text` 写文字。

`对象.方法(...)` 可以先理解为“请这个对象做这件事”。`=` 将右边得到的结果保存到左边变量；`return` 将结果交给调用者。

## 第一步：拆主张——先得到问题清单

**代码位置：131–143 行；给模型的 PLAN 指令在 99–102 行。**

```python
plan = model.ask("plan", PLAN, {"task": task, "source_catalog": ...})
questions = plan.get("questions")
journal.write("plan.json", plan)
```

上面第一行省略号只为讲解缩短目录构造，不是可直接运行的替代代码。

输入是任务全文和来源目录，目录只有 ID、URL、访问时间，**此时还没给来源正文**。模型返回一个字典，questions 是里面的问题列表，每题有 claim_key、question、completion_condition、query、source_type。

程序检查问题数必须为 1–3、必要字段非空、ID 不重复。`if` 表示条件判断，`raise ValueError(...)` 表示不符合就抛出错误，外层会记录失败。

输出：`plan.json`；trace.jsonl 也有 decompose 事件。首次实际输出 Q1 地址与样本、Q2 价格与库存、Q3 负资产计算。

**给老师讲：**“task.md 是研究委托；我让模型先生成问题与完成条件，写入 plan.json。Q1 是研究问题，读完资料后才产生 Q1C1 等具体候选陈述。”

注意：课程叫“拆主张”，本实现先拆问题，原子陈述在第三步生成，职责跨了两段。提示要求单个陈述，但模型有时将地址、价格、面积等多项事实装进同一候选；当前代码不能保证严格原子化。

## 第二步：拟查询——让查询有目标

**代码位置：145–149 行；local_search 函数在 67–76 行。**

```python
for index, question in enumerate(questions, 1):
    journal.event("plan_query", question)
    ranked, matches = local_search(question["query"], sources)
```

`for` 每次取一个问题；`enumerate(..., 1)` 同时给出从 1 开始的轮次编号。`question["query"]` 从字典按键取查询文字。`ranked, matches = ...` 是把函数返回的两个结果分别放进两个变量。

query 和 source_type 是第一步模型一起给出的。本地搜索按词语重合度排序，ranked 是全部来源的排序，matches 是有关键词匹配的来源 ID。source_type 作为问题元数据记录并传给模型，**当前不作为 Python 的硬性来源过滤条件**。

输出：`trace.jsonl` 的 plan_query 与 search_frozen 事件，包含查询、匹配结果、empty 标记。原 query 也在 plan.json。

**给老师讲：**“这次使用冻结资料，不是联网搜索。查询决定来源的阅读顺序，但全部 15 条来源仍会给模型；没有匹配也会留下 empty=true。”

## 第三步：写回观察——先记录看见什么，再提候选

**代码位置：150–167 行；PROPOSE 指令在 104–109 行。**

```python
evidence = [{"source_id": "TASK", "text": task, ...}] + ranked
journal.event("tool", {"name": "read_frozen", ..., "observation": evidence})
proposal = model.ask("proposal_" + str(index), PROPOSE, {...})
candidates = proposal.get("candidates")
```

这是省略部分字段的阅读示意。`[] + ranked` 把两个列表拼在一起：TASK 提供任务里的计算假设，其他元素是来源正文。

输入是完整任务、本轮问题、全部冻结正文，以及前轮保存的 observations/gaps。模型给出 candidates 与 gaps；每个候选包含 statement、kind、bindings 和 calculation。bindings 记录 source_id 与逐字 quote；kind 区分 fact、calculation、inference。

第 165 行由 Python 分配 Q1C1、Q1C2 等候选编号，而不是采用模型自报编号。第 167 行把问题及缺口追加到内存里的 gaps 列表；通过第四步后才统一写 gaps.json。

输出：正文观察在 `trace.jsonl`；首轮提议原始返回在 `02-proposal_1-response.json`，请求在 `02-proposal_1-request.json`。模型的候选稍后也进入 claims.json。

**给老师讲：**“我记录读到的正文，再请模型形成有引用的候选。没有资料支持的地方写缺口，不把模型猜测当观察。”

这一版没有新网页抓取，所以它没有本次网页抓取失败；API 调用失败会由 deepseek_client.py 保存 error 文件和 api_error 事件，不自动重试。不能把旧 HyperResearch 抓取错误当成本次新增失败。

## 第四步：绑定并核验——链接存在还不够

**代码位置：166、168–188 行；literal_errors 在 79–96 行；CHECK 指令在 111–115 行。**

```python
candidate["literal_errors"] = literal_errors(candidate, evidence)
checked = model.ask("check_" + str(index), CHECK, {...})
if candidate["literal_errors"]:
    effective.update(status="missing", reason="; ".join(candidate["literal_errors"]))
journal.write("claims.json", ledger)
journal.write("gaps.json", gaps)
```

第一层 Python 查来源是否存在、quote 是否逐字出现在正文。`quote not in source["text"]` 是字符串包含关系检查，不会理解意思。
第二层模型在独立上下文中读候选与原文，检查数值、时间、地理范围、否定方向及算术，返回 supported / conflict / missing 和 reason。

如果 Python 找不到引用，最终 verdict 强制 missing，即使模型误说 supported 也不能放行。若只是语义上出错而引文存在，当前仍依赖模型检查，可能漏检。

ledger 是累计核验记录的列表；每项保存 candidate、模型原判 model_verdict、程序合并后的 verdict。每轮检查成功后更新 claims.json 和 gaps.json。

**给老师讲：**“程序能查引文是否存在，模型负责查它是否支持这句话。两层分开记录；有引用不等于意思正确，而且独立上下文仍是同一个模型，不是独立专家。”

真实失败例子：Q2C1 的模型理由承认“合理但略超原文”，却给 supported，程序没识别这个语义矛盾。见 [本次对照与失败说明](live-comparison-01.md)。

## 第五步：记账预算——它穿插在每轮，不是最后才算

**代码位置：153–154、168–169 行；费用检查在 deepseek_client.py 的 55–83 行。**

```python
spent += 1
journal.event("budget", {"operation": "proposal", "spent": spent, "remaining_budget": 6-spent})
```

`spent += 1` 等于 `spent = spent + 1`。提议前加一，检查前再加一；最多三个问题，所以最多六个操作单位。
这里按**一批提议/一批检查**计数，不是每一个候选算一单位；一轮可能有多个候选。若老师要求按单个候选记账，需要另行调整口径，不能把批次隐瞒。

API 调用另记：规划 1 次 + 3×（提议 1 次 + 检查 1 次）+ 报告 1 次 + 审查 1 次 = 本次 9 次。
客户端每次发送前检查金额预留和次数上限；响应后用 token 用量按保守费率估算。六个操作单位不等于六次 API，也不等于六元。

输出：trace.jsonl 的 budget/api_return 事件；run.json 最终写 spent、remaining_budget、api_calls、estimated_cost_cny。本次分别是 6、0、9、0.733804；费用是估计，不是实际账单。

**给老师讲：**“我有两本账：课堂操作次数和模型调用费用。每次提议、检查都记账，规划和写报告也要付费，不能漏掉。”

## 第六步：停止与交付——报告生成，不等于审查通过

**代码位置：189–224 行；run.json 的写入在 run_live.py 第 100 行。**

```python
selected = [row for row in ledger if row["verdict"]["status"] == "supported"]
report = model.ask("report", REPORT, {...})
journal.write_text("report.md", body)
audit = model.ask("report_audit", AUDIT, {...})
```

第一行是列表推导式，可读成“遍历 ledger，只收集 verdict 为 supported 的记录”。报告输入是这些记录、缺口、被拒绝的候选（只准作为限制）、来源目录与原任务，不是直接再喂全部来源正文。

第 216 行是关键门禁：

```python
passed = audit["passed"] and not audit["issues"] and not mechanical and all(r.get("status") == "covered" for r in coverage)
```

`and` 要求所有条件同时成立；`not audit["issues"]` 表示问题列表为空；`all(...)` 要求覆盖列表每项都 covered。
所以审查器嘴上说 passed=true 还不够：有 issues、有未知引用、或覆盖项缺失，都不能通过。审查器自己也可能误判，原结果必须保留。

输出：第 206 行 report.md；第 218 行 report-audit.json；第 224 行 return state，把状态交给外层 run_live.py；外层第 100 行才写 run.json。

**给老师讲：**“研究轮次跑完就停止并形成有边界的报告，审查状态单独记录。本次 stop_reason 是 planned_rounds_completed，但 status 是 blocked_review，说明流程结束了、交付没过。”

即使审查通过，本版 human_review 仍是 pending，deliverable 仍是 false；没有冒充学生或专家已经验收。

## 回头看准备工作：第 20–64 行

freeze 复制原任务字节，将 15 条来源正文写成 corpus.json，排除旧报告和 AI 摘要，manifest.json 保存哈希。
load_frozen 读三个文件、重新计算哈希，不一致就报错，再返回 task、sources、manifest。
哈希可以证明当前副本与保存指纹相符，不能证明所有来源真实，也不能证明旧研究每一步都读了相同资料。

## 本机产物在哪里

首次冻结输入目录：`.local-runs/frozen-20261101/`，包含 task.md、corpus.json、manifest.json。
首次真实输出目录：`.local-runs/deepseek-flash-01/`。课堂新跑时输出到命令里指定的 classroom 时间戳目录。

| 你想展示什么 | 打开哪个文件 |
|---|---|
| 原任务 | 冻结目录 task.md；与 evidence/task.md 字节一致 |
| 问题清单/完成条件/查询 | plan.json |
| 原始模型返回 | 对应编号的 response.json；模型 JSON 文本在 choices[0].message.content 内 |
| 原文观察/工具执行/预算流水 | trace.jsonl，每行一个 JSON 事件 |
| 候选和核验 | claims.json |
| 缺口 | gaps.json |
| 报告 | report.md |
| 审查为什么没过 | report-audit.json |
| 最终状态/用量/停止原因 | run.json |
| 模型、价格口径和源码指纹 | protocol.json |

## 母图与当前实现的差别

通用六步框架可以根据缺证重新拟查询并循环。当前程序先规划最多三轮，再逐轮读取、提议、检查；前轮 gaps 会传给后轮，但**不会自动修改已经规划的 query，不会联网补抓，不会失败后自动重试**。
六步是职责，不是执行顺序严格一段接一段：拆解分两阶段，预算穿插全程，落盘由记录器和外层入口协作完成。

## 课堂一分钟讲稿

“我先固定 task.md 和来源正文，哈希检查是否改变。DeepSeek 把任务拆成最多三组问题，生成查询和完成条件。我在冻结资料里排序、读取全部来源，记录原文观察，再让模型提出带引用的候选。Python 查引文是否存在，同模型的另一个上下文检查取值和范围是否支持。每轮提议和检查各算一个操作单位，API 费用另记。最后根据核验记录写报告并审查，停止原因和复核状态分开。本次有报告，但审查仍阻塞；检查器也存在错误放行，不能因为输出了 supported 就认定正确。”

## 自测：先回答这三问

1. task.md 和 plan.json 有什么区别？
2. 第 153 行 spent 加一、第 168 行又加一，分别付出了什么操作？
3. 为什么 audit 的 passed=true，程序最后仍会得到 blocked_review？

能指着真实代码和文件回答这三问，再继续逐行读字符串处理、列表推导式和异常处理。
