# 153. Find Minimum in Rotated Sorted Array

## 题目

给定一个升序数组，但是它可能被旋转过。

例如：

```text
[0, 1, 2, 4, 5, 6, 7]
```

旋转后可能变成：

```text
[4, 5, 6, 7, 0, 1, 2]
```

要求返回数组中的最小值。

题目保证数组中没有重复元素。

## 思路

这题属于旋转排序数组里的结构二分。

它和普通二分不太一样：普通二分通常是找 `target`，而这题没有具体 `target`，我们要找的是最小值所在的位置。

关键判断是比较：

```python
nums[mid]
nums[right]
```

如果：

```python
nums[mid] > nums[right]
```

说明 `mid` 在左边较大的那段里，最小值一定在 `mid` 右边。

所以：

```python
left = mid + 1
```

这里可以排除 `mid`，因为 `nums[right]` 已经比 `nums[mid]` 小，`mid` 不可能是最小值。

如果：

```python
nums[mid] <= nums[right]
```

说明从 `mid` 到 `right` 这一段是有序的，最小值可能就是 `mid`，也可能在 `mid` 左边。

所以：

```python
right = mid
```

这里不能写 `right = mid - 1`，因为 `mid` 仍然有可能是答案。

## 为什么代码量比普通二分少

这题看起来有点奇怪，是因为它不是在判断：

```text
nums[mid] 和 target 的大小关系
```

而是在判断：

```text
最小值在 mid 右边，还是在包含 mid 的左边
```

所以它没有 `nums[mid] == target` 这一支。

每一轮只需要做一个结构判断：

```text
nums[mid] > nums[right]
```

然后缩小搜索范围。

## 代码

```python
class Solution:
    def findMin(self, nums: list[int]) -> int:
        left = 0
        right = len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid

        return nums[left]
```

## 复杂度

时间复杂度：O(log n)

空间复杂度：O(1)

## 心得

这题虽然原理能懂，但是代码量比普通二分少，是因为它不是普通的 `target` 查找题。

旋转排序数组的关键是判断哪一边有序，或者判断最小值落在哪一侧。

找最小值时可以固定拿 `nums[right]` 当参照物：

- `nums[mid] > nums[right]`：最小值一定在右边，排除 `mid`。
- `nums[mid] <= nums[right]`：`mid` 可能就是最小值，保留 `mid`。

循环结束时，`left == right`，这个位置就是最小值的位置。
