# 875. Koko Eating Bananas

## 题目

给定若干堆香蕉 `piles` 和总小时数 `h`。

Koko 每小时选择一堆香蕉，以速度 `speed` 吃香蕉。

问最小的 `speed` 是多少，才能在 `h` 小时内吃完所有香蕉。

## 思路

这题是典型的二分答案。

搜索空间不是数组下标，而是吃香蕉速度：

```python
speed
```

最小速度：

```python
1
```

最大速度：

```python
max(piles)
```

因为一小时最多吃完最大那一堆就够了，再快没有意义。

## 单调性

速度越大，越容易在 `h` 小时内吃完。

速度越小，越难吃完。

所以可行性长这样：

```text
False False False True True True
                  ^
              要找第一个 True
```

也就是：

```text
找最小可行 speed
```

## check 函数

`can_finish(speed)` 表示：

```text
以 speed 的速度吃，能不能在 h 小时内吃完。
```

每一堆香蕉需要的小时数是向上取整：

```python
(pile + speed - 1) // speed
```

例如：

```text
pile = 10
speed = 3
```

真实除法是：

```text
10 / 3 = 3.333...
```

实际需要 4 小时，所以要向上取整。

## 代码

```python
class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        min_speed = 1
        max_speed = max(piles)

        def can_finish(speed: int) -> bool:
            hours = 0

            for pile in piles:
                hours += (pile + speed - 1) // speed

            return hours <= h

        while min_speed < max_speed:
            mid_speed = (min_speed + max_speed) // 2

            if can_finish(mid_speed):
                max_speed = mid_speed
            else:
                min_speed = mid_speed + 1

        return min_speed
```

## 为什么 True 时是 `max_speed = mid_speed`

如果：

```python
can_finish(mid_speed) == True
```

说明 `mid_speed` 可以吃完。

但是题目问的是：

```text
最小可行速度
```

所以 `mid_speed` 本身有可能就是答案，不能扔掉。

因此写：

```python
max_speed = mid_speed
```

意思是：

```text
mid 可行，答案可能是 mid，也可能在 mid 左边。
```

不能写：

```python
max_speed = mid_speed - 1
```

因为这会把 `mid_speed` 直接排除掉。万一 `mid_speed` 正好就是最小可行速度，答案就丢了。

## 为什么 False 时是 `min_speed = mid_speed + 1`

如果：

```python
can_finish(mid_speed) == False
```

说明 `mid_speed` 太慢，不能吃完。

由于速度越大越容易吃完，所以：

```text
mid_speed 以及所有比它更小的速度，都不可能是答案。
```

因此 `mid_speed` 可以被排除，写：

```python
min_speed = mid_speed + 1
```

这里不是因为“小的一定 +1”，而是因为：

```text
mid 已经被证明不可能是答案，所以要排除 mid。
```

## 为什么另一种写法不对

错误写法：

```python
if can_finish(mid_speed):
    max_speed = mid_speed - 1
else:
    min_speed = mid_speed
```

### 问题一：会丢答案

例如：

```text
speed:       1   2   3   4   5
can_finish: F   F   F   T   T
```

答案是 `4`。

如果某一轮：

```python
mid_speed = 4
can_finish(4) == True
```

错误写法会执行：

```python
max_speed = mid_speed - 1
```

也就是：

```python
max_speed = 3
```

这样直接把正确答案 `4` 排除了。

### 问题二：可能死循环

假设：

```python
min_speed = 3
max_speed = 4
```

那么：

```python
mid_speed = (3 + 4) // 2
mid_speed = 3
```

如果：

```python
can_finish(3) == False
```

错误写法执行：

```python
min_speed = mid_speed
```

也就是：

```python
min_speed = 3
```

区间还是 `[3, 4]`，没有变化，下一轮还是 `mid_speed = 3`，就会死循环。

所以必须写：

```python
min_speed = mid_speed + 1
```

## 正确模板

找最小可行答案：

```python
while left < right:
    mid = (left + right) // 2

    if check(mid):
        right = mid
    else:
        left = mid + 1

return left
```

含义：

```text
check(mid) == True:
    mid 可行，可能是答案，保留 mid
    right = mid

check(mid) == False:
    mid 不可行，不可能是答案，排除 mid
    left = mid + 1
```

## 复杂度

- 时间复杂度：O(n log m)
- 空间复杂度：O(1)

其中 `n` 是 `piles` 的长度，`m = max(piles)`。

## 心得

1. 这题不是在数组里二分，而是在答案范围里二分。
2. 看到“最小速度 / 最小容量 / 最小天数”这类题，可以想二分答案。
3. 找最小可行答案时，True 表示 `mid` 可行，不能排除 `mid`，所以 `right = mid`。
4. False 表示 `mid` 不可行，可以排除 `mid`，所以 `left = mid + 1`。
5. `left = mid` 或 `right = mid` 这类写法都要特别注意是否会死循环。
