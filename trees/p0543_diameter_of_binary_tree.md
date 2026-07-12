# 543. Diameter of Binary Tree

## 题目

给定一棵二叉树，返回树的直径。

直径是任意两个节点之间最长路径的长度。这条路径不一定经过整棵树的根节点。

题目中的长度按边数计算。

例如：

```text
        1
       / \
      2   3
     / \
    4   5
```

最长路径可以是：

```text
4 -> 2 -> 1 -> 3
```

这条路径经过 3 条边，所以答案是 `3`。

## 思考顺序

### 1. `dfs(node)` 返回什么

定义：

```text
dfs(node) 返回从 node 向下走到最远叶子时包含的节点数量。
```

也就是以 `node` 为根的子树深度。

这个返回值不是整棵子树的直径，而是父节点还能继续使用的单边深度。

### 2. 空节点返回什么

空树不包含节点：

```python
if not node:
    return 0
```

### 3. 左右子树返回什么

```python
left_depth = dfs(node.left)
right_depth = dfs(node.right)
```

分别表示从左孩子和右孩子向下能够延伸的最大节点数。

### 4. 当前节点如何更新直径

如果一条路径经过当前节点，它可以由下面两部分组成：

```text
左子树最深路径 -> 当前节点 -> 右子树最深路径
```

所以经过当前节点的直径候选值是：

```python
left_depth + right_depth
```

用它更新整棵树中见过的最大直径：

```python
self.ans = max(self.ans, left_depth + right_depth)
```

### 5. 当前节点返回什么给父节点

父节点向下延伸的路径不能在当前节点同时分叉到左右两边，只能选择较深的一侧：

```python
return 1 + max(left_depth, right_depth)
```

这里的 `1` 表示当前节点自己。

## 代码

```python
class Solution:
    def diameterOfBinaryTree(self, root: TreeNode | None) -> int:
        self.ans = 0

        def dfs(node):
            if not node:
                return 0

            left_depth = dfs(node.left)
            right_depth = dfs(node.right)

            self.ans = max(self.ans, left_depth + right_depth)

            return 1 + max(left_depth, right_depth)

        dfs(root)
        return self.ans
```

## 为什么直径是 `left_depth + right_depth`

这里最容易混淆节点数和边数。

假设：

```text
left_depth = 2
right_depth = 1
```

左侧最深路径可能是：

```text
当前节点 -> 左孩子 -> 左侧叶子
```

从当前节点出发，左侧贡献 2 条边。虽然 `left_depth` 在左子树内部表示 2 个节点，但从当前节点连接到这些节点时，边数也正好是 2。

右侧同理贡献 1 条边。

所以经过当前节点的路径长度是：

```text
2 + 1 = 3 条边
```

不需要再加 `1`。如果写成：

```python
left_depth + right_depth + 1
```

算出来的是路径上的节点数量，不是题目要求的边数。

## 为什么 `dfs` 不能返回直径

经过当前节点的直径可以同时使用左右两边：

```text
左侧最深路径 + 右侧最深路径
```

但是当路径继续返回给父节点时，不能把两边一起带上去，否则路径会在当前节点产生分叉，不再是一条简单路径。

所以必须区分两个状态：

```text
self.ans         当前见过的最大直径，可以同时使用左右两边。
dfs(node) 返回值  交给父节点的单边最大深度，只能选择一边。
```

这是本题最重要的思维。

## 为什么需要全局答案

直径不一定经过整棵树的根节点。

例如某棵树的左子树内部非常深，而根节点的右子树很浅，最长路径可能完全位于左子树内部。

因此 DFS 经过每个节点时，都要计算一次：

```python
left_depth + right_depth
```

并用 `self.ans` 保留所有节点中的最大值。

`self.ans` 必须在每次调用主函数时重新初始化：

```python
self.ans = 0
```

否则复用同一个 `Solution` 对象时，可能残留上一次调用的答案。

## 为什么是后序遍历

当前节点必须先知道左右子树的深度，才能：

1. 更新经过当前节点的直径。
2. 计算返回给父节点的单边深度。

代码顺序是：

```text
左子树 -> 右子树 -> 当前节点
```

所以这是后序、自底向上的递归。

## 与 104 最大深度的关系

104 的核心返回值是：

```python
return 1 + max(left_depth, right_depth)
```

543 完全复用了这段深度计算，只是在返回之前多做了一件事：

```python
self.ans = max(self.ans, left_depth + right_depth)
```

可以理解为：

```text
543 = 104 的深度递归 + 每个节点处更新一次直径。
```

## 递归展开示例

对于：

```text
        1
       / \
      2   3
     / \
    4   5
```

在叶子节点 `4`：

```text
left_depth = 0
right_depth = 0
直径候选 = 0
返回深度 = 1
```

在节点 `2`：

```text
left_depth = 1
right_depth = 1
直径候选 = 2
返回深度 = 2
```

在根节点 `1`：

```text
left_depth = 2
right_depth = 1
直径候选 = 3
返回深度 = 3
```

最终全局最大直径是 `3`。

## 常见错误

### 认为直径一定经过根节点

只在根节点计算一次左右深度会漏掉完全位于某棵子树内部的最长路径。

应该在每个节点都更新一次全局答案。

### 给直径额外加 `1`

错误：

```python
self.ans = max(self.ans, left_depth + right_depth + 1)
```

这计算的是路径节点数。本题要求边数，所以不加 `1`。

### 把左右深度之和返回给父节点

错误：

```python
return 1 + left_depth + right_depth
```

返回给父节点的路径不能分叉，只能选择左右较深的一侧。

正确：

```python
return 1 + max(left_depth, right_depth)
```

### 忘记初始化全局答案

每次进入 `diameterOfBinaryTree` 都要执行：

```python
self.ans = 0
```

## 复杂度

时间复杂度：O(n)，每个节点访问一次。

辅助空间复杂度：O(h)，`h` 是树高，对应递归调用栈。

- 平衡树中约为 O(log n)。
- 树退化成链表时最坏为 O(n)。

## 心得

1. 当前节点可以用左右两边更新全局答案，但返回给父节点时只能选择一边。
2. 树题中必须分别说明“递归函数返回什么”和“最终答案是什么”，它们不一定相同。
3. 最大深度按节点向下递归，直径按边计数，因此候选直径是 `left_depth + right_depth`，不需要额外加 `1`。
4. 当答案可能出现在任意子树内部时，可以在后序遍历每个节点时更新全局最大值。
