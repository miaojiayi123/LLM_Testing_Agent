# test_runner.py
from target import tester

def run_case(expression: str) -> dict:
    """
    执行单条测试用例
    调用 tester.py 的 run_expression
    返回字典：stdout, stderr, status
    """
    try:
        result = tester.run_expression(expression)
        return result
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "status": "error"}