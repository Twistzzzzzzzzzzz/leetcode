# 424. Longest Repeating Character Replacement

## 题目

给定一个只包含大写英文字母的字符串 `s`，最多可以把其中 `k` 个字符替换成其他字符。

返回经过最多 `k` 次替换后，可以得到的最长重复字符子串长度。

## 思路

这题是可变长度滑动窗口。

窗口表示当前正在考虑的一段连续子串：

```python
s[left:right + 1]
```

窗口里如果想变成同一个字符，最划算的做法一定是：

```text
保留窗口里出现次数最多的字符，把其他字符都替换掉
```

所以需要替换的字符数量是：

```text
窗口长度 - 窗口内最高频字符次数
```

窗口合法条件是：

```text
窗口长度 - 窗口内最高频字符次数 <= k
```

如果超过 `k`，说明当前窗口需要替换的字符太多了，就移动 `left` 收缩窗口。

## 核心公式

```python
window_len = right - left + 1
max_freq = max(freq.values())

window_len - max_freq <= k
```

可以这样理解：

```text
窗口中不是“最多那个字符”的其他字符，都需要被替换。
```

## 代码

```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        freq: dict[str, int] = {}
        left = 0
        answer = 0

        for right, char in enumerate(s):
            freq[char] = freq.get(char, 0) + 1
            max_freq = max(freq.values())

            while right - left + 1 - max_freq > k:
                freq[s[left]] -= 1
                left += 1
                max_freq = max(freq.values())

            answer = max(answer, right - left + 1)

        return answer
```

## 字典里找最大频率

如果只需要最高频次数，可以直接写：

```python
max_freq = max(freq.values())
```

如果想先找最高频字符，再取它的次数，可以写：

```python
max_char = max(freq, key=freq.get)
max_freq = freq[max_char]
```

你的写法：

```python
max_ele = freq[max(freq, key=freq.get)]
```

意思就是：

1. `max(freq, key=freq.get)` 找到 value 最大的 key
2. `freq[...]` 再通过这个 key 拿到对应的 value

不过代码里不要把变量命名为 `dict`，因为 `dict` 是 Python 自带的数据类型名。

## 模板对应

```python
for right in range(n):
    加入右端元素

    while 窗口不合法:
        移除左端元素
        left += 1

    更新最大长度
```

这题里：

```text
窗口不合法 = right - left + 1 - max_freq > k
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

题目只包含大写英文字母，最多 26 种字符，所以每次 `max(freq.values())` 可以看成常数开销。

## 心得

1. 核心公式：`窗口长度 - 窗口内最高频字符次数 <= k`。
2. 窗口长度是 `right - left + 1`，实际写代码时 `right` 经常用 `i` 表示。
3. 字典找最大 value 对应的 key 可以用：`max(freq, key=freq.get)`。
4. 这题的本质是：窗口里除了出现最多的那个字符，其他字符都需要被替换。
5. 最长型滑动窗口依旧是：加入右端元素，窗口不合法就收缩左端，合法后更新最大长度。
