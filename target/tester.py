# target/tester.py

from .markdown2_wrapper import convert_md_to_html

def run_test_case(input_md: str) -> dict:
    """
    执行一个 Markdown 转 HTML 的测试。
    返回:
      - stdout: 成功时的 HTML 输出
      - stderr: 错误信息
      - status: 'finished' 或 'error'
    """
    try:
        html = convert_md_to_html(input_md)
        return {"stdout": html, "stderr": "", "status": "finished"}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "status": "error"}