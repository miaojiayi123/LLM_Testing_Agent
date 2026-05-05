# llm_agent.py
from openai import OpenAI


API_KEY = "sk-9f925d4c71924125b038269fc9c1de27"

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com"
)

def ask_llm(prompt: str, model: str = "deepseek-v4-pro", temperature: float = 0.3) -> str:
    """
    调用 DeepSeek API 返回 LLM 响应
    
    参数:
    - prompt: 提示词
    - model: DeepSeek 模型，推荐 'deepseek-v4-pro'（支持思考模式）
    - temperature: 输出随机性，0-1，默认 0.3

    返回:
    - LLM 生成文本
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是专业的软件测试智能体，擅长分析 Python 程序并生成测试用例和测试策略。"},
                {"role": "user", "content": prompt}
            ],
            stream=False,                     # 非流式输出
            reasoning_effort="high",          # 高推理模式
            extra_body={"thinking": {"type": "enabled"}}  # 启用思考模式
        )
        # 返回 LLM 生成文本
        return response.choices[0].message.content
    except Exception as e:
        print(f"[ERROR] DeepSeek API 调用失败: {e}")
        return ""