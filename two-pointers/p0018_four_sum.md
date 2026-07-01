# 18. 4Sum

## 题目

给定一个整数数组 `nums` 和一个整数 `target`，找出所有不重复的四元组：

```text
[nums[a], nums[b], nums[c], nums[d]]
```

要求四个数相加等于 `target`。

## 关键思路

4Sum 是 3Sum 的延伸。

本质仍然是降维：

```text
固定两个数，把 4Sum 变成 2Sum
```

先排序，然后：

1. 固定第一个数 `nums[first]`。
2. 固定第二个数 `nums[second]`。
3. 在 `second` 右边的有序区间里，用左右双指针找两个数。

剩下两个数需要满足：

```python
nums[left] + nums[right] == target - nums[first] - nums[second]
```

## 为什么还是排序加双指针

这题满足几个条件：

1. 要找若干数之和。
2. 不要求返回原始下标。
3. 数组可以排序。
4. 结果不能重复。

所以可以考虑排序加双指针。

排序有两个作用：

- 让双指针移动方向可预测。
- 把相同数字放在一起，方便提前去重。

## 细节 1：固定第一个数去重

如果当前第一个数和上一个第一个数相同，就跳过：

```python
if first > 0 and nums[first] == nums[first - 1]:
    continue
```

否则会生成重复四元组。

## 细节 2：固定第二个数去重

第二层循环也要去重。

但要注意边界是 `second > first + 1`，不是简单的 `second > 0`。

```python
if second > first + 1 and nums[second] == nums[second - 1]:
    continue
```

含义是：在同一个 `first` 下，如果当前 `second` 和前一个 `second` 相同，就跳过。

## 细节 3：找到答案后跳过左右重复值

当找到一个答案后，先移动 `left` 和 `right`：

```python
left += 1
right -= 1
```

然后跳过重复值：

```python
while left < right and nums[left] == nums[left - 1]:
    left += 1

while left < right and nums[right] == nums[right + 1]:
    right -= 1
```

这里比较的是刚刚用过的值：

- `nums[left] == nums[left - 1]`
- `nums[right] == nums[right + 1]`

这样可以避免生成重复答案。

## 细节 4：不要用 `if answer not in result`

去重要在生成重复答案之前完成。

不要依赖：

```python
if answer not in result:
```

更好的方式是排序后提前跳过重复值。

## 代码

```python
class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        nums.sort()
        result: list[list[int]] = []
        length = len(nums)

        for first in range(length):
            if first > 0 and nums[first] == nums[first - 1]:
                continue

            for second in range(first + 1, length):
                if second > first + 1 and nums[second] == nums[second - 1]:
                    continue

                left = second + 1
                right = length - 1
                two_sum_target = target - nums[first] - nums[second]

                while left < right:
                    current_sum = nums[left] + nums[right]

                    if current_sum == two_sum_target:
                        result.append(
                            [nums[first], nums[second], nums[left], nums[right]]
                        )

                        left += 1
                        right -= 1

                        while left < right and nums[left] == nums[left - 1]:
                            left += 1

                        while left < right and nums[right] == nums[right + 1]:
                            right -= 1
                    elif current_sum < two_sum_target:
                        left += 1
                    else:
                        right -= 1

        return result
```

## 复杂度

- 时间复杂度：O(n^3)
- 空间复杂度：O(1)，不算返回结果

排序是 O(n log n)，两层固定数字是 O(n^2)，里面双指针是 O(n)，所以主要复杂度是 O(n^3)。

## 心得

1. 4Sum 的本质也是降维：固定两个数，把四数之和变成两数之和。
2. 这类题细节很多，尤其是每一层固定值的去重边界。
3. `second` 去重时要写 `second > first + 1`，表示同一个 `first` 下跳过重复的第二个数。
4. 找到答案后，要移动 `left` 和 `right`，再跳过左右重复值。
5. 排序不只是为了双指针，也是为了去重。
