# 427. Construct Quad Tree

## 题目

给定一个只包含 0 和 1 的正方形矩阵，将它构造成四叉树 Quad Tree。

每个节点有两种情况：

- 当前区域的值全部相同：创建叶子节点。
- 当前区域存在不同值：创建非叶子节点，并把区域平均分成四块继续递归。

## 这题不是普通二叉树遍历

这题仍然属于树结构，但核心不是遍历一棵已有的树，而是根据矩阵递归构造一棵新树。

它更接近分治 Divide and Conquer：

```text
一个大正方形
-> 判断能否直接表示
-> 不能就拆成四个更小的正方形
-> 分别递归构造
-> 把四棵子树接到当前节点
```

## 递归函数的职责

定义：

```python
build(row, col, size)
```

表示：

> 根据左上角为 `(row, col)`、边长为 `size` 的正方形区域，构造并返回对应的四叉树根节点。

只用三个参数，就能唯一确定当前区域：

```text
行范围：[row, row + size)
列范围：[col, col + size)
```

## 第一步：判断区域是否一致

先记录左上角的值：

```python
first_value = grid[row][col]
```

再遍历当前区域。如果所有格子都等于 `first_value`，整个区域可以压缩成一个叶子节点：

```python
return Node(bool(first_value), True)
```

这里的终止条件不只是：

```python
size == 1
```

即使区域很大，只要所有值相同，也应该立即停止继续划分。

## 第二步：划分四个子区域

如果当前区域不一致：

```python
half = size // 2
```

四个区域的左上角分别是：

| 区域 | `row` | `col` |
| --- | --- | --- |
| topLeft | `row` | `col` |
| topRight | `row` | `col + half` |
| bottomLeft | `row + half` | `col` |
| bottomRight | `row + half` | `col + half` |

每个子区域的边长都是 `half`：

```python
top_left = build(row, col, half)
top_right = build(row, col + half, half)
bottom_left = build(row + half, col, half)
bottom_right = build(row + half, col + half, half)
```

画成坐标变化就是：

```text
(row, col)                 (row, col + half)
        topLeft | topRight
        --------+---------
      bottomLeft| bottomRight
(row + half, col)          (row + half, col + half)
```

## 第三步：创建非叶子节点

四棵子树构造完成后，把它们接到当前节点：

```python
return Node(
    True,
    False,
    top_left,
    top_right,
    bottom_left,
    bottom_right,
)
```

对于非叶子节点，题目不会使用 `val` 判断答案，所以 `val` 写 `True` 或 `False` 都可以。真正重要的是：

```python
isLeaf == False
```

以及四个孩子是否正确。

## 代码

```python
class Solution:
    def construct(self, grid):
        n = len(grid)

        def build(row, col, size):
            first_value = grid[row][col]
            is_same = True

            for i in range(row, row + size):
                for j in range(col, col + size):
                    if grid[i][j] != first_value:
                        is_same = False
                        break
                if not is_same:
                    break

            if is_same:
                return Node(bool(first_value), True)

            half = size // 2

            top_left = build(row, col, half)
            top_right = build(row, col + half, half)
            bottom_left = build(row + half, col, half)
            bottom_right = build(row + half, col + half, half)

            return Node(
                True,
                False,
                top_left,
                top_right,
                bottom_left,
                bottom_right,
            )

        return build(0, 0, n)
```

## 为什么两个 `break` 都需要

内层循环发现不同值后：

```python
break
```

只会退出列循环，外层的行循环仍然可能继续。

所以还要在外层判断：

```python
if not is_same:
    break
```

这样一旦确定区域不一致，就不用继续扫描剩余格子。

## 复杂度

当前写法在每个递归节点都重新扫描对应区域。

最坏情况下，每一层所有区域合计会扫描 O(n²) 个格子，而树最多有 O(log n) 层：

- 时间复杂度：O(n² log n)
- 递归调用栈：O(log n)
- 四叉树本身最坏需要 O(n²) 个节点

这里通常把返回结果占用的空间与额外辅助空间分开讨论。

## 可选优化：二维前缀和

如果先构造二维前缀和，就能在 O(1) 时间得到任意区域内 1 的数量 `region_sum`。

对于边长为 `size` 的区域：

```text
region_sum == 0          -> 全是 0
region_sum == size²      -> 全是 1
其他情况                 -> 需要继续划分
```

这样无需在每个递归节点重新扫描区域，总体可以降到 O(n²)。不过第一次学习这题时，先掌握当前清晰的扫描 + 分治写法更重要。

## 心得

1. 看到“把一个大区域不断等分，并根据子区域构造结果”，可以考虑分治递归。
2. 递归函数应先明确当前区域的表示方式；这里使用左上角坐标加边长。
3. 区域值全部相同时立即创建叶子节点，不必一直拆到单个格子。
4. 区域不一致时，把边长减半，并正确计算四个子区域的左上角坐标。
5. 递归构造树的常见结构是：递归得到孩子节点，再由当前层把孩子接到新节点上并返回。
