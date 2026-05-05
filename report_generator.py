# report_generator.py
import os
import json

def generate_report(results: list,
                    report_path: str = "results/report.md",
                    failed_path: str = "results/failed_cases.json"):
    """
    生成软件测试智能体实验报告，并保存失败用例

    参数:
    - results: 测试结果列表，每个元素包含：
        {
            "case": {...},       # 测试用例
            "result": {...},     # 执行结果
            "judge": "PASS/FAIL/CRASH/TIMEOUT"
        }
    - report_path: Markdown 测试报告保存路径
    - failed_path: 失败用例 JSON 保存路径
    """

    # 确保结果目录存在
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    # 统计各类测试结果
    total = len(results)
    passed = sum(1 for r in results if r["judge"] == "PASS")
    failed = sum(1 for r in results if r["judge"] == "FAIL")
    crashed = sum(1 for r in results if r["judge"] == "CRASH")
    timeout = sum(1 for r in results if r["judge"] == "TIMEOUT")

    # 保存失败用例到 JSON
    failed_cases = [r for r in results if r["judge"] != "PASS"]
    with open(failed_path, "w", encoding="utf-8") as f:
        json.dump(failed_cases, f, ensure_ascii=False, indent=2)

    # 生成 Markdown 报告内容
    report_lines = [
        "# 软件测试智能体实验报告",
        "",
        "## 一、测试统计",
        f"- 测试用例总数: {total}",
        f"- 通过用例: {passed}",
        f"- 失败用例: {failed}",
        f"- 崩溃用例: {crashed}",
        f"- 超时用例: {timeout}",
        "",
        "## 二、失败用例详情",
        "```json",
        json.dumps(failed_cases, ensure_ascii=False, indent=2),
        "```"
    ]

    # 写入 Markdown 文件
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"[INFO] 测试报告生成完成: {report_path}")
    print(f"[INFO] 失败用例已保存: {failed_path}")