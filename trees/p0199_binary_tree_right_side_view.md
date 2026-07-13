# 199. Binary Tree Right Side View

## 题目

给定一棵二叉树，想象自己站在树的右侧，按照从上到下的顺序返回能够看到的节点值。

## 识别题型

题目要求每一层选出一个节点，因此首先想到层序遍历：

```text
按层处理
-> BFS
-> queue
-> 每层开始时记录 level_size
```

从右侧看到的并不一定是某个节点的右孩子，而是这一层位置最靠右的节点。

例如一棵只有左孩子的树：

```text
    1
   /
  2
 /
3
```

右视图仍然是：

```text
[1, 2, 3]
```

所以不能只沿着 `root.right` 一直向下走。

## 原始思路

你的写法是正确的：先收集一整层，再取这一层的最后一个值。

```python
while queue:
    level = []
    level_size = len(queue)

    for _ in range(level_size):
        node = queue.popleft()
        level.append(node.val)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    ans.append(level[-1])
```

因为节点按照从左到右的顺序进入队列，所以每层最后处理的节点就是最右侧节点。

## 简化思路

题目只需要每层最右侧的一个值，并不需要保存整层结果。

在本层循环中，最后一次迭代满足：

```python
i == level_size - 1
```

因此可以直接把这个节点加入答案：

```python
for i in range(level_size):
    node = queue.popleft()

    if i == level_size - 1:
        ans.append(node.val)
```

这只是减少了临时的 `level` 列表。两种写法的总体时间和空间复杂度相同。

## 为什么要提前保存 `level_size`

进入一层时：

```python
level_size = len(queue)
```

此时队列里恰好是当前层的所有节点。

处理当前层时，又会把下一层的孩子加入队列。如果直接根据不断变化的 `len(queue)` 循环，当前层和下一层就可能混在一起。

所以 `level_size` 是当前层的固定边界。

## 入队顺序与取值位置必须配套

当前代码使用：

```python
先加入左孩子
再加入右孩子
```

因此当前层按照从左到右的顺序处理，应该取最后一个节点：

```python
if i == level_size - 1:
```

也可以先加入右孩子、再加入左孩子。那样每层第一个处理的才是最右侧节点，应改为：

```python
if i == 0:
```

所以不能孤立地背“取第一个”或“取最后一个”，需要先确认队列中的节点顺序。

## 代码

```python
from collections import deque


class Solution:
    def rightSideView(self, root):
        if not root:
            return []

        ans = []
        queue = deque([root])

        while queue:
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()

                if i == level_size - 1:
                    ans.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return ans
```

## DFS 写法

这题也可以使用 DFS：

1. 先访问右子树，再访问左子树。
2. 记录当前节点的深度。
3. 第一次到达某个深度时，当前节点就是这一层最右侧的节点。

```python
class Solution:
    def rightSideView(self, root):
        ans = []

        def dfs(node, depth):
            if not node:
                return

            if depth == len(ans):
                ans.append(node.val)

            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)

        dfs(root, 0)
        return ans
```

这里再次说明：树题不等于递归题。199 可以用 BFS，也可以用 DFS，只是 BFS 与“逐层取一个节点”的题意更直接对应。

## 复杂度

### BFS

- 时间复杂度：O(n)
- 空间复杂度：O(w)

`n` 是节点总数，`w` 是树的最大宽度。

### DFS

- 时间复杂度：O(n)
- 空间复杂度：O(h)

`h` 是树高，空间主要来自递归调用栈。

## 心得

1. 题目要求每一层选出一个节点，是 BFS 的明显信号。
2. 右视图不是只沿右孩子向下走，而是取每一层位置最靠右的节点。
3. 左孩子先入队、右孩子后入队时，每层最后处理的节点就是最右侧节点。
4. 只需要每层最后一个值时，可以直接判断 `i == level_size - 1`，不必保存整个 `level` 列表。
5. `level_size` 必须在处理当前层之前固定下来，避免把下一层节点混入当前层。
