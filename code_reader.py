# code_reader.py
def read_code_files(files=None) -> str:
    """
    读取被测程序源码，用于 LLM 分析
    """
    if files is None:
        files = ["target/calculator.py"]
    content = ""
    for file in files:
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                content += "\n===== {} =====\n".format(file)
                content += f.read()
        except Exception as e:
            print(f"读取文件 {file} 出错: {e}")
    return content