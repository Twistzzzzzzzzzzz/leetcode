# 98. Validate Binary Search Tree

## 题目

判断一棵二叉树是否为合法的二叉搜索树 Binary Search Tree，简称 BST。

合法 BST 必须满足：

```text
当前节点左子树中的所有节点值 < 当前节点值
当前节点右子树中的所有节点值 > 当前节点值
左右子树本身也必须是合法 BST
```

这里使用严格小于和严格大于，因此重复值也会使 BST 不合法。

## 第一次思路的问题

### 少一个孩子不代表一定合法

原代码中：

```python
if not root.left or not root.right:
    return True
```

例如：

```text
    5
   /
  7
```

根节点没有右孩子，但 7 被放在 5 的左边，仍然不符合 BST。

只有空树可以直接判断为合法：

```python
if not root:
    return True
```

### `latter` 没有保存前一个值

原代码在每个节点中先执行：

```python
latter = node.val
```

然后马上判断：

```python
if node.val < latter:
```

这相当于比较：

```python
node.val < node.val
```

条件永远为 `False`。而且 `latter` 每轮都会重新创建，并没有保存上一个节点的值。

### 层序遍历结果不需要递增

合法 BST：

```text
        5
       / \
      3   8
     / \ / \
    2  4 6  9
```

它的层序遍历是：

```text
5, 3, 8, 2, 4, 6, 9
```

这个序列并不递增，所以不能比较 BFS 中相邻节点的大小来验证 BST。

真正具有严格递增性质的是 BST 的中序遍历，不是层序遍历。

### 只比较父子节点仍然不够

考虑：

```text
        10
          \
           15
          /  \
         6    20
```

节点 6 小于父节点 15，看起来符合“左孩子更小”。

但节点 6 位于根节点 10 的右子树中，还必须满足：

```text
6 > 10
```

它没有满足祖先节点带来的限制，因此整棵树不是 BST。

## 核心方法：上下界递归

BST 的限制来自当前节点的所有祖先，所以递归时需要同时传入当前节点允许出现的范围。

定义：

```python
check(node, lower, upper)
```

表示：

> 检查以 `node` 为根的子树是否为合法 BST，并且其中每个节点都必须满足祖先传来的范围限制。

当前节点必须严格满足：

```python
lower < node.val < upper
```

如果超出范围：

```python
if node.val <= lower or node.val >= upper:
    return False
```

## 左右子树如何更新范围

假设当前节点值为 `node.val`。

进入左子树时，左侧原有下界不变，但所有节点都必须小于当前节点：

```python
check(node.left, lower, node.val)
```

进入右子树时，右侧原有上界不变，但所有节点都必须大于当前节点：

```python
check(node.right, node.val, upper)
```

可以记成：

```text
左子树：更新 upper
右子树：更新 lower
```

初始根节点没有范围限制，因此使用：

```python
check(root, float("-inf"), float("inf"))
```

## 错误案例如何被发现

再次观察：

```text
        10
          \
           15
          /
         6
```

范围变化：

```text
节点 10：(-inf, inf)
节点 15：(10, inf)
节点  6：(10, 15)
```

节点 6 不满足：

```text
10 < 6 < 15
```

所以返回 `False`。这就是上下界能够发现跨越多层祖先错误的原因。

## 代码

```python
class Solution:
    def isValidBST(self, root):
        def check(node, lower, upper):
            if not node:
                return True

            if node.val <= lower or node.val >= upper:
                return False

            return (
                check(node.left, lower, node.val)
                and check(node.right, node.val, upper)
            )

        return check(root, float("-inf"), float("inf"))
```

这里使用 `and` 组合左右子树结果。Python 具有短路机制：左子树已经不合法时，不会继续执行右子树检查。

## BFS 也可以实现

错误不在于使用 BFS，而在于队列里只保存了节点，没有保存祖先带来的范围。

如果希望使用 BFS，队列元素应为：

```text
(node, lower, upper)
```

```python
from collections import deque


class Solution:
    def isValidBST(self, root):
        if not root:
            return True

        queue = deque([(root, float("-inf"), float("inf"))])

        while queue:
            node, lower, upper = queue.popleft()

            if node.val <= lower or node.val >= upper:
                return False

            if node.left:
                queue.append((node.left, lower, node.val))

            if node.right:
                queue.append((node.right, node.val, upper))

        return True
```

这说明：

```text
上下界是解题所需的状态
DFS 或 BFS 只是携带这个状态的不同遍历方式
```

递归写法更短，也更自然地表达了祖先范围向子树传递的过程，因此作为本题主解。

## 另一种方法：中序遍历

合法 BST 的中序遍历必须严格递增。

因此也可以在中序遍历过程中比较当前值和前一个值：

```python
previous = float("-inf")
```

如果出现：

```python
node.val <= previous
```

说明不合法。

注意这里能比较相邻值，是因为使用的是中序遍历；原来的层序遍历不具备递增性质。

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(h)

每个节点最多访问一次。`h` 是树高，递归栈在平衡树中为 O(log n)，在链状树中最坏为 O(n)。

## 心得

1. BST 的要求不是“左孩子小、右孩子大”，而是“左子树所有节点小、右子树所有节点大”。
2. 验证 BST 时，每个节点必须满足祖先共同确定的合法范围：`lower < node.val < upper`。
3. 进入左子树时更新上界，进入右子树时更新下界。
4. BST 不允许重复值，所以边界判断必须使用 `<=` 和 `>=` 排除相等情况。
5. BFS 并非不能解决本题，但队列必须同时保存节点和上下界；不能比较层序遍历中的相邻值。
6. 中序遍历可以比较前后值，是因为合法 BST 的中序序列严格递增。
