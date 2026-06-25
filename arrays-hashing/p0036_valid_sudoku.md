# 36. Valid Sudoku

## 题目

判断一个 9x9 数独棋盘是否有效。

需要满足：

- 每一行不能有重复数字
- 每一列不能有重复数字
- 每一个 3x3 小宫格不能有重复数字

`.` 表示空格，不需要判断。

## 思路

这道题如果分开检查：

1. 检查所有行
2. 检查所有列
3. 检查所有 3x3 小宫格

会写出三套遍历逻辑。

更好的方式是：只遍历棋盘一次，同时维护三类集合。

```python
rows = [set() for _ in range(9)]
cols = [set() for _ in range(9)]
boxes = [set() for _ in range(9)]
```

每遇到一个数字 `value`，同时检查：

- 它是否已经出现在当前行
- 它是否已经出现在当前列
- 它是否已经出现在当前 3x3 小宫格

如果任意一个集合里已经有这个数字，说明数独无效。

## 为什么用集合

集合 `set` 的查找通常是 O(1)。

如果用列表，每次判断某个数字是否出现过需要 O(n)。

这题需要频繁判断重复，所以集合更合适。

## 小宫格编号

最巧妙的地方是这一行：

```python
box = (row // 3) * 3 + (col // 3)
```

它把 3x3 小宫格编号成 0 到 8。

可以先看行属于哪一组：

```text
row 0,1,2 -> row // 3 = 0
row 3,4,5 -> row // 3 = 1
row 6,7,8 -> row // 3 = 2
```

再看列属于哪一组：

```text
col 0,1,2 -> col // 3 = 0
col 3,4,5 -> col // 3 = 1
col 6,7,8 -> col // 3 = 2
```

所以：

```text
box = 宫格所在大行 * 3 + 宫格所在大列
```

例如：

```text
row = 4, col = 7
row // 3 = 1
col // 3 = 2
box = 1 * 3 + 2 = 5
```

这个位置属于第 5 个小宫格。

## 代码

```python
class Solution:
    def isValidSudoku(self, board: list[list[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        for row in range(9):
            for col in range(9):
                value = board[row][col]

                if value == ".":
                    continue

                box = (row // 3) * 3 + (col // 3)

                if value in rows[row] or value in cols[col] or value in boxes[box]:
                    return False

                rows[row].add(value)
                cols[col].add(value)
                boxes[box].add(value)

        return True
```

## 另一种 HashMap 写法

也可以把行、列、小宫格都做成 HashMap 的 key。

例如：

```python
seen = set()

for row in range(9):
    for col in range(9):
        value = board[row][col]

        if value == ".":
            continue

        row_key = ("row", row, value)
        col_key = ("col", col, value)
        box_key = ("box", row // 3, col // 3, value)
```

这种写法也很直观：只要同一个 key 出现第二次，就说明重复了。

## 复杂度

- 时间复杂度：O(1)
- 空间复杂度：O(1)

因为棋盘固定是 9x9。

如果把棋盘大小抽象成 n x n，则时间复杂度是 O(n²)。

## 心得

1. 依旧是把三次遍历变成一次遍历：一次性维护多个集合。
2. 集合的查找通常是 O(1)，列表查找是 O(n)，所以这里选择集合。
3. `box = (row // 3) * 3 + (col // 3)` 很巧妙，它把小宫格位置映射成 0 到 8 的编号。
4. 也可以用 HashMap / set，把行、列、小宫格都做成 key，这种写法也很直观。
5. 识别这类题时，如果题目要求同时满足多种“不重复”约束，可以考虑一次遍历，同时维护多个集合。
