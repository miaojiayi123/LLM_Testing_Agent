# 软件测试智能体 (Software Testing Agent)

本项目是一个基于 **DeepSeek LLM** 的软件测试智能体（Software Testing Agent），能够自动分析 Python 被测程序、生成测试用例、执行测试、判定结果，并生成测试报告。

---

## 一、项目概述

智能体功能包括：

1. **自动分析源码**：读取被测程序并调用 LLM 分析功能和接口。
2. **自动生成测试用例**：覆盖正常输入、边界条件、异常输入。
3. **自动执行测试用例**：通过统一接口调用被测程序。
4. **自动判定结果**：根据执行结果判定 PASS / FAIL / CRASH / TIMEOUT。
5. **自动生成报告**：输出 Markdown 测试报告、失败用例 JSON，并可调用 LLM 分析失败原因。

目标是实现一个 **完整闭环的自动化测试工具**，可用于课程实验、软件测试学习和 LLM 实践。

---

## 二、目录结构

```
LLM_Testing_Agent/
├── main.py                    # 智能体入口
├── llm_agent.py               # 调用 DeepSeek API 模块
├── code_reader.py             # 读取源码模块
├── test_generator.py          # 自动生成测试用例模块
├── test_runner.py             # 执行测试模块
├── result_analyzer.py         # 判定测试结果模块
├── report_generator.py        # 生成报告模块
├── target/                    # 被测程序及测试接口
│   ├── markdown2_wrapper.py   # 被测程序封装
│   ├── tester.py              # 测试接口
│   └── calculator.py          # 可选被测程序
├── testcases/                 # 测试用例存放（可选）
└── results/                   # 运行结果文件夹
```

---

## 三、环境要求

- Python 3.9+
- 依赖库：
```bash
pip install -r requirements.txt
```
- 如需手动安装（等价）：
```bash
pip install openai markdown2 python-dotenv coverage
```
- DeepSeek API Key（推荐通过 `.env` 配置）

推荐 `.env` 配置方式：
```bash
cp .env.example .env
```
然后编辑 `.env`：
```env
DEEPSEEK_API_KEY=你的DeepSeekKey
```

---

## 四、快速运行

1. 打开 VS Code 或终端，进入项目根目录：
```bash
cd path/to/LLM_Testing_Agent
```

2. 运行智能体：
```bash
python main.py
```

若报告中的白盒覆盖率显示 `disabled`，请确认已安装 `coverage`：
```bash
pip install coverage
```

3. 程序执行流程：

- 读取被测程序源码
- 调用 DeepSeek 分析功能
- 自动生成测试用例
- 执行测试用例
- 判定结果
- 生成报告

4. 运行完成后在 `results/` 文件夹查看输出：

- `report.md`：测试报告
- `failed_cases.json`：失败用例
- `failure_analysis.md`：失败分析（可选）

---

## 五、测试用例设计

- 测试用例由 LLM 自动生成
- 输入示例：
```json
{
  "input_md": "# Hello World",
  "expected_type": "normal",
  "purpose": "测试一级标题转换"
}
```

- 覆盖：
  - 标题（#、## 等）
  - 列表（有序、无序）
  - 代码块与行内代码
  - 链接、加粗、斜体
  - 空输入、非法输入
  - 综合 Markdown 场景

---

## 六、模块说明

| 模块                     | 功能                                                |
|---------------------------|---------------------------------------------------|
| `main.py`                | 智能体入口，整合所有模块，执行完整流程              |
| `llm_agent.py`            | 调用 DeepSeek API，实现分析、生成测试用例、失败分析 |
| `code_reader.py`          | 读取被测程序源码                                    |
| `test_generator.py`       | LLM 自动生成测试用例                                |
| `test_runner.py`          | 执行测试用例                                        |
| `result_analyzer.py`      | 判定 PASS / FAIL / CRASH / TIMEOUT                  |
| `report_generator.py`     | 生成 Markdown 测试报告和失败用例                    |
| `target/`                 | 被测程序封装及测试接口                              |

---

## 七、运行示例

```
[INFO] 软件测试智能体启动
[INFO] 读取源码...
[INFO] 调用 DeepSeek 分析源码...
[INFO] 调用 DeepSeek 自动生成测试用例...
[INFO] 执行测试用例...
[INFO] 用例 #1 执行完成，判定: PASS
[INFO] 用例 #2 执行完成，判定: FAIL
[INFO] 生成测试报告...
[INFO] 调用 DeepSeek 分析失败用例...
[INFO] 软件测试智能体执行完成！
```

生成的报告示例：

```
总测试用例数：30
通过：25
失败：5
崩溃：0
超时：0
```

---

## 八、注意事项

1. 确保 DeepSeek API Key 正确并可联网访问。
2. 被测程序必须可用，测试接口 (`tester.py`) 需封装核心函数。
3. LLM 生成的测试用例可能包含复杂 Markdown，需要测试程序能正确解析。
4. 报告、失败用例和失败分析会自动生成在 `results/` 目录。

---

## 九、扩展与优化
