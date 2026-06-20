# LeetCode Python

这个仓库用于长期整理 LeetCode 题解、测试用例和学习笔记，主要语言是 Python。

## 目录结构

```text
leetcode-python/
  problems/
    easy/       简单题题解
    medium/     中等题题解
    hard/       困难题题解
  tests/        本地测试用例
  notes/        方法论、题型和复盘笔记
  templates/    题解模板
  scripts/      辅助脚本
```

## 初次使用

```powershell
cd "C:\Users\Twistzz\Desktop\Files\学习\Graduate\leetcode-python"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest
```

## 新增题目

推荐使用脚本创建题解文件和测试文件：

```powershell
python scripts/new_problem.py 1 easy "Two Sum" --method twoSum
```

生成后的文件命名约定：

```text
problems/easy/p0001_two_sum.py
tests/test_p0001_two_sum.py
```

建议每道题至少记录：

- 解法思路
- 时间复杂度和空间复杂度
- 关键边界条件
- 做错或卡住的原因

## 常用命令

```powershell
python -m pytest
python -m ruff check .
python -m ruff format .
```

