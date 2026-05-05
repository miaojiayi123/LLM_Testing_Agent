# 软件测试智能体实验报告

## 一、测试统计
- 测试用例总数: 30
- 通过用例: 11
- 失败用例: 0
- 崩溃用例: 19
- 超时用例: 0

## 二、失败用例详情
```json
[
  {
    "case": {
      "expression": "1+2",
      "expected_type": "normal",
      "purpose": "基本加法"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "3-1",
      "expected_type": "normal",
      "purpose": "基本减法"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "2*3",
      "expected_type": "normal",
      "purpose": "基本乘法"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "6/2",
      "expected_type": "normal",
      "purpose": "基本除法"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "2.5+1.5",
      "expected_type": "normal",
      "purpose": "小数加法"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "3.14*2",
      "expected_type": "normal",
      "purpose": "小数乘法"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "-3+2",
      "expected_type": "normal",
      "purpose": "负数作为操作数"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "4*-2",
      "expected_type": "normal",
      "purpose": "负数乘法"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "(1+2)*3",
      "expected_type": "normal",
      "purpose": "括号影响优先级"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "1+(2*3)",
      "expected_type": "normal",
      "purpose": "括号结合运算"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "(2.5+1.5)*(3-2)",
      "expected_type": "normal",
      "purpose": "小数与括号组合"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "10/3",
      "expected_type": "normal",
      "purpose": "非整除结果"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "2+3*4-1",
      "expected_type": "normal",
      "purpose": "运算符优先级验证"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "0-5",
      "expected_type": "normal",
      "purpose": "零减正数"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "1/1",
      "expected_type": "normal",
      "purpose": "除法结果为一"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "2 * (3 + 4)",
      "expected_type": "normal",
      "purpose": "带空格的表达式"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "((1+2)*3)",
      "expected_type": "normal",
      "purpose": "多层嵌套括号"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "-3.14*2/(1-2)",
      "expected_type": "normal",
      "purpose": "负数小数复杂表达式"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  },
  {
    "case": {
      "expression": "(1+2)*(3/(4-2))",
      "expected_type": "normal",
      "purpose": "嵌套括号与除法"
    },
    "result": {
      "stdout": "",
      "stderr": "module 'target.tester' has no attribute 'run_expression'",
      "status": "error"
    },
    "judge": "CRASH"
  }
]
```