# 450. Delete Node in a BST

## 题目

给定一棵二叉搜索树 BST 的根节点 `root` 和一个值 `key`，删除值等于 `key` 的节点，并返回删除后的根节点。

删除过程包含两个任务：

```text
利用 BST 性质找到目标节点。
找到后重新连接它的左右子树，使结果仍然是 BST。
```

## 递归函数的定义

定义：

```text
deleteNode(root, key) 返回删除 key 后，以 root 为起点的子树新根节点。
```

这个定义与 701. Insert into a Binary Search Tree 完全一致：递归函数返回“处理完成后的子树根节点”，父节点负责接回。

## 利用 BST 寻找目标

如果 `key` 小于当前节点：

```python
root.left = self.deleteNode(root.left, key)
```

如果 `key` 大于当前节点：

```python
root.right = self.deleteNode(root.right, key)
```

如果相等，就找到了需要删除的节点。

## 删除节点的三种情况

### 没有左孩子

```python
if not node.left:
    return node.right
```

右子树直接替代当前节点。

这同时包含两种情况：

```text
当前节点只有右孩子。
当前节点是叶子，右孩子也是 None。
```

叶子节点会返回 `None`，父节点于是把对应指针设为 `None`。

### 没有右孩子

```python
if not node.right:
    return node.left
```

左子树直接替代当前节点。

### 左右孩子都存在

你的做法是提升整棵右子树：

```python
new_root = node.right
```

然后在右子树中寻找最左节点：

```python
leftmost = new_root

while leftmost.left:
    leftmost = leftmost.left
```

把原来的左子树接到这个最左节点下面：

```python
leftmost.left = node.left
```

最后返回右子树根作为新的当前子树根：

```python
return new_root
```

## 为什么接到右子树的最左节点

假设删除节点 `5`：

```text
        5
       / \
      3   7
         / \
        6   8
```

提升右子树根 `7`，然后找到右子树最小节点 `6`：

```text
        7
       / \
      6   8
```

节点 `6` 是右子树最左节点，所以它没有左孩子。把原来的左子树 `3` 接到这里：

```text
        7
       / \
      6   8
     /
    3
```

仍然满足 BST：

```text
原左子树中的所有值 < 5
右子树中的所有值 > 5
所以原左子树中的所有值也一定 < 右子树中的所有值
```

而右子树最左节点的位置正好空着，可以安全连接原左子树。

## 代码

```python
class Solution:
    def deleteNode(self, root, key):
        def delete_current(node):
            if not node.left:
                return node.right

            if not node.right:
                return node.left

            new_root = node.right
            leftmost = new_root

            while leftmost.left:
                leftmost = leftmost.left

            leftmost.left = node.left
            return new_root

        if not root:
            return None

        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            return delete_current(root)

        return root
```

## 为什么删除后必须返回子树根

删除可能改变当前子树的根节点。

例如：

```text
parent -> node
          \
           child
```

删除 `node` 后，`child` 应该替代它：

```text
parent -> child
```

因此递归必须返回 `child`，再由父节点执行：

```python
parent.left = 返回的 child
```

如果删除的是整棵树根节点，最外层调用者也必须接住返回的新根：

```python
root = solution.deleteNode(root, key)
```

这就是为什么树修改题经常使用：

```python
root.left = recursive_call(root.left)
root.right = recursive_call(root.right)
return root
```

## 返回过程如何逐层接回

假设目标位于左子树：

```python
root.left = self.deleteNode(root.left, key)
```

当前层会暂停，等待下一层返回“删除完成后的左子树根节点”。

下一层可能返回：

```text
原来的子树根：目标在更深处，当前根没变。
某个孩子节点：当前子树根被删除，孩子提升。
None：被删除的是叶子节点。
```

无论是哪一种，父节点都通过同一条赋值语句正确接回。

这正是“返回处理后的子树根节点”模板的价值。

## 与 701 插入的联系

701 插入节点：

```python
root.left = self.insertIntoBST(root.left, val)
```

450 删除节点：

```python
root.left = self.deleteNode(root.left, key)
```

两题的共同模板是：

```text
向下利用 BST 性质寻找位置。
向上返回处理后的子树根节点并逐层接回。
```

区别是：

```text
插入只会在空位置创建新节点。
删除可能让子树根变成孩子、右子树根或 None。
```

## 另一种常见写法：复制后继值

有两个孩子时，也可以找到中序后继，也就是右子树最小节点：

```python
successor = root.right

while successor.left:
    successor = successor.left
```

用后继值覆盖当前值，再从右子树删除重复的后继节点：

```python
root.val = successor.val
root.right = self.deleteNode(root.right, successor.val)
```

这种方法与当前“提升右子树并连接原左子树”的方法都正确。

区别是：

```text
当前方法移动子树引用。
后继值方法保留当前节点对象，只替换值并再次删除后继。
```

## 找不到 `key` 会怎样

搜索最终会到达：

```python
if not root:
    return None
```

这个 `None` 会返回给原本就是空的孩子位置，因此树不会发生变化。

随后每一层仍然返回自己的原根节点，最终得到原树。

## 常见错误

### 找到目标后直接返回 `None`

如果目标有孩子，这会把它的整棵子树全部丢失。

### 两个孩子都存在时只返回右子树

如果没有先把原左子树接到合适位置，左子树会丢失。

### 找到右子树任意节点连接左子树

必须保持 BST 顺序。当前方案选择右子树的最左节点，因为它是右子树最小值且左位置为空。

### 不接住递归返回值

删除可能改变子树根。只调用递归而不执行 `root.left/right = 返回值`，父节点仍会指向旧节点。

### 删除整棵树根后仍使用旧 `root`

调用者必须接住 `deleteNode` 返回的新根。

## 复杂度

时间复杂度：O(h)，`h` 是树高。

搜索目标沿一条路径向下；两个孩子都存在时，再沿右子树向左寻找最小节点，总体仍受树高限制。

- 平衡 BST 中为 O(log n)。
- BST 退化成链表时最坏为 O(n)。

辅助空间复杂度：O(h)，来自递归调用栈。

## 心得

1. BST 删除的难点不是找到目标，而是决定删除后哪棵子树应该替代它。
2. 没有左孩子就返回右子树，没有右孩子就返回左子树。
3. 两个孩子都存在时，可以提升右子树，再把原左子树接到右子树最左节点。
4. 插入和删除都使用“返回处理后的子树根节点，再由父节点逐层接回”的递归模板。
