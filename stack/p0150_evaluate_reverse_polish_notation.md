# 150. Evaluate Reverse Polish Notation

## 题目

给定一个逆波兰表达式 `tokens`，计算表达式的结果。

逆波兰表达式的特点是：

```text
数字 数字 运算符
```

例如：

```text
["2", "1", "+", "3", "*"]
```

表示：

```text
(2 + 1) * 3
```

结果是 `9`。

## 思路

这题适合用栈。

遍历 `tokens`：

1. 如果当前 token 是数字，直接入栈。
2. 如果当前 token 是运算符，就从栈里弹出两个数字。
3. 用这两个数字计算结果，再把结果放回栈。

最后栈里剩下的那个数字就是答案。

## 为什么用栈

逆波兰表达式天然适合栈。

因为每当遇到一个运算符，它要使用的数字一定是前面最近出现、还没被使用的两个数字。

也就是：

```text
最近的两个有效数字
```

这正好符合栈保存最近状态的特点。

## 弹出顺序很重要

遇到运算符时，要弹出两个数：

```python
right = stack.pop()
left = stack.pop()
```

第一个弹出的是右操作数，第二个弹出的是左操作数。

对于加法和乘法，顺序影响不大。

但对于减法和除法，顺序非常重要：

```python
left - right
left / right
```

不能写反。

## 除法要向 0 截断

题目要求整数除法向 `0` 截断。

Python 的 `//` 是向下取整，不适合直接用于负数除法。

例如：

```python
-3 // 2 == -2
```

但这题期望：

```text
-3 / 2 -> -1
```

所以这里使用：

```python
int(left / right)
```

`int(...)` 会向 `0` 截断。

## 代码

```python
class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        stack: list[int] = []

        for token in tokens:
            if token in {"+", "-", "*", "/"}:
                right = stack.pop()
                left = stack.pop()

                if token == "+":
                    stack.append(left + right)
                elif token == "-":
                    stack.append(left - right)
                elif token == "*":
                    stack.append(left * right)
                else:
                    stack.append(int(left / right))
            else:
                stack.append(int(token))

        return stack[-1]
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(n)

其中 `n` 是 `tokens` 的长度。

## 心得

1. 逆波兰表达式遇到数字就入栈，遇到运算符就弹出两个数字计算。
2. 栈适合保存“最近还没被使用的数字”。
3. 弹出顺序要注意：先弹出的是右操作数，后弹出的是左操作数。
4. 减法和除法不能写反。
5. 除法不能直接用 `//`，因为负数时 `//` 不是向 `0` 截断。
