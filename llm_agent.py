# llm_agent.py
import os
from openai import OpenAI

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv()


def _build_client():
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


client = _build_client()

def ask_llm(
    prompt: str,
    model: str = "deepseek-v4-pro",
    temperature: float = 0.3,
    enable_thinking: bool = True,
) -> str:
    """
    调用 DeepSeek API 返回 LLM 响应
    
    参数:
    - prompt: 提示词
    - model: DeepSeek 模型，推荐 'deepseek-v4-pro'（支持思考模式）
    - temperature: 输出随机性，0-1，默认 0.3

    返回:
    - LLM 生成文本
    """
    if client is None:
        print("[WARN] 未检测到 DEEPSEEK_API_KEY，跳过 LLM 调用")
        return ""

    try:
        request_kwargs = dict(
            model=model,
            messages=[
                {"role": "system", "content": "你是专业的软件测试智能体，擅长分析 Python 程序并生成测试用例和测试策略。"},
                {"role": "user", "content": prompt}
            ],
            stream=False,                     # 非流式输出
            reasoning_effort="high",          # 高推理模式
            temperature=temperature,
        )
        if enable_thinking:
            request_kwargs["extra_body"] = {"thinking": {"type": "enabled"}}

        response = client.chat.completions.create(**request_kwargs)
        # 返回 LLM 生成文本
        return response.choices[0].message.content
    except Exception as e:
        print(f"[ERROR] DeepSeek API 调用失败: {e}")
        return ""
