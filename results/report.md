# 软件测试智能体实验报告

## 零、被测对象信息
- 被测包: markdown2
- 版本: 2.5.5
- 模块路径: /opt/homebrew/anaconda3/lib/python3.12/site-packages/markdown2.py
- 源码路径: /opt/homebrew/anaconda3/lib/python3.12/site-packages/markdown2.py

## 一、测试统计
- 测试用例总数: 10
- 通过用例: 9
- 失败用例: 1
- 崩溃用例: 0
- 超时用例: 0

## 二、方法与层级统计
- 已启用测试方法: 黑盒断言 + 白盒覆盖率
- 已启用测试层级: 单元测试（函数调用） + 集成测试（子进程CLI）
- 单元层通过数: 10/10
- 集成层通过数: 10/10
- 跨层输出一致用例数: 9/10

## 三、白盒覆盖率
- 覆盖率采集状态: enabled
- 覆盖率说明: ok
- 行覆盖率: 23.43%
- 分支覆盖率: 23.13%
- 覆盖源码: /opt/homebrew/anaconda3/lib/python3.12/site-packages/markdown2.py

## 四、失败用例详情
```json
[
  {
    "case": {
      "input_md": "```python\nprint('x')\n```",
      "expected_type": "normal",
      "must_contain": [
        "<code",
        "print"
      ],
      "purpose": "围栏代码块"
    },
    "result": {
      "unit": {
        "stdout": "<div class=\"codehilite\">\n<pre><span></span><code><span class=\"nb\">print</span><span class=\"p\">(</span><span class=\"s1\">&#39;x&#39;</span><span class=\"p\">)</span>\n</code></pre>\n</div>\n",
        "stderr": "",
        "status": "finished"
      },
      "integration": {
        "stdout": "<p><code>python\nprint('x')\n</code></p>\n",
        "stderr": "",
        "status": "finished"
      }
    },
    "judge": "FAIL",
    "judge_detail": {
      "overall": "FAIL",
      "unit": "PASS",
      "integration": "PASS",
      "outputs_consistent": false
    }
  }
]
```

## 五、失败原因分析与改进建议
### 失败原因分析（本地规则）

#### 失败用例 #1
- 判定结果: FAIL
- 测试目的: 围栏代码块
- 输入摘要: ```python
print('x')
```
- 根因分类: 测试可观测性不足
- 影响范围: 中（影响定位效率）
- 修复优先级: P2（常规）
- 建议负责人: 测试框架负责人
- 单元层判定: PASS
- 集成层判定: PASS
- 跨层输出一致性: False
- 集成层错误信息: 
- 失败原因: 输出与断言不一致，但未定位到明确缺失片段。
- 改进建议: 增加更细粒度断言与日志，定位具体转换差异。
