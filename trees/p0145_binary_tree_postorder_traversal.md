# 145. Binary Tree Postorder Traversal

## 题目

给定一棵二叉树的根节点 `root`，返回它的后序遍历结果。

后序遍历的顺序是：

```text
左子树 -> 右子树 -> 当前节点
```

对于：

```text
        1
       / \
      2   3
     / \   \
    4   5   6
```

后序遍历结果为：

```text
[4, 5, 2, 6, 3, 1]
```

## 思路

定义：

```text
dfs(node) 负责按照后序顺序遍历以 node 为根的整棵子树。
```

先递归处理左右子树，等两个子问题都完成后，再记录当前节点：

```python
dfs(node.left)
dfs(node.right)
ans.append(node.val)
```

因为当前节点最后处理，所以叫后序遍历。

## 代码

```python
class Solution:
    def postorderTraversal(self, root: TreeNode | None) -> list[int]:
        ans = []

        def dfs(node):
            if not node:
                return

            dfs(node.left)
            dfs(node.right)
            ans.append(node.val)

        dfs(root)
        return ans
```

## 后序遍历适合什么题

后序遍历会先得到左右子树的信息，再计算当前节点，因此特别适合自底向上的任务，例如：

- 计算树的高度或最大深度。
- 判断二叉树是否平衡。
- 计算二叉树直径。
- 汇总左右子树的节点数或总和。
- 寻找普通二叉树的最近公共祖先。

很多题虽然没有要求输出后序序列，但只要代码结构是：

```python
left = dfs(node.left)
right = dfs(node.right)
return combine(left, right)
```

本质上仍然是后序遍历思想。

## 复杂度

时间复杂度：O(n)。

辅助空间复杂度：O(h)，`h` 是树高，对应递归调用栈；最坏为 O(n)。

## 心得

1. 后序的“后”表示当前节点在左右子树之后处理。
2. 后序顺序固定为“左、右、根”。
3. 当当前节点的答案依赖左右孩子返回的结果时，优先想到后序遍历。
4. 后序不仅是输出顺序，也是大量高度、平衡和直径问题背后的递归结构。
