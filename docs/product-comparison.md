# 作业二 · 2.3 深度研究产品对照

编号更正：本文件是课程作业二的 2.3 小节，不是“六步调研框架”的作业三。实际作业三代码与轨迹另见同级 outputs 下的 lesson03-submission。

整理与访问日期：2026-10-30（Australia/Perth）。对应作业清单 2.3-01、2.3-02、2.3-03。

本节完成三家官方材料收集、四系统比较和 HyperResearch 优点／限度分析。它是机制与证据可见性的比较，不是四家同题实测，不提供速度、费用或准确率排名。整份课程作业尚未全部完成；第一次 HyperResearch 运行仍为 `blocked`。

## 比较口径

- 【源码可见】：本机 HyperResearch 源码可检查的机制；不表示某次运行实际执行了所有分支。
- 【公开材料】：厂商文档或产品页描述；不等于已验证内部实现或效果。
- 【自己实跑】：本次已有报告、运行清单、机器返回与日志支持的观察。
- 【无法核实】：所选材料不足以确认；不能改写成“该产品没有这个功能”。

HyperResearch 对象是本机 0.11.1，仓库 HEAD 为 `75b1ecfb2891184fad2cc1a2ddf9abe476f5b54c`。其余对象分别是 OpenAI 文档中的 Work 深度研究体验、Gemini Apps Deep Research，以及 Perplexity 当前产品页的 Deep Research in Computer。产品形态不同，不能将旧 API、旧产品和当前界面混作一套内部架构。

## 四系统比较矩阵

| 系统 | 循环／执行路线 | 状态与产物 | 何时停止或交付 | 核验与引用 | 证据档次与边界 |
|---|---|---|---|---|---|
| HyperResearch | 【源码可见】按 tier 选步骤；light 为 1→2→10 单稿→15→16；full 另含 critics、补抓及 14.5。[H1] | 【源码可见】磁盘 run.json、事件和分步产物；【自己实跑】五步 done，整体 blocked。[H2][R1] | 【源码可见】finish 调用 verify；失败写 blocked/verify；【自己实跑】本次长度项未通过。[H2][R2] | 【源码可见】结构检查与 lint 分开；light 不含 14.5。【自己实跑】引用密度通过不代表逐句真实性通过。[H1][R2] | 【源码可见＋自己实跑】机制和故障都有落点；【无法核实】本次结果不证明优于商业产品。 |
| OpenAI Deep Research | 【公开材料】给出问题、范围及上下文，跨来源调查后审阅报告并追问。[O1] | 【公开材料】报告、来源及后续对话；【无法核实】所选页面未说明内部状态结构。[O1] | 【无法核实】该页面未给出停止阈值或与 finish 对应的验收算法。[O1] | 【公开材料】用户可审阅报告及来源；【无法核实】是否存在与 14.5 等价的独立逐句核验及其覆盖率。[O1] | 【公开材料】本次未运行该商业产品，不用 API 文档替代产品实测。 |
| Gemini Deep Research | 【公开材料】先生成可编辑计划，再启动研究；产品介绍描述搜索／浏览／推理循环。[G1][G2] | 【公开材料】生成报告后通知；历史报告依赖 Keep Activity 开启，可导出 Docs。[G1] | 【公开材料】介绍页的初代架构说明称模型判断资料足够后综合；【无法核实】当前版本的精确停止阈值。[G2] | 【公开材料】初代架构说明涉及发现不一致和多轮自我批评；【无法核实】当前独立逐句核验实现与覆盖率。[G2] | 【公开材料】操作文档与历史架构说明分开；不是本次实测。 |
| Perplexity Deep Research | 【公开材料】当前 Computer 产品页描述计划、子任务和并行检索，采用 Search as Code。[P1] | 【公开材料】报告可继续转成演示文稿等产物；更新日志说明可保留上下文及资产进行分叉。[P1][P2] | 【无法核实】已读页面未公开停止阈值或机器验收规则。[P1][P2] | 【公开材料】厂商宣称引用每项主张并核对可信数据；【无法核实】不能据此认定引文覆盖率或正确率为 100%。[P1] | 【公开材料】仅描述当前 Computer 形态；不把厂商榜单声明当成自己的成绩。 |

表内编号对应下方证据索引。“无法核实”是本节的证据边界，不是产品缺陷判决。

## HyperResearch 的优点

### 优点一 过程可以落到具体文件

