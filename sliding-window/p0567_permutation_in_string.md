# 567. Permutation in String

## 题目

给定两个字符串 `s1` 和 `s2`，判断 `s2` 是否包含 `s1` 的某个排列。

换句话说，判断 `s2` 中是否存在一个长度等于 `len(s1)` 的子串，并且这个子串和 `s1` 的字符频率完全相同。

## 思路

这题是固定长度滑动窗口。

窗口长度固定为：

```python
k = len(s1)
```

因为排列不会改变字符数量，所以只需要检查 `s2` 中每个长度为 `k` 的窗口，是否和 `s1` 字符频率一致。

先用字典统计 `s1` 的字符频率：

```python
freq[char] = s1 中还需要匹配的 char 数量
```

遍历 `s2` 时：

1. 右端字符进入窗口，如果它在 `freq` 中，就把需求数量减一。
2. 如果窗口长度超过 `k`，左端字符离开窗口，如果它在 `freq` 中，就把需求数量加一。
3. 当窗口长度刚好等于 `k` 时，如果 `freq` 里所有值都是 `0`，说明当前窗口正好是 `s1` 的一个排列。

## 代码

```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        freq: dict[str, int] = {}
        k = len(s1)

        for char in s1:
            freq[char] = freq.get(char, 0) + 1

        left = 0

        for right, char in enumerate(s2):
            if char in freq:
                freq[char] -= 1

            while right - left + 1 > k:
                if s2[left] in freq:
                    freq[s2[left]] += 1
                left += 1

            if right - left + 1 == k and all(value == 0 for value in freq.values()):
                return True

        return False
```

## 为什么 `> k` 和 `>= k` 不能随便换

这两个写法都可以，但它们对应的检查位置不同。

### 写法一：窗口达到 `k` 后先检查，再收缩

```python
加入右端元素

if freq 全部为 0:
    return True

while right - left + 1 >= k:
    移除左端元素
    left += 1
```

这个写法的意思是：

```text
窗口一达到长度 k，就检查一次，然后立刻缩小到 k - 1。
```

所以下一轮加入新字符后，窗口又刚好变成 `k`。

### 写法二：窗口超过 `k` 后先收缩，再检查

```python
加入右端元素

while right - left + 1 > k:
    移除左端元素
    left += 1

if right - left + 1 == k and freq 全部为 0:
    return True
```

这个写法的意思是：

```text
窗口允许保持长度 k。只有超过 k 时才收缩。
```

所以检查答案必须放在收缩之后。

如果只把 `>= k` 改成 `> k`，但检查答案仍然放在收缩之前，就可能检查到长度为 `k + 1` 的窗口，从而错过正确答案。

例如：

```python
s1 = "ab"
s2 = "aab"
```

正确答案是 `True`，因为 `"ab"` 是 `s2` 的一个长度为 2 的子串。

如果窗口长度已经是 `"aa"`，下一轮先加入 `"b"`，窗口会暂时变成 `"aab"`。

这时候应该先收缩成 `"ab"`，再检查答案。

## `all`

```python
all(value == 0 for value in freq.values())
```

意思是：

```text
检查 freq 里的每个 value 是否都等于 0。
```

如果都等于 `0`，说明当前窗口里的字符刚好抵消了 `s1` 的需求。

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

其中 `n` 是 `s2` 的长度。因为题目只包含小写英文字母，字典最多 26 个 key，所以 `all(...)` 可以看成常数开销。

## 心得

1. 排列问题本质上经常是字符频率问题。
2. 看到“是否包含某个排列”，可以想到固定长度窗口，因为排列长度不会变。
3. 这题可以用频率抵消：进入窗口就减一，离开窗口就加一。
4. 使用 `> k` 时，要先收缩窗口，再在长度等于 `k` 时检查答案。
5. 使用 `>= k` 时，通常是先检查长度为 `k` 的窗口，再立刻收缩到 `k - 1`。两种写法不能只改符号，不改检查位置。
