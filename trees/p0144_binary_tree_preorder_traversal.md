# 144. Binary Tree Preorder Traversal

## 题目

给定一棵二叉树的根节点 `root`，返回它的前序遍历结果。

前序遍历的顺序是：

```text
当前节点 -> 左子树 -> 右子树
```

对于：

```text
        1
       / \
      2   3
     / \   \
    4   5   6
```

前序遍历结果为：

```text
[1, 2, 4, 5, 3, 6]
```

## 思路

定义：

```text
dfs(node) 负责按照前序顺序遍历以 node 为根的整棵子树。
```

到达一个节点后，先把当前值加入答案，再递归处理左右子树：

```python
ans.append(node.val)
dfs(node.left)
dfs(node.right)
```

因为当前节点在左右子树之前处理，所以叫前序遍历。

## 代码

```python
class Solution:
    def preorderTraversal(self, root: TreeNode | None) -> list[int]:
        ans = []

        def dfs(node):
            if not node:
                return

            ans.append(node.val)
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ans
```

## 前序遍历适合什么题

前序遍历会先处理父节点，再进入左右孩子，因此适合自顶向下的任务，例如：

- 记录从根到当前节点的路径。
- 把父节点状态传给孩子。
- 复制或序列化二叉树。
- 在进入子树前先处理当前节点。

## 复杂度

时间复杂度：O(n)。

辅助空间复杂度：O(h)，`h` 是树高，对应递归调用栈；最坏为 O(n)。

## 心得

1. 前序的“前”表示当前节点在左右子树之前处理。
2. 前序顺序固定为“根、左、右”。
3. 代码框架和中序、后序完全相同，只是 `ans.append(node.val)` 放在最前面。
4. 当前节点的信息需要先传给孩子时，可以优先想到前序或自顶向下 DFS。
