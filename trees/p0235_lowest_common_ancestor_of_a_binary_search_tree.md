# 235. Lowest Common Ancestor of a Binary Search Tree

## 题目

给定一棵二叉搜索树 BST，以及其中两个节点 `p` 和 `q`，返回它们的最近公共祖先。

最近公共祖先是同时包含 `p` 和 `q` 的最深节点。一个节点也可以是它自己的祖先。

例如：

```text
          6
        /   \
       2     8
      / \   / \
     0   4 7   9
        / \
       3   5
```

- `2` 和 `8` 的最近公共祖先是 `6`。
- `2` 和 `4` 的最近公共祖先是 `2`。
- `3` 和 `5` 的最近公共祖先是 `4`。

## 核心：利用 BST 的有序性

BST 满足：

```text
左子树中的所有值 < 当前节点值
右子树中的所有值 > 当前节点值
```

因此站在当前 `root` 时，只需要比较 `p.val`、`q.val` 和 `root.val`。

## 三种情况

### 两个目标都比当前节点小

```python
if p.val < root.val and q.val < root.val:
```

说明 `p` 和 `q` 都位于左子树，最近公共祖先也一定在左边：

```python
return self.lowestCommonAncestor(root.left, p, q)
```

### 两个目标都比当前节点大

```python
if p.val > root.val and q.val > root.val:
```

说明两个目标都位于右子树：

```python
return self.lowestCommonAncestor(root.right, p, q)
```

### 两个目标不在同一侧

剩余情况包括：

```text
p 在左边，q 在右边
p 在右边，q 在左边
root 就是 p
root 就是 q
```

这些情况下，当前 `root` 就是两条搜索路径第一次分开的节点，也就是最近公共祖先：

```python
return root
```

## 代码

```python
class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if not root:
            return None

        if p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestor(root.left, p, q)

        if p.val > root.val and q.val > root.val:
            return self.lowestCommonAncestor(root.right, p, q)

        return root
```

你的写法：

```python
if root.val > q.val and root.val > p.val:
```

与：

```python
if p.val < root.val and q.val < root.val:
```

完全等价。整理后的写法只是把两个目标放在左边，更接近“两个目标都小于当前节点”的自然语言。

## 为什么“分叉点”就是最近公共祖先

从 BST 根节点搜索 `p` 和 `q` 时：

- 如果两者都小于当前值，两条搜索路径会一起向左。
- 如果两者都大于当前值，两条搜索路径会一起向右。

只要它们始终处于同一侧，当前节点就还不是最深的公共祖先，可以继续缩小范围。

第一次出现下面情况时：

```text
两个目标分别位于两侧，或者当前节点就是其中一个目标
```

两条搜索路径无法再一起向下。当前节点因此是最深的共同位置。

## 为什么必须使用严格比较

条件应该写：

```python
p.val < root.val and q.val < root.val
```

以及：

```python
p.val > root.val and q.val > root.val
```

不要把等号随意加入同侧判断。

例如：

```text
p = 节点 2
q = 节点 4
root = 节点 2
```

此时 `root` 本身就是 `p`，并且也是 `q` 的祖先，所以答案应该是 `2`。

严格比较会让两个同侧条件都不成立，最终正确执行：

```python
return root
```

## 为什么不需要先确定 `p` 和 `q` 的大小顺序

代码分别判断两者是否都小于或都大于当前节点：

```python
p.val < root.val and q.val < root.val
p.val > root.val and q.val > root.val
```

这些条件关于 `p`、`q` 是对称的，因此不需要提前保证：

```text
p.val < q.val
```

## 与普通二叉树 LCA 的区别

普通二叉树没有大小关系，无法根据节点值决定只进入哪一侧，通常需要同时递归搜索左右子树。

BST 可以利用有序性，每次只沿一个方向继续寻找，因此代码更短，平均效率也更高。

不要把这份写法直接用于普通二叉树。只有题目明确说明是 BST 时，才能根据值选择左右方向。

## 迭代写法

递归并不是必须的，也可以不断移动当前节点：

```python
class Solution:
    def lowestCommonAncestor(self, root, p, q):
        current = root

        while current:
            if p.val < current.val and q.val < current.val:
                current = current.left
            elif p.val > current.val and q.val > current.val:
                current = current.right
            else:
                return current

        return None
```

迭代版与递归版的判断逻辑完全相同，但不使用递归调用栈。

## 属于哪种递归思路

代码先根据当前节点和两个目标的值决定答案或下一步方向，再进入某一棵子树。

因此可以看作自顶向下的 BST 搜索。它不像普通树后序题那样需要先获取左右子树返回值。

## 常见错误

### 把它当作普通二叉树题

这会忽略题目给出的 BST 有序性，写出不必要的全树搜索。

### 只根据一个目标决定方向

最近公共祖先与两个目标都有关。必须确认 `p` 和 `q` 是否位于当前节点同一侧。

### 两个目标分居两侧时继续递归

分居两侧正说明当前节点就是分叉点，应直接返回当前节点。

### 忘记节点可以是自己的祖先

如果当前节点等于 `p` 或 `q`，并且另一个目标位于其子树中，当前节点就是最近公共祖先。

### 在普通二叉树中使用值比较

普通二叉树不保证左小右大，根据值选择方向可能漏掉答案。

## 复杂度

时间复杂度：O(h)，每次只进入一棵子树，`h` 是树高。

- 平衡 BST 中为 O(log n)。
- BST 退化成链表时最坏为 O(n)。

递归版本辅助空间复杂度：O(h)。

迭代版本辅助空间复杂度：O(1)。

## 心得

1. 题目明确给出 BST 时，要主动利用左小右大的有序性。
2. 两个目标都小就向左，都大就向右，否则当前节点就是第一次分叉的位置。
3. 当前节点可能等于 `p` 或 `q`，所以同侧判断必须使用严格比较。
4. BST 的最近公共祖先本质上是同时追踪两个目标的搜索路径，并寻找它们第一次分开的节点。
