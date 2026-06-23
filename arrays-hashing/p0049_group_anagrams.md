# 49. Group Anagrams

## 题目

给定一个字符串数组 `strs`，把所有字母异位词分到同一组。

字母异位词指的是：字符种类和每个字符出现次数相同，只是顺序不同。

例如：

```text
"eat"、"tea"、"ate"
```

它们排序后都是：

```text
"aet"
```

所以它们应该被分到同一组。

## 思路

这道题的关键是：为每个单词找到一个统一的“类别标识”。

对于 Anagram 来说，排序后的字符串可以作为统一标准形式：

```python
key = "".join(sorted(word))
```

例如：

```text
eat -> aet
tea -> aet
ate -> aet
```

然后用字典来分组：

- `key` 表示类别
- `value` 是属于这个类别的原始单词列表

所以这道题不是保存排序后的字符串作为答案，而是用排序后的字符串当作字典的 key，再把原始 `word` 放进对应分组。

## 代码

```python
class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups = {}

        for word in strs:
            key = "".join(sorted(word))

            if key not in groups:
                groups[key] = []
            groups[key].append(word)

        return list(groups.values())
```

## 字典分组模板

遇到“多个类别、每个类别有多个元素”的题，可以想到桶思想，也就是 HashMap 分组。

模板：

```python
groups = {}

for item in items:
    key = get_key(item)

    if key not in groups:
        groups[key] = []

    groups[key].append(item)
```

关键点：

- `key` 用来表示类别
- `groups[key]` 是这个类别对应的桶
- `append(item)` 放进去的是原始元素

## 为什么不要两两比较

分组题不要优先想“两两比较”。

如果每个单词都和其他单词比较，会很容易写出复杂的逻辑，例如：

- left / right
- pop
- visited
- 嵌套循环

更好的思路是：每个元素自己判断“我应该被放进哪个桶”。

这样每个单词只需要计算一次 key，然后放进对应分组。

## 复杂度

设：

- `n` 是字符串数量
- `k` 是字符串平均长度

时间复杂度：O(n * k log k)

因为每个字符串都要排序，单个字符串排序是 O(k log k)。

空间复杂度：O(n * k)

因为字典里最终会保存所有字符串。

## 心得

1. Anagram 可以通过 `sorted(word)` 得到统一的标准形式；例如 `"eat"`、`"tea"`、`"ate"` 排序后都是 `"aet"`。
2. 对于“多个类别、每个类别有多个元素”的分组题，可以使用桶思想，也就是 HashMap：`key` 表示类别，`value` 是属于这个类别的元素列表。
3. 分组题不要优先想“两两比较”，而要想“每个元素应该被放进哪个桶”。这可以避免复杂的 `left/right`、`pop`、`visited` 逻辑。
4. 字典分组模板是：先算 `key`，再初始化 `groups[key]`，最后把原始元素 `append` 进去。
5. 这题的关键不是保存排序后的字符串，而是用排序后的字符串作为 `key`，同时把原始 `word` 放进对应分组。