【源码可见】分步技能在执行时加载，tier 路线明确；研究过程不是只有一段最终回答。[H1]

【自己实跑】本次保留了 run.json、报告、verify JSON，并新增了一条“任务→搜索→URL→抓取→note ID→报告句子”的来源追踪。[R1][R2][R3] 这让检查者能够发现来源日期冲突或抓取失败，而不只依赖执行者总结。它体现可追踪性，不保证信息已经全部正确。

### 优点二 失败能够作为交付物保存

【源码可见】finish 将检查结果写入 manifest，并记录失败项。[H2]

【自己实跑】本次未因报告已经生成就宣布成功：`length-in-range=false`，整体状态保留为 `blocked`。[R1][R2] 这是可复核的失败案例，适合课程中讨论停止条件和验证边界。

## HyperResearch 的限度

### 限度一 混排文本的机械计数可能不适配

【源码可见】是否走字符计数分支，取决于空白分隔 token 的平均长度是否达到 15，而不是识别中文。[H3]

【自己实跑】本报告平均值 9.28，按 1111 个空白分隔 token 计数，低于带容差下限 1600，导致长度失败。[R2][R4] 这是本次实际触发的问题。改走字符分支可能满足长度条件，但不能推导正文充分、事实正确，故未修改源码或阈值来“过关”。

### 限度二 light 的检查范围有限

【源码可见】light 跳过完整 critics 和 14.5 引文句子绑定检查；这是路线设计，不能误报为 full 步骤执行失败。[H1]

【自己实跑】verify 的 9 项中有 8 项通过，但独立 lint 仍为 2 个 error、23 个 warning、20 个 info。[R2][R5] 数字警告是待核查提示，不是已证实的数字错误。结构验收通过也不等于研究内容无缺口。

### 限度三 状态与费用字段不是外部事实证明

【源码可见】`finish_run` 有验收逻辑，但底层 `set_status` 只验证合法状态并写入，不能把“只有 finish 能写 done”的注释当作不可绕过的安全保证。[H4] 这是源码边界，不是声称本次有人绕过。

【自己实跑】spend 字段全部为 0，尽管已有笔记和代理运行记录；实际额外费用仍未核实。[R1] `budget_usd=6.0` 不等于账户已设置硬扣费上限，更不能作为实际花费不超过 A$10 的证据。

## 官方材料与短摘录

以下短摘录仅支持相邻陈述。页面内容可能更新，访问日期统一为 2026-10-30。三家均未在本次作业中启动商业研究任务。

### O1 OpenAI

