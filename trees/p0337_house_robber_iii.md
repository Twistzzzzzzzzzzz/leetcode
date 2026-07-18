# 337. House Robber III

## 题目

每个二叉树节点代表一间房，节点值是这间房中的金额。

如果两个直接相连的节点在同一晚都被偷，就会触发警报。也就是说：

```text
偷当前节点 -> 不能偷它的左右孩子
不偷当前节点 -> 左右孩子可以自行选择偷或不偷
```

求不触发警报时能够偷到的最大金额。

## 为什么这题难

前面的树题经常让 `dfs(node)` 返回一个结果，例如：

- 子树高度
- 子树是否平衡
- 子树中的节点数量

但这题中，以 `node` 为根的子树能获得多少收益，取决于父节点是否被偷。

父节点需要知道当前子树的两种条件结果：

```text
偷 node 时，子树最多得到多少
不偷 node 时，子树最多得到多少
```

因此不能让每个节点只返回一个没有条件的最大值，而要同时返回两个状态。

## 原始思路中正确的部分

你的入口是正确的：

```text
选择偷当前节点
选择不偷当前节点
比较两种结果
```

如果偷当前节点，可以继续考虑四棵孙子子树；如果不偷当前节点，可以考虑两个孩子子树。

这个递推方向理论上可以写成：

```text
偷当前节点的收益
= 当前节点值 + 四棵孙子子树各自的最优收益

不偷当前节点的收益
= 左孩子子树最优收益 + 右孩子子树最优收益
```

但直接这样写有几个问题。

## 原始写法的问题

### 可能访问 `None.left`

```python
recursion(node.left.left)
```

即使 `node` 存在，`node.left` 仍然可能是 `None`。这时访问 `node.left.left` 会报错。

### 偷当前节点时漏掉了 `node.val`

偷当前节点的收益必须包含：

```python
node.val
```

只计算孙子子树会漏掉当前房子的金额。

### 递归函数的职责不完整

如果 `recursion(node)` 只返回四棵孙子树的收益之和，它并没有表示：

> 以 `node` 为根的子树最多能偷多少。

而且“偷还是不偷”的选择不能只在根节点做一次，树中的每个节点都需要做这个选择。

### 会重复计算同一棵子树

直接递归孩子和孙子时，同一棵子树可能从不同路径反复计算，最坏会接近指数级时间。

可以使用记忆化解决重复计算，但本题还有更自然的树形动态规划写法。

## 树形动态规划

定义：

```python
dfs(node) -> (rob, not_rob)
```

元组含义固定为：

```text
rob：偷 node 时，以 node 为根的子树最大收益
not_rob：不偷 node 时，以 node 为根的子树最大收益
```

这里采用你最终代码的 `(rob, not_rob)` 顺序。顺序本身可以反过来，但定义后必须在整份代码中保持一致。

## 空节点返回什么

空节点既没有金额，也没有孩子：

```python
if not node:
    return 0, 0
```

表示偷或不偷空节点，收益都是 0。

## 为什么使用后序遍历

当前节点的两个状态必须先知道左右子树的两个状态：

```python
left_rob, left_not_rob = dfs(node.left)
right_rob, right_not_rob = dfs(node.right)
```

然后才能计算当前节点：

```text
先处理左子树
再处理右子树
最后处理当前节点
```

这正是后序遍历。

## 状态转移

### 状态一：偷当前节点

如果偷当前节点，左右孩子都不能偷，因此只能使用两个孩子的 `not_rob` 状态：

```python
rob_current = (
    node.val
    + left_not_rob
    + right_not_rob
)
```

金额是在相加，不能写成减法。

### 状态二：不偷当前节点

如果不偷当前节点，左右孩子没有被当前节点限制。

每个孩子都可以自行选择收益更高的状态：

```python
not_rob_current = (
    max(left_rob, left_not_rob)
    + max(right_rob, right_not_rob)
)
```

不偷当前节点，并不意味着必须偷孩子。

可能某个孩子金额很低，而它下面的节点金额更高，此时这个孩子选择 `not_rob` 反而更好，所以必须取两种状态的最大值。

## 状态关系表

| 当前节点选择 | 孩子允许使用的状态 |
| --- | --- |
| 偷当前节点 | 孩子只能不偷：`child_not_rob` |
| 不偷当前节点 | 孩子自由选择：`max(child_rob, child_not_rob)` |

这张表就是整道题最核心的状态转移。

## 返回给父节点

当前节点算完两种状态后，不急着决定最终选哪一种，而是都返回：

```python
return rob_current, not_rob_current
```

因为父节点是否被偷，会决定它能使用当前节点的哪个状态。

只有到了整棵树的根节点，上方已经没有父节点限制，才直接选择最大值：

```python
rob_root, not_rob_root = dfs(root)
return max(rob_root, not_rob_root)
```

## 为什么不再显式访问孙子节点

偷当前节点时使用：

```python
left_not_rob
right_not_rob
```

`left_not_rob` 已经表示“不偷左孩子时，左孩子下面整棵子树的最优收益”。

这个状态内部自然会选择合适的孙子节点，因此当前节点不需要自己再访问：

```python
node.left.left
node.left.right
```

状态已经把更深层的选择压缩成了一个数字。

## 代码

```python
class Solution:
    def rob(self, root):
        def dfs(node):
            if not node:
                return 0, 0

            left_rob, left_not_rob = dfs(node.left)
            right_rob, right_not_rob = dfs(node.right)

            rob_current = (
                node.val
                + left_not_rob
                + right_not_rob
            )

            not_rob_current = (
                max(left_rob, left_not_rob)
                + max(right_rob, right_not_rob)
            )

            return rob_current, not_rob_current

        rob_root, not_rob_root = dfs(root)
        return max(rob_root, not_rob_root)
```

## 一个小例子

```text
    2
   / \
  1   3
```

叶子节点 1 返回：

```text
(rob=1, not_rob=0)
```

叶子节点 3 返回：

```text
(rob=3, not_rob=0)
```

节点 2：

```text
rob_current = 2 + 0 + 0 = 2
not_rob_current = max(1, 0) + max(3, 0) = 4
```

根节点返回：

```text
(2, 4)
```

最终答案是 4。

## 如何识别树形动态规划

看到以下特征，可以考虑让每个节点返回多个状态：

1. 每个节点都有选或不选等决策。
2. 父节点的选择会限制孩子能做的选择。
3. 当前节点需要左右子树的状态才能计算自己。
4. 相同结构的问题会在每棵子树上重复出现。

常见形式是：

```python
def dfs(node):
    left_states = dfs(node.left)
    right_states = dfs(node.right)

    state_a = ...
    state_b = ...

    return state_a, state_b
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(h)

每个节点只计算一次，每次只进行常数次状态转移。`h` 是树高，额外空间来自递归调用栈。

## 心得

1. 这题的正确入口是比较“偷当前节点”和“不偷当前节点”。
2. 难点在于父节点需要知道孩子在两种条件下的收益，所以每个节点必须同时返回两个状态。
3. 偷当前节点时，孩子只能使用 `not_rob`；不偷当前节点时，孩子可以选择 `rob` 与 `not_rob` 中更大的一个。
4. 当前节点依赖左右子树结果，因此使用后序遍历。
5. 元组顺序可以是 `(rob, not_rob)` 或 `(not_rob, rob)`，但定义后必须始终保持一致。
6. 树形 DP 的关键是先问：父节点为了做决定，需要从每棵子树得到哪些条件状态？
