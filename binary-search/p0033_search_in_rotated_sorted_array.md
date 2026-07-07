# 33. Search in Rotated Sorted Array

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

要求在数组中查找 `target`，找到返回下标，找不到返回 `-1`。

题目保证数组中没有重复元素。

## 思路

这题是旋转排序数组里的 target 查找。

普通二分依赖整个数组有序，但旋转数组整体不一定有序。不过每次从中间切开以后，左半边和右半边至少有一边是有序的。

所以每一轮要先做两件事：

1. 如果 `nums[mid] == target`，直接返回。
2. 否则判断左半边有序，还是右半边有序。

如果左半边有序：

```python
nums[left] <= nums[mid]
```

再判断 `target` 是否落在左半边：

```python
nums[left] <= target < nums[mid]
```

如果在左半边，就向左找：

```python
right = mid - 1
```

否则向右找：

```python
left = mid + 1
```

如果右半边有序：

```python
nums[left] > nums[mid]
```

再判断 `target` 是否落在右半边：

```python
nums[mid] < target <= nums[right]
```

如果在右半边，就向右找：

```python
left = mid + 1
```

否则向左找：

```python
right = mid - 1
```

## 等号为什么这样写

这些等号不是随便加的，它们分别对应闭区间搜索和边界值是否可能是答案。

### `while left <= right`

这里用的是闭区间：

```text
[left, right]
```

当 `left == right` 时，区间里还有一个元素没有检查，所以必须继续进入循环。

找具体 `target` 时，通常写：

```python
while left <= right:
```

找边界时，才更常见：

```python
while left < right:
```

### `nums[left] <= nums[mid]`

这句是在判断左半边是否有序。

当 `left == mid` 时，左半边只有一个元素，也应该算有序。

所以这里要写：

```python
nums[left] <= nums[mid]
```

不能写成：

```python
nums[left] < nums[mid]
```

### `nums[left] <= target < nums[mid]`

左边要包含 `nums[left]`，因为 `target` 可能正好等于左边界。

右边不包含 `nums[mid]`，因为前面已经单独判断过：

```python
if nums[mid] == target:
    return mid
```

走到后面的范围判断时，已经确定 `target != nums[mid]`。

所以左半边的判断范围是：

```text
[left, mid)
```

对应：

```python
nums[left] <= target < nums[mid]
```

### `nums[mid] < target <= nums[right]`

右半边同理。

左边不包含 `nums[mid]`，因为 `mid` 已经检查过。

右边要包含 `nums[right]`，因为 `target` 可能正好等于右边界。

所以右半边的判断范围是：

```text
(mid, right]
```

对应：

```python
nums[mid] < target <= nums[right]
```

## 代码

```python
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
```

## 复杂度

时间复杂度：O(log n)

空间复杂度：O(1)

## 心得

这题的关键不是直接套普通二分，而是先判断哪一半有序。

等号的核心记法：

- `left` 和 `right` 是还没排除的边界，所以 `target` 可能等于 `nums[left]` 或 `nums[right]`。
- `mid` 已经被单独检查过，所以后面的范围判断不再包含 `nums[mid]`。

因此：

```python
nums[left] <= target < nums[mid]
nums[mid] < target <= nums[right]
```

这两个判断分别表示：

```text
target 在左半边 [left, mid)
target 在右半边 (mid, right]
```
