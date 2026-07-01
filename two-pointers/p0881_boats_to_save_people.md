# 881. Boats to Save People

## 题目

给定每个人的体重 `people`，以及每艘船的承重 `limit`。

每艘船最多坐两个人，求最少需要多少艘船。

## 思路

先排序：

```python
people.sort()
```

然后使用左右双指针：

- `left` 指向当前最轻的人
- `right` 指向当前最重的人

每一轮都优先处理最重的人。

如果最轻的人和最重的人可以同船：

```python
people[left] + people[right] <= limit
```

就让他们一起上船，`left += 1`。

无论能不能配对，最重的人这一轮都一定会上船，所以 `right -= 1`，船数加一。

## 为什么最重的人无论如何都要上船

当前 `right` 指向还没安排的人里最重的一个。

如果他不能和最轻的人一起坐船，那么他也不可能和其他更重的人一起坐船。

所以他只能单独坐一艘船。

如果他能和最轻的人一起坐船，那就是一个合适配对。

因此每一轮都可以确定：`people[right]` 一定会被安排上船。

## 代码

```python
class Solution:
    def numRescueBoats(self, people: list[int], limit: int) -> int:
        people.sort()

        left = 0
        right = len(people) - 1
        boats = 0

        while left <= right:
            if people[left] + people[right] <= limit:
                left += 1

            right -= 1
            boats += 1

        return boats
```

## 复杂度

- 时间复杂度：O(n log n)
- 空间复杂度：O(1)

主要成本来自排序。

## 心得

1. 这题依旧是最小值和最大值配对，用左右双指针。
2. 每一轮都先考虑当前最重的人。
3. 无论是否能和最轻的人配对，最重的人这一轮都会上船。
4. 如果最轻和最重都不能一起坐船，那最重的人只能单独坐船。
