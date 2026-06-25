# 128. Longest Consecutive Sequence

## 题目

给定一个未排序数组 `nums`，找出数字连续的最长序列长度。

要求时间复杂度是 O(n)。

例如：

```text
nums = [100, 4, 200, 1, 3, 2]
```

最长连续序列是：

```text
[1, 2, 3, 4]
```

所以返回 `4`。

## 如何识别这类题

看到这些关键词时，可以优先想到 `set`：

- 未排序数组
- 要求 O(n)
- 需要频繁判断某个数字是否存在
- 数值范围很大，不能用计数数组

这题的 `nums[i]` 范围很大，如果用计数数组，会浪费大量空间。

所以更适合把所有数字放进集合：

```python
nums_set = set(nums)
```

集合查找通常是 O(1)，可以快速判断：

```python
num + 1 in nums_set
```

## 思路

关键不是从每个数字都开始往后数。

如果每个数字都往后找连续序列，会重复计算。

比如：

```text
1, 2, 3, 4
```

如果从 `1` 数一遍，从 `2` 又数一遍，从 `3` 又数一遍，就浪费了。

所以只从连续序列的起点开始数。

一个数字 `num` 是起点的条件是：

```python
num - 1 not in nums_set
```

也就是说，前一个数字不存在。

然后从这个起点开始不断检查：

```python
current + 1 in nums_set
```

直到序列断掉。

## 代码

```python
class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        nums_set = set(nums)
        longest = 0

        for num in nums_set:
            if num - 1 in nums_set:
                continue

            current = num
            length = 1

            while current + 1 in nums_set:
                current += 1
                length += 1

            longest = max(longest, length)

        return longest
```

## 为什么是 O(n)

虽然代码里有 `while`，但每个数字最多只会作为某个连续序列的一部分被访问一次。

因为只有序列起点才会进入扩展逻辑。

不是起点的数字会被跳过：

```python
if num - 1 in nums_set:
    continue
```

所以整体时间复杂度仍然是 O(n)。

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(n)

空间主要来自 `nums_set`。

## 心得

1. 一开始也可能想到哈希表或计数数组，但这题值域很大，不能用计数数组。
2. 看到 `unsorted array + O(n) time`，并且需要判断数字是否存在，可以优先想到 `set`。
3. 这题的关键是只从连续序列的起点开始扩展：`num - 1 not in nums_set`。
4. 不要从每个数字都开始往后数，否则会重复计算。
