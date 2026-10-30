# 一页数据流：第一次真实 light 运行

| 顺序 | 实际入口／返回／产物 | 后续使用与停止边界 |
|---|---|---|
| 入口 | [冻结任务](../evidence/task.md)：Cockburn Central house 三事项 | 截止日、地理范围、房型与财务假设固定 |
| 拆解 | [prompt-decomposition.json](../evidence/prompt-decomposition.json) | 选择 light；不是完整 16 步 |
| 返回 1：搜索 | WebSearch：`Furlong Street Cockburn Central WA 6164`；[原返回](../evidence/evidence-search-return.txt) | 找到 REIWA URL；搜索工具概述不等于原网页 |
| 返回 2：抓取 | `hyperresearch fetch`；REIWA 4.48 秒，`ok:true`；[原返回](../evidence/evidence-fetch-return.txt) | URL 输出被 head 截断到 600 字符，不补造其余 JSON |
| 来源 ID | `11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025` | [短原文及指纹](../evidence/source-excerpt.json) 记录历史成交价；不支持现在估值 |
| 进入报告 | [report.md](../evidence/report.md)：范围说明、事项 1 表、来源登记（原第 7／21／122 行） | ID 贯穿；日期分歧与范围缺口保留 |
| 润色／可读性 | [polish-log.json](../evidence/polish-log.json)、原 run 五步 done | 不是正式引用全检或基准分数 |
| 交付门 | [verify](../evidence/run-verify-full.json)：8/9 通过 | length-in-range 失败：1111 < 1600 |
| 停止 | [run.json](../evidence/run.json)：blocked_on=verify | 未手改 done；不足资料不补成肯定结论 |

旁支失败：Microburbs 的 Cloudflare 挑战、OnTheHouse 的 junk/empty content 都在返回 2 中，不能把抓取进度完成当成有效正文成功。

简图（文本表示）：任务 → 拆解 → 搜索返回 → URL → 抓取返回 → note ID → 报告 → verify → **blocked**。

本页是历史运行数据流，不是重新执行或教师成功轨迹。
