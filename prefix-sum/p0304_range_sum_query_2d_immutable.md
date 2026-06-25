# 304. Range Sum Query 2D - Immutable

## 题目

给定一个不可变的二维矩阵 `matrix`。

需要多次调用：

```python
sumRegion(row1, col1, row2, col2)
```

返回左上角 `(row1, col1)` 到右下角 `(row2, col2)` 这个矩形区域内所有数字的和。

## 如何识别这类题

看到这些关键词时，可以优先想到前缀和：

- 多次查询区间和
- 多次查询矩形区域和
- 查询要求很快，例如 O(1)
- 原数组或矩阵不修改，题目里出现 `Immutable`

脑海里的第一反应应该是：

```text
查询阶段要快，就把重复计算提前放到构造阶段完成。
```

一维数组区间和可以用一维前缀和。

二维矩阵区域和可以用二维前缀和。

如果题目还要求频繁更新元素，就不能只用普通前缀和，后面可能要考虑树状数组或线段树。

## 思路

构造一个多一圈 padding 的二维前缀和矩阵 `prefix`。

`prefix[row + 1][col + 1]` 表示：

```text
原矩阵中，从 (0, 0) 到 (row, col) 这个矩形的总和
```

也就是说，每个位置都提前保存一个左上角矩形的和。

构造公式：

```python
prefix[row + 1][col + 1] = (
    matrix[row][col]
    + prefix[row][col + 1]
    + prefix[row + 1][col]
    - prefix[row][col]
)
```

含义是：

- 当前格子本身：`matrix[row][col]`
- 加上上方区域：`prefix[row][col + 1]`
- 加上左方区域：`prefix[row + 1][col]`
- 减掉重复加了一次的左上角区域：`prefix[row][col]`

## 为什么要加一圈 Padding

外圈加一圈 `0` 可以极大减少边界判断。

如果没有 padding，第一行、第一列要单独处理：

```text
row == 0 怎么办？
col == 0 怎么办？
左上角不存在怎么办？
```

有了 padding 后，所有位置都可以使用同一套公式。

这也是这题最值得记住的技巧之一。

## 查询公式

要求：

```text
(row1, col1) 到 (row2, col2)
```

可以用大矩形减掉不需要的部分：

```python
prefix[row2 + 1][col2 + 1]
- prefix[row1][col2 + 1]
- prefix[row2 + 1][col1]
+ prefix[row1][col1]
```

含义是：

1. 先拿到从左上角到右下角的大矩形。
2. 减掉目标区域上方的矩形。
3. 减掉目标区域左边的矩形。
4. 左上角被减了两次，所以再加回来一次。

## 代码

```python
class NumMatrix:
    def __init__(self, matrix: list[list[int]]) -> None:
        height = len(matrix)
        width = len(matrix[0])
        self.prefix = [[0] * (width + 1) for _ in range(height + 1)]

        for row in range(height):
            for col in range(width):
                self.prefix[row + 1][col + 1] = (
                    matrix[row][col]
                    + self.prefix[row][col + 1]
                    + self.prefix[row + 1][col]
                    - self.prefix[row][col]
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self.prefix[row2 + 1][col2 + 1]
            - self.prefix[row1][col2 + 1]
            - self.prefix[row2 + 1][col1]
            + self.prefix[row1][col1]
        )
```

## 复杂度

构造阶段：

- 时间复杂度：O(m * n)
- 空间复杂度：O(m * n)

查询阶段：

- 时间复杂度：O(1)
- 空间复杂度：O(1)

这里 `m` 是行数，`n` 是列数。

## 心得

1. 这是最适合重做的前缀和题之一。
2. 看到查询需要 O(1)，就要想到在构造阶段提前保存可复用的结果。
3. 每个格子都复用上方、左方、左上方的数据，可以极大减少重复计算。
4. 在外圈加一个全为 `0` 的 padding，可以极大减少边界问题。
5. 二维前缀和的查询公式本质是“总矩形 - 上方矩形 - 左方矩形 + 左上角重复减掉的矩形”。
