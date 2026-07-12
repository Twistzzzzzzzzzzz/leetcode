# 94. Binary Tree Inorder Traversal

## 题目

给定一棵二叉树的根节点 `root`，返回它的中序遍历结果。

中序遍历的顺序是：

```text
左子树 -> 当前节点 -> 右子树
```

例如：

```text
        1
       / \
      2   3
     / \   \
    4   5   6
```

中序遍历结果为：

```text
[4, 2, 5, 1, 3, 6]
```

## 思路

定义：

```text
dfs(node) 负责按照中序顺序遍历以 node 为根的整棵子树。
```

对于每个节点依次执行：

1. 递归遍历左子树。
2. 把当前节点加入答案。
3. 递归遍历右子树。

空节点不需要加入答案，直接返回：

```python
if not node:
    return
```

## 代码

```python
class Solution:
    def inorderTraversal(self, root: TreeNode | None) -> list[int]:
        ans = []

        def dfs(node):
            if not node:
                return

            dfs(node.left)
            ans.append(node.val)
            dfs(node.right)

        dfs(root)
        return ans
```

## `ans` 为什么不需要 `nonlocal`

内部函数执行的是：

```python
ans.append(node.val)
```

这只是修改外层列表里的内容，没有让变量 `ans` 指向一个新列表，所以不需要声明 `nonlocal ans`。

如果在内部函数里写的是：

```python
ans = ans + [node.val]
```

这会重新给 `ans` 赋值，作用域规则就不同了。

## 三种遍历的关系

三种递归遍历的框架完全相同，区别只是处理当前节点的位置：

```text
前序：ans.append -> 左 -> 右
中序：左 -> ans.append -> 右
后序：左 -> 右 -> ans.append
```

这题把 `ans.append(node.val)` 放在两次递归之间，所以是中序遍历。

## 中序遍历和 BST

普通二叉树的中序结果不一定有序。

只有当题目明确说明这是一棵二叉搜索树 BST 时，中序遍历结果才会严格递增。这也是中序遍历在 BST 题中非常常见的原因。

## 复杂度

时间复杂度：O(n)，每个节点恰好访问一次。

辅助空间复杂度：O(h)，`h` 是树高，对应递归调用栈。

- 平衡树中约为 O(log n)。
- 树退化成链表时最坏为 O(n)。

如果把返回结果 `ans` 也算入空间，则还需要 O(n)。

## 心得

1. 树的递归遍历首先要写空节点终止条件。
2. 前序、中序、后序不需要背三套代码，只需要观察“处理当前节点”放在哪里。
3. 中序遍历就是：先完整处理左子树，再记录当前节点，最后处理右子树。
4. 不要看到中序遍历就认为结果有序，只有 BST 才有这个性质。
