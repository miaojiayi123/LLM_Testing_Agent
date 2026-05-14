# 软件测试智能体 (Software Testing Agent)

本项目是一个基于 **DeepSeek LLM** 的软件测试智能体（Software Testing Agent），用于自动测试本机安装的 `markdown2` 包本体。系统可自动分析源码、生成测试用例、执行多层测试、统计覆盖率并输出报告。

---

## 一、项目概述

智能体功能包括：

1. **自动分析源码**：读取本机 `markdown2` 源码并调用 LLM 进行分析。
2. **自动生成测试用例**：LLM 生成为主，内置规则兜底，避免流程中断。
3. **多层自动执行**：同时执行单元层（函数调用）和集成层（CLI 子进程）测试。
4. **自动判定结果**：给出单层判定、总判定及跨层输出一致性。
5. **白盒覆盖率统计**：统计行覆盖率与分支覆盖率（依赖 `coverage.py`）。
6. **自动生成报告**：输出 Markdown 报告与失败用例 JSON。

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
├── whitebox_analyzer.py       # 白盒覆盖率采集模块
├── requirements.txt           # 依赖清单
├── 实验报告.md                # 课程实验说明文档（根目录）
├── target/                    # 被测程序及测试接口
│   ├── markdown2_wrapper.py   # 被测程序封装
│   ├── tester.py              # 测试接口
│   └── __init__.py
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

- 读取本机 `markdown2` 源码
- 调用 DeepSeek 分析功能（不可用时继续执行）
- 自动生成测试用例（失败时回退兜底用例）
- 执行单元层 + 集成层测试
- 判定结果并检查跨层一致性
- 统计白盒覆盖率（行/分支）
- 生成报告

4. 运行完成后在 `results/` 文件夹查看输出：

- `report.md`：测试报告
- `failed_cases.json`：失败用例

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
  - 空输入、特殊字符
  - 综合 Markdown 场景

---

## 六、模块说明

| 模块                    | 功能                                                |
| ----------------------- | --------------------------------------------------- |
| `main.py`             | 智能体入口，整合所有模块，执行完整流程              |
| `llm_agent.py`        | 调用 DeepSeek API，实现分析、生成测试用例、失败分析 |
| `code_reader.py`      | 读取被测程序源码                                    |
| `test_generator.py`   | LLM 自动生成测试用例                                |
| `test_runner.py`      | 执行测试用例                                        |
| `result_analyzer.py`  | 多层判定与一致性分析（unit / integration / overall） |
| `whitebox_analyzer.py`| 白盒覆盖率采集（行/分支）                            |
| `report_generator.py` | 生成 Markdown 测试报告和失败用例                     |
| `target/`             | 对本机 `markdown2` 的调用封装与测试接口              |

---

## 七、运行示例

```
[INFO] 软件测试智能体启动
[INFO] 被测对象: markdown2 x.y.z
[INFO] 读取源码...
[INFO] 调用 DeepSeek 分析源码...
[INFO] 调用 DeepSeek 自动生成测试用例...
[INFO] 执行测试用例（多层）...
[INFO] 用例 #1 执行完成，判定: PASS (unit=PASS, integration=PASS)
[INFO] 采集白盒覆盖率（行/分支）...
[INFO] 生成测试报告...
[INFO] 软件测试智能体执行完成！
```

生成的报告示例：

```
测试用例总数：N
通过用例：A
失败用例：B
行覆盖率：X%
分支覆盖率：Y%
```

---

## 八、注意事项

1. 确保 DeepSeek API Key 正确并可联网访问。
2. 被测对象为本机安装的 `markdown2` 包，请确认环境可正常导入 `markdown2`。
3. 若网络不可用或 LLM 调用失败，系统会自动回退兜底用例继续执行。
4. 报告与失败用例会生成在 `results/` 目录；课程说明文档在根目录 `实验报告.md`。

---
