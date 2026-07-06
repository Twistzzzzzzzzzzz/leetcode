# 74. Search a 2D Matrix

## 题目

给定一个二维矩阵 `matrix` 和目标值 `target`，判断 `target` 是否存在于矩阵中。

矩阵满足：

1. 每一行从左到右递增。
2. 每一行的第一个数大于上一行的最后一个数。

这意味着整个矩阵从左到右、从上到下可以看成一个整体有序的一维数组。

## 思路一：两次二分

你的写法是两次二分：

1. 先根据每一行的第一个元素，找到 `target` 可能在哪一行。
2. 再在这一行里做普通二分。

第一段二分相当于找：

```text
最后一个 matrix[row][0] <= target 的 row
```

如果 `target` 比第一行第一个元素还小，那么候选行不存在，直接返回 `False`。

找到候选行之后，再在这一行里找 `target`。

## 代码：两次二分

```python
class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        row_left = 0
        row_right = len(matrix)

        while row_left < row_right:
            row_mid = (row_left + row_right) // 2

            if target > matrix[row_mid][0]:
                row_left = row_mid + 1
            elif target < matrix[row_mid][0]:
                row_right = row_mid
            else:
                return True

        row = row_left - 1
        if row < 0:
            return False

        col_left = 0
        col_right = len(matrix[0]) - 1

        while col_left <= col_right:
            col_mid = (col_left + col_right) // 2

            if target > matrix[row][col_mid]:
                col_left = col_mid + 1
            elif target < matrix[row][col_mid]:
                col_right = col_mid - 1
            else:
                return True

        return False
```

## 为什么第一段结束后要 `row_left - 1`

第一段二分中：

```python
row_right = len(matrix)
while row_left < row_right:
```

这是左闭右开区间。

循环结束时，`row_left` 指向的是：

```text
第一个 matrix[row][0] > target 的行
```

所以真正可能包含 `target` 的行是它前一行：

```python
row = row_left - 1
```

如果 `row < 0`，说明 `target` 比所有行的第一个元素都小，不可能存在。

## 思路二：把矩阵看成一维数组

因为这题的矩阵整体有序，也可以把它看成长度为：

```python
rows * cols
```

的一维数组。

一维下标 `mid` 映射回二维坐标：

```python
row = mid // cols
col = mid % cols
```

然后直接做普通二分。

## 代码：一维映射

```python
class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        rows = len(matrix)
        cols = len(matrix[0])
        left = 0
        right = rows * cols - 1

        while left <= right:
            mid = (left + right) // 2
            row = mid // cols
            col = mid % cols
            value = matrix[row][col]

            if value == target:
                return True
            if value < target:
                left = mid + 1
            else:
                right = mid - 1

        return False
```

## 复杂度

两次二分：

- 时间复杂度：O(log m + log n)
- 空间复杂度：O(1)

一维映射二分：

- 时间复杂度：O(log(m * n))
- 空间复杂度：O(1)

两者本质复杂度非常接近。

## 心得

1. 这题可以先定位行，再在行内二分。
2. 第一段二分是在找“最后一个行首小于等于 `target` 的行”。
3. 左闭右开写法结束后，常常需要看 `left` 指向的是第一个不满足还是第一个满足，再决定是否要 `left - 1`。
4. 如果矩阵整体有序，可以把二维矩阵当成一维数组二分。
5. 一维下标转二维坐标：`row = mid // cols`，`col = mid % cols`。
