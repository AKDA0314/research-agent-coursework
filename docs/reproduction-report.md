# 作业二：HyperResearch 复现、边界与失败证据

## 结论先行

真实运行：`cockburn-central-house-timing-3443a3`。Light 的 1、2、10、15、16 记录为 done；整次 run 仍是 `blocked`，`blocked_on=verify`。这不是“安装失败”，也不是“研究已经完全成功”。[运行清单](../evidence/run.json)

## 命令与证据等级

用户提供的终端截图显示以下命令已执行；这里是脱敏转录，不是重新执行的安装输出，也不是完整 shell 录屏：

```sh
source .venv/bin/activate
python --version
python -m pip install -e "<HYPERRESEARCH_SOURCE>"
hyperresearch profile list
hyperresearch install . --profile full --json
```

截图中 Python 为 3.12.14，安装版本为 hyperresearch 0.11.1，安装返回 `ok:true`。启动 Claude 曾出现非阻塞的 `Executable not found in $PATH: "node"`；后来终端 `node --version` 返回 v24.22.2。不能仅据后一条命令证明所有 hook 环境问题都已修复。完整安装日志未纳入本包；不要将转录当作逐字原始机器日志。

本包保存的实际机器输出：[搜索返回](../evidence/evidence-search-return.txt)、[抓取返回](../evidence/evidence-fetch-return.txt)、[verify JSON](../evidence/run-verify-full.json)、[lint](../evidence/lint-after.json)、[事件记录](../evidence/events.jsonl)。路径已脱敏，摘要及命令输出可能不完整，原始文件指纹见 [导出清单](../evidence/export-manifest.json)。

安装 gear=full 与研究 tier=light 并不冲突：tier 决定跑哪些步骤，gear 调整来源数量等规模数字，不代表模型能力。技能渲染的数量抽查另见 [源码抽查](../results/source-audit.json)。

## 三个容易混淆的机制

### 1. run.json 是运行账本，不是研究答案

| 字段 | 人话 | 本次观察 |
|---|---|---|
| steps | 每道工序有没有被记为完成 | 五个 light 步骤 done；不能自动推出每步内容正确 |
| chapters | 分章调研的章节账本 | 本次为空对象，不是缺了五个 light 步骤 |
| spend | 工具写进来的费用／计数 | 四项都是 0；已有真实抓取，因此不能据此说免费或没执行 |
| blocked_on | 卡在哪个关口 | verify |
| verify | 最近记录的交付检查 | passed=false，length-in-range 失败 |

### 2. 交付门是出库检查，不是事实裁判

`verify_run` 检查产物；CLI `run finish` 调用 `finish_run`，它先检查再写 done 或 blocked。底层 `set_status` 接受合法状态写入，并非不可绕过的安全边界。我们没有绕过，也没有手改状态。

| verify 项 | 结果 | 能检查什么；不能证明什么 |
|---|---|---|
| report-exists | 通过 | 文件存在；不证明正确 |
| levers-rendered | 通过 | shim 文件在；不证明宿主逐字遵循 |
| length-in-range | **失败** | 1111 个空白分隔词低于 1600 容差下限；不等于直接测量研究深度 |
| required-headings | 通过 | 要求的标题在；不证明内容覆盖足够 |
| citation-density | 通过 | 引用密度 22.50/1000 词；不证明引用支持句子 |
| no-scaffold-leak | 通过 | 未触发脚手架泄露规则；不证明没有其他错误 |
| quote-integrity | 通过 | 未触发该机械规则；不等于外网逐句核验 |
| retracted-citations | 通过 | 未触发本地撤回引用规则；不证明全球无撤稿 |
| artifact:polish-log.json | 通过 | 润色日志存在；不证明已正式评测 |

长度分支按平均空白 token 长度是否达到 15 选择字符计数，并不是汉字检测。本次平均约 9.28，所以按 1111 词计；总字符 11,457 中汉字 2,840。“约 7,700 汉字”的旧说法已撤回。不会靠凑字或改阈值伪装过关。[复现](../evidence/length-check-repro.txt)

独立 lint 仍有 2 error、23 warning、20 info。错误是来源推荐关系及来源分析覆盖缺失；警告包括指令覆盖、数字提示。提示不等于已证实事实错误。[原始 lint](../evidence/lint-after.json)

### 3. citecheck 是句子和来源的检查器，但有覆盖边界

`core/citecheck.py` 分三层：解析报告中的句子—引用对；机械 triage 用数字、文本片段等筛查；再对需要 LLM 的部分抽样。机械匹配不是语义蕴含证明，相同数字也可能指不同年份或不同指标。抽样也不是全覆盖。

本次 light 没执行 14.5；只能说模块源码可见，不能说本报告已经通过它。LLM 复核也不是 RACE/FACT。相关源码固定于 [0.11.1 commit](https://github.com/jordan-gibbs/hyperresearch/tree/75b1ecfb2891184fad2cc1a2ddf9abe476f5b54c/src/hyperresearch)。

## 已有资料的失败和更正

- 1 公里点位未核验；附近样本距离、可比年度价格、历史库存仍缺资料。
- Microburbs 返回 Cloudflare JS challenge。
- OnTheHouse 单套页面返回 `Skipped junk content`，错误被截断；suburb 页面明确 `Empty or near-empty content`。
- REIWA 抓取成功，但命令 `head -c 600` 截断了每条 JSON；抓取进度的绿色对勾不等于最终 `ok:true`。
- 搜索摘要提及 OnTheHouse 22 May，与 REIWA 13 May 不同；该页抓取失败，冲突尚未解决。
- `source-trace.md` 的包装描述需区分：网页原文存在磁盘中；`untrusted-source` 包装由读取／输出路径施加，不能声称所有原始笔记文件本身都存着这层围栏。

历史复盘不覆盖重写，更正集中在本说明中。原报告、状态、源码、计费设置均未修改。

## 新增的离线实验

### 隔离包装

直接调用固定快照的 `core/untrusted.py`。相同 URL、相同正文，只把 note 类型从 `note` 改为 `interim`。前者包装，后者不包装；伪造的结束围栏在前者中被改名。[真实执行结果](../results/isolation.json)

这验证源代码函数分支，不是 `note show` 的端到端试验，也不是证明 Agent 能抵御所有提示注入。内部类型被视为可信，类型标记的可信度本身仍重要。

### 单因素 A/B

同一份房产任务、同一冻结材料、同一候选及顺序、同一个选择器、同一 6 操作单位预算；只把“引用 ID 存在”换成“绑定字段并核对取值”。负资产候选故意把贷款阈值写成 768,000，正确假设是 800,000。弱检查器选中它；绑定检查器标 conflict。价格、库存缺证两边都不填补。[前后返回](../results/property-ablation.json)

这是新六步框架对原任务的**离线检查器重放**，不是修改 HyperResearch 后重跑整条 Agent 流水线。老师若要求同一 HyperResearch 宿主的端到端单因素重跑，这一项还需补做；本包不将局部实验冒充它。

另以课程 checkpoint 冻结句子验证“正确候选已经在集合里，仍选错”：候选相同、选择器相同、预算相同，只改变检查器。[结果](../results/checker-ablation.json) 在 `before.trace` 第一条 `bind_verify` 中，错误值被判 supported，`before.selected.resume_origin.value` 因而取错；问题首先在检查器，不是这次候选集没有生成正确答案。该归因只限于此可控轨迹。
