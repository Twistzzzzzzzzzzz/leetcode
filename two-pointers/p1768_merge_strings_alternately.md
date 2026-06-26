# 1768. Merge Strings Alternately

## 题目

给定两个字符串 `word1` 和 `word2`，要求交替合并它们。

如果某个字符串更长，把剩余部分直接接到结果末尾。

## 思路

使用两个指针：

- `index1` 指向 `word1` 当前字符
- `index2` 指向 `word2` 当前字符

当两个字符串都还有字符时，每轮依次加入：

```python
word1[index1]
word2[index2]
```

如果其中一个字符串先结束，另一个字符串剩下的部分可以用切片一次性加入结果。

最后用 `"".join(result)` 得到答案。

## 代码

```python
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        result: list[str] = []
        index1 = 0
        index2 = 0

        while index1 < len(word1) and index2 < len(word2):
            result.append(word1[index1])
            result.append(word2[index2])
            index1 += 1
            index2 += 1

        if index1 < len(word1):
            result.append(word1[index1:])

        if index2 < len(word2):
            result.append(word2[index2:])

        return "".join(result)
```

## 字符串拼接补充

这题用了刷题里常见的字符串构造方式：

```python
result = []
result.append(ch)
answer = "".join(result)
```

专门的字符串拼接笔记放在：

[Python 字符串拼接](../notes/python_string_concatenation.md)

## 复杂度

- 时间复杂度：O(m + n)
- 空间复杂度：O(m + n)

其中 `m` 是 `word1` 的长度，`n` 是 `word2` 的长度。

## 心得

1. 循环构造字符串时，优先考虑 `list.append` 加最后一次 `"".join(...)`。
2. `join` 的调用者是分隔符，不是要被追加内容的目标字符串。
3. 字符串不可变，拼接方法通常都会返回一个新字符串，不会原地修改原字符串。
