# 作业三：六步不是六次点击

代码在 [six_step.py](../src/six_step.py)。六步是职责；一次提议、一轮检查各花一个操作单位，最多六单位，即三对。查询和离线阅读属于提议里的子动作，不额外冒充美元预算。

| 职责 | 输入 | 输出及代码位置 |
|---|---|---|
| 1 拆主张 | 冻结问题和明确任务范围 | task.claims 的 claim_key、completion_condition；decompose 事件 |
| 2 拟查询 | 各主张的缺口 | query、source_type；plan_query 事件 |
| 3 写回观察 | 冻结来源 ID 或不存在的来源 | 原文 observation、pointer；空结果写 EMPTY_RESULT；propose_observe 事件 |
| 4 绑定核验 | claim、candidate、source、quote、value | verify_candidate 输出 supported / conflict / missing |
| 5 记账 | 每次提议和检查 | spent、remaining_budget；不足一对预算则不开始新提议 |
| 6 停止交付 | 已核验候选、未执行候选、余额 | stop_reason 与 review_status 分列；choose_candidate / stop_policy |

分解和查询由人工／AI 预先写入冻结 task，不是动态语言模型。下一步以来源是否存在、检查结果和预算为依据；它是小型确定性框架，不是通用自主研究系统。

## 两组证据，不能混成一次成功

1. 课程 checkpoint 冻结小题：[同一 fixture](../fixtures/checkpoint.json)，[成功](../results/six-success.json) 为 conflict→missing→supported，六单位；[冲突](../results/six-conflict.json) 为一对操作后 conflict。候选是手工编制的，不叫模型输出。检查器只认识明确声明的规则。
2. 原房产任务：[原任务](../evidence/task.md)，[冻结输入](../fixtures/property.json)，[同题轨迹](../results/six-property.json)。价格、库存 missing，情景算术 supported；六单位后 missing_evidence，不交付完整买入判断。地址定位与其他范围条件未核验，不隐含为通过。

原房产题的“成功完整研究”仍不存在；我们没有为满足成功轨迹要求伪造缺失来源。成功示例来自课程小题。若老师要求成功和冲突都必须来自完整原房产题，需要进一步补证并真实运行。

`review_status=rule_checked` 仅指本程序窄规则已核对，不指独立人工或 LLM 二审。`review_scope` 在结果里明确写出这一点；正式独立复核未做。

## Same-task comparison

同一原始 Cockburn Central 任务：新框架离线重放 vs 自己已有的 HyperResearch light。标签为【代码可见】【自己实跑】【公开流程】【未执行／无法核实】。

| 对照点 | 自己的六步框架 | HyperResearch 0.11.1 |
|---|---|---|
| 问题如何拆开 | 【代码可见＋离线实跑】property fixture 3 个主张；地址范围仍是未通过的总体前提 | 【自己实跑】prompt-decomposition.json；内容是否充分需另外审查 |
| 下一步由谁决定 | 【代码可见】固定查询／候选队列，检查器输出及预算决定可选答案和停止 | 【源码可见】入口 tier 路由、步骤技能由宿主执行；不是我们新框架调用宿主 |
| 状态写在哪 | 【自己实跑】results/six-property.json 的 trace、selected、spent、stop_reason | 【自己实跑】run.json、events.jsonl、磁盘报告及分步文件 |
| 谁执行工具 | 【自己实跑】Python 离线字典读取和计算，无联网搜索 | 【自己实跑】Claude 宿主、抓取代理经 Bash 执行 hyperresearch fetch；已留两条真实返回 |
| 引用如何核验 | 【代码可见】quote 必须在来源中，rule 解析值，核对 claim_key/value；规则不覆盖则 missing | 【源码可见】citecheck 解析、triage、抽样 LLM；【本环境未执行】light 未跑 14.5 |
| 何时停止 | 【自己实跑】六操作单位；价格／库存缺证，stop_reason=missing_evidence | 【自己实跑】五步 done 后 verify 长度失败，整体 blocked；spend=0 不能证明费用上限 |
| 同一取值写反在哪层拦 | 【离线实跑】property-ablation 的 negative_equity 错阈值由绑定检查判 conflict | 【无法核实】未将同一变体注入真实 HyperResearch；不可声称本次交付门或未运行的 citecheck 必拦 |
| 复核与停止是否分开 | 【代码可见】stop_reason、review_status、review_scope、deliverable 分列 | 【自己实跑】run 状态与 verify 分开；【未执行】正式 RACE/FACT |

## 学生需要亲自解释

为什么有引用仍可能错？为什么空结果也算一次观察？为什么 V=800,000 是零权益而不是负权益？为什么 done 或 completed 不等于独立复核通过？为什么六单位不是六美元？这五问尚不能由 AI 代替学生作答。
