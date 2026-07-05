# 209. Minimum Size Subarray Sum

## 题目

给定一个正整数数组 `nums` 和一个正整数 `target`。

找出总和大于等于 `target` 的最短连续子数组长度。

如果不存在这样的子数组，返回 `0`。

## 思路

这题是可变长度滑动窗口里的“最短型”。

窗口表示当前连续子数组：

```python
nums[left:right + 1]
```

窗口状态是：

```python
window_sum = 当前窗口的和
```

因为题目里的数字都是正数，所以：

- `right` 右移，窗口和只会变大
- `left` 右移，窗口和只会变小

这就适合普通滑动窗口。

## 关键点

当 `window_sum >= target` 时，当前窗口已经满足条件。

因为题目问最短长度，所以不能马上停下，而是要：

1. 先用当前窗口更新答案
2. 再尝试移除左端元素，让窗口变短

对应代码：

```python
while window_sum >= target:
    answer = min(answer, right - left + 1)
    window_sum -= nums[left]
    left += 1
```

答案更新必须放在缩小窗口之前。

因为缩小前的窗口是一个已经满足条件的合法答案。

## 代码

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        answer = float("inf")
        left = 0
        window_sum = 0

        for right, num in enumerate(nums):
            window_sum += num

            while window_sum >= target:
                answer = min(answer, right - left + 1)
                window_sum -= nums[left]
                left += 1

        return 0 if answer == float("inf") else answer
```

## `float("inf")`

当题目问最小值时，可以把初始答案设成无穷大：

```python
answer = float("inf")
```

这样第一次找到合法答案时，一定可以被更新掉。

最后如果答案还是无穷大，说明没有找到合法子数组：

```python
return 0 if answer == float("inf") else answer
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

虽然有内层 `while`，但每个元素最多被右指针加入一次、被左指针移除一次，所以总时间仍然是 O(n)。

## 心得

1. 最短型滑动窗口中，答案应该在满足条件时更新，并且要放在缩小窗口之前。
2. 当题目问最小值时，可以把初值设为 `float("inf")`，再用 `min` 不断更新。
3. 正数数组里的窗口和有单调性，所以适合滑动窗口；如果数组里有负数，就要谨慎，可能需要前缀和。
