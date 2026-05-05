# main.py
import os
import json
from code_reader import read_code_files
from llm_agent import ask_llm
from test_generator import generate_test_cases
from test_runner import run_case
from result_analyzer import basic_judge
from report_generator import generate_report

def main():
    print("[INFO] 软件测试智能体启动")

    #读取被测程序源码
    print("[INFO] 读取源码...")
    code_content = read_code_files()
    
    #LLM 分析代码功能和测试策略
    print("[INFO] 调用 DeepSeek 分析源码...")
    analysis_prompt = f"""
你是专业的软件测试智能体，请分析下面的 Python 被测程序，并输出：
1. 程序功能总结
2. 核心函数和接口
3. 建议的测试方法（边界测试、异常输入、随机测试等）
4. 重点测试场景
请用自然语言输出。
源码如下：
{code_content[:15000]}  # 截断防止过长
"""
    code_analysis = ask_llm(analysis_prompt)
    print("[INFO] 代码分析完成")

    #LLM 自动生成测试用例
    print("[INFO] 调用 DeepSeek 自动生成测试用例...")
    test_cases = generate_test_cases(code_analysis, num_cases=30)
    if not test_cases:
        print("[ERROR] 测试用例生成失败，程序退出")
        return
    print(f"[INFO] 已生成 {len(test_cases)} 个测试用例")

    #执行测试用例
    print("[INFO] 执行测试用例...")
    results = []
    for idx, case in enumerate(test_cases, start=1):
        # Markdown 被测程序使用 input_md 作为字段
        expression = case.get("input_md") or case.get("expression") or ""
        result = run_case(expression)
        judge = basic_judge(case, result)
        results.append({
            "case": case,
            "result": result,
            "judge": judge
        })
        print(f"[INFO] 用例 #{idx} 执行完成，判定: {judge}")

    #生成报告
    print("[INFO] 生成测试报告...")
    os.makedirs("results", exist_ok=True)
    generate_report(
        results,
        report_path="results/report.md",
        failed_path="results/failed_cases.json"
    )

    #LLM 分析失败用例（可选）
    failed_cases = [r for r in results if r["judge"] != "PASS"]
    if failed_cases:
        print("[INFO] 调用 DeepSeek 分析失败用例...")
        failure_prompt = f"""
下面是失败测试用例，请分析可能的失败原因并提供改进建议：
{json.dumps(failed_cases, ensure_ascii=False, indent=2)}
"""
        failure_analysis = ask_llm(failure_prompt)
        with open("results/failure_analysis.md", "w", encoding="utf-8") as f:
            f.write("# 失败用例分析\n\n")
            f.write(failure_analysis)
        print("[INFO] 失败用例分析完成: results/failure_analysis.md")
    else:
        print("[INFO] 所有测试用例通过，无失败用例分析")

    print("[INFO] 软件测试智能体执行完成！")

if __name__ == "__main__":
    main()