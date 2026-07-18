# 1448. Count Good Nodes in Binary Tree

## 题目

如果从根节点到当前节点的路径中，没有任何节点值大于当前节点值，那么当前节点就是一个 good node。

返回整棵树中 good node 的数量。

注意题目允许相等：

```text
node.val >= 路径上此前出现过的最大值
```

## 识别题型

题目反复强调：

- 从根节点到当前节点的路径
- 当前节点需要和所有祖先比较
- 进入子节点时需要知道此前的最大值

这类题适合自顶向下 DFS：把路径状态作为递归参数传给孩子。

本题需要传递的状态是：

```text
path_maximum = 从根到当前节点之前，路径上的最大值
```

## 递归函数的职责

定义：

```python
dfs(node, path_maximum)
```

表示：

> 已知祖先路径最大值为 `path_maximum`，统计以 `node` 为根的子树中有多少个 good node。

当前节点需要完成三件事：

1. 判断自己是否为 good node。
2. 更新传给孩子的路径最大值。
3. 汇总自己、左子树和右子树的数量。

```python
is_good = int(node.val >= path_maximum)
new_maximum = max(path_maximum, node.val)

return (
    is_good
    + dfs(node.left, new_maximum)
    + dfs(node.right, new_maximum)
)
```

这里同时出现了两种信息流动：

```text
path_maximum 从父节点传给孩子：自顶向下
good node 数量从孩子返回父节点：自底向上汇总
```

## 你的写法为什么正确

你的版本先写：

```python
self.count = 1
maximum = root.val
dfs(root.left, maximum)
dfs(root.right, maximum)
```

根节点到自身的路径上没有其他节点，所以根节点一定是 good node。题目保证 `root` 非空时，这样先把答案设为 1，再从两个孩子开始遍历是正确的。

不过这种写法特殊处理了根节点，而且依赖实例变量 `self.count`。如果同一个 `Solution` 对象被多次调用，就必须确保每次都正确重置它。

更统一的处理方式是从根节点开始 DFS，并把初始最大值设为负无穷：

```python
return dfs(root, float("-inf"))
```

这样根节点会按照和其他节点完全相同的规则被统计，空树也能自然返回 0。

## 为什么不能使用整棵树的全局最大值

`maximum` 表示的是当前路径最大值，不是遍历到目前为止整棵树的最大值。

例如：

```text
       3
      / \
    100  4
```

节点 100 不在节点 4 的祖先路径上，所以它不能影响节点 4 的判断。

递归参数会沿每条分支分别传递：

```text
左分支得到自己的 maximum
右分支得到自己的 maximum
```

不要用一个跨分支共享、只增不减的全局最大值，否则左子树的信息会错误地污染右子树。

## 代码

```python
class Solution:
    def goodNodes(self, root):
        def dfs(node, path_maximum):
            if not node:
                return 0

            is_good = int(node.val >= path_maximum)
            new_maximum = max(path_maximum, node.val)

            return (
                is_good
                + dfs(node.left, new_maximum)
                + dfs(node.right, new_maximum)
            )

        return dfs(root, float("-inf"))
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(h)

每个节点只访问一次。`h` 是树高，额外空间来自递归调用栈；最坏情况下链状树为 O(n)，平衡树为 O(log n)。

## 心得

1. 看到“从根到当前节点的路径上满足某种条件”，可以考虑 DFS，并把路径状态作为参数向下传递。
2. 本题传递的不是整棵树最大值，而是当前根到节点路径上的最大值。
3. 当前节点满足 `node.val >= path_maximum` 时才是 good node，相等也算。
4. 先计算 `new_maximum`，再把它分别传给左右孩子；不同分支的路径状态不能互相影响。
5. 用递归返回值汇总数量，可以避免实例变量和对根节点的特殊处理。
