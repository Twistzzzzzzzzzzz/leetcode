# 41. First Missing Positive

## 题目

给定一个未排序数组 `nums`，找出数组中缺失的最小正整数。

要求：

- 时间复杂度 O(n)
- 空间复杂度 O(1)

## 优化前：使用 Set

最容易想到的是用集合记录出现过的数字。

```python
class SetSolution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        nums_set = set(nums)
        candidate = 1

        while candidate in nums_set:
            candidate += 1

        return candidate
```

这个写法很直观：

1. 先把所有数字放进集合。
2. 从 `1` 开始找。
3. 第一个不在集合里的正整数就是答案。

时间复杂度是 O(n)，但空间复杂度是 O(n)。

题目要求 O(1) 额外空间，所以还要继续优化。

## 关键观察

如果数组长度是 `n`，答案一定在：

```text
1 到 n + 1
```

原因是：

- 如果 `1..n` 中缺了某个数，答案就在 `1..n` 里面。
- 如果 `1..n` 全都存在，那么答案就是 `n + 1`。

所以我们只关心 `1..n` 这些数字。

小于 `1` 的数、大于 `n` 的数，都不可能影响答案。

## 原地哈希

这题可以把原数组当成哈希表。

目标是：

```text
数字 1 放到下标 0
数字 2 放到下标 1
数字 3 放到下标 2
...
数字 x 放到下标 x - 1
```

也就是：

```text
nums[x - 1] == x
```

整理完以后，从前往后扫描：

- 如果 `nums[0] != 1`，答案是 `1`
- 如果 `nums[1] != 2`，答案是 `2`
- 如果 `nums[i] != i + 1`，答案是 `i + 1`

如果所有位置都正确，答案就是 `n + 1`。

## 代码

```python
class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        n = len(nums)

        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                target_index = nums[i] - 1
                nums[i], nums[target_index] = nums[target_index], nums[i]

        for i in range(n):
            if nums[i] != i + 1:
                return i + 1

        return n + 1
```

## 为什么用 while

交换一次之后，当前位置换回来的数字仍然可能需要继续放到正确位置。

所以这里不能只用 `if`，要用 `while`。

例如：

```text
nums = [3, 4, -1, 1]
```

第一个位置是 `3`，应该放到下标 `2`。

交换后当前位置可能又换回来一个新的数字，仍然需要继续判断。

## 为什么还是 O(n)

虽然代码里有 `while`，但每次成功交换，至少会把一个数字放到它应该在的位置。

每个数字最多被放对一次。

所以总交换次数是 O(n)，整体时间复杂度仍然是 O(n)。

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

因为直接把原数组当成哈希表，没有额外创建集合。

## 另一种方法：负号标记

原地哈希还有另一种写法：用负号标记某个数字是否出现过。

核心还是利用这个事实：

```text
答案一定在 1..n+1
```

所以只需要关心 `1..n` 这些数字。

做法分三步：

1. 先把所有无关数字，也就是 `<= 0` 或 `> n` 的数字，改成 `n + 1`。
2. 遍历数组，看到数字 `x`，就把下标 `x - 1` 的位置标记成负数。
3. 最后从前往后找第一个仍然是正数的位置，这个位置对应的数字就是缺失的最小正整数。

代码：

```python
class NegativeMarkingSolution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        n = len(nums)

        for i in range(n):
            if nums[i] <= 0 or nums[i] > n:
                nums[i] = n + 1

        for i in range(n):
            value = abs(nums[i])

            if 1 <= value <= n:
                index = value - 1
                if nums[index] > 0:
                    nums[index] = -nums[index]

        for i in range(n):
            if nums[i] > 0:
                return i + 1

        return n + 1
```

这里要用 `abs(nums[i])`，因为某些位置可能已经被标记成负数了，但它原本代表的数字仍然要被读取。

这一版和交换版一样，都是把原数组当哈希表：

- 交换版：让数字 `x` 站到下标 `x - 1`
- 负号版：用下标 `x - 1` 的正负号表示数字 `x` 是否出现过

## 心得

1. 这一题的关键点在于：长度为 `n` 的数组，答案一定在 `1..n + 1` 中。
2. 这种方法可以看作一种“不严格的排序”，只把 `1..n` 这些有用数字放回对应位置。
3. `while` 每次至少会放对一个元素，所以时间复杂度还是 O(n)。
4. 这种方法也用到了哈希表思想，只是把原列表当成哈希表，下标当作哈希表索引。
5. 本质上和优化前版本类似，最后都是从前往后扫描一遍“哈希表”，找到第一个缺失的位置。
6. 负号标记法也是原地哈希：下标表示数字，正负号表示这个数字是否出现过。
