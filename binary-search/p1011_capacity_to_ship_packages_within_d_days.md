# 1011. Capacity To Ship Packages Within D Days

## 题目

给定包裹重量数组 `weights` 和天数 `days`。

包裹必须按顺序装船，每天最多运输 `capacity` 重量。

问最小船容量是多少，才能在 `days` 天内运完所有包裹。

## 思路

这题是典型的二分答案。

搜索空间不是数组下标，而是：

```text
船的容量 capacity
```

容量越大，越容易在 `days` 天内运完。

容量越小，越难运完。

所以可行性长这样：

```text
False False False True True True
                  ^
              要找第一个 True
```

也就是：

```text
找最小可行 capacity
```

## 搜索边界

最小容量：

```python
max(weights)
```

因为船至少要能装下最重的那个包裹。

最大容量：

```python
sum(weights)
```

因为如果船一天能装下所有包裹，那么 1 天就能运完。

所以搜索范围是：

```python
[max(weights), sum(weights)]
```

## check 函数

`can_load(capacity)` 表示：

```text
船容量为 capacity 时，能不能在 days 天内运完。
```

模拟过程：

1. 从第一天开始。
2. 按顺序装包裹。
3. 如果当前包裹装不下，就换下一天。
4. 如果使用天数超过 `days`，说明容量不够。

## 代码

```python
class Solution:
    def shipWithinDays(self, weights: list[int], days: int) -> int:
        min_capacity = max(weights)
        max_capacity = sum(weights)

        def can_load(capacity: int) -> bool:
            used_days = 1
            loaded = 0

            for weight in weights:
                if loaded + weight > capacity:
                    loaded = 0
                    used_days += 1

                loaded += weight

                if used_days > days:
                    return False

            return True

        while min_capacity < max_capacity:
            mid_capacity = (min_capacity + max_capacity) // 2

            if can_load(mid_capacity):
                max_capacity = mid_capacity
            else:
                min_capacity = mid_capacity + 1

        return min_capacity
```

## 为什么 True 时保留 `mid`

如果：

```python
can_load(mid_capacity) == True
```

说明这个容量可以完成运输。

但题目问的是最小容量，所以 `mid_capacity` 本身可能就是答案，不能排除。

因此写：

```python
max_capacity = mid_capacity
```

## 为什么 False 时排除 `mid`

如果：

```python
can_load(mid_capacity) == False
```

说明这个容量太小，无法完成运输。

所以 `mid_capacity` 以及更小的容量都不可能是答案，应该写：

```python
min_capacity = mid_capacity + 1
```

## 和 Koko Eating Bananas 的关系

这题和 875 Koko Eating Bananas 是同一种模板。

共同点：

```text
都不是在数组里找元素，而是在答案范围里找最小可行值。
```

区别：

- Koko 的 `check(speed)` 是计算吃完需要多少小时。
- 这题的 `check(capacity)` 是模拟需要多少天装完。

## 复杂度

- 时间复杂度：O(n log S)
- 空间复杂度：O(1)

其中 `n` 是 `weights` 的长度，`S = sum(weights) - max(weights)` 量级的搜索范围。

## 心得

1. 看到“最小容量”“在 D 天内完成”这类题，可以优先考虑二分答案。
2. 搜索左边界通常是“必须满足的最低要求”，这里是 `max(weights)`。
3. 搜索右边界通常是“肯定可行的最大方案”，这里是 `sum(weights)`。
4. `check(capacity)` 要按题目规则模拟，而不是排序或打乱包裹顺序。
5. 找最小可行答案时，True 保留 `mid`，False 排除 `mid`。
