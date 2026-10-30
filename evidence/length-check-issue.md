# length-in-range 失败：记录（未修改源码、阈值或 done 状态）
日期：2026-10-30。源码：`<HYPERRESEARCH_SOURCE>/src/hyperresearch/core/runs.py`（hyperresearch 0.11.1，editable 安装）。

## 检查源码
- `_NO_WORD_BOUNDARY_AVG_TOKEN_CHARS = 15.0`（runs.py 约第 34 行）。
- `_lacks_word_boundaries(text)`：按 ASCII 空白切分，计算"平均每 token 字符数"，>= 15.0 才判定为无词边界（中日泰文），否则按空格词数计长度。**判断依据是平均 token 长度，不是检测汉字。**
- 判定为无词边界时：`len(text)` 与 `char_targets_no_word_boundary`（full 档 structured = 6000–15000 字符，±20%）比较；否则 `len(text.split())` 与 `word_targets`（structured = 2000–5000 词，±20%，即下限 1600）比较。

## 复现证据（`closeout/length-check-repro.txt`，对最终报告，用 python -I 运行）
- 字符数 11457；空白切分 token 数 1111；平均 token 长度 9.28；阈值 15.0；`lacks_word_boundaries = False`。
- 汉字数 2840，占比 24.8%。报告含大量 ASCII（`[[笔记 ID]]` 链接、URL、表格竖线、数字），且表格竖线与空格把文本切成较短 token，平均长度达不到 15。
- 因此走了词数路径：1111 词 < 1600，失败。`run finish` 第一次（补充前）为 816 词，同一原因。
- 若按字符路径：11457 在 6000×0.8 到 15000×1.2 之间，会通过。这只是反事实推演，未据此改动任何东西，也未手改状态。

## 结论
- 该检查对"中英混排 + 大量链接/URL/表格"的中文报告，会被 15 字符阈值误导到词数路径。这是检查器对混排文本的判定条件问题，同时我也确认报告在词数口径下确实短于 structured 档的下限。
- 我之前说"全文约 7,700 个汉字"不准确：7,700 是补充前的字符数（含 ASCII），汉字更少。以本文件数字为准。
- 处置：保持 blocked (verify)，不改源码/阈值/done。
