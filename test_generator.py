# test_generator.py
import json
from llm_agent import ask_llm

def generate_test_cases(code_analysis: str, num_cases: int = 30) -> list:
    """
    使用 LLM 根据代码分析生成测试用例
    返回 JSON 列表，每个测试用例包含：
    - expression: 输入表达式
    - expected_type: normal/error
    - purpose: 测试目的
    """
    prompt = f"""
请为下面的 Python 被测程序生成 {num_cases} 个测试用例，仅输出 JSON 数组。
每个用例包含：
- expression: 输入表达式
- expected_type: normal/error
- purpose: 测试目的
覆盖：
- 基本运算、括号、小数、负数
- 错误输入
- 随机复杂表达式

代码分析:
{code_analysis}
"""
    try:
        response = ask_llm(prompt)
        cases = json.loads(response)
        return cases
    except Exception as e:
        print(f"生成测试用例失败: {e}")
        return []