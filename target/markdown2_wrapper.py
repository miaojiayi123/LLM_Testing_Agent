# target/markdown2_wrapper.py
import inspect

import markdown2  # type: ignore


def get_markdown2_info() -> dict:
    return {
        "module_path": getattr(markdown2, "__file__", ""),
        "source_path": inspect.getsourcefile(markdown2) or "",
        "version": getattr(markdown2, "__version__", "unknown"),
    }

def convert_md_to_html(md_text: str) -> str:
    """
    调用 markdown2 将 Markdown 文本转换为 HTML。
    返回字符串：
        - HTML 输出
        - 如果输入错误，则抛出异常
    """
    try:
        # 始终调用本机安装的 markdown2 包本体
        return markdown2.markdown(md_text, extras=["fenced-code-blocks"])
    except Exception as e:
        raise e