[Web search — ChatGPT Learn](https://learn.chatgpt.com/docs/web-search?surface=app&translationFallback=zh-Hant)，定位 “Research a topic in Work”。

> Review the report and its sources, then ask follow-up questions in the chat.

【公开材料】支持“多来源调查、报告及来源审阅、后续追问”，不足以证明内部独立核验器或停止算法。页面出现两种入口说明，本节不据此断言所有账户界面相同。

### G1 Google 操作说明

[Use Deep Research in Gemini Apps](https://support.google.com/gemini/answer/15719111?hl=en)，定位 “Start a Deep Research report”“Find your research reports”“Share, export, or copy”。

> To update the research plan before you create a report, click Edit plan.

【公开材料】支持计划编辑、通知、历史保存条件与导出功能；不能单凭操作说明证明内部事实核验质量。

### G2 Google 产品与架构介绍

[Gemini Deep Research](https://gemini.google/overview/deep-research/)，定位 “How we built the first Deep Research”“An agentic system”。

> Once the model determines enough information has been gathered, it synthesizes the findings into a comprehensive report.

【公开材料】可说明厂商披露过的资料充分性判断和研究循环；该段位于初代架构回顾，不把它认作当前所有模型的完整实现规范。

### P1 Perplexity 当前产品页

[Deep Research built for the hardest questions](https://www.perplexity.ai/en-GB/hub/products/deep-research)，定位 “Built on Perplexity's search technology” 及 FAQ。

> We let the model write code that assembles search itself

【公开材料】支持代码组织检索的产品描述；页面的引用质量和成绩属于厂商声明，不作为本次独立测量。

### P2 Perplexity 更新记录

[Deep Research, command panel, and enterprise controls](https://www.perplexity.ai/changelog/deep-research-command-panel-forking-inline-actions-and-enterprise-controls)，发布日期 2026-06-18，定位 “Deep Research in Computer”“Forking”。

> Forking lets you ask a follow-up question or explore a new iteration in a fresh thread

【公开材料】支持研究进入 Computer 后可延续工作以及分叉上下文的描述，不证明完整内部状态可导出。

本次检索中，该更新页的两个 hub 旧链接读取失败；后来打开了上方 P1 当前产品页。没有把读取失败页面写成已读证据，也没有据此断言产品不可用。

## 本地证据索引

| 编号 | 文件与定位 | 用途 |
|---|---|---|
| H1 | [入口技能与 tier 路由](https://github.com/jordan-gibbs/hyperresearch/blob/75b1ecfb2891184fad2cc1a2ddf9abe476f5b54c/src/hyperresearch/skills/hyperresearch.md#L30) | 分步加载、light/full 路线及 14.5 的范围 |
| H2 | [verify_run](https://github.com/jordan-gibbs/hyperresearch/blob/75b1ecfb2891184fad2cc1a2ddf9abe476f5b54c/src/hyperresearch/core/runs.py#L453) 与 [finish_run](https://github.com/jordan-gibbs/hyperresearch/blob/75b1ecfb2891184fad2cc1a2ddf9abe476f5b54c/src/hyperresearch/core/runs.py#L651) | 验收与最终状态转换 |
| H3 | [计数启发式](https://github.com/jordan-gibbs/hyperresearch/blob/75b1ecfb2891184fad2cc1a2ddf9abe476f5b54c/src/hyperresearch/core/runs.py#L34) | 平均 token 长度阈值 |
| H4 | [set_status](https://github.com/jordan-gibbs/hyperresearch/blob/75b1ecfb2891184fad2cc1a2ddf9abe476f5b54c/src/hyperresearch/core/runs.py#L268) | 底层状态写入边界 |
| R1 | [run.json](../evidence/run.json) | profile_steps、status、verify、spend |
| R2 | [run-verify-full.json](../evidence/run-verify-full.json) | 9 项检查与唯一失败项 |
| R3 | [source-trace.md](../evidence/source-trace.md) | 单条来源到报告的追踪；其引用的抓取返回存在截断 |
| R4 | [length-check-repro.txt](../evidence/length-check-repro.txt) | 平均 9.28、1111 token 等复现数据 |
| R5 | [lint-after.json](../evidence/lint-after.json) | 资料库独立检查结果 |
| R6 | [导出清单](../evidence/export-manifest.json) | 运行成果、失败、数据缺口及文件指纹 |

补充说明：R6 形成后，R3 和搜索／抓取证据文件已新增。因此不能继续说“所有原始返回都缺失”；也不能因找回了一个批次的截断输出，就说“完整日志全部找齐”。

## 交作业汇报稿

> 我已完成一次 HyperResearch light 真实运行，并整理了报告和失败证据。五个步骤记录完成，但整次运行没有通过最终检查，状态仍是 blocked。长度检查把含 URL、英文 ID 和表格的中文报告按空白切分计数，得到 1111，低于带容差下限 1600；资料库 lint 和研究数据覆盖也仍有问题。我保留了原始状态，没有修改阈值来过关。
>
> 作业二的 2.3 小节比较了 HyperResearch、OpenAI、Gemini 和 Perplexity。HyperResearch 有源码和本次运行记录，三家商业产品只有官方公开依据，没有做同题实测。因此我的结论不是哪家更强，而是它们的过程可见性和控制方式不同。HyperResearch 的优势是分步产物可追踪、失败可复核；限度是 light 的核验范围、混排文本规则及费用记录的可靠性。商业产品材料没有披露的内部机制，我标为无法核实，没有直接说它们不存在。
>
> 本次没有启动第二次研究、单因素对照或正式 RACE/FACT 评测；实际额外费用尚未核实。整份作业的隔离实验、对照实验及其他未验收项仍需按清单完成，不能将这份第三块交付当成全部结课。

## 本节验收

- 2.3-01：已提供三家官方链接、访问日期与短摘录。
- 2.3-02：已提供四系统 × 五个比较维度，并逐项标注证据类型。
- 2.3-03：已提供两条优点、三条限度及源码／运行依据。
- 未修改原研究报告、run.json、源码或计费设置；未自动改变看板勾选状态。



提交包更新：上面的汇报稿保留了较早阶段的状态。后来新增的离线检查器对照和隔离包装实验见 reproduction-report.md；它们不是第二次收费研究或正式基准评测。
