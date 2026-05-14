# main.py
import os
import json
from code_reader import read_code_files
from llm_agent import ask_llm
from test_generator import generate_test_cases
from test_runner import run_case
from result_analyzer import judge_multilevel
from report_generator import generate_report, build_local_failure_analysis
from target.markdown2_wrapper import get_markdown2_info
from whitebox_analyzer import collect_coverage_metrics

def main():
    print("[INFO] 软件测试智能体启动")
    target_info = get_markdown2_info()
    print(f"[INFO] 被测对象: markdown2 {target_info.get('version', 'unknown')}")
    print(f"[INFO] 被测源码: {target_info.get('source_path', 'unknown')}")

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
    test_cases = generate_test_cases(code_analysis, num_cases=50)
    if not test_cases:
        print("[ERROR] 测试用例生成失败，程序退出")
        return
    print(f"[INFO] 已生成 {len(test_cases)} 个测试用例")

    #执行测试用例（单元层 + 集成层）
    print("[INFO] 执行测试用例（多层）...")
    results = []
    for idx, case in enumerate(test_cases, start=1):
        input_md = case.get("input_md", "")
        result = run_case(input_md)
        judge_detail = judge_multilevel(case, result)
        results.append({
            "case": case,
            "result": result,
            "judge": judge_detail["overall"],
            "judge_detail": judge_detail
        })
        print(
            f"[INFO] 用例 #{idx} 执行完成，判定: {judge_detail['overall']} "
            f"(unit={judge_detail['unit']}, integration={judge_detail['integration']})"
        )

    print("[INFO] 采集白盒覆盖率（行/分支）...")
    coverage_metrics = collect_coverage_metrics(test_cases)
    if not coverage_metrics.get("enabled"):
        print(
            "[WARN] 白盒覆盖率未启用: "
            f"{coverage_metrics.get('reason', 'unknown reason')}。"
            "可执行 `pip install coverage` 后重试。"
        )

    # 失败用例分析（优先 LLM，失败时回退到本地规则）
    failed_cases = [r for r in results if r["judge"] != "PASS"]
    failure_analysis = ""
    if failed_cases and code_analysis:
        print("[INFO] 调用 DeepSeek 分析失败用例...")
        failure_prompt = f"""
下面是失败测试用例，请按以下固定模板输出 Markdown 分析，不要输出与模板无关内容：

模板字段（每个失败用例都要有）：
- 判定结果
- 测试目的
- 输入摘要
- 根因分类（如：功能实现偏差/异常处理缺失/测试可观测性不足/分析规则覆盖不足）
- 影响范围（高/中/低，并简述影响）
- 修复优先级（P1/P2/P3）
- 建议负责人（如：被测模块开发负责人/Markdown解析逻辑负责人/测试框架负责人）
- 失败原因
- 改进建议（至少2条，可执行）

请使用标题“### 失败原因分析（LLM）”，并按“#### 失败用例 #序号”分段。

失败用例如下：
{json.dumps(failed_cases, ensure_ascii=False, indent=2)}
"""
        failure_analysis = ask_llm(failure_prompt)
        if failure_analysis.strip():
            print("[INFO] 失败用例分析完成（LLM）")

    if failed_cases and not failure_analysis.strip():
        print("[INFO] 使用本地规则生成失败原因分析与改进建议...")
        failure_analysis = build_local_failure_analysis(failed_cases)

    if not failed_cases:
        failure_analysis = build_local_failure_analysis(failed_cases)

    #生成合并报告（包含失败分析）
    print("[INFO] 生成测试报告...")
    os.makedirs("results", exist_ok=True)
    generate_report(
        results,
        report_path="results/report.md",
        failed_path="results/failed_cases.json",
        failure_analysis=failure_analysis,
        target_info=target_info,
        coverage_metrics=coverage_metrics
    )

    print("[INFO] 软件测试智能体执行完成！")

if __name__ == "__main__":
    main()
