# 1325. Delete Leaves With a Given Value

## 题目

删除二叉树中所有值等于 `target` 的叶子节点。

删除后，如果某个父节点因此变成了值为 `target` 的新叶子，也要继续删除它，直到不能再删除为止。

## 识别题型

这题有两个明显信号：

1. 当前节点是否需要删除，取决于左右孩子处理完成后的状态。
2. 当前节点可能被保留，也可能被替换成 `None`。

因此应该想到：

```text
后序遍历
+
递归返回处理后的子树根节点
```

## 为什么必须使用后序遍历

考虑：

```text
    1
   /
  2
 /
2
```

`target = 2`。

最下面的 2 被删除后，上面的 2 原本不是叶子，现在变成了新的叶子，也应该被删除。

所以当前节点必须先等待左右子树处理完：

```python
node.left = dfs(node.left)
node.right = dfs(node.right)
```

然后再判断当前节点现在是不是目标叶子：

```python
if node.val == target and not node.left and not node.right:
    return None
```

顺序是：

```text
左子树 -> 右子树 -> 当前节点
```

这就是后序遍历。

## 递归函数的职责

定义：

```python
dfs(node)
```

表示：

> 删除以 `node` 为根的子树中所有符合条件的叶子，并返回处理完成后的子树根节点。

它可能返回：

```text
node：当前节点仍然保留
None：当前节点应该从树中断开
```

父节点必须接住这个返回值：

```python
node.left = dfs(node.left)
node.right = dfs(node.right)
```

## 为什么在子节点那层写 `node = None` 没用

假设：

```text
    5
   /
  3
```

递归进入节点 3 时，局部变量 `node` 指向节点 3。

如果只写：

```python
node = None
```

改变的是当前函数中的局部变量指向：

```text
当前层 node -> None
```

但父节点仍然保存着：

```text
节点 5 的 left -> 节点 3
```

所以树中的连接没有改变。

可以用普通变量类比：

```python
a = TreeNode(3)
b = a

b = None
```

此时只有 `b` 变成了 `None`，`a` 仍然指向原来的节点。

## 为什么 `node.left = None` 可以生效

```python
node.left = None
```

修改的是节点对象内部保存的 `left` 属性。

只要其他变量也指向这个节点对象，它们都会看到该属性发生了变化。

这与下面的操作不同：

```python
node = None
```

后者只重新绑定当前局部变量，并没有修改节点对象或父节点中的连接。

## `return None` 为什么能够删除节点

严格来说，单独执行：

```python
return None
```

也不会自动修改父节点。

真正完成断链的是父节点接住返回值：

```python
node.left = dfs(node.left)
```

如果左子树递归返回 `None`，这句就变成：

```python
node.left = None
```

父节点到被删除节点的连接因此被断开。

所以完整机制是：

```text
子节点返回新的子树根节点
-> 父节点接住返回值
-> 父节点更新 left 或 right 指针
```

## 为什么没被删除的节点也必须 `return node`

如果代码只有：

```python
if 应该删除:
    return None
```

却没有：

```python
return node
```

那么不需要删除时，Python 函数走到末尾仍会默认返回 `None`。

父节点执行：

```python
node.left = dfs(node.left)
```

就会把本来应该保留的孩子也接成 `None`。

因此两个分支必须完整：

```python
if 当前节点应该删除:
    return None

return node
```

## 为什么最外层要 `return dfs(root)`

根节点没有父节点帮它接住返回值。

如果根节点最终也变成了目标叶子，`dfs(root)` 会返回 `None`。

错误写法：

```python
dfs(root)
return root
```

这里丢掉了递归结果，仍然返回原来的根节点引用。

正确写法：

```python
return dfs(root)
```

调用者相当于负责接住整棵树处理后的新根节点。

## 代码

```python
class Solution:
    def removeLeafNodes(self, root, target):
        def dfs(node):
            if not node:
                return None

            node.left = dfs(node.left)
            node.right = dfs(node.right)

            if node.val == target and not node.left and not node.right:
                return None

            return node

        return dfs(root)
```

内部 `dfs` 可以直接使用外层的 `target`，因此不需要每次递归都重复传入它。写成 `dfs(node, target)` 也能工作，只是参数略显重复。

## 删除节点的本质

Python 中通常不需要手动销毁节点对象。

树和链表中的“删除”本质上是：

```text
修改指向该节点的连接
```

当树中不再有任何连接指向该节点，并且程序其他地方也没有保存它的引用时，Python 会在合适的时候回收这个对象。

## 通用的树结构修改模板

如果当前节点可能被删除或替换，可以使用：

```python
def transform(node):
    if not node:
        return None

    node.left = transform(node.left)
    node.right = transform(node.right)

    if 当前节点应该被删除:
        return None

    return node

root = transform(root)
```

可以把它记成：

```text
向下处理子树，向上接回新根。
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(h)

每个节点只访问一次。`h` 是树高，额外空间来自递归调用栈。

## 心得

1. 当前节点是否删除取决于孩子处理后的状态，所以使用后序遍历。
2. `node = None` 只改变当前递归层的局部变量，不会修改父节点的 `left` 或 `right`。
3. 递归应返回处理后的子树根节点，父节点通过 `node.left/right = dfs(...)` 接住结果。
4. 被删除的节点返回 `None`，被保留的节点必须返回 `node`。
5. 根节点也可能被删除，所以最外层必须返回 `dfs(root)`。
6. 树和链表中删除节点的本质，是断开指向该节点的连接。
