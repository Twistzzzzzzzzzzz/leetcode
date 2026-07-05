# 394. Decode String

## 题目

给定一个编码字符串 `s`，按照规则解码。

编码格式类似：

```text
k[encoded_string]
```

表示把 `encoded_string` 重复 `k` 次。

例如：

```text
3[a2[c]]
```

结果是：

```text
accaccacc
```

## 思路

这题适合用栈处理嵌套结构。

核心变量：

- `repeat`：当前读到的重复次数
- `current`：当前层正在构造的字符串
- `stack`：保存进入下一层之前的状态

遇到不同字符时：

1. 如果是数字，累积到 `repeat`。
2. 如果是 `[`，保存当前状态 `(current, repeat)`，然后进入新的一层。
3. 如果是 `]`，弹出上一层状态，把当前层字符串重复后接回上一层。
4. 如果是普通字母，拼到 `current`。

## 为什么数字要这样累积

数字可能不止一位。

例如：

```text
10[a]
```

不能只读一个字符。

所以看到数字时要写：

```python
repeat = repeat * 10 + int(char)
```

这和之前 271 Encode and Decode Strings 里“长度可能有多位，所以要先找到分隔符”的问题类似。

这里没有 `#` 分隔符，而是通过逐字符扫描来累积数字。

## 为什么遇到 `[` 要保存状态

遇到 `[` 说明要进入一个新的嵌套层。

进入新层前，必须保存当前层的信息：

```python
stack.append((current, repeat))
```

其中：

- `current` 是进入括号前已经构造好的字符串
- `repeat` 是这个括号内容需要重复的次数

然后重置：

```python
repeat = 0
current = ""
```

开始构造括号内部的字符串。

## 为什么遇到 `]` 要弹栈

遇到 `]` 说明当前这一层结束了。

这时弹出上一层保存的状态：

```python
previous, count = stack.pop()
```

然后把当前层字符串重复 `count` 次，接回上一层：

```python
current = previous + current * count
```

## 状态变化示例

输入：

```text
3[a2[c]]
```

| 字符 | 动作 | stack | repeat | current |
| --- | --- | --- | --- | --- |
| `"3"` | 数字累积：`repeat = 0 * 10 + 3` | `[]` | `3` | `""` |
| `"["` | 保存当前状态：`("", 3)`，然后重置 | `[("", 3)]` | `0` | `""` |
| `"a"` | 普通字符，拼到 `current` | `[("", 3)]` | `0` | `"a"` |
| `"2"` | 数字累积：`repeat = 0 * 10 + 2` | `[("", 3)]` | `2` | `"a"` |
| `"["` | 保存当前状态：`("a", 2)`，然后重置 | `[("", 3), ("a", 2)]` | `0` | `""` |
| `"c"` | 普通字符，拼到 `current` | `[("", 3), ("a", 2)]` | `0` | `"c"` |
| `"]"` | 弹出 `("a", 2)`，合并：`"a" + "c" * 2` | `[("", 3)]` | `0` | `"acc"` |
| `"]"` | 弹出 `("", 3)`，合并：`"" + "acc" * 3` | `[]` | `0` | `"accaccacc"` |

## 一开始走弯路的原因

一开始如果用 `i`、`j` 手动切片，会很容易写复杂。

因为这题同时有：

- 多位数字
- 普通字母
- 左括号
- 右括号
- 嵌套结构

如果硬用下标去找每一段数字和字母，很容易出现边界问题。

更自然的方式是逐字符扫描：

```text
数字就累积
左括号就保存状态
右括号就恢复状态
字母就拼接
```

这样每一种字符都有固定职责，代码会简单很多。

## 代码

```python
class Solution:
    def decodeString(self, s: str) -> str:
        stack: list[tuple[str, int]] = []
        repeat = 0
        current = ""

        for char in s:
            if char.isdigit():
                repeat = repeat * 10 + int(char)
            elif char == "[":
                stack.append((current, repeat))
                repeat = 0
                current = ""
            elif char == "]":
                previous, count = stack.pop()
                current = previous + current * count
            else:
                current += char

        return current
```

## 复杂度

- 时间复杂度：O(n + m)
- 空间复杂度：O(n + m)

其中 `n` 是输入字符串长度，`m` 是最终解码后的字符串长度。

## 心得

1. 这题的关键是嵌套结构，适合用栈保存进入下一层之前的状态。
2. 数字可能是多位数，所以要用 `repeat = repeat * 10 + int(char)` 累积。
3. 遇到 `[` 保存当前状态，并重置当前层。
4. 遇到 `]` 恢复上一层状态，并把当前层结果重复后拼回去。
5. 不要一开始就用复杂的 `i/j` 下标切片硬解析，逐字符扫描更稳定。
