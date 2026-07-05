# 219. Contains Duplicate II

## 题目

给定数组 `nums` 和整数 `k`。

判断是否存在两个不同下标 `i` 和 `j`，满足：

```text
nums[i] == nums[j]
abs(i - j) <= k
```

也就是：有没有两个相同数字，它们的下标距离不超过 `k`。

## 思路一：滑动窗口 + set

这题可以理解成：

```text
对每个位置 i，只需要检查它前面 k 个位置里有没有相同数字
```

所以维护一个大小最多为 `k` 的窗口。

窗口里保存的是：

```text
当前下标前面最多 k 个元素
```

如果当前数字已经在窗口里，说明找到了距离不超过 `k` 的重复元素，返回 `True`。

如果没有，就把当前数字加入窗口。

当窗口大小超过 `k` 时，移除最左边的元素。

## 为什么收缩在加入后

代码顺序是：

```python
if num in window:
    return True

window.add(num)

if len(window) > k:
    window.remove(nums[index - k])
```

原因是：

```text
加入当前元素后，这个窗口是给下一个 index 使用的。
```

也就是说，在检查当前 `index` 时，窗口里应该是它前面的最多 `k` 个元素。

检查完当前数字后，再把当前数字加入窗口，为下一个位置做准备。

如果加入后窗口超过 `k`，再把过期元素移除。

## 代码一

```python
class Solution:
    def containsNearbyDuplicate(self, nums: list[int], k: int) -> bool:
        window: set[int] = set()

        for index, num in enumerate(nums):
            if num in window:
                return True

            window.add(num)

            if len(window) > k:
                window.remove(nums[index - k])

        return False
```

## 思路二：HashMap 记录最近下标

这题也可以用字典写得更简洁。

字典含义：

```text
num -> 上一次出现的下标
```

遍历时，如果当前数字之前出现过，并且距离不超过 `k`，就返回 `True`。

否则更新这个数字最近一次出现的位置。

## `enumerate(nums)` 的作用

`enumerate(nums)` 可以在遍历列表时，同时拿到：

- 下标
- 元素值

例如：

```python
for index, num in enumerate(nums):
    ...
```

比手写：

```python
for index in range(len(nums)):
    num = nums[index]
```

更简洁。

## 代码二

```python
class HashMapSolution:
    def containsNearbyDuplicate(self, nums: list[int], k: int) -> bool:
        last_seen: dict[int, int] = {}

        for index, num in enumerate(nums):
            if num in last_seen and index - last_seen[num] <= k:
                return True

            last_seen[num] = index

        return False
```

## 复杂度

滑动窗口写法：

- 时间复杂度：O(n)
- 空间复杂度：O(k)

HashMap 写法：

- 时间复杂度：O(n)
- 空间复杂度：O(n)

## 心得

1. 这题可以理解成维护一个最近 `k` 个元素的窗口。
2. 窗口里用 `set`，可以 O(1) 判断当前数字是否已经出现过。
3. 收缩放在加入后，是因为加入当前元素后，窗口是给下一个下标使用的。
4. 更简洁的写法是用 HashMap 记录每个数字上一次出现的位置。
5. `enumerate(nums)` 可以同时拿到下标和元素值。
