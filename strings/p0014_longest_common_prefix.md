# 14. Longest Common Prefix

## 题目

给定一个字符串数组 `strs`，找出这些字符串的最长公共前缀。

如果不存在公共前缀，返回空字符串 `""`。

例如：

```text
strs = ["flower", "flow", "flight"]
```

它们都以 `"fl"` 开头，所以返回：

```text
"fl"
```

## 暴力解法

先用第一个字符串作为参考，逐列比较所有字符串的同一位置字符。

如果当前位置所有字符串都相同，就把这个字符加入答案。

如果某个字符串长度不够，或者字符不一样，就停止。

```python
class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        ans = []

        for i in range(len(strs[0])):
            same = True

            for j in range(len(strs)):
                if i >= len(strs[j]):
                    same = False
                    break
                if strs[0][i] != strs[j][i]:
                    same = False
                    break

            if same:
                ans.append(strs[0][i])
            else:
                break

        return "".join(ans)
```

## 优化思路

这道题不一定能从复杂度阶数上优化。

因为想确认公共前缀，最坏情况下还是需要比较很多字符。

可以做的优化是减少不必要的判断：

1. 先找到最短的字符串 `shortest`。
2. 最长公共前缀不可能比 `shortest` 更长。
3. 所以外层循环只需要遍历 `shortest`。
4. 一旦发现某个位置字符不同，立刻返回当前前缀。

## 代码

```python
class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        if not strs:
            return ""

        shortest = min(strs, key=len)

        for index in range(len(shortest)):
            for word in strs:
                if shortest[index] != word[index]:
                    return shortest[:index]

        return shortest
```

## 复杂度

设：

- `n` 是字符串数量
- `m` 是最短字符串的长度

时间复杂度：O(n * m)

空间复杂度：O(1)

这里的时间复杂度本质上还是要看需要比较多少字符。

在最坏情况下，所有字符串的前 `m` 个字符都一样，就必须比较 `n * m` 次。

## 心得

1. 不是每道题都能以复杂度阶数来优化。
2. 这道题本质上还是避免不了 O(n * m)，也就是“字符串数量 * 最短字符串长度”。
3. 这类题的优化更多是减少不必要的比较，比如先找到最短字符串，再尽早返回。
4. 写代码时要先处理空数组 `strs`，否则 `min(strs, key=len)` 会报错。
