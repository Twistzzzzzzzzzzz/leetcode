# 15. 3Sum

## 题目

给定一个整数数组 `nums`，找出所有不重复的三元组：

```text
[nums[i], nums[j], nums[k]]
```

要求三元组里的三个数相加等于 `0`。

## 关键思路

表面上这题像是三指针。

但更准确地说，是：

```text
固定一个数，把 3Sum 变成 2Sum
```

先排序，然后枚举第一个数 `nums[index]`。

此时问题变成：

```text
在 index 右边的有序数组里，找两个数，使它们的和等于 -nums[index]
```

这就变成了 167 Two Sum II 那类双指针问题。

## 为什么要先排序

排序后才能使用左右双指针。

因为排序让指针移动有明确方向：

- 如果 `nums[left] + nums[right]` 太小，说明需要更大的数，所以 `left += 1`。
- 如果 `nums[left] + nums[right]` 太大，说明需要更小的数，所以 `right -= 1`。

这里可以直接使用：

```python
nums.sort()
```

这题不是考排序实现，不需要自己手写排序。

排序还有另一个重要作用：方便去重。

排序会把相同数字放在一起，这样就可以通过相邻元素判断是否重复。

所以这题里排序不只是为了双指针，也是为了把相同数字集中起来，提前跳过重复值。

## 去重

这题要求结果不能重复，所以要处理三层去重。

去重要在“生成重复答案之前”完成。

不要依赖：

```python
if answer not in result:
```

这种写法是在重复答案已经产生之后再补救。

更好的思路是：提前跳过重复值，不让重复答案产生。

### 1. 固定数去重

如果当前固定的数和前一个固定数相同，直接跳过：

```python
if index > 0 and nums[index] == nums[index - 1]:
    continue
```

否则会得到重复三元组。

### 2. `left` 去重

找到一个答案后，`left` 右移。

如果新的 `nums[left]` 和刚才用过的左边数字相同，就继续跳过。

```python
while left < right and nums[left] == nums[left - 1]:
    left += 1
```

### 3. `right` 去重

同理，`right` 左移后，如果新的 `nums[right]` 和刚才用过的右边数字相同，也继续跳过。

```python
while left < right and nums[right] == nums[right + 1]:
    right -= 1
```

## 代码

```python
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        result: list[list[int]] = []

        for index in range(len(nums)):
            if index > 0 and nums[index] == nums[index - 1]:
                continue

            left = index + 1
            right = len(nums) - 1
            target = -nums[index]

            while left < right:
                current_sum = nums[left] + nums[right]

                if current_sum == target:
                    result.append([nums[index], nums[left], nums[right]])
                    left += 1
                    right -= 1

                    while left < right and nums[left] == nums[left - 1]:
                        left += 1

                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1

        return result
```

## 复杂度

- 时间复杂度：O(n^2)
- 空间复杂度：O(1)，不算返回结果

排序是 O(n log n)，外层固定一个数是 O(n)，内层双指针整体是 O(n)，所以主要复杂度是 O(n^2)。

## 心得

1. 表面上是三指针，但固定一个数后，就变成了双指针问题。
2. 如果题目要求找若干数之和，并且数组可以排序，且不要求返回原始下标，就可以考虑排序加双指针。
3. 已排序是双指针的重要触发点，因为指针移动后的结果变化方向可预测。
4. 3Sum 的本质是降维：固定一个数，把三数之和变成两数之和。
5. 排序的另一个作用是去重。排序不只是为了双指针，也是为了把相同数字放在一起。
6. 去重要在生成重复答案之前完成，不要依赖 `if answer not in result`，更好的思路是提前跳过重复值。
7. 排序可以直接用 `nums.sort()`，这题不是考手写排序。
