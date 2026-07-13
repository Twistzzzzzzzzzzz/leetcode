# 701. Insert into a Binary Search Tree

## 题目

给定一棵二叉搜索树 BST 的根节点 `root` 和一个不存在于树中的值 `val`，将新值插入树中，并返回插入后的根节点。

只要插入后仍然满足 BST 性质，答案可能不唯一。最自然的做法是沿搜索路径找到第一个空位置。

BST 性质：

```text
val < 当前节点值：进入左子树
val > 当前节点值：进入右子树
```

## 递归函数的定义

定义：

```text
insertIntoBST(root, val) 返回插入 val 后，以 root 为起点的那棵子树的新根节点。
```

注意返回的不是“刚创建的新节点”，而是“处理完成后的整棵子树根节点”。

这个定义能够统一处理：

```text
当前子树为空，需要创建新根节点。
当前子树非空，只修改它的左子树或右子树。
```

## 向下寻找空位

如果当前子树为空：

```python
if not root:
    return TreeNode(val)
```

这里创建的新节点会作为当前子树的新根返回给上一层。

如果插入值更小：

```python
root.left = self.insertIntoBST(root.left, val)
```

如果插入值更大：

```python
root.right = self.insertIntoBST(root.right, val)
```

题目保证 `val` 不在原树中，因此可以使用 `if/else`。

## 为什么最后返回 `root`

当当前节点非空时，新值只会被插入它的某一棵子树，当前节点本身仍然是这棵子树的根。

所以连接完处理后的孩子后返回：

```python
return root
```

最外层收到的就是插入完成后的整棵树根节点。

## 代码

```python
class Solution:
    def insertIntoBST(self, root: TreeNode | None, val: int) -> TreeNode:
        if not root:
            return TreeNode(val)

        if val < root.val:
            root.left = self.insertIntoBST(root.left, val)
        else:
            root.right = self.insertIntoBST(root.right, val)

        return root
```

## 递归会不会直接返回到最外层

不会。

每次递归调用都会在调用栈中保留自己的局部变量和暂停位置。最底层返回后，只会先回到直接调用它的上一层。

假设：

```text
    4
   /
  2
```

插入 `1`。

### 向下递归

第一层：

```python
insertIntoBST(root=4, val=1)
```

执行到：

```python
4.left = insertIntoBST(2, 1)
```

这一层暂停，等待第二层返回值。

第二层：

```python
insertIntoBST(root=2, val=1)
```

执行到：

```python
2.left = insertIntoBST(None, 1)
```

这一层也暂停，等待第三层返回值。

第三层：

```python
insertIntoBST(root=None, val=1)
```

命中空节点：

```python
return TreeNode(1)
```

## 向上逐层返回并接回

第三层创建的 `Node(1)` 先返回给第二层：

```python
2.left = Node(1)
```

第二层完成连接后：

```python
return root  # 返回节点 2
```

这个节点 `2` 已经带着新左孩子 `1`：

```text
  2
 /
1
```

节点 `2` 再返回给第一层：

```python
4.left = Node(2)
```

第一层最后返回节点 `4`：

```text
    4
   /
  2
 /
1
```

完整过程：

```text
向下：4 -> 2 -> None

向上：
Node(1)
-> 2.left = Node(1)，返回 Node(2)
-> 4.left = Node(2)，返回 Node(4)
```

递归返回是一次一层，不会从最底层直接跳回最外层。

## 每一层都真的重新连接了吗

是的，形式上每一层都会恢复并执行：

```python
root.left = 递归返回值
```

或者：

```python
root.right = 递归返回值
```

不过中间层有时接回的仍然是原来的节点对象。

例如：

```python
4.left = 返回的节点 2
```

原来的 `4.left` 本来就是节点 `2`，所以这次赋值表面上没有改变它指向的对象。

但节点 `2` 的内部已经改变：

```text
插入前：2.left = None
插入后：2.left = Node(1)
```

因此返回的节点 `2` 代表的是一棵已经处理完成的子树。

核心理解：

```text
每一层接回的是“处理后的子树根节点”。
```

## 为什么不能只调用递归

错误写法：

```python
self.insertIntoBST(root.left, val)
```

最底层虽然会创建并返回：

```python
TreeNode(val)
```

但上一层没有接住这个返回值，没有任何节点的 `left` 或 `right` 指向新节点。新节点因此不会进入原树。

必须写：

```python
root.left = self.insertIntoBST(root.left, val)
```

这和 100. Same Tree 中“递归结果必须被使用”是同一类问题。

## 为什么只写 `root = TreeNode(val)` 不够

在空节点那一层写：

```python
root = TreeNode(val)
```

只会让当前函数的局部变量 `root` 指向新节点，不会自动修改上一层的：

```python
parent.left
```

需要把新节点返回：

```python
return TreeNode(val)
```

再由父节点接住：

```python
parent.left = 返回的新节点
```

## 为什么这种模板很重要

下面这些树操作都可能改变某棵子树的根节点：

- 插入节点
- 删除节点
- 树旋转
- 递归构造树
- 修改或替换一棵子树

因此常用统一模板：

```python
def modify(root):
    if not root:
        return new_subtree_root

    root.left = modify(root.left)
    root.right = modify(root.right)

    return root
```

父节点不需要知道子树内部发生了什么，只需接住处理后的子树根节点。

## 迭代写法

迭代版可以保存当前节点并直接在最终空位连接一次：

```python
class Solution:
    def insertIntoBST(self, root, val):
        if not root:
            return TreeNode(val)

        current = root

        while True:
            if val < current.val:
                if current.left:
                    current = current.left
                else:
                    current.left = TreeNode(val)
                    break
            else:
                if current.right:
                    current = current.right
                else:
                    current.right = TreeNode(val)
                    break

        return root
```

迭代版没有递归展开和回溯，因此辅助空间是 O(1)。

## 常见错误

### 没有接住递归返回值

创建出的新节点无法连接到父节点。

### 空树时仍然返回原来的 `root`

空树插入后，新节点就是新的根，必须返回 `TreeNode(val)`。

### 找到空位后忘记逐层返回当前根

非空层需要 `return root`，把处理后的子树根继续传给上一层。

### 忘记题目是 BST

必须根据值的大小只进入一侧，不需要遍历整棵树。

## 复杂度

时间复杂度：O(h)，只沿一条搜索路径向下，`h` 是树高。

- 平衡 BST 中为 O(log n)。
- BST 退化成链表时最坏为 O(n)。

递归版本辅助空间复杂度：O(h)。

迭代版本辅助空间复杂度：O(1)。

## 心得

1. 递归函数返回的是“插入完成后的子树根节点”，不是只返回新插入的节点。
2. 递归向下时，每一层暂停等待；递归向上时，一次返回一层，每层恢复赋值并接回处理后的子树。
3. 中间层即使接回原来的节点对象，该节点内部的子树也可能已经改变。
4. 可以把 BST 插入记成：向下找空位，向上逐层接回子树。
