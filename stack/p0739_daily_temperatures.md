# 739. Daily Temperatures

## 题目

给定一个数组 `temperatures`，其中 `temperatures[i]` 表示第 `i` 天的温度。

对于每一天，求还要等几天才会出现更高的温度。

如果之后不会出现更高温度，答案是 `0`。

## 思路

这题是单调栈的入门题。

栈里存的不是温度，而是下标。

栈里保存的是：

```text
还没有找到更高温度的那些天的下标
```

当遍历到第 `index` 天时，如果当前温度 `temperature` 比栈顶下标对应的温度更高：

```python
temperatures[stack[-1]] < temperature
```

说明当前这一天就是栈顶那一天等待的“更暖的一天”。

于是弹出栈顶下标，并计算等待天数：

```python
previous_index = stack.pop()
answer[previous_index] = index - previous_index
```

## 为什么栈里存下标

因为这题最后要返回的是“等了几天”，不是更高温度是多少。

等待天数需要用两个下标相减：

```python
index - previous_index
```

如果栈里只存温度，就没法直接知道它是哪一天，也就没法计算等待天数。

所以这里栈里应该存下标。

这点很重要。

## 为什么要用 `while`

当前温度可能同时解决前面很多天的问题。

例如：

```text
temperatures = [73, 71, 70, 76]
```

当遍历到 `76` 时，它比前面的 `70`、`71`、`73` 都高。

所以要连续弹出多个下标，给它们填答案。

因此这里要用：

```python
while stack and temperatures[stack[-1]] < temperature:
```

而不是只用一次 `if`。

## 栈的单调性

这个栈从栈底到栈顶，对应的温度是递减的。

因为如果当前温度比栈顶更高，栈顶就会被弹出并得到答案。

最后留在栈里的，都是还没找到更高温度的下标。

这就是单调栈的基本感觉：

```text
栈里保存一批还没找到答案的元素。
新元素来了以后，尝试帮栈顶元素结算答案。
```

## 代码

```python
class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        answer = [0] * len(temperatures)
        stack: list[int] = []

        for index, temperature in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temperature:
                previous_index = stack.pop()
                answer[previous_index] = index - previous_index

            stack.append(index)

        return answer
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(n)

虽然有 `while`，但每个下标最多入栈一次、出栈一次，所以总时间复杂度仍然是 O(n)。

## 心得

1. 这里的栈是用来存下标的，不是直接存温度。
2. 存下标是因为答案要计算等待天数：`index - previous_index`。
3. 单调栈保存的是还没找到答案的元素。
4. 当前温度可能一次解决多个旧下标，所以要用 `while`。
5. 看到“下一个更大元素”“还要等多久才出现更大值”，可以考虑单调栈。
