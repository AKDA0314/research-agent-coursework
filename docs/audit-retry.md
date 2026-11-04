# 审查输出截断：只重跑最后一步

学生亲自执行的 my-run-20261101-144909 在第九次调用失败：响应 finish_reason=length，completion_tokens=5000，审查 JSON 未完成。前八次调用结束，report.md 已保存。
这与 HyperResearch 最小报告长度门禁不同；也不是人民币 5 元预算用完。费用估计为 0.767612 元。

提高 max_tokens 可以给输出更多空间，但不能保证停止重复。新增 [retry_audit.py](../scripts/retry_audit.py) 只复用已经保存的第九次请求，不重新规划、提议、核验候选或写报告。

## 建议先只改变一个因素

保持 5000 输出 token，把审查提示改为 compact：去重，最多 12 条 issues，每条最多 100 字符，最多 20 项 coverage。
如果仍有问题列不完，必须标 issues_truncated / coverage_truncated，review_complete=false；程序不把截短意见当完整通过。
这只测试输出组织方式，不修复旧审查输入缺少运行日志等其他问题，不证明报告质量或运行稳定性。

在仓库根目录、同一个终端窗口执行：

```sh
audit_out=".local-runs/audit-retry-$(date +%Y%m%d-%H%M%S)"
python3 scripts/retry_audit.py --source-run .local-runs/my-run-20261101-144909 --out "$audit_out" --key-file .local-runs/deepseek.env --style compact --max-tokens 5000 --max-cny 0.5
```

只发一次生成请求，不自动重试。单次预算默认 0.5 元，并检查原运行加本次预留不超过 5 元；多次另行重跑的累计费用不由这个合计自动覆盖。
追加 `--dry-run` 可先检查设置，不读密钥、不发网络请求、不创建结果目录。

## 如果专门测试“只增加上限”

换新的输出目录，使用 `--style original --max-tokens 8000`，原提示保持不变。这与 compact 是两个备选实验，不需要两个都运行。
同时改 compact 和 max_tokens 会变成两个因素，不能把效果只归因于增加上限。

## 结果含义

- failed：API 输出仍截断、解析/字段不合法或预算等执行错误；查看对应 error 和 response 文件。
- blocked_review：本次审查完成了可解析返回，但存在 issues、missing、未审完或引用问题；不是需要反复重跑直到通过。
- audit_completed：程序按本次规则认为审查通过；human_review 仍 pending，deliverable 仍 false，不代表专家验收。

新目录保存 protocol.json、trace.jsonl、01-report_audit-request.json、01-report_audit-response.json、run.json，以及成功解析并验证后的 report-audit.json。API 错误另存 error.json；校验错误记录在 run.json 和 trace.jsonl。
原目录和原 run.json 永远不改；这是一条附属于原运行的重审记录，不会把历史 failed 改成 done。

输入校验会对照保存请求中的报告、任务哈希与当前报告；原始 JSON input 的序列化文字保持一致。protocol 记录来源请求、报告、审查数据的哈希和本次改动。
这次没有修改 six_step.py 的 224 行主流程，图和逐段讲解的行号仍对应；客户端仅增加可配置调用次数上限，原主流程默认仍最多 9 次。
