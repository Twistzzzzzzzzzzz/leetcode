# 26. Remove Duplicates from Sorted Array

## 题目

给定一个升序数组 `nums`，要求原地删除重复元素。

返回去重后的长度 `k`，并且让 `nums` 的前 `k` 个元素是不重复的结果。

## 思路

因为数组已经升序排列，重复元素一定会挨在一起。

使用快慢指针：

- `slow`：当前去重后有效区间的最后一个位置
- `fast`：负责向后扫描数组

如果 `nums[fast] != nums[slow]`，说明 `fast` 找到了一个新的数字。

这时让 `slow` 向前走一步，并把这个新数字写到 `nums[slow]`。

## 为什么返回 `slow + 1`

`slow` 存的是下标，不是长度。

如果最后一个有效元素在下标 `slow`，那么有效长度就是：

```python
slow + 1
```

例如：

```text
nums = [1, 1, 2]
去重后有效部分是 [1, 2]
最后一个有效元素 2 的下标是 1
长度是 1 + 1 = 2
```

所以这题不一定要额外维护 `count`。

更直接的写法是返回 `slow + 1`。

## 代码

```python
class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        if not nums:
            return 0

        slow = 0

        for fast in range(1, len(nums)):
            if nums[fast] != nums[slow]:
                slow += 1
                nums[slow] = nums[fast]

        return slow + 1
```

## 和 `count = 1` 的关系

如果题目保证数组非空，也可以写：

```python
slow = 0
count = 1
```

每发现一个新数字，就 `count += 1`。

但这种写法需要额外维护一个变量。

实际上 `slow` 已经能表示有效区间的末尾，所以返回 `slow + 1` 更自然。

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

只遍历一次数组，并且在原数组上覆盖。

## 心得

1. 这题可以用快慢指针：`fast` 负责扫描，`slow` 负责维护去重后的有效区间。
2. 一开始如果写 `count`，数组非空时应该设为 `1`。
3. 更好的方式是不维护 `count`，直接返回 `slow + 1`。
4. 因为 `slow` 是最后一个有效元素的下标，下标转长度需要加一。
