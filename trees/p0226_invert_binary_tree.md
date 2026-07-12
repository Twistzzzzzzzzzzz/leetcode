# 226. Invert Binary Tree

## 题目

给定一棵二叉树的根节点 `root`，交换树中每个节点的左右子树，并返回翻转后的根节点。

例如：

```text
翻转前：                 翻转后：

        4                       4
       / \                     / \
      2   7                   7   2
     / \ / \                 / \ / \
    1  3 6  9               9  6 3  1
```

## 思路

翻转整棵树可以拆成两个步骤：

1. 交换当前节点的左孩子和右孩子。
2. 对交换后的左右子树执行相同操作。

定义递归函数：

```text
invert(node) 负责原地翻转以 node 为根的整棵子树。
```

空节点没有左右孩子，直接结束：

```python
if not node:
    return
```

交换当前节点：

```python
node.left, node.right = node.right, node.left
```

然后继续翻转两个孩子：

```python
invert(node.left)
invert(node.right)
```

## 代码

```python
class Solution:
    def invertTree(self, root: TreeNode | None) -> TreeNode | None:
        def invert(node):
            if not node:
                return

            node.left, node.right = node.right, node.left

            invert(node.left)
            invert(node.right)

        invert(root)
        return root
```

## 为什么内部函数不需要返回节点

这份写法直接修改原来的节点：

```python
node.left, node.right = node.right, node.left
```

也就是说，`invert(node)` 的职责是“完成修改”，而不是“创建并返回一棵新树”。

因此内部函数可以没有显式返回值：

```python
def invert(node) -> None:
```

外层调用完成后，原来的 `root` 已经指向翻转后的整棵树，所以最后返回：

```python
return root
```

## 为什么交换后再递归没有问题

交换完成后：

```text
原来的右子树来到了左边。
原来的左子树来到了右边。
```

接下来分别调用：

```python
invert(node.left)
invert(node.right)
```

两棵子树仍然都会被处理，只是位置已经互换，因此不会遗漏。

这份代码先处理当前节点，再进入左右子树，所以属于前序 DFS 思路。

也可以先递归翻转原来的左右子树，最后再交换，这会形成后序写法，同样能够得到正确答案。

## 临时变量与元组交换

你的原始写法：

```python
temp = node.left
node.left = node.right
node.right = temp
```

完全正确。

Python 还可以简写为：

```python
node.left, node.right = node.right, node.left
```

右侧会先取出原来的两个引用，再分别赋给左侧，因此不会因为第一次赋值而丢失原来的左子树。

## 复杂度

时间复杂度：O(n)，每个节点交换一次。

辅助空间复杂度：O(h)，`h` 是树高，对应递归调用栈。

- 平衡树中约为 O(log n)。
- 树退化成链表时最坏为 O(n)。

## 心得

1. 树的整体操作经常可以拆成“处理当前节点，再递归处理左右子树”。
2. 这题是原地修改节点关系，内部递归不需要构造或返回一棵新树。
3. 翻转后根节点仍然是原来的根节点，只是每一层的左右孩子都交换了，所以最终返回 `root`。
4. 交换左右引用可以用临时变量，也可以使用 Python 的元组交换。
5. 判断遍历顺序要看当前节点的处理位置：这里先交换再递归，因此是前序思想。
