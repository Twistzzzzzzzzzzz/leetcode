# 81. Search in Rotated Sorted Array II

## 题目

给定一个可能被旋转过的升序数组 `nums`，判断 `target` 是否存在。

和 33. Search in Rotated Sorted Array 的区别是：这题允许数组中存在重复元素。

例如：

```text
nums = [2, 5, 6, 0, 0, 1, 2]
target = 0
```

返回：

```text
True
```

## 思路

整体思路和 33 一样：

1. 先检查 `nums[mid] == target`。
2. 再判断哪一半是有序的。
3. 如果 `target` 在有序的那一半，就往那一半找；否则去另一半。

但是这题多了重复元素，所以会出现一种特殊情况：

```python
nums[left] == nums[mid] == nums[right]
```

这时无法判断左半边有序还是右半边有序。

例如：

```text
[1, 0, 1, 1, 1]
 left   mid right
```

三个位置的值都可能相等，只看 `left`、`mid`、`right` 无法确定旋转点在左边还是右边。

不过在进入这个判断之前，已经检查过：

```python
if nums[mid] == target:
    return True
```

所以如果三端相等，而且 `nums[mid]` 不是 `target`，那么 `nums[left]` 和 `nums[right]` 也不是 `target`。

因此可以安全地收缩两边：

```python
left += 1
right -= 1
```

这一步不是普通二分砍掉一半，而是为了跳过无法判断方向的重复值。

## 和 33 的区别

33 不允许重复元素，所以只要判断：

```python
nums[left] <= nums[mid]
```

就能知道左半边是否有序。

81 允许重复元素，所以当：

```python
nums[left] == nums[mid] == nums[right]
```

时，左右两边都可能藏着旋转点，无法判断哪一边有序。

这时只能先移动边界：

```python
left += 1
right -= 1
```

剩下的逻辑和 33 基本一致。

## 代码

```python
class Solution:
    def search(self, nums: list[int], target: int) -> bool:
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return True

            if nums[left] == nums[mid] == nums[right]:
                left += 1
                right -= 1
            elif nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return False
```

## 复杂度

平均时间复杂度：O(log n)

最坏时间复杂度：O(n)

空间复杂度：O(1)

最坏情况是数组里有大量重复元素，二分无法判断方向，只能不断执行：

```python
left += 1
right -= 1
```

所以会退化成线性收缩。

## 心得

这题和 33 的核心区别是：

```python
if nums[left] == nums[right] == nums[mid]:
```

因为可能三端都相等。

三端相等时，无法判断哪一边有序，也就无法决定丢掉左半边还是右半边。

但如果 `nums[mid]` 已经确认不是 `target`，并且三端相等，那么 `nums[left]` 和 `nums[right]` 也不是 `target`，所以可以同时收缩两边。
