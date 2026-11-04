"""Produce a provenance comparison after one live run, not a quality score."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def compare(folder):
    folder = Path(folder)
    current, protocol = read_json(folder / "run.json"), read_json(folder / "protocol.json")
    old = read_json(ROOT / "evidence/run.json")
    baseline = (folder / "baseline-report.md").read_bytes()
    if hashlib.sha256(baseline).hexdigest() != protocol["baseline_report_sha256"]:
        raise ValueError("Baseline was changed after the run")
    if hashlib.sha256((ROOT / "evidence/task.md").read_bytes()).hexdigest() != current["task_sha256"]:
        raise ValueError("Task identity mismatch")
    report = (folder / "report.md").read_text(encoding="utf-8") if (folder / "report.md").exists() else ""
    historical = baseline.decode("utf-8")
    events = [json.loads(line) for line in (folder / "trace.jsonl").read_text(encoding="utf-8").splitlines()]
    returned = [e["data"] for e in events if e["event"] == "api_return"]
    counts = current.get("claim_counts", {})
    def size(text):
        return {"characters": len(text), "han_characters": len(re.findall(r"[\u4e00-\u9fff]", text)),
                "unique_citation_markers": len(set(re.findall(r"\[\[([^\]]+)\]\]", text)))}
    metrics = {"comparison_kind": "single observational comparison; not a controlled framework-quality experiment",
               "same_task_sha256": current["task_sha256"], "frozen_corpus_sha256": current["corpus_sha256"],
               "historical_status": old["status"], "live_status": current["status"],
               "live_api_calls": current["api_calls"], "returned_models": sorted({r.get("returned_model", "unknown") for r in returned}),
               "live_conservative_cost_cny": current["estimated_cost_cny"], "live_claim_counts": counts,
               "historical_report_size": size(historical), "live_report_size": size(report),
               "size_warning": "Different citation conventions and appendices; counts are NOT quality scores.",
               "formal_race_fact": "not_run", "repeat_stability": "not_tested", "human_quality_review": "pending"}
    (folder / "comparison-metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = [
        ("任务身份", "原提交 evidence/task.md", "逐字节哈希相同：" + current["task_sha256"], "文件哈希"),
        ("问题拆解", "历史分解产物", "DeepSeek 生成 plan.json", "真实运行文件；充分性需审查"),
        ("工具与资料", "历史联网搜索/抓取，部分输出截断", "本地检索并读取 15 条冻结正文；无补抓", "历史返回＋本次 trace.jsonl"),
        ("状态与预算", "run.json；spend=0 不能推断免费", "run.json；API 次数 " + str(current["api_calls"]) + "；费用估计 CNY " + str(current["estimated_cost_cny"]), "运行清单＋API usage，非账单"),
        ("引用核验", "light 未执行 14.5；交付门不等于语义正确", "逐字引用检查＋独立上下文同模型核验；" + str(counts), "历史路线＋claims.json；标签非真值"),
        ("停止", str(old["status"]) + "；verify 长度失败", current["status"] + "；" + current["stop_reason"], "两份 run.json；停止口径不同"),
        ("取值写反", "没有对真实完整报告执行同一变体的端到端试验", "语义检查器负责判断；测试覆盖拒绝流程，不保证模型必定识别", "代码/测试；不得夸大为本次实证"),
        ("报告质量", "旧报告作为基线保存，未输入新模型", "须检查任务覆盖、事实支持、缺口和推断边界", "人工/AI 阅读复核另列，不能用字数代替"),
        ("稳定性与基准", "单次历史运行", "一次 DeepSeek 运行；不重试；RACE/FACT 未做", "实验协议"),
    ]
    text = "# 单次真实运行对照\n\n本表由运行清单生成；它记录行为和证据，不给报告质量打分。\n\n"
    text += "| 对照点 | 历史 HyperResearch light | 新六步 DeepSeek | 证据档次 |\n|---|---|---|---|\n"
    text += "\n".join("| " + " | ".join(row) + " |" for row in rows)
    text += "\n\n模型、历史检索过程和预算不同；不能归因于框架本身。完整原始任务保留历史执行约束，本次协议明确记录变更，不冒充单因素对照。\n"
    (folder / "comparison.md").write_text(text, encoding="utf-8")
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_folder", type=Path)
    print(json.dumps(compare(parser.parse_args().run_folder), ensure_ascii=False, indent=2))
