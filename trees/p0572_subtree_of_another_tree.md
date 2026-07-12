# 572. Subtree of Another Tree

## 题目

给定两棵二叉树 `root` 和 `subRoot`，判断 `root` 中是否存在一棵与 `subRoot` 结构和值都完全相同的子树。

这题包含两个不同任务：

```text
寻找候选起点
从候选起点判断两棵树是否完全相同
```

第二个任务就是刚刚完成的 100. Same Tree。

## 两个递归函数的职责

### `isSubtree(root, subRoot)`

定义：

```text
在以 root 为根的整棵树中，寻找是否存在与 subRoot 完全相同的子树。
```

它负责遍历所有可能的起点。

### `same_tree(node_p, node_q)`

定义：

```text
判断以 node_p 和 node_q 为根的两棵树是否完全相同。
```

它负责验证某一个候选起点。

职责不同，所以不要把“寻找”和“完整匹配”混成同一个判断。

## 边界情况

如果 `subRoot` 是空树，可以把它视为任意树的子树：

```python
if not subRoot:
    return True
```

如果 `subRoot` 非空但 `root` 已经为空，就不可能继续找到：

```python
if not root:
    return False
```

LeetCode 这题通常保证 `subRoot` 至少有一个节点，但按这个顺序写可以让函数的边界行为更完整。

## 检查当前候选起点

先判断当前 `root` 是否就是答案：

```python
if same_tree(root, subRoot):
    return True
```

`same_tree` 内部会同时比较：

```text
当前节点值
左子树结构和值
右子树结构和值
```

因此外层不需要提前判断：

```python
root.val == subRoot.val
```

## 当前起点失败后继续搜索

如果当前起点不能完整匹配，仍然要继续在左右子树寻找：

```python
return isSubtree(root.left, subRoot) or isSubtree(
    root.right,
    subRoot,
)
```

只要任意一侧找到，就返回 `True`。

## 代码

```python
class Solution:
    def isSubtree(self, root, subRoot):
        if not subRoot:
            return True

        if not root:
            return False

        def same_tree(node_p, node_q):
            if not node_p and not node_q:
                return True

            if not node_p or not node_q:
                return False

            if node_p.val != node_q.val:
                return False

            return same_tree(node_p.left, node_q.left) and same_tree(
                node_p.right,
                node_q.right,
            )

        if same_tree(root, subRoot):
            return True

        return self.isSubtree(root.left, subRoot) or self.isSubtree(
            root.right,
            subRoot,
        )
```

## 第二版为什么会错误

第二版使用了：

```python
if root.val == subRoot.val:
    return check(root, subRoot)
else:
    return self.isSubtree(root.left, subRoot) or self.isSubtree(
        root.right,
        subRoot,
    )
```

问题是：

```text
节点值相同，只表示当前节点是一个可能的起点。
它不保证从这里开始的整棵树一定完全相同。
```

例如：

```text
root:             subRoot:

    1                 1
   /
  1
```

在最上面的节点：

```python
root.val == subRoot.val
```

但 `check(root, subRoot)` 会因为结构不同返回 `False`。

真正的答案位于 `root.left`：

```text
root.left 与 subRoot 完全相同
```

如果直接：

```python
return check(root, subRoot)
```

就会过早返回 `False`，失去继续搜索 `root.left` 的机会。

## 正确的控制流程

当前节点是否匹配和是否继续向下搜索，不应该写成排他的 `if/else`。

正确顺序是：

```text
1. 尝试把当前节点作为起点完整匹配。
2. 匹配成功，立即返回 True。
3. 当前起点失败，继续搜索左右子树。
```

代码对应：

```python
if same_tree(root, subRoot):
    return True

return self.isSubtree(root.left, subRoot) or self.isSubtree(
    root.right,
    subRoot,
)
```

## 为什么不需要先比较当前值

可以先写：

```python
if root.val == subRoot.val and same_tree(root, subRoot):
    return True
```

但不是必须，因为 `same_tree` 的第一批判断已经包括：

```python
if node_p.val != node_q.val:
    return False
```

省略外层值判断可以减少重复逻辑，让控制流程更清楚。

## 与 100. Same Tree 的联系

100 只解决：

```text
这两个确定的根节点开始，整棵树是否相同？
```

572 在它外面增加了一层搜索：

```text
root 中的哪个节点可能是 subRoot 的起点？
```

因此：

```text
572 = 遍历 root 的所有候选节点 + 100 的完整树比较
```

这种“枚举候选起点，再调用已有判定函数”的拆分方式在很多题里都很常见。

## `or` 的短路机制

```python
self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
```

如果左子树已经找到答案并返回 `True`，Python 不会继续搜索右子树。

## 复杂度

设：

```text
n = root 的节点数
m = subRoot 的节点数
```

最坏情况下，`root` 中许多节点都可能成为候选起点，每次完整比较最多访问 `m` 个节点。

时间复杂度：O(nm)。

辅助空间复杂度：O(h1 + h2)，来自搜索 `root` 和比较 `subRoot` 时的递归调用栈。

## 心得

1. 这题要拆成“寻找候选起点”和“验证两棵树完全相同”两个职责。
2. 当前节点值相同只代表它可能是起点，不代表完整结构一定匹配。
3. 当前候选起点匹配失败后，仍然必须继续搜索左右子树，不能过早返回 `False`。
4. 可以复用 100. Same Tree 的递归逻辑，不需要重新发明比较方法。
