# 242. Valid Anagram

## 题目

判断字符串 `t` 是否是字符串 `s` 的字母异位词。

字母异位词的意思是：两个字符串包含完全相同的字符，并且每个字符出现的次数也相同，只是顺序可以不同。

例如：

```text
s = "anagram"
t = "nagaram"
```

它们都由 `a`、`n`、`a`、`g`、`r`、`a`、`m` 组成，所以返回 `True`。

## 思路

这道题和 217 不一样。

217 是判断一个数组里有没有重复元素，只需要知道“某个元素是否出现过”，所以可以用集合 `set`。

242 是比较两个字符串，需要知道“每个字符分别出现了几次”，所以更适合用字典 `dict`。

做法：

1. 先遍历 `s`，用字典 `count` 记录每个字符出现的次数。
2. 再遍历 `t`，每遇到一个字符，就在 `count` 里把这个字符的次数减 1。
3. 如果 `t` 中出现了 `count` 里没有的字符，直接返回 `False`。
4. 最后检查 `count` 里所有值是否都是 `0`。
5. 如果都是 `0`，说明两个字符串的字符种类和出现次数完全一样。

## 代码

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        count = {}

        for char in s:
            count[char] = count.get(char, 0) + 1

        for char in t:
            if char not in count:
                return False
            count[char] -= 1

        for value in count.values():
            if value != 0:
                return False

        return True
```

## 字典里的 `.values()`

字典 `dict` 可以通过 `.values()` 取出所有的值。

例如：

```python
count = {"a": 0, "b": 0, "c": 1}

for value in count.values():
    print(value)
```

这里会依次遍历 `0`、`0`、`1`。

`.values()` 返回的是一个可以遍历的数据结构，使用方式很像列表。

## 为什么不用两个字典

也可以分别统计 `s` 和 `t`：

```python
count_s = {}
count_t = {}
```

然后比较两个字典是否一样。

但这道题可以只用一个字典：

- 遍历 `s` 时，每个字符出现一次就 `+1`
- 遍历 `t` 时，每个字符出现一次就 `-1`

最后如果所有值都回到 `0`，说明两个字符串刚好抵消。

这种写法可以避免创建两个字典。

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

空间复杂度这里通常记作 O(1)，因为题目只包含小写英文字母，最多只有 26 种字符。

如果字符种类不固定，也可以理解为 O(k)，`k` 是不同字符的数量。

## 心得

1. 字典的值可以通过 `.values()` 方法获得，返回的是一个类似列表、可以遍历的数据结构。
2. 当比较两个数组或字符串时，可以使用 `dict` 记录每个元素出现的次数，并且可以灵活运用 `+1` 和 `-1`，避免创建两个字典。
