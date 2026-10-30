# 补充验收：真实源码核验 A/B 与同源任务轨迹

## 纠正之前过严的要求

课程要求选一处问题、只改一个设计因素、在相同任务材料预算下重跑，并没有明确说必须再启动一整次收费 HyperResearch 宿主研究。此前把“没完整再跑”直接说成必然未完成，过于绝对。

本次实际执行固定版本的 `extract_pairs`、`triage_pairs`、`sample_needs_llm`，不是把自己的 citation_only 函数改名成 HyperResearch。仍须说明它是模块实验，不是完整宿主或正式 FACT。

## 冻结任务与证据

固定小任务：根据已有 REIWA 原文核对 11 Furlong Street **历史成交价**，不得把它写成当前估值。它取自作业二原任务中的地址／历史成交核实，范围已明确缩小，不宣称等同整份买入调查。

[fixture](../fixtures/reiwa-binding.json) 绑定 [真实短原文及原笔记指纹](../evidence/source-excerpt.json)，没有新抓取。别名 `reiwa-record` 对应原 note ID，别名仅用于隔离测试，未修改原库。SQLite 是临时内存库，claims 行由这条原文构造，并非复制原 vault 的 claims 状态。

候选顺序固定为：当前估值 768,000；历史成交价 876,000；历史成交价 768,000。三条都是人工编制的测试候选，**不表示原报告写过前两条错误句子**。选择器固定为第一个通过候选；两边预算均 6 单位。

## 实际前后返回

| 候选 | 原机械 triage 实际返回 | 新增字段／取值绑定后的决策 |
|---|---|---|
| 当前估值 768,000 | supported-mechanical | conflict：字段不是历史成交价 |
| 历史成交价 876,000 | needs-llm | conflict：取值与片段不符 |
| 历史成交价 768,000 | supported-mechanical | supported |

唯一改变因素是检查决策增加字段／取值绑定。原文、临时数据库、任务、候选集合与顺序、选择器、预算均相同。原机械核验放行第一条，选择器选错；增加绑定后选择第三条。原 `needs-llm` 返回完整保留，没有真调用 LLM；在新框架原机械适配器中，它映射为缺少可交付支持，而不是已证伪。

还观察到：第一条虽带数字、属于 strong，但已经在机械层通过，因此不会进入 `sample_needs_llm`；不能把“strong 抽样”误说成所有带数字句子都必经 LLM。

[完整前后返回与源码指纹](../results/hyperresearch-binding-ablation.json) 包含真实 upstream 返回、selected、spent、remaining_budget 和复核边界。两边都未独立复核，`deliverable=false`；不能将选对直接写成独立审核通过。

## 作业三的同题成功／冲突

新增 [成功轨迹](../results/six-reiwa-success.json) 与 [冲突轨迹](../results/six-reiwa-conflict.json)。两者 task_id、任务条件、来源与预算一致，候选集合是两种测试情形：成功情形包含一个正确候选，冲突情形没有可通过候选。**这两个情形不是单因素 A/B**；单因素 A/B 是上面的固定候选集合实验。

| 七项比较 | 自己的六步框架 | HyperResearch 0.11.1 的对应落点 |
|---|---|---|
| 拆问题 | 【代码＋离线实跑】recorded_price、sold_price、完成条件 | 【原运行】原任务的地址／成交记录核实；新子任务不是新增的宿主分解 |
| 决定下一步 | 【代码】冻结候选队列、核验、预算 | 【源码】入口路由与步骤技能；【本次】测试 harness 固定候选，不让宿主重新生成 |
| 保存状态 | 【实跑】six-reiwa-success/conflict JSON | 【原运行】run.json；【本实验】单独保存 upstream 返回，不写原 run |
| 执行工具 | 【实跑】本地冻结字典读取 | 【实跑】真实 extract_pairs/triage_pairs/sample_needs_llm；无联网 |
| 核验引用 | 【实跑】quote、field、claim_key、value 一致 | 【实跑】原机械数字匹配能放行错字段；未启动 LLM 尾部核验 |
| 停止 | 【实跑】三对操作；completed 或 conflict，复核另列 | 【本实验】相同六单位由 harness 记账；不能说原 HyperResearch 使用六单位预算 |
| 取值／字段错在哪拦 | 【实跑】新增 binding 判 conflict | 【实跑】原机械层放行相同数字的错字段；不推断完整 LLM 阶段必然失败 |

## 复跑

普通离线轨迹及测试：

```sh
python3 scripts/run_offline.py
python3 -m unittest discover -s tests -v
python3 scripts/validate_submission.py
```

真实源码 A/B（另需本机固定快照路径；脚本校验 commit，不安装或修改依赖）：

```sh
python3 scripts/run_source_experiment.py /path/to/hyperresearch
```

改进只证明本组结构化字段规则能拒绝该测试反例，不证明通用语义理解、更高模型能力、真实房产当前价值或全流水线安全。完整房产题仍缺证，原 run 仍 blocked，正式 RACE/FACT 未运行。
