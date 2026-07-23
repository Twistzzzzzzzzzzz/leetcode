# 463. Island Perimeter

## 题目

`grid` 是一个由 `0` 和 `1` 组成的二维网格：

- `0` 表示水；
- `1` 表示陆地；
- 陆地格只会通过上、下、左、右四个方向相邻。

计算岛屿的周长。

## 你的思路

遍历每个陆地格，并分别检查它的四条边：

```text
相邻位置超出网格 -> 这一条边属于周长
相邻位置是水     -> 这一条边属于周长
相邻位置是陆地   -> 这是内部公共边，不计入周长
```

因此，每发现一条直接接触水或网格外部的陆地边，就给答案加 `1`。

## 为什么你的代码是正确的

一个陆地格最多贡献四条周长边。

以它的上边为例：

```python
if row == 0 or grid[row - 1][col] == 0:
    perimeter += 1
```

有两种情况会让上边暴露：

1. `row == 0`：当前格位于第一行，上方已经超出网格；
2. 上方相邻格是水。

其余三个方向完全相同。

## 整理后的显式写法

```python
class Solution:
    def islandPerimeter(self, grid: list[list[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])
        perimeter = 0

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 0:
                    continue

                if row == 0 or grid[row - 1][col] == 0:
                    perimeter += 1
                if row == rows - 1 or grid[row + 1][col] == 0:
                    perimeter += 1
                if col == 0 or grid[row][col - 1] == 0:
                    perimeter += 1
                if col == cols - 1 or grid[row][col + 1] == 0:
                    perimeter += 1

        return perimeter
```

你的原代码写了：

```python
row == 0 or (row > 0 and grid[row - 1][col] == 0)
```

可以简化为：

```python
row == 0 or grid[row - 1][col] == 0
```

因为 Python 的 `or` 会短路：

- 如果 `row == 0` 已经为 `True`；
- Python 就不会继续访问 `grid[row - 1][col]`。

另外，`rows = len(grid)` 表示行数，比用 `len(grid) - 1` 表示最后一个下标更容易理解。

## Graph 视角

这是一道网格图题：

```text
每个格子可以看作一个节点
上下左右关系可以看作边
```

不过本题并不要求寻找：

- 某个节点是否可达；
- 有多少个连通分量；
- 一整片区域中有哪些格子。

我们只需要检查每个陆地格与四个相邻位置之间的关系，所以不需要 DFS、BFS 或 `visited`。

这说明：

```text
网格题可以用图来建模，但不一定需要图遍历。
```

## 四方向模板写法

以后网格题经常要重复访问上下左右，可以把方向统一保存起来：

```python
directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]
```

然后对每块陆地检查四个相邻位置：

```python
for row_change, col_change in directions:
    next_row = row + row_change
    next_col = col + col_change

    is_outside = (
        next_row < 0
        or next_row >= rows
        or next_col < 0
        or next_col >= cols
    )

    if is_outside or grid[next_row][next_col] == 0:
        perimeter += 1
```

这里同样利用了短路求值：

```python
if is_outside or grid[next_row][next_col] == 0:
```

如果相邻坐标已经越界，Python 不会再访问网格，因此不会产生下标错误。

## 另一种计数理解

每个陆地格最初贡献四条边：

```text
周长 = 陆地格数量 * 4
```

如果两个陆地格相邻，它们之间有一条公共边。

这条公共边曾被两个格子各计算一次，因此需要减去 `2`：

```text
周长 = 陆地格数量 * 4 - 相邻陆地对数量 * 2
```

扫描时只检查上方和左方，就能保证每对相邻陆地只计算一次。

这个公式和逐边检查本质相同；当前写法更直接，也更贴近题意。

## 复杂度

设网格有 `m` 行、`n` 列：

- 时间复杂度：O(mn)
- 额外空间复杂度：O(1)

虽然每个陆地格会检查四个方向，但 `4` 是常数，因此总时间仍然是 O(mn)。

## 易错点

### 把行数写成最后一个下标

```python
rows = len(grid) - 1
```

这样并非错误，但变量实际表示的是 `last_row_index`，容易在循环和边界判断中混淆。

更推荐：

```python
rows = len(grid)
```

最后一行下标再写成：

```python
rows - 1
```

### 越界后仍访问网格

边界判断必须放在访问相邻格之前，并利用 `or` 的短路特性。

### 相邻陆地之间的公共边也计入周长

只有相邻位置是水或越界时才加 `1`。陆地与陆地之间的边位于岛屿内部。

### 看到网格就强行使用 DFS

先问清楚题目是否真的需要搜索整个连通区域。本题直接遍历并统计每条暴露边即可。

## 心得

1. 网格可以看作图，但 Graph 题不一定都要使用 DFS、BFS 或 `visited`。
2. 对每块陆地而言，相邻位置越界或是水，对应的那一条边就属于周长。
3. 网格四方向问题可以先写四个显式判断；熟悉后再整理成 `directions` 模板。
4. 边界判断与网格访问放在同一个 `or` 中时，可以利用短路求值避免越界。
5. `rows`、`cols` 最好表示行数和列数，不要同时拿它们表示最后一个合法下标。
