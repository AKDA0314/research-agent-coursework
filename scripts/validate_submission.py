"""Run tests, check portable Markdown links and scan submission-only text.

Heuristic secret scan is not a guarantee. Do not add raw logs without review.
"""
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    checked = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, capture_output=True, text=True)
    problems = []
    patterns = {"home_path": r"/Users/[^\s<>]+", "OAuth": r"(?:code_challenge=|oauth/authorize\?)", "private_key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY", "GitHub_token": r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})", "API_key": r"sk-[A-Za-z0-9_-]{20,}"}
    files = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts or path.name == "validation.json":
            continue
        if path.suffix not in {".py", ".md", ".json", ".jsonl", ".txt", ".log"} and path.name != ".gitignore":
            problems.append(str(path.relative_to(ROOT)) + ": unexpected file type")
            continue
        text = path.read_text(encoding="utf-8")
        if path.suffix != ".py":
            for name, pattern in patterns.items():
                if re.search(pattern, text):
                    problems.append(str(path.relative_to(ROOT)) + ": " + name)
        if path.suffix == ".md":
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if "://" in link or link.startswith(("#", "<", "mailto:")):
                    continue
                target = link.split("#")[0]
                if target and not (path.parent / target).exists():
                    # Exported historical documents contain source-local paths, not portable links.
                    problems.append(str(path.relative_to(ROOT)) + ": broken link " + target)
        files.append({"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest = json.loads((ROOT / "evidence/export-manifest.json").read_text())
    for row in manifest["files"]:
        if hashlib.sha256((ROOT / row["exported"]).read_bytes()).hexdigest() != row["exported_sha256"]:
            problems.append("Export hash mismatch: " + row["exported"])
    original_run = json.loads((ROOT / "evidence/run.json").read_text())
    if original_run["status"] != "blocked" or original_run["verify"]["passed"] is not False:
        problems.append("Original blocked status changed")
    function = ast.parse((ROOT / "src/react_loop.py").read_text()).body[1]
    body = (ROOT / "src/react_loop.py").read_text().splitlines()[function.body[0].lineno - 1:function.end_lineno]
    count = sum(bool(line.strip()) and not line.lstrip().startswith("#") for line in body)
    result = {"passed": checked.returncode == 0 and not problems, "test_exit_code": checked.returncode, "test_output": checked.stdout + checked.stderr, "react_function_body_lines": count, "problems": problems, "scan_scope": "Submission text, heuristic credential-pattern checks, relative Markdown targets, exported hashes, original blocked status. Not a formal security audit or teacher acceptance.", "files": files}
    (ROOT / "results/validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in {"files", "test_output"}}, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
