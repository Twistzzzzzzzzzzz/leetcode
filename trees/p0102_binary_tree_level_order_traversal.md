# 102. Binary Tree Level Order Traversal

## 题目

给定一棵二叉树的根节点 `root`，按从上到下、从左到右的顺序返回每一层的节点值。

例如：

```text
        3
       / \
      9   20
         /  \
        15   7
```

返回：

```python
[[3], [9, 20], [15, 7]]
```

## 先修正一个重要印象

树题不等于递归题。

更准确的关系是：

```text
树：数据结构
DFS / BFS：遍历策略
递归 / while：实现方式
```

树既可以使用 DFS，也可以使用 BFS。

DFS 既可以用递归实现，也可以用 `while + stack` 实现。

BFS 通常使用 `while + queue` 实现。

```text
Tree
├── DFS
│   ├── 递归
│   └── stack + while
└── BFS
    └── queue + while
```

因此看到树题时，不要先问“递归还是 while”，应该先问题目要求什么访问顺序。

## 为什么这题使用 BFS

102 明确要求：

```text
第 1 层 -> 第 2 层 -> 第 3 层
```

这种按距离从近到远、一层一层访问节点的策略叫 BFS，广度优先搜索。

BFS 的核心数据结构是先进先出的队列 FIFO：

```text
最早进入队列的节点最先被处理。
```

## 队列如何保证层序

假设：

```text
    3
   / \
  9   20
```

初始只放入根节点：

```text
queue = [3]
```

从队头取出 `3`，再把它的孩子加入队尾：

```text
queue = [9, 20]
```

下一次先取出 `9`，再取出 `20`。因此同一层会按照从左到右的顺序处理，下一层则排在当前层后面。

对应操作：

```python
node = queue.popleft()
queue.append(node.left)
queue.append(node.right)
```

## 为什么使用 `deque`

Python 中最适合实现队列的是：

```python
from collections import deque
```

`deque` 是双端队列，可以高效地从两端添加或删除：

```python
queue.append(node)   # 从右侧加入，O(1)
queue.popleft()      # 从左侧取出，O(1)
```

普通列表也可以写：

```python
node = queue.pop(0)
```

但 `list.pop(0)` 是 O(n)，因为删除第一个元素后，后面的所有元素都要整体向前移动。

| 操作 | `list` | `deque` |
| --- | --- | --- |
| 尾部加入 | `append()`，O(1) | `append()`，O(1) |
| 尾部删除 | `pop()`，O(1) | `pop()`，O(1) |
| 头部删除 | `pop(0)`，O(n) | `popleft()`，O(1) |
| 随机下标访问 | 适合 | 不适合 |
| 常见用途 | 数组、栈 | 队列、BFS |

核心记忆：

```text
DFS 迭代通常用 list 当 stack。
BFS 通常用 deque 当 queue。
```

## 为什么要保存 `level_size`

每轮 `while` 开始时：

```python
level_size = len(queue)
```

此时队列中恰好是当前层所有待处理节点。

然后：

```python
for _ in range(level_size):
```

只处理当前层固定数量的节点。

处理过程中会把孩子加入队尾，但这些孩子属于下一层，不会被当前这轮 `for` 提前处理。

如果不先锁定当前层大小，队列长度会随着孩子加入而变化，不同层就可能混在一起。

## 空树为什么需要提前返回

原始代码直接写：

```python
queue = deque([root])
```

如果 `root` 是 `None`，队列会变成：

```text
deque([None])
```

它并不是空队列，所以 `while queue` 仍然成立。

随后取出的 `node` 是 `None`：

```python
level.append(node.val)
```

这里会报错。

因此创建队列前先处理空树：

```python
if not root:
    return []
```

## 代码

```python
from collections import deque


class Solution:
    def levelOrder(self, root):
        if not root:
            return []

        ans = []
        queue = deque([root])

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

            ans.append(level)

        return ans
```

## 每个变量表示什么

```text
queue       还没有处理的节点，按进入先后排列
level_size  当前层一共有多少个节点
level       当前层的节点值
ans         所有已经处理完成的层
```

每轮流程：

```text
锁定当前层大小
-> 依次取出当前层节点
-> 把下一层孩子加入队尾
-> 保存完整的当前层
```

## 能不能使用递归

可以使用 DFS，并额外记录节点深度：

```python
class Solution:
    def levelOrder(self, root):
        ans = []

        def dfs(node, depth):
            if not node:
                return

            if depth == len(ans):
                ans.append([])

            ans[depth].append(node.val)

            dfs(node.left, depth + 1)
            dfs(node.right, depth + 1)

        dfs(root, 0)
        return ans
```

这份代码虽然最终也得到分层结果，但实际访问顺序仍然是 DFS：先深入左子树，再返回处理右子树。

它只是利用 `depth` 把访问到的节点放进对应层。

因此：

```text
递归也能得到答案。
BFS 更直接符合“逐层访问”的题意。
第一次学习层序遍历时，应优先掌握 BFS + deque 模板。
```

## 不用 `deque` 的另一种 O(n) 写法

可以使用列表加读取下标，避免 `pop(0)`：

```python
queue = [root]
index = 0

while index < len(queue):
    node = queue[index]
    index += 1

    if node.left:
        queue.append(node.left)
    if node.right:
        queue.append(node.right)
```

不过如果还要精确分层，需要另外记录每层边界。标准的 `deque + popleft()` 更直观。

## 看到树题时如何选择

优先考虑 BFS 的信号：

- 每一层
- 层序遍历
- 第 `k` 层
- 离根最近
- 最短路径
- 右视图或每层最大值

优先考虑 DFS 的信号：

- 子树
- 深度或高度
- 左右子树返回值
- 根到叶路径
- 判断某棵子树

先选择遍历策略，再选择递归还是迭代实现。

## 常见错误

### 没有处理空树

`deque([None])` 不是空队列，必须提前返回 `[]`。

### 使用 `list.pop(0)`

逻辑正确，但每次头部删除是 O(n)，应优先使用 `deque.popleft()`。

### 没有锁定当前层大小

处理当前层时不断加入下一层节点，容易把多层放进同一个 `level`。

### 在循环外复用同一个 `level`

每一轮 `while` 都要创建新的：

```python
level = []
```

### 把递归和 DFS 当成同一个概念

DFS 是遍历策略；递归只是 DFS 的一种常见实现方式。

## 复杂度

时间复杂度：O(n)，每个节点入队和出队各一次。

辅助空间复杂度：O(w)，`w` 是树的最大宽度，也就是队列中最多同时保存的节点数。

返回结果本身需要 O(n) 空间。

## 心得

1. 树是数据结构，DFS/BFS 是遍历策略，递归/while 是实现方式，三者不能混为一谈。
2. 题目要求逐层处理时，优先想到 BFS + queue。
3. Python 中队列优先使用 `deque`，因为 `popleft()` 是 O(1)。
4. `level_size = len(queue)` 用来锁定当前层，下一层节点即使入队也不会被当前轮处理。
5. `deque([root])` 前必须检查空树，否则队列中会放入 `None`。
