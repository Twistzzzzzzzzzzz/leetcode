# 3. Longest Substring Without Repeating Characters

## 题目

给定一个字符串 `s`，找出其中不含重复字符的最长子串长度。

注意这里是子串 `substring`，必须是连续的一段。

## 思路

这题是可变长度滑动窗口的核心题。

窗口表示当前正在维护的一段连续子串：

```python
s[left:right + 1]
```

窗口状态用 `seen` 集合维护：

```python
seen = 当前窗口里已经出现过的字符
```

窗口的合法条件是：

```text
窗口内没有重复字符
```

所以当当前字符 `s[right]` 已经在 `seen` 里时，说明加入它会导致窗口不合法。

这时要不断移除左边界字符：

```python
while s[right] in seen:
    seen.remove(s[left])
    left += 1
```

直到 `s[right]` 不再重复，再把它加入窗口。

每次窗口恢复合法后，更新最长长度：

```python
answer = max(answer, right - left + 1)
```

## 代码

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen: set[str] = set()
        left = 0
        answer = 0

        for right, char in enumerate(s):
            while char in seen:
                seen.remove(s[left])
                left += 1

            seen.add(char)
            answer = max(answer, right - left + 1)

        return answer
```

## 为什么这里用 `while`

因为一个重复字符可能需要连续移除多个左边字符，窗口才会重新合法。

例如：

```python
s = "abba"
```

当右指针走到第二个 `"b"` 时，只移除一次左边的 `"a"` 还不够，窗口里仍然有 `"b"`。

所以这里不能只用 `if`，要用 `while` 一直收缩到窗口合法。

## 关于 `length`

你的写法里用了一个额外变量 `length`，每次加入字符就 `+1`，每次移除字符就 `-1`。

这当然可以。

不过滑动窗口里窗口长度可以直接由左右边界算出来：

```python
right - left + 1
```

所以可以省掉 `length`，减少一个需要同步维护的状态。

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(min(n, m))

其中 `n` 是字符串长度，`m` 是字符集大小。

虽然里面有 `while`，但每个字符最多被加入集合一次、移出集合一次，所以总时间仍然是 O(n)。

## 心得

1. 看到“最长子串”“不重复”“连续”这几个信息，可以优先想到可变长度滑动窗口。
2. 这题的窗口状态是 `seen`，表示当前窗口里有哪些字符。
3. 窗口不合法的条件是：当前字符已经在 `seen` 里。
4. 不合法时移动 `left`，并且移动前要先把 `s[left]` 从 `seen` 中移除。
5. 最长型滑动窗口通常是先收缩到合法，再更新答案。
6. 窗口长度可以用 `right - left + 1` 直接计算，不一定需要额外维护 `length`。
