import importlib
import json
import tempfile

from target.markdown2_wrapper import convert_md_to_html, get_markdown2_info


def collect_coverage_metrics(test_cases: list) -> dict:
    """
    白盒覆盖率采集。优先使用 coverage.py 的分支覆盖能力。
    """
    info = get_markdown2_info()
    source_path = info.get("source_path", "")

    try:
        coverage = importlib.import_module("coverage")
    except Exception:
        return {
            "enabled": False,
            "reason": "coverage.py not installed",
            "line_rate": None,
            "branch_rate": None,
            "source_path": source_path,
        }

    cov = coverage.Coverage(branch=True, include=[source_path] if source_path else None)
    cov.start()
    for case in test_cases:
        input_md = case.get("input_md", "")
        try:
            convert_md_to_html(input_md)
        except Exception:
            pass
    cov.stop()
    cov.save()

    line_rate = None
    branch_rate = None
    files = list(cov.get_data().measured_files())
    if source_path and source_path in files:
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8", suffix=".json", delete=True) as f:
            cov.json_report(outfile=f.name)
            f.seek(0)
            data = json.load(f)
            file_data = data.get("files", {}).get(source_path, {})
            summary = file_data.get("summary", {})
            line_rate_pct = summary.get("percent_covered", None)
            branch_rate_pct = summary.get("percent_covered_branches", None)
            if branch_rate_pct is None:
                branch_rate_pct = summary.get("percent_branches_covered", None)
            if branch_rate_pct is None:
                covered_branches = summary.get("covered_branches", None)
                num_branches = summary.get("num_branches", None)
                if isinstance(covered_branches, (int, float)) and isinstance(num_branches, (int, float)) and num_branches > 0:
                    branch_rate_pct = (covered_branches / num_branches) * 100.0
            if line_rate_pct is not None:
                line_rate = float(line_rate_pct) / 100.0
            if branch_rate_pct is not None:
                branch_rate = float(branch_rate_pct) / 100.0

    return {
        "enabled": True,
        "reason": "",
        "line_rate": line_rate,
        "branch_rate": branch_rate,
        "source_path": source_path,
    }
