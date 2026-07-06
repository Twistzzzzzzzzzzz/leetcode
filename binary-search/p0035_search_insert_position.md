# 35. Search Insert Position

## 题目

给定一个升序数组 `nums` 和一个目标值 `target`。

如果 `target` 在数组中，返回它的下标。

如果不存在，返回它应该被插入的位置。

## 思路

这题本质是：

```text
找第一个 >= target 的位置。
```

也就是 `lower_bound(target)`。

如果数组中存在 `target`，第一个 `>= target` 的位置就是 `target` 的位置。

如果数组中不存在 `target`，第一个 `>= target` 的位置就是它应该插入的位置。

如果所有元素都小于 `target`，返回 `len(nums)`，表示插入到数组末尾。

## 代码

```python
class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        left = 0
        right = len(nums)

        while left < right:
            mid = (left + right) // 2

            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid

        return left
```

## 为什么等于时不用单独 return

你的写法里有：

```python
elif nums[mid] > target:
    right = mid
else:
    return mid
```

这题这样写可以通过。

但如果把它理解成 `lower_bound`，就可以统一写成：

```python
if nums[mid] < target:
    left = mid + 1
else:
    right = mid
```

因为：

```text
nums[mid] >= target 时，mid 可能就是第一个 >= target 的位置。
```

所以保留 `mid`，继续往左找。

这样能和后面的边界查找题保持同一套思路。

## 区间含义

这里使用左闭右开区间：

```text
[left, right)
```

所以：

```python
right = len(nums)
while left < right
```

`right = len(nums)` 是有意义的，因为答案可能是插入到最后。

## 复杂度

- 时间复杂度：O(log n)
- 空间复杂度：O(1)

## 心得

1. Search Insert Position 本质是 `lower_bound`。
2. `lower_bound` 是找第一个 `>= target` 的位置。
3. 等于时不一定要直接返回，也可以保留 `mid`，继续向左收缩。
4. 左闭右开写法中，`right = len(nums)` 可以表示插入到数组末尾。
