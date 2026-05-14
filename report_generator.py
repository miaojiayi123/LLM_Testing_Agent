# report_generator.py
import os
import json


def build_local_failure_analysis(failed_cases: list) -> str:
    """
    在无法调用 LLM 时，基于失败结果生成本地分析与改进建议。
    """
    if not failed_cases:
        return "本轮测试无失败用例，无需失败原因分析与改进建议。"

    lines = [
        "### 失败原因分析（本地规则）",
        "",
    ]
    for i, item in enumerate(failed_cases, start=1):
        case = item.get("case", {})
        result = item.get("result", {})
        judge_detail = item.get("judge_detail", {})
        judge = item.get("judge", "")
        purpose = case.get("purpose", "未提供测试目的")
        input_md = case.get("input_md", "")
        must_contain = case.get("must_contain", [])
        unit_result = result.get("unit", {})
        integration_result = result.get("integration", {})
        stdout = unit_result.get("stdout", "")
        stderr = unit_result.get("stderr", "")

        reasons = []
        suggestions = []
        root_cause = "判定逻辑/断言规则"
        impact = "中"
        priority = "P2（常规）"
        owner = "测试与解析模块负责人"

        if judge == "CRASH":
            reasons.append(f"运行报错：{stderr or '未知异常'}")
            suggestions.append("增强输入合法性校验与异常处理，避免直接抛出未捕获异常。")
            root_cause = "异常处理缺失"
            impact = "高（影响执行稳定性）"
            priority = "P1（高优先）"
            owner = "被测模块开发负责人"
        elif judge == "FAIL":
            missing_tokens = [x for x in must_contain if x not in stdout]
            if missing_tokens:
                reasons.append("输出缺少预期 HTML 片段: " + ", ".join(missing_tokens))
                suggestions.append("检查 Markdown 解析逻辑，补齐对应语法的转换规则。")
                root_cause = "功能实现偏差"
                impact = "中（影响功能正确性）"
                priority = "P2（常规）"
                owner = "Markdown 解析逻辑负责人"
            else:
                reasons.append("输出与断言不一致，但未定位到明确缺失片段。")
                suggestions.append("增加更细粒度断言与日志，定位具体转换差异。")
                root_cause = "测试可观测性不足"
                impact = "中（影响定位效率）"
                priority = "P2（常规）"
                owner = "测试框架负责人"
        else:
            reasons.append("失败类型未被规则覆盖。")
            suggestions.append("扩展判定与分析规则，覆盖该类型异常。")
            root_cause = "分析规则覆盖不足"
            impact = "低到中"
            priority = "P3（优化）"
            owner = "测试框架负责人"

        lines.extend(
            [
                f"#### 失败用例 #{i}",
                f"- 判定结果: {judge}",
                f"- 测试目的: {purpose}",
                f"- 输入摘要: {input_md[:120]}",
                f"- 根因分类: {root_cause}",
                f"- 影响范围: {impact}",
                f"- 修复优先级: {priority}",
                f"- 建议负责人: {owner}",
                f"- 单元层判定: {judge_detail.get('unit', 'unknown')}",
                f"- 集成层判定: {judge_detail.get('integration', 'unknown')}",
                f"- 跨层输出一致性: {judge_detail.get('outputs_consistent', 'unknown')}",
                f"- 集成层错误信息: {integration_result.get('stderr', '')[:200]}",
                f"- 失败原因: {'；'.join(reasons)}",
                f"- 改进建议: {'；'.join(suggestions)}",
                "",
            ]
        )

    return "\n".join(lines)


def generate_report(results: list,
                    report_path: str = "results/report.md",
                    failed_path: str = "results/failed_cases.json",
                    failure_analysis: str = "",
                    target_info: dict | None = None,
                    coverage_metrics: dict | None = None):
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
    - failure_analysis: 失败原因分析与改进建议（可由 LLM 或本地规则生成）
    - target_info: 被测对象信息（如版本、源码路径）
    """

    # 确保结果目录存在
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    # 统计各类测试结果
    total = len(results)
    passed = sum(1 for r in results if r["judge"] == "PASS")
    failed = sum(1 for r in results if r["judge"] == "FAIL")
    crashed = sum(1 for r in results if r["judge"] == "CRASH")
    timeout = sum(1 for r in results if r["judge"] == "TIMEOUT")
    unit_passed = sum(1 for r in results if r.get("judge_detail", {}).get("unit") == "PASS")
    integration_passed = sum(1 for r in results if r.get("judge_detail", {}).get("integration") == "PASS")
    consistent_count = sum(1 for r in results if r.get("judge_detail", {}).get("outputs_consistent") is True)

    # 保存失败用例到 JSON
    failed_cases = [r for r in results if r["judge"] != "PASS"]
    with open(failed_path, "w", encoding="utf-8") as f:
        json.dump(failed_cases, f, ensure_ascii=False, indent=2)

    cov = coverage_metrics or {}
    line_rate = cov.get("line_rate")
    branch_rate = cov.get("branch_rate")
    line_rate_text = f"{line_rate * 100:.2f}%" if isinstance(line_rate, float) else "unknown"
    branch_rate_text = f"{branch_rate * 100:.2f}%" if isinstance(branch_rate, float) else "unknown"

    # 生成 Markdown 报告内容
    report_lines = [
        "# 软件测试智能体实验报告",
        "",
        "## 零、被测对象信息",
        f"- 被测包: markdown2",
        f"- 版本: {(target_info or {}).get('version', 'unknown')}",
        f"- 模块路径: {(target_info or {}).get('module_path', 'unknown')}",
        f"- 源码路径: {(target_info or {}).get('source_path', 'unknown')}",
        "",
        "## 一、测试统计",
        f"- 测试用例总数: {total}",
        f"- 通过用例: {passed}",
        f"- 失败用例: {failed}",
        f"- 崩溃用例: {crashed}",
        f"- 超时用例: {timeout}",
        "",
        "## 二、方法与层级统计",
        "- 已启用测试方法: 黑盒断言 + 白盒覆盖率",
        "- 已启用测试层级: 单元测试（函数调用） + 集成测试（子进程CLI）",
        f"- 单元层通过数: {unit_passed}/{total}",
        f"- 集成层通过数: {integration_passed}/{total}",
        f"- 跨层输出一致用例数: {consistent_count}/{total}",
        "",
        "## 三、白盒覆盖率",
        f"- 覆盖率采集状态: {'enabled' if cov.get('enabled') else 'disabled'}",
        f"- 覆盖率说明: {cov.get('reason', '') or 'ok'}",
        f"- 行覆盖率: {line_rate_text}",
        f"- 分支覆盖率: {branch_rate_text}",
        f"- 覆盖源码: {cov.get('source_path', 'unknown')}",
        "",
        "## 四、失败用例详情",
        "```json",
        json.dumps(failed_cases, ensure_ascii=False, indent=2),
        "```",
        "",
        "## 五、失败原因分析与改进建议",
        failure_analysis or "本轮未生成失败分析内容。"
    ]

    # 写入 Markdown 文件
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"[INFO] 测试报告生成完成: {report_path}")
    print(f"[INFO] 失败用例已保存: {failed_path}")
