# 100. Same Tree

## 题目

给定两棵二叉树的根节点 `p` 和 `q`，判断它们是否完全相同。

两棵树相同必须同时满足：

1. 对应节点的值相同。
2. 对应节点的存在情况相同，也就是结构相同。
3. 左右子树也分别相同。

例如：

```text
    1           1
   / \         / \
  2   3       2   3
```

这两棵树相同。

下面两棵树即使节点值集合相同，结构也不同：

```text
    1           1
   /             \
  2               2
```

因此它们不相同。

## 递归函数的定义

定义：

```text
check(node_p, node_q) 返回以 node_p 和 node_q 为根的两棵子树是否完全相同。
```

每一层都需要同时观察两个对应节点。

## 三种节点情况

### 两个节点都为空

```python
if not node_p and not node_q:
    return True
```

两边同时走到空节点，说明这一对应位置结构相同。

### 只有一个节点为空

```python
if not node_p or not node_q:
    return False
```

因为“两个都为空”的情况已经在前面返回，所以执行到这里时，`or` 表示必然只有一个为空，结构不同。

这两个判断的顺序不能随意交换。如果先写 `if not node_p or not node_q`，两个都为空时也会被错误地返回 `False`。

### 两个节点都存在

先比较当前值：

```python
if node_p.val != node_q.val:
    return False
```

当前值相同后，还必须保证左右子树都相同：

```python
return (
    check(node_p.left, node_q.left)
    and check(node_p.right, node_q.right)
)
```

## 代码

```python
class Solution:
    def isSameTree(self, p: TreeNode | None, q: TreeNode | None) -> bool:
        def check(node_p, node_q):
            if not node_p and not node_q:
                return True

            if not node_p or not node_q:
                return False

            if node_p.val != node_q.val:
                return False

            return check(node_p.left, node_q.left) and check(
                node_p.right,
                node_q.right,
            )

        return check(p, q)
```

## 第一版为什么会错误

第一版调用了递归：

```python
check(node_p.left, node_q.left)
check(node_p.right, node_q.right)
```

但没有接住或返回递归结果。

假设左子树不同：

```python
check(node_p.left, node_q.left)  # 返回 False
```

这个 `False` 只是在当前表达式中产生，随后便被丢弃。程序仍然会继续执行，并在最后无条件：

```python
return True
```

因此第一版实际上只可靠地比较了当前节点值，没有让深层子树的错误向上传播。

树递归不仅要调用子问题，还必须把子问题的返回值用于当前答案。

正确方式可以先接住：

```python
left_same = check(node_p.left, node_q.left)
right_same = check(node_p.right, node_q.right)

return left_same and right_same
```

也可以直接返回组合结果。

## 为什么使用 `and`

当前两棵子树完全相同，需要同时满足：

```text
当前节点值相同
左子树相同
右子树相同
```

前面已经排除了当前值不同的情况，因此最后只需：

```python
left_same and right_same
```

只要任意一侧返回 `False`，当前层也必须返回 `False`。

## `and` 的短路机制

写成：

```python
return check(node_p.left, node_q.left) and check(
    node_p.right,
    node_q.right,
)
```

如果左子树已经返回 `False`，Python 不会继续计算右侧表达式，因为：

```text
False and 任何结果
```

最终都只能是 `False`。

这叫逻辑短路，可以避免不必要的递归比较。

## 为什么不能只比较遍历结果

如果遍历结果没有记录空节点位置，不同结构可能产生相同的值序列。

例如前序遍历：

```text
    1           1
   /             \
  2               2
```

两棵树的普通前序值序列都是：

```text
[1, 2]
```

但树的结构不同。

因此这题直接同步比较两个对应节点更自然，也能同时检查值和结构。

## 属于哪种遍历思路

代码先比较当前节点的存在情况和值，再递归比较左右子树：

```text
当前节点 -> 左子树 -> 右子树
```

因此可以看作前序、自顶向下的 DFS 比较。

## 常见错误

### 忽略递归返回值

只写 `check(...)` 不会自动改变当前函数的返回值，必须接住或直接返回。

### 只比较节点值

节点值相同不代表结构相同，还要递归检查对应左右孩子。

### 空节点判断顺序错误

先处理两个都为空，再处理只有一个为空。

### 使用 `or` 组合左右结果

左右子树必须同时相同，所以应该用 `and`。使用 `or` 会让只有一侧相同的树被误判。

## 复杂度

时间复杂度：O(n)，最坏需要检查所有对应节点；`n` 表示实际比较的节点数量。

辅助空间复杂度：O(h)，`h` 是递归比较过程中的最大树高。

## 心得

1. 比较两棵树时，每一层要同时携带两个对应节点。
2. 两棵树相同需要“当前值相同、左子树相同、右子树相同”三个条件同时成立。
3. 递归结果不会自动向上传播，必须通过 `return` 或变量接住后参与当前结果。
4. `and` 不仅表示左右两边都要相同，还能在左侧失败时利用短路机制提前结束。
