# result_analyzer.py

def basic_judge(case: dict, result: dict) -> str:
    """
    根据测试用例和执行结果判定 PASS/FAIL/CRASH
    """
    expected_type = case.get("expected_type", "normal")
    status = result.get("status", "")
    stdout = result.get("stdout", "")
    stderr = result.get("stderr", "")

    if status == "error":
        return "CRASH" if expected_type == "normal" else "PASS"
    if expected_type == "error":
        return "FAIL" if stdout else "PASS"
    return "PASS"