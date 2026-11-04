# AI assistance disclosure

The learner provided the task, screenshots, existing local research artifacts, and the course submission requirements.
Claude previously executed the actual HyperResearch light run and its closeout/source tracing; this package does not claim that Codex independently repeated that research.
Codex wrote the new ReAct and six-step Python scaffold, tests, frozen teaching candidates, replay/export scripts, comparison documentation, and English README, and executed the offline tests.
The classroom observation sentence was supplied by the assignment; all generated candidates are explicitly handcrafted fixtures.
No formal evaluator labels are passed into the candidate generator or selector; the selector receives checker verdicts, which are not independent ground truth.
No live language model was evaluated in the historical offline experiments, and no performance improvement claim is made.
Original research report and run status were preserved, and original absolute local paths were redacted only in exported copies.
The earlier product-comparison label “作业三” was incorrect; that document belongs to assignment 2 section 2.3.
The learner must review and personally explain the six responsibilities and, if required by the instructor's handwritten rule, rewrite assignment 1 independently.
Passing automated tests verifies these examples and program invariants; it does not establish independent factual correctness, educational mastery, or instructor acceptance.
Follow-up work added a REIWA quotation-based subtask, success/conflict traces, and an actual pinned HyperResearch citecheck module ablation on a temporary fixture database. AI authored the test mutations and added the field-binding rule; these mutations are not attributed to the original report.

On 2026-11-01, at the learner's request, Codex added a separate DeepSeek live
runner, API client, hash-verified corpus freezing, complete redacted call logs,
usage accounting and transport/control tests. The old hardcoded candidates are
retained only as explicitly labeled historical tests; the live runner imports
none of them. The learner supplies a local API key; the authorized model is
DeepSeek V4.1 Flash with a CNY 5 client-side budget and one run, without retries.
Run status is recorded in the private run manifest, not inferred from this
disclosure. Model and checker use separate contexts of the same provider/model;
this is not independent expert review. This follow-up does not claim stability,
same-model causal framework superiority, or a formal RACE/FACT score.

The first live execution completed 9 generation calls and wrote a report, but
its final state is blocked_review. Codex read both reports, checked selected
claims against frozen source text, and documented checker/auditor limitations
in live-comparison-01.md. This was AI-assisted post-run review, not learner
human acceptance; neither report was silently corrected or regenerated.

2026-11-04: Official DeepSeek Harness generated an isolated repair draft and tests, but timed out and included incorrect logic. Codex reviewed, reimplemented the binding guard, and added regression/integration tests. Historical reports were preserved. Details: [binding-fix](binding-fix.md). This does not establish student authorship or live model-quality gains.

2026-11-04 (2 km scope revision): At the learner's explicit request, Codex archived
new public property/planning sources, created a separate task and frozen corpus,
computed distances from platform map pins, and recorded unresolved inventory gaps.
Codex implemented a fail-closed structured semantic-review contract and typed
Decimal calculations, with offline regression tests. No new paid model run was
started during preparation. Original tasks, reports and failures were preserved.
These changes do not establish model quality gains or a controlled experiment.

## 2026-11-04: V2 failed-run regression repair

Codex inspected the student's actual `furlong-2km-run-20261104-184811` artifacts and implemented safe legacy calculation normalization, explicit per-atom verification, additional evidence guards for property counts/area/spatial record identity, source-transformation metadata, and separate gap-disclosure coverage. It added twelve offline regression tests, including a mocked end-to-end run. The original task, snapshot, reports and logs were preserved; no paid run was executed by the assistant. Prompt changes guide evidence selection but cannot guarantee a correct report or audit pass. See [the repair record](furlong-review-fix.md) for exact limits and reproduction commands.

2026-11-04：针对真实运行 furlong-2km-fixed-20261104-190259 的25条主张超限异常，AI协助增加有界送检调度、未检候选持久化及5项离线回归测试。未执行付费模型运行。详见 atom-overflow-fix.md。

2026-11-04：用户授权更新GitHub。AI整理六次真实运行的公开审阅副本、逐次复盘和中文步骤注释。公开trace保留事件但省略来源全文，导出清单记录原件/副本哈希；密钥与完整API载荷留在本机。未调用付费模型，不宣称修复后实跑或稳定性验证完成。
