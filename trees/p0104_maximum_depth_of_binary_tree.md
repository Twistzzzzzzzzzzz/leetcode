# 104. Maximum Depth of Binary Tree

## 题目

给定一棵二叉树的根节点 `root`，返回这棵树的最大深度。

最大深度是从根节点到最远叶子节点所经过的节点数量。

例如：

```text
        3
       / \
      9   20
         /  \
        15   7
```

最长路径可以是：

```text
3 -> 20 -> 15
```

一共有 3 个节点，所以最大深度是 `3`。

注意：这题计算的是节点数，不是边数。

## 看到树题时的固定思考顺序

### 第一步：明确题目要返回什么

先判断答案类型：

```text
一个值、一个节点，还是一个列表？
```

104 要返回一个整数，表示树的最大深度。

### 第二步：定义递归函数

写代码前，先强制说出一句完整的话：

```text
dfs(node) 返回以 node 为根的二叉树的最大深度。
```

这是整道题最重要的定义。

如果不清楚 `dfs(node)` 返回什么，就无法判断空节点应该返回什么，也无法组合左右子树的结果。

### 第三步：确定空节点的 base case

空树没有节点，因此深度是 `0`：

```python
if not node:
    return 0
```

不能只判断叶子节点：

```python
if not node.left and not node.right:
```

因为传入的 `node` 本身可能就是 `None`，这时访问 `node.left` 会报错。

### 第四步：递归获得左右子树结果

根据刚才定义的递归函数：

```python
left_depth = dfs(node.left)
right_depth = dfs(node.right)
```

它们分别表示：

```text
left_depth   左子树的最大深度
right_depth  右子树的最大深度
```

这里不要继续展开所有递归层。先相信 `dfs` 能正确处理规模更小的左右子树。

### 第五步：组合左右结果

从当前节点到叶子的路径只能选择左边或右边较深的一条，因此使用 `max`：

```python
max(left_depth, right_depth)
```

当前节点自己还占一层，所以：

```python
return 1 + max(left_depth, right_depth)
```

这里的 `1` 代表当前节点。

### 第六步：从根节点启动递归

```python
return dfs(root)
```

## 代码

```python
class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        def dfs(node):
            if not node:
                return 0

            left_depth = dfs(node.left)
            right_depth = dfs(node.right)

            return 1 + max(left_depth, right_depth)

        return dfs(root)
```

## 为什么这是后序遍历

主要代码顺序是：

```python
left_depth = dfs(node.left)
right_depth = dfs(node.right)
return 1 + max(left_depth, right_depth)
```

也就是：

```text
左子树 -> 右子树 -> 当前节点
```

当前节点必须先知道左右子树有多深，才能计算自己的深度，所以这是后序遍历思想。

以后遇到下面这种关系时，可以优先想到后序：

```text
当前节点的答案依赖左右子树返回的结果。
```

典型题包括：

- 104. Maximum Depth of Binary Tree
- 110. Balanced Binary Tree
- 543. Diameter of Binary Tree
- 124. Binary Tree Maximum Path Sum

## 递归展开

对于：

```text
        3
       / \
      9   20
         /  \
        15   7
```

左子树：

```text
dfs(9)
    dfs(None) -> 0
    dfs(None) -> 0
    return 1 + max(0, 0) -> 1
```

右子树：

```text
dfs(20)
    dfs(15) -> 1
    dfs(7)  -> 1
    return 1 + max(1, 1) -> 2
```

回到根节点：

```text
dfs(3)
    left_depth = 1
    right_depth = 2
    return 1 + max(1, 2) -> 3
```

递归返回值会从叶子逐层向上传递，因此这种方式也叫自底向上。

## 通用返回值型树递归模板

```python
def dfs(node):
    if not node:
        return base_result

    left_result = dfs(node.left)
    right_result = dfs(node.right)

    current_result = combine(node, left_result, right_result)
    return current_result
```

104 对应：

```text
base_result = 0
left_result = 左子树深度
right_result = 右子树深度
combine = 1 + max(left_result, right_result)
```

## 另一种写法：自顶向下

也可以把当前深度从父节点传给孩子：

```python
class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        answer = 0

        def dfs(node, depth):
            nonlocal answer

            if not node:
                return

            answer = max(answer, depth)

            dfs(node.left, depth + 1)
            dfs(node.right, depth + 1)

        dfs(root, 1)
        return answer
```

这个版本中：

```text
dfs(node, depth) 表示当前来到 node，并且 node 位于第 depth 层。
```

它先处理当前节点，再把深度传给孩子，因此属于前序、自顶向下的思路。

104 两种方式都可以完成，但后序返回值写法更自然，因为不需要额外维护 `answer`。

## 如何判断前序还是后序

问自己：

```text
处理当前节点时，是否必须先知道左右子树的结果？
```

- 如果需要，通常使用后序，让孩子把结果返回给父节点。
- 如果不需要，而是要把当前状态传给孩子，通常使用前序。

| 类型 | 信息方向 | 常见代码 |
| --- | --- | --- |
| 前序 / 自顶向下 | 父节点把信息传给孩子 | `dfs(child, depth + 1)` |
| 后序 / 自底向上 | 孩子把结果返回给父节点 | `left = dfs(node.left)` |

## 常见错误

### 忘记处理空树

错误：

```python
if not root.left and not root.right:
```

当 `root` 是 `None` 时会报错。

正确：

```python
if not node:
    return 0
```

### 忘记计算当前节点

错误：

```python
return max(left_depth, right_depth)
```

正确：

```python
return 1 + max(left_depth, right_depth)
```

### 把左右深度相加

错误：

```python
return 1 + left_depth + right_depth
```

一条从当前节点到叶子的向下路径只能选择一侧，不能同时经过左右子树。

正确：

```python
return 1 + max(left_depth, right_depth)
```

左右相加会在后面的“二叉树直径”中出现，但那时计算的是一条可能经过当前节点、连接左右两侧的路径，不是最大深度。

### 没有定义递归函数的返回值

树递归写不下去，最常见的原因不是不会递归，而是没有先说清楚：

```text
dfs(node) 到底返回什么？
```

只要这句话明确，base case 和递推关系通常都会自然出现。

## 复杂度

时间复杂度：O(n)，每个节点访问一次。

辅助空间复杂度：O(h)，`h` 是树高，对应递归调用栈。

- 平衡树中约为 O(log n)。
- 树退化成链表时最坏为 O(n)。

## 心得

看到树题时，可以固定问五句话：

1. `dfs(node)` 表示什么？
2. `node` 为空时返回什么？
3. 左子树会返回什么？
4. 右子树会返回什么？
5. 当前节点如何组合左右结果？

套到 104：

```text
dfs(node) 返回当前子树的最大深度。
空树深度是 0。
左右递归分别返回左右子树深度。
当前深度 = 1 + max(左深度, 右深度)。
```

不要试图同时在脑中展开整棵树。先相信已经定义好的递归函数能够返回子问题答案，再处理当前节点。
