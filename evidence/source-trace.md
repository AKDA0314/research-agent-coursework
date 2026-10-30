# 来源追踪：11 Furlong Street 的 REIWA 成交记录

追踪对象：笔记 ID `11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025`。本文件只整理现有会话和文件里的记录，没有联网、没有重新运行任何命令、没有修改报告或运行状态。时间均为 2026-10-30，UTC。

## 1. 原始任务中的哪个问题需要它

- 任务单 `<LAB>/task.md` 第 13 行与第 14 行：先核实地址拼写、定位和所属 suburb，不预设该地址在售或房型已确认。
- 用户原话（`<LAB>/research/runs/cockburn-central-house-timing-3443a3/query.md`）："具体地址是11 furlong st, Cockburn Central 这一块附近。"
- 因此它服务于输出要求 1（范围说明）里的地址核实，也给事项 1（价格变化）提供目标地址的上一次成交。

## 2. 搜索如何发现这个 URL

- 工具：WebSearch，mode=standard，query 为 `Furlong Street Cockburn Central WA 6164`。
- 调用时间 2026-10-30T10:17:12Z，返回 10:17:22Z，tool_use_id=`toolu_01Ei5Qv6bWi8ukWdbuPDmygz`。
- 原始返回已提取到 `<LAB>/research/runs/cockburn-central-house-timing-3443a3/closeout/evidence-search-return.txt`。它是链接列表加一段搜索工具生成的概述，不是页面原文。
- 链接列表里与目标地址直接相关的两条：
  - `https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/`（标题 "Back to search results"）
  - `https://www.onthehouse.com.au/property/wa/cockburn-central-6164/11-furlong-st-cockburn-central-wa-6164-41710582`（标题 "11 Furlong Street, Cockburn Central, WA 6164 sold on 22 May 2025 | OnTheHouse"）
- 搜索概述还写了 "11 Furlong Street: ... One source records a sale on 22 May 2025 for $768,000, while Reiwa gives 13 May 2025"。这是搜索摘要，当时没有读过原页面，报告没有把它当作证据。
- 两条 URL 随后被我写入 `<LAB>/research/runs/cockburn-central-house-timing-3443a3/temp/url-queue.md` 的 B1 批次，交给抓取代理。

## 3. 抓取实际返回了什么

原始记录：`<LAB>/research/runs/cockburn-central-house-timing-3443a3/closeout/evidence-fetch-return.txt`，取自抓取代理 batch 1 的会话记录 `<USER_HOME>/.claude/projects/-Users-REDACTED-Documents-ChatGPT-----Agent-outputs-hyperresearch-lab/e9ff650e-afb9-4fbc-8438-b2af03277b38/subagents/agent-af90a84a0adf9b1f6.jsonl` 第 14 行（命令）与第 15 行（返回），tool_use_id=`toolu_011HK5ESn5d2fJv4vRg9YJsW`，10:18:15Z 发出，10:19:43Z 前返回。工具是 Bash 里的 `hyperresearch fetch <url> --tag cockburn-central -j`，底层 Crawl4AI 0.9.5。代理的命令对每个 URL 的输出用了 `head -c 600` 截断，所以下面的 JSON 都不完整，这是代理命令造成的。

- REIWA（`https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/`）：FETCH、SCRAPE、COMPLETE 均为 ✓，总耗时 4.48s，JSON 为 `"ok": true`、`"note_id": "11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025"`。
- OnTheHouse（`https://www.onthehouse.com.au/property/wa/cockburn-central-6164/11-furlong-st-cockburn-central-wa-6164-41710582`）：抓取过程 ✓，耗时 32.89s，但 JSON 为 `"ok": false`，错误信息开头是 `"Skipped junk content from https://www.onthehouse.com.au/property/wa/cockburn-central-6164/11-furlong-st-cockburn-central-wa-6164-4`（被截断，其后的原因文字在原始返回里缺失）。这条没有入库。
- 补充：同一次命令里 microburbs 报 `Blocked by anti-bot protection: Cloudflare JS challenge`，OnTheHouse suburb 页面报 `Empty or near-empty content`。这解决了我上一份复盘里"批次 1 其余未入库 URL 没有失败原因记录"的说法：原因其实在这份原始返回里。该复盘与报告我按要求没有改。
- 抓取代理最终回给我的消息只有 "placeholder"，所以上面这条工具返回才是真实证据。

