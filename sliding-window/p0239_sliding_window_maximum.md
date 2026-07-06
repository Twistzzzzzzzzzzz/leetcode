# 239. Sliding Window Maximum

## 题目

给定数组 `nums` 和窗口大小 `k`。

窗口每次向右移动一格，返回每个窗口里的最大值。

## 你的思路

你的写法是：

1. 先计算第一个窗口的最大值和最大值下标。
2. 窗口右移时，如果新进来的数更大，就更新当前最大值。
3. 如果当前最大值已经滑出窗口，就重新扫描当前窗口找最大值。

这个思路很自然，也能帮助理解窗口最大值为什么需要维护下标。

不过它最坏情况下会退化到 O(nk)。

例如数组一直递减：

```python
nums = [9, 8, 7, 6, 5, 4]
k = 3
```

每次窗口右移，原来的最大值都会离开窗口，于是需要重新扫描窗口。

## 标准思路：单调队列

这题的核心考点通常是单调队列。

队列里存的是下标，不是值。

并且队列对应的值保持从大到小：

```text
nums[queue[0]] >= nums[queue[1]] >= nums[queue[2]]
```

这样队首永远是当前窗口最大值的下标。

## 为什么队列要从大到小

当新元素 `nums[right]` 进入窗口时，如果它比队尾元素更大，那么队尾元素以后不可能成为最大值。

原因是：

```text
新元素更大，并且位置更靠右，生命周期还更长。
```

所以可以把队尾较小的元素弹出：

```python
while queue and nums[queue[-1]] <= nums[right]:
    queue.pop()
```

然后把当前下标加入队尾：

```python
queue.append(right)
```

## 为什么队列里存下标

因为需要判断队首元素是否已经离开当前窗口。

当前窗口左边界是：

```python
left = right - k + 1
```

如果：

```python
queue[0] < left
```

说明队首下标已经不在窗口内，要弹出：

```python
queue.popleft()
```

如果只存值，就不知道这个值是否已经滑出窗口。

## 代码

```python
from collections import deque


class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        decreasing: deque[int] = deque()
        answer: list[int] = []

        for right, num in enumerate(nums):
            while decreasing and nums[decreasing[-1]] <= num:
                decreasing.pop()

            decreasing.append(right)

            left = right - k + 1
            if decreasing[0] < left:
                decreasing.popleft()

            if right >= k - 1:
                answer.append(nums[decreasing[0]])

        return answer
```

## 模板

```python
queue = deque()

for right in range(len(nums)):
    while queue and nums[queue[-1]] <= nums[right]:
        queue.pop()

    queue.append(right)

    left = right - k + 1
    if queue[0] < left:
        queue.popleft()

    if right >= k - 1:
        answer.append(nums[queue[0]])
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(k)

每个下标最多入队一次、出队一次，所以总时间是 O(n)。

## 心得

1. 固定窗口最大值不能只维护一个最大值，因为最大值可能滑出窗口。
2. 如果最大值滑出后每次都重新扫描窗口，最坏情况会变成 O(nk)。
3. 单调队列维护的是“当前窗口里仍然可能成为最大值的下标”。
4. 新元素进来时，队尾比它小或等于它的元素都可以删除，因为它们不可能再成为最大值。
5. 队首下标如果小于当前窗口左边界，就说明已经滑出窗口，要从队首移除。
6. 这题和单调栈很像，但窗口会从左边滑动，所以需要能从两端操作的 `deque`。
