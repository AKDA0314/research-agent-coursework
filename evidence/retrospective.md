# 运行复盘：cockburn-central-house-timing-3443a3（2026-10-30）

## 最终状态
- run 状态：`blocked`，`blocked_on: verify`，未手改 done。`run verify` 完整返回：`closeout/run-verify-full.json`（passed=false，退出码 1，唯一失败项 length-in-range）。
- 路线：light，1→2→10（单稿）→15→16 均已执行；`run finish` 运行 2 轮（第 1 轮 816 词，补充来源登记/敏感性表后第 2 轮 1111 词，下限 1600）。第三轮未做。

## 已完成步骤
1 分解（light/structured，无分歧）；2 宽度检索（6 次 WebSearch，3 个抓取代理共 19 个 URL，入库 15 条笔记，其中 1 条 deprecated、1 条为地理编码）；10 单稿；15 润色（10 处引号与措辞修正，1 条升级项 `[[search]]` 经核实为真实笔记）；16 可读性（9 条建议，采纳 5、跳过 4）。

## 失败原因
见 `closeout/length-check-issue.md` 与 `closeout/length-check-repro.txt`：检查按"平均 token 长度 ≥ 15"判断是否为无词边界文字，本报告平均 9.28，走了空格词数路径（1111 词 < 1600）。字符路径下 11457 字符会落在范围内，但这只是反事实，未据此改动。报告含大量 ASCII（笔记 ID、URL、表格），汉字仅 2840 个。更正：我此前说"约 7,700 个汉字"不准确，7,700 是当时的总字符数。

## 来源与数据缺口
- 缺口：无点位级坐标与 1 公里半径；无上一完整年度的 suburb house 中位价与样本量；无 suburb/附近 house 的两时点库存；未确认该地址是否在售；无 RBA/Cotality 一手数据；无新房供应/批准数据。
- 未取得：microburbs（bot_block，escalation #1 仍 queued）；OnTheHouse 11 Furlong 与 suburb 页面及批次 1 其余 URL（无失败原因记录）。
- 抓取代理批次 1、2 的回传只有 "placeholder"，靠直接核对 vault 确认；Perth 季度页面 claims JSON 因转义错误无法导入。
- 引文核验：light 档未跑 14.5；API Magazine、REIWA 年初预测、会长专栏、Network Exchange 依据抓取摘要使用。对抗性检索 2 次，未用学术 API。

## 笔记整理（CLAUDE.md 收尾）
- 15 条笔记原本均已有具体摘要，未改写摘要。
- 为 11 条笔记补加运行标签 `cockburn-central-house-timing`（此前只有 4 条带有）；为 3 条笔记补 tier/content_type（deprecated 旧文：practitioner/article；Nominatim：ground_truth/dataset；REIWA 9 月季度说明：institutional/article）。这些 tier 为我的判断，不是来源声明。命令记录：`closeout/curation-commands.log`。
- lint 前后：`closeout/lint-before.json`（2 error / 24 warning / 20 info）→ `closeout/lint-after.json`（2 / 23 / 20）。仅消除 1 条 uncurated 警告。
- 未修复：provenance、extract-coverage 两个 error（本次没有 Suggested-by 面包屑与 source-analysis 笔记，属流程缺失，补不了且不应伪造）；instruction-coverage 2 条警告（需改报告，已被禁止）；orphaned-notes 15 条与 singleton-tags 5 条（info，合并/加链接不明确无损，未动）；numeric-consistency 21 条（报告中的数字提示，未逐条处理）。

## 路径
- 报告：`research/notes/final_report_cockburn-central-house-timing-3443a3.md`
- run 目录：`research/runs/cockburn-central-house-timing-3443a3/`（run.json、query.md、scaffold.md、prompt-decomposition.json、temp/search-plan.md、temp/coverage-gaps.md、polish-log.json、readability-*.json、audit_findings.json、closeout/）
- 费用：run.json 的 spend 恒为 0，未实际记录，花费无法给出数字；预算 6 美元仅为登记，非硬上限。

## 尚未完成 / 明确未做
- 未做第二次研究、对照实验；正式 RACE/FACT 评测未运行、未提交。
- run 未通过交付门（保持 blocked）；未改源码、阈值、计费设置，未新增付费服务。
- 作业项待办：说明长度检查问题（本文件）、决定是否另行补写后重新 `run finish`、处理 microburbs 升级项。
