# test_generator.py
import json
import re
from llm_agent import ask_llm


def _fallback_test_cases() -> list:
    return [
        {"input_md": "# Hello", "expected_type": "normal", "must_contain": ["<h1>Hello</h1>"], "purpose": "一级标题转换"},
        {"input_md": "## Subtitle", "expected_type": "normal", "must_contain": ["<h2>Subtitle</h2>"], "purpose": "二级标题转换"},
        {"input_md": "- a\n- b", "expected_type": "normal", "must_contain": ["<ul>", "<li>a</li>", "<li>b</li>"], "purpose": "无序列表"},
        {"input_md": "1. a\n2. b", "expected_type": "normal", "must_contain": ["<ol>", "<li>a</li>", "<li>b</li>"], "purpose": "有序列表"},
        {"input_md": "**bold** and *italic*", "expected_type": "normal", "must_contain": ["<strong>bold</strong>", "<em>italic</em>"], "purpose": "行内样式"},
        {"input_md": "[OpenAI](https://openai.com)", "expected_type": "normal", "must_contain": ["<a href=\"https://openai.com\">OpenAI</a>"], "purpose": "链接转换"},
        {"input_md": "```python\nprint('x')\n```", "expected_type": "normal", "must_contain": ["<code", "print"], "purpose": "围栏代码块"},
        {"input_md": "", "expected_type": "normal", "must_contain": [""], "purpose": "空字符串输入"},
        {"input_md": "plain text", "expected_type": "normal", "must_contain": ["<p>plain text</p>"], "purpose": "普通段落"},
        {"input_md": "### 中文标题", "expected_type": "normal", "must_contain": ["<h3>中文标题</h3>"], "purpose": "中文内容兼容"},
    ]


def generate_test_cases(code_analysis: str, num_cases: int = 30) -> list:
    """
    使用 LLM 根据代码分析生成测试用例。
    返回 JSON 列表，每个测试用例包含：
    - input_md: Markdown 输入
    - expected_type: normal/error
    - must_contain: 输出 HTML 必须包含的片段列表
    - purpose: 测试目的
    """
    prompt = f"""
请为下面的 Python 被测程序生成 {num_cases} 个测试用例，仅输出 JSON 数组，不要附加解释文本。
每个用例包含：
- input_md: Markdown 输入文本
- expected_type: normal/error
- must_contain: 字符串数组，表示输出 HTML 必须包含的片段。若 expected_type=error 可置为空数组
- purpose: 测试目的
覆盖：
- 标题、列表、链接、加粗/斜体、代码块
- 空输入与特殊字符
- 多语言文本

代码分析:
{code_analysis}
"""
    def _parse_cases(raw: str):
        text = raw.strip()
        # 去掉 ```json ... ``` 包裹
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)

        # 1) 先尝试整段直接解析
        try:
            return json.loads(text)
        except Exception:
            pass

        # 2) 从文本中提取第一个 JSON 数组片段
        start = text.find("[")
        end = text.rfind("]")
        if start != -1 and end != -1 and end > start:
            candidate = text[start : end + 1]
            return json.loads(candidate)

        raise json.JSONDecodeError("No JSON array found", text, 0)

    try:
        response = ask_llm(prompt, temperature=0.0, enable_thinking=False)
        if not response.strip():
            print("[WARN] LLM 未返回结果，使用内置兜底测试用例")
            return _fallback_test_cases()[:num_cases]

        cases = _parse_cases(response)
        valid_cases = []
        for case in cases:
            if not isinstance(case, dict):
                continue
            input_md = case.get("input_md", "")
            expected_type = case.get("expected_type", "normal")
            must_contain = case.get("must_contain", [])
            purpose = case.get("purpose", "")

            if not isinstance(must_contain, list):
                must_contain = []

            valid_cases.append(
                {
                    "input_md": str(input_md),
                    "expected_type": "error" if expected_type == "error" else "normal",
                    "must_contain": [str(x) for x in must_contain],
                    "purpose": str(purpose),
                }
            )

        if not valid_cases:
            print("[WARN] LLM 用例格式无效，使用内置兜底测试用例")
            return _fallback_test_cases()[:num_cases]

        return valid_cases[:num_cases]
    except json.JSONDecodeError:
        print("[WARN] LLM 输出不是合法 JSON，使用内置兜底测试用例")
        return _fallback_test_cases()[:num_cases]
    except Exception as e:
        print(f"生成测试用例失败: {e}")
        return _fallback_test_cases()[:num_cases]
