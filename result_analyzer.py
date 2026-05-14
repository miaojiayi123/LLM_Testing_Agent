# result_analyzer.py

def basic_judge(case: dict, result: dict) -> str:
    """
    根据测试用例和执行结果判定 PASS/FAIL/CRASH
    """
    expected_type = case.get("expected_type", "normal")
    must_contain = case.get("must_contain", [])
    status = result.get("status", "")
    stdout = result.get("stdout", "")
    stderr = result.get("stderr", "")

    if status == "error":
        return "CRASH" if expected_type == "normal" else "PASS"

    if expected_type == "error":
        return "PASS" if stderr else "FAIL"

    for token in must_contain:
        if token not in stdout:
            return "FAIL"
    return "PASS"


def judge_multilevel(case: dict, combined_result: dict) -> dict:
    """
    多层测试判定：分别判断单元层/集成层，再给出总判定与一致性结论。
    """
    unit_result = combined_result.get("unit", {})
    integration_result = combined_result.get("integration", {})

    unit_judge = basic_judge(case, unit_result)
    integration_judge = basic_judge(case, integration_result)

    unit_stdout = unit_result.get("stdout", "")
    integration_stdout = integration_result.get("stdout", "")
    outputs_consistent = unit_stdout == integration_stdout

    overall = "PASS" if unit_judge == "PASS" and integration_judge == "PASS" else "FAIL"
    if unit_judge == "CRASH" or integration_judge == "CRASH":
        overall = "CRASH"
    elif overall == "PASS" and not outputs_consistent:
        overall = "FAIL"

    return {
        "overall": overall,
        "unit": unit_judge,
        "integration": integration_judge,
        "outputs_consistent": outputs_consistent,
    }
