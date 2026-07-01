# 682. Baseball Game

## 题目

给定一组操作 `operations`，计算棒球比赛的总得分。

操作含义：

- 整数字符串：记录一个新的分数
- `"+"`：记录前两个有效分数之和
- `"D"`：记录前一个有效分数的两倍
- `"C"`：删除前一个有效分数

## 思路

这题适合用栈。

原因是每个操作都和“最近的有效分数”有关：

- `"C"` 需要删除上一个有效分数
- `"D"` 需要读取上一个有效分数
- `"+"` 需要读取上一个和上上一个有效分数

栈正好适合保存最近状态。

在 Python 里，可以直接用 `list` 当栈：

```python
scores.append(x)  # 入栈
scores.pop()      # 出栈
scores[-1]        # 栈顶，也就是最近的有效分数
scores[-2]        # 上上个有效分数
```

更完整的栈基础笔记见：

[栈基础](../notes/stack_basics.md)

## 代码

```python
class Solution:
    def calPoints(self, operations: list[str]) -> int:
        scores: list[int] = []

        for operation in operations:
            if operation == "+":
                scores.append(scores[-1] + scores[-2])
            elif operation == "D":
                scores.append(scores[-1] * 2)
            elif operation == "C":
                scores.pop()
            else:
                scores.append(int(operation))

        return sum(scores)
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(n)

其中 `n` 是操作数量。

## 心得

1. 看到“上一个”“上上一个”“删除最近记录”这类描述，可以优先想到栈。
2. 栈最重要的特点是后进先出，适合处理最近的有效状态。
3. Python 里刷题通常直接用 `list` 当栈。
4. `stack[-1]` 表示最近一次有效记录，`stack[-2]` 表示上上次有效记录。
