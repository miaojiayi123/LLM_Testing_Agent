# code_reader.py
import inspect


def _get_markdown2_source_path() -> str:
    try:
        import markdown2  # type: ignore
        return inspect.getsourcefile(markdown2) or getattr(markdown2, "__file__", "")
    except Exception as e:
        print(f"读取 markdown2 本体路径失败: {e}")
        return ""


def read_code_files(files=None) -> str:
    """
    读取被测程序源码，用于 LLM 分析
    """
    if files is None:
        source_path = _get_markdown2_source_path()
        files = [source_path, "target/tester.py"] if source_path else ["target/tester.py"]
    content = ""
    for file in files:
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                content += "\n===== {} =====\n".format(file)
                content += f.read()
        except Exception as e:
            print(f"读取文件 {file} 出错: {e}")
    return content
