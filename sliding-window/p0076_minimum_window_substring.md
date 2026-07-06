# 76. Minimum Window Substring

## 题目

给定两个字符串 `s` 和 `t`，在 `s` 中找到一个最短子串，使它包含 `t` 中的所有字符。

如果不存在这样的子串，返回空字符串。

## 思路

这题是滑动窗口里的“最短覆盖”问题。

窗口表示当前正在检查的子串：

```python
s[left:right + 1]
```

目标是：

```text
窗口里包含 t 需要的所有字符，并且长度尽可能短。
```

## `freq` 的含义

这里的 `freq` 不是普通的窗口计数字典。

它表示：

```text
当前窗口距离满足 t，还缺多少字符。
```

例如：

```python
t = "AABC"
```

初始：

```python
freq = {
    "A": 2,
    "B": 1,
    "C": 1,
}
```

当右指针遇到目标字符时：

```python
freq[char] -= 1
```

可以这样理解：

- `freq[ch] > 0`：这个字符还缺
- `freq[ch] == 0`：这个字符刚好满足
- `freq[ch] < 0`：这个字符在窗口里多了

## `matched` 的含义

`target` 表示一共有多少类字符需要满足：

```python
target = len(freq)
```

`matched` 表示当前已经满足了多少类字符。

当某个字符的需求刚好变成 `0` 时：

```python
matched += 1
```

当左指针移除某个字符后，如果它的需求重新变成正数：

```python
matched -= 1
```

当：

```python
matched == target
```

说明窗口已经覆盖了 `t` 的所有字符。

## 代码

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or len(t) > len(s):
            return ""

        freq: dict[str, int] = {}
        for char in t:
            freq[char] = freq.get(char, 0) + 1

        left = 0
        matched = 0
        target = len(freq)
        best_len = float("inf")
        best_left = 0
        best_right = 0

        for right, char in enumerate(s):
            if char in freq:
                freq[char] -= 1
                if freq[char] == 0:
                    matched += 1

            while matched == target:
                if right - left + 1 < best_len:
                    best_len = right - left + 1
                    best_left = left
                    best_right = right

                left_char = s[left]
                if left_char in freq:
                    freq[left_char] += 1
                    if freq[left_char] > 0:
                        matched -= 1
                left += 1

        return "" if best_len == float("inf") else s[best_left:best_right + 1]
```

## 模板对应

这题依旧是滑动窗口最短型模板。

右扩：

```python
if char in freq:
    freq[char] -= 1
    if freq[char] == 0:
        matched += 1
```

窗口合法时：

```python
while matched == target:
    更新最短答案

    移除 s[left]
    如果移除后 freq[s[left]] > 0:
        matched -= 1

    left += 1
```

## 为什么答案更新在 `while` 里面

当 `matched == target` 时，当前窗口已经合法。

但题目要最短窗口，所以要一边更新答案，一边尝试收缩左边界。

每次收缩前，当前窗口都是一个合法候选答案：

```python
best_len = min(best_len, right - left + 1)
```

一旦移除左端字符导致 `matched < target`，窗口就不合法了，停止收缩，继续右扩。

## 复杂度

- 时间复杂度：O(m + n)
- 空间复杂度：O(k)

其中 `m` 是 `s` 的长度，`n` 是 `t` 的长度，`k` 是 `t` 中不同字符的数量。

每个字符最多被右指针加入一次，被左指针移除一次。

## 心得

1. 万变不离其宗，还是滑动窗口：右扩、判断合法、合法后收缩。
2. 右扩时，如果当前字符是目标字符，`freq[ch] -= 1`；如果 `freq[ch] == 0`，说明这一类字符刚好满足，`matched += 1`。
3. 窗口合法时，先更新最短答案，再移除 `s[left]`。
4. 如果移除后 `freq[s[left]] > 0`，说明这一类字符又不满足了，`matched -= 1`。
5. 这题的关键是把 `freq` 理解成“还缺多少”，而不是单纯理解成窗口里有多少。
