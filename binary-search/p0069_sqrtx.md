# 69. Sqrt(x)

## 题目

给定一个非负整数 `x`，返回 `x` 的整数平方根。

整数平方根的意思是：

```text
floor(sqrt(x))
```

也就是不超过真实平方根的最大整数。

## 思路

这题可以转化成：

```text
找最大的 mid，使得 mid * mid <= x。
```

所以它是“最大可行答案”二分。

## 推理过程

1. 要返回整数平方根，也就是 `floor(sqrt(x))`。
2. 等价于找最大的 `mid`，使得 `mid * mid <= x`。
3. 所以这是“最大可行答案”二分。
4. `check(mid) = mid * mid <= x`。
5. `check(mid)` 为 `True`，说明 `mid` 可行，要往右找：

```python
left = mid
```

6. `check(mid)` 为 `False`，说明 `mid` 太大：

```python
right = mid - 1
```

7. 因为有 `left = mid`，必须使用右中位数：

```python
mid = (left + right + 1) // 2
```

## 核心记忆

```text
找最大可行答案：
while left < right
mid 取右中位数
True 时 left = mid
False 时 right = mid - 1
```

## 代码

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        left = 0
        right = x

        while left < right:
            mid = (left + right + 1) // 2

            if mid * mid <= x:
                left = mid
            else:
                right = mid - 1

        return left
```

## 为什么要用右中位数

如果找最大可行答案时写普通中位数：

```python
mid = (left + right) // 2
```

并且在可行时写：

```python
left = mid
```

当：

```python
left + 1 == right
```

会得到：

```python
mid == left
```

这时 `left = mid` 不会让边界变化，循环可能卡住。

所以要写：

```python
mid = (left + right + 1) // 2
```

这样当只剩两个候选值时，`mid` 会取右边那个值，保证边界继续收缩。

## 复杂度

- 时间复杂度：O(log x)
- 空间复杂度：O(1)

## 心得

1. 整数平方根可以理解成“最大可行答案”。
2. 可行条件是 `mid * mid <= x`。
3. 可行时继续往右找，不可行时往左收缩。
4. 只要代码里有 `left = mid`，就要警惕死循环。
5. 找最大可行答案时，使用右中位数：`(left + right + 1) // 2`。
