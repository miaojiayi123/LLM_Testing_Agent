# test_runner.py
import subprocess
import sys
import tempfile
from target import tester


def run_case_unit(input_md: str) -> dict:
    """
    单元层测试：直接函数调用
    返回字典：stdout, stderr, status
    """
    try:
        result = tester.run_test_case(input_md)
        return result
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "status": "error"}


def run_case_integration(input_md: str) -> dict:
    """
    集成层测试：通过子进程调用 `python -m markdown2`，模拟外部调用场景。
    """
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=True) as f:
            f.write(input_md)
            f.flush()
            proc = subprocess.run(
                [sys.executable, "-m", "markdown2", f.name],
                text=True,
                capture_output=True,
                timeout=8,
                check=False,
            )
        if proc.returncode == 0:
            return {"stdout": proc.stdout, "stderr": proc.stderr, "status": "finished"}
        return {"stdout": proc.stdout, "stderr": proc.stderr or f"exit code {proc.returncode}", "status": "error"}
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "integration run timeout", "status": "timeout"}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "status": "error"}


def run_case(input_md: str) -> dict:
    """
    组合测试：单元层 + 集成层
    """
    unit_result = run_case_unit(input_md)
    integration_result = run_case_integration(input_md)
    return {
        "unit": unit_result,
        "integration": integration_result,
    }
