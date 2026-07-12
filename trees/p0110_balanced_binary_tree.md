# 110. Balanced Binary Tree

## 题目

给定一棵二叉树，判断它是否为高度平衡二叉树。

一棵树平衡，需要满足：

```text
对于树中的每一个节点，左子树和右子树的高度差都不超过 1。
```

注意，不是只检查根节点。任何一棵子树不平衡，整棵树都不平衡。

## 原始思路的问题

原始代码的方向正确：使用后序遍历，先计算左右子树，再判断当前节点。

但递归函数混合了两种返回值：

```python
if not node:
    return 0
```

这里返回深度。

后面却返回：

```python
return False
return True
```

这里返回布尔值。

父节点执行：

```python
left_depth = check_balance(node.left)
```

期待得到的是左子树的真实深度，例如 `2` 或 `3`，但实际可能得到 `True` 或 `False`。

Python 中：

```python
True == 1
False == 0
```

所以代码不一定立刻报错，`abs(True - False)` 甚至可以运行，但此时比较的已经不是真实深度，结果会悄悄出错。

另外，原代码中的：

```python
ans = True
```

没有被修改或返回，可以删除。

## 递归函数的正确约定

让 `check_balance(node)` 始终返回整数：

```text
非负整数：以 node 为根的子树平衡，返回它的真实深度。
-1：以 node 为根的子树不平衡。
```

这里的 `-1` 是哨兵值，因为正常深度不可能为负数。

一个返回值同时携带了两类信息：

```text
子树是否平衡
子树的最大深度
```

## 思考顺序

### 1. 空树

空树是平衡的，深度为 `0`：

```python
if not node:
    return 0
```

### 2. 检查左子树

```python
left_depth = check_balance(node.left)
```

如果左子树已经返回 `-1`，整棵当前子树一定不平衡，可以立即向上传播：

```python
if left_depth == -1:
    return -1
```

### 3. 检查右子树

```python
right_depth = check_balance(node.right)
```

右子树不平衡时同样立即返回：

```python
if right_depth == -1:
    return -1
```

### 4. 检查当前节点

```python
if abs(left_depth - right_depth) > 1:
    return -1
```

左右子树本身都平衡，也不代表当前节点一定平衡，还必须检查它们的深度差。

### 5. 返回当前子树深度

如果左右子树和当前节点都平衡，就返回真实深度：

```python
return 1 + max(left_depth, right_depth)
```

最后只需判断根节点的递归结果是不是 `-1`：

```python
return check_balance(root) != -1
```

## 代码

```python
class Solution:
    def isBalanced(self, root: TreeNode | None) -> bool:
        def check_balance(node):
            if not node:
                return 0

            left_depth = check_balance(node.left)
            if left_depth == -1:
                return -1

            right_depth = check_balance(node.right)
            if right_depth == -1:
                return -1

            if abs(left_depth - right_depth) > 1:
                return -1

            return 1 + max(left_depth, right_depth)

        return check_balance(root) != -1
```

## 为什么返回 `max` 而不是 `min`

`check_balance(node)` 在子树平衡时返回的是：

```text
从 node 到最远叶子节点的最大深度。
```

假设：

```text
left_depth = 2
right_depth = 1
```

当前子树的最深路径应该选择左边：

```python
1 + max(2, 1) == 3
```

如果使用：

```python
1 + min(2, 1) == 2
```

得到的是较浅路径，会低估当前子树的真实高度。

父节点需要这个真实的最大深度，才能准确判断自己的左右高度差。

因此：

```text
abs(left_depth - right_depth)  用于判断当前节点是否平衡。
1 + max(left_depth, right_depth)  用于把真实深度返回给父节点。
```

这两行代码承担的职责不同。

## 为什么发现 `-1` 要立即返回

平衡二叉树要求每一个节点都平衡。

只要左子树或右子树中任意位置不平衡，当前子树就不可能重新变平衡。因此没有必要继续把 `-1` 当深度参与计算，应该直接向父节点传播。

这种写法也会提前结束不再需要的计算。

## 为什么是后序遍历

当前节点需要先知道：

```text
左子树是否平衡以及左子树深度
右子树是否平衡以及右子树深度
```

才能判断自己是否平衡，所以处理顺序是：

```text
左子树 -> 右子树 -> 当前节点
```

这是后序、自底向上的递归。

## 与 104、543 的联系

这三道题都使用相同的深度返回值：

```python
return 1 + max(left_depth, right_depth)
```

区别在于当前节点额外做什么：

| 题目 | 当前节点的处理 |
| --- | --- |
| 104. Maximum Depth | 直接返回当前深度 |
| 543. Diameter | 用 `left_depth + right_depth` 更新全局直径 |
| 110. Balanced Binary Tree | 深度差超过 `1` 时返回 `-1` |

可以把 110 理解为：

```text
104 的最大深度递归 + 不平衡哨兵 -1
```

## 为什么不能对每个节点重新计算深度

另一种直观做法是：

1. 对当前节点分别调用最大深度函数。
2. 检查当前节点是否平衡。
3. 再递归检查左右子树。

这样会反复计算同一棵子树的深度，最坏时间复杂度可能达到 O(n²)。

当前写法在一次后序遍历中同时得到深度和平衡状态，每个节点只访问一次。

## 常见错误

### 混合返回整数和布尔值

递归函数的返回含义必须统一。这里始终返回整数，`-1` 只是一个特殊整数状态。

### 子树已经不平衡却继续计算

得到 `-1` 后应立即返回 `-1`，不能把它继续当作真实深度。

### 平衡时只返回 `True`

父节点还需要当前子树深度，返回 `True` 会丢失信息。

### 使用 `min` 返回较浅深度

平衡判断需要知道真实的最大高度，所以必须返回 `1 + max(...)`。

### 只检查根节点

根节点左右高度差不超过 `1`，不代表它的内部子树也平衡。必须在后序遍历中检查每个节点。

## 复杂度

时间复杂度：O(n)，每个节点最多访问一次。

辅助空间复杂度：O(h)，`h` 是树高，对应递归调用栈。

- 平衡树中约为 O(log n)。
- 树退化成链表时最坏为 O(n)。

## 心得

1. 递归函数的返回类型和含义必须保持一致，不能让父节点猜测拿到的是深度还是布尔值。
2. 可以使用正常结果范围之外的值作为哨兵，例如用 `-1` 表示“不平衡”。
3. 判断当前节点是否平衡要比较左右深度；返回给父节点时要返回较深一侧加当前节点。
4. 104、543、110 的主体都是同一个后序深度模板，区别只在当前节点如何使用左右深度。