## 4. 保存为哪个 note ID

- 笔记 ID：`11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025`
- 文件：`<LAB>/research/notes/11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025.md`
- frontmatter：source=`https://reiwa.com.au/11-furlong-street-cockburn-central-4900193/`，fetched_at=2026-10-30T10:18:57Z，fetch_provider=crawl4ai，body 在 `<untrusted-source>` 围栏内。笔记当前状态 draft，后来我补了运行标签 `cockburn-central-house-timing`（`<LAB>/research/runs/cockburn-central-house-timing-3443a3/closeout/curation-commands.log`）。
- 页面正文要点（笔记第 34 行、39 行、79 行）：Sold price $768,000，Sold 13 May 2025，Landsize 172m，由 Semple Property Group 的 Tanya Forzatti 出售。

## 5. 报告中哪一句引用了它

报告文件 `<LAB>/research/notes/final_report_cockburn-central-house-timing-3443a3.md`：

- 第 7 行（1. 范围说明）：REIWA 有 "11 Furlong Street, Cockburn Central WA 6164" 的成交记录（2025-05-13，$768,000），可证实该地址存在且属 Cockburn Central，邮编 6164；该记录描述为 4 卧 3 卫 2 车位、2021 年建成的双层 townhouse，位于 Mojo Urban Living，地块 172 ㎡，页面类型标为 House。
- 第 21 行（事项 1 证据表）："目标地址上次成交 | 11 Furlong St | $768,000，2025-05-13"，核验状态写"已读取"。
- 第 122 行（第 6 节来源登记）：列出该笔记 ID、URL 与"已读取原文，用于地址核实"。

## 6. 能支持什么、不能支持什么

能支持（均限于这一页的内容）：
- REIWA 上存在 11 Furlong Street, Cockburn Central WA 6164 的成交记录，地址拼写和 suburb、邮编对得上。
- 该记录写的成交价 $768,000、成交日 2025-05-13、4 卧 3 卫 2 车位、地块 172 ㎡、2021 年建、位于 Mojo Urban Living。
- 页面类型标签是 House，同时描述文字称它为 townhouse，所以"该区域 house 含小地块 townhouse"这一可比性提醒有来源依据。

不能支持：
- 该房产现在的价值或是否在售（这是 2025 年的成交记录，且在售页只读了第 1 页）。
- 门牌级坐标和 1 公里半径（页面没有给坐标，Nominatim 只到街道级，见笔记 `search`）。
- 区域价格趋势或 suburb 中位价：单次成交不能代表市场，也不能和 2026 年的成交直接拼成涨幅。
- 成交日期的最终核定：REIWA 写 13 May 2025，OnTheHouse 搜索结果标题写 22 May 2025，后者页面抓取失败，冲突没有解决，报告采用 REIWA 的读取原文。
- 成交价的准确性本身：这是单一来源的页面记录，没有与 Landgate 等一手登记交叉核对。
- 任务单里 AUD 1,000,000 购价的任何依据：那是教学假设，与此成交价无关。

## 证据文件清单
- `<LAB>/research/runs/cockburn-central-house-timing-3443a3/closeout/evidence-search-return.txt`：原始搜索返回
- `<LAB>/research/runs/cockburn-central-house-timing-3443a3/closeout/evidence-fetch-return.txt`：原始抓取命令与返回
- `<LAB>/research/notes/11-furlong-street-cockburn-central-wa-6164-sold-13-may-2025.md`：笔记
- `<LAB>/research/notes/final_report_cockburn-central-house-timing-3443a3.md`：报告
- `<LAB>/research/runs/cockburn-central-house-timing-3443a3/temp/url-queue.md`：URL 分批记录
- `<LAB>/task.md`、`<LAB>/research/runs/cockburn-central-house-timing-3443a3/query.md`：任务来源

closeout 目录里另有一份 `evidence-index.md`（不是我写的，本次没有读全、没有修改）。
