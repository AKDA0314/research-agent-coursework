# 真实运行的公开审阅副本

六次记录及逐次解释见 [实践复盘](../../docs/practice-history.md)。原始状态均保留，没有将失败或审查拒绝改成 done。

每个运行目录包含当时实际生成的报告、审查、主张与日志；不存在的步骤不补造文件。最新190259运行止于 proposal_1，因此没有 report.md 或 report-audit.json。

trace.jsonl保留所有事件及顺序，但read_frozen来源全文替换为长度与SHA-256。完整API请求/响应与原始来源仍在本机，清单记录其哈希；公开日志不是逐字完整请求回放。局部原文绑定及回归案例用于解释核验失败，来源权利归原作者。

导出工具为 scripts/export_public_runs.py，使用固定运行与文件白名单，不读取密钥，不修改原件。运行它需要已有的本机历史目录。完整性记录见 [export-manifest.json](export-manifest.json)。
