# 栈基础

## 什么是栈

栈是一种数据结构，英文叫 `Stack`。

它的核心规则是：

```text
后进先出
Last In, First Out
LIFO
```

也就是最后放进去的东西，最先被拿出来。

可以把它理解成一摞盘子：

- 最后放上去的盘子在最上面。
- 要拿盘子时，也只能先拿最上面的。

## Python 里怎么表示栈

LeetCode 里通常直接用 `list` 当栈。

```python
stack = []
```

### 入栈

```python
stack.append(5)
stack.append(2)
stack.append(9)
```

此时：

```python
stack == [5, 2, 9]
```

栈顶是最后一个元素：

```python
stack[-1]  # 9
```

### 出栈

```python
top = stack.pop()
```

`pop` 会删除并返回最后一个元素。

```python
top == 9
stack == [5, 2]
```

## 栈最重要的 4 个操作

| 操作 | Python 写法 | 含义 |
| --- | --- | --- |
| 入栈 | `stack.append(x)` | 把元素放到栈顶 |
| 出栈 | `stack.pop()` | 删除并返回栈顶元素 |
| 看栈顶 | `stack[-1]` | 只看最后一个元素，不删除 |
| 判断空栈 | `if stack` / `if not stack` | 判断栈是否为空 |

例子：

```python
stack = []

stack.append(1)
stack.append(2)

print(stack[-1])  # 2

x = stack.pop()
print(x)          # 2

print(stack)      # [1]
```

## LeetCode 里需要掌握栈的什么特性

### 1. 栈能记住最近的东西

这是最核心的。

比如 682 Baseball Game：

- `"C"`：删除上一个有效分数
- `"D"`：上一个有效分数乘以 `2`
- `"+"`：前两个有效分数相加

这里反复用到：

- 上一个
- 上上一个
- 最近的有效记录

所以用栈非常自然。

对应写法：

```python
stack[-1]  # 上一个
stack[-2]  # 上上一个
```

### 2. 栈适合处理撤销

只要题目里出现这些描述，可以想到栈：

- 删除上一个
- 撤销上一步
- 回退到之前
- 取消最近的操作

例如 682 Baseball Game：

```python
if operation == "C":
    stack.pop()
```

因为 `"C"` 要删除最近一次有效分数。

### 3. 栈适合处理括号匹配

经典题：

- 20. Valid Parentheses

例如：

```text
({[]})
```

遇到左括号就入栈：

```python
stack.append("(")
```

遇到右括号，就检查它能否和栈顶匹配：

```python
top = stack.pop()
```

括号匹配的本质是：

```text
最近打开的括号，必须最先关闭。
```

这正好是后进先出。

### 4. 栈适合处理嵌套结构

只要题目有一层套一层的结构，也可以考虑栈。

常见场景：

- 括号嵌套
- 路径回退
- 表达式计算
- 字符串解码

栈可以帮你保存当前层的信息，进入下一层时入栈，结束当前层时出栈。

### 5. 栈适合处理单调关系

这是后面会学的进阶栈，叫单调栈 `Monotonic Stack`。

典型题：

- 739. Daily Temperatures
- 496. Next Greater Element I
- 84. Largest Rectangle in Histogram

这类题常问：

- 下一个更大的元素
- 下一个更小的元素
- 左边或右边第一个比我大的数

单调栈可以保存一批“还没找到答案的元素”。

当前阶段先知道这个方向即可，不需要马上深入。

## LeetCode 栈题的识别信号

看到这些关键词，可以优先想栈：

- 最近的
- 上一个
- 撤销
- 删除前一个
- 括号匹配
- 嵌套结构
- 路径回退
- 表达式计算
- 下一个更大元素

## 模板 1：普通栈模拟

适合 682 Baseball Game。

```python
stack = []

for operation in operations:
    if operation == "C":
        stack.pop()
    elif operation == "D":
        stack.append(stack[-1] * 2)
    elif operation == "+":
        stack.append(stack[-1] + stack[-2])
    else:
        stack.append(int(operation))

return sum(stack)
```

核心：

- 需要最近的有效记录：`stack[-1]`
- 需要删除最近记录：`stack.pop()`

## 模板 2：括号匹配

适合 20. Valid Parentheses。

```python
stack = []
matches = {
    ")": "(",
    "]": "[",
    "}": "{",
}

for char in s:
    if char in "([{":
        stack.append(char)
    else:
        if not stack:
            return False
        if stack.pop() != matches[char]:
            return False

return not stack
```

核心：

```text
右括号必须匹配最近的左括号。
```

## 现在可以怎么理解栈

栈就是一个只能从末尾添加、从末尾删除的列表。

Python 里常用：

```python
stack.append(x)
stack.pop()
stack[-1]
```

LeetCode 里栈最常用于：

1. 保存最近状态。
2. 撤销最近操作。
3. 匹配括号或嵌套结构。
4. 找下一个更大或更小元素。

下一题可以练 20. Valid Parentheses，这是栈最基础、最典型的题。
