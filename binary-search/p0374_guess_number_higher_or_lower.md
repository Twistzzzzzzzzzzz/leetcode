# 374. Guess Number Higher or Lower

## 题目

题目会在 `1..n` 中选择一个数字。

你需要通过 LeetCode 提供的 `guess(num)` API 猜出这个数字。

`guess(num)` 的返回值含义是：

```text
0  表示 num 正好是答案
1  表示 num 比答案小，也就是要猜更大的数
-1 表示 num 比答案大，也就是要猜更小的数
```

## 思路

这是最基础的闭区间二分。

搜索空间是：

```python
[1, n]
```

每次猜中间值：

```python
num = (lower + upper) // 2
```

然后根据 `guess(num)` 的返回值缩小范围。

## 代码

```python
class Solution:
    def guessNumber(self, n: int) -> int:
        lower = 1
        upper = n

        while lower <= upper:
            num = (lower + upper) // 2
            result = guess(num)

            if result == 0:
                return num
            if result == 1:
                lower = num + 1
            else:
                upper = num - 1
```

## 为什么 `result == 1` 时往右

题目里的 `guess(num)` 返回 `1`，意思是：

```text
your guess is lower than the picked number
```

也就是：

```text
num 猜小了，答案比 num 大。
```

所以 `num` 以及左边都不可能是答案，应该写：

```python
lower = num + 1
```

## 为什么 `result == -1` 时往左

`guess(num)` 返回 `-1`，意思是：

```text
your guess is higher than the picked number
```

也就是：

```text
num 猜大了，答案比 num 小。
```

所以 `num` 以及右边都不可能是答案，应该写：

```python
upper = num - 1
```

## 区间含义

这里使用闭区间：

```text
[lower, upper]
```

所以循环条件是：

```python
while lower <= upper
```

当 `lower == upper` 时，区间里还有一个数字，也要继续检查。

## 复杂度

- 时间复杂度：O(log n)
- 空间复杂度：O(1)

## 心得

1. 这题是普通闭区间二分，不是边界二分。
2. `guess(num) == 1` 表示猜小了，要往右找。
3. `guess(num) == -1` 表示猜大了，要往左找。
4. 闭区间 `[lower, upper]` 用 `while lower <= upper`。
5. 每次排除 `num` 本身，所以写 `lower = num + 1` 或 `upper = num - 1`。
