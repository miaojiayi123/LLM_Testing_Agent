# target/markdown2_wrapper.py
import markdown2

def convert_md_to_html(md_text: str) -> str:
    """
    调用 markdown2 将 Markdown 文本转换为 HTML。
    返回字符串：
        - HTML 输出
        - 如果输入错误，则抛出异常
    """
    try:
        # 解析 markdown，带 extras（例如代码高亮等）
        html = markdown2.markdown(md_text, extras=["fenced-code-blocks"])
        return html
    except Exception as e:
        raise e