# 树基础

树专题通常是第一次大量接触递归的地方，但必须先修正一个容易形成的印象：

```text
树题不等于递归题。
```

更准确地说：

| 层次 | 含义 | 例子 |
| --- | --- | --- |
| 数据结构 | 数据怎样组织 | 二叉树、BST |
| 遍历策略 | 按什么顺序访问 | DFS、BFS |
| 实现方式 | 代码怎样保存待处理状态 | 递归、`while + stack`、`while + queue` |

它们之间的常见关系是：

```text
Tree
├── DFS
│   ├── 递归
│   └── stack + while
└── BFS
    └── queue + while
```

递归是 DFS 的常见实现，不是所有树题的固定写法。看到题目后，应该先判断需要 DFS 还是 BFS，再选择递归或迭代实现。

刚开始看树题时，很容易觉得每个节点都会继续分成左右两边，脑子里要同时记住很多层。实际上，大多数二叉树题都可以统一成一个问题：

```text
当前节点要做什么？
左子树能帮我解决什么？
右子树能帮我解决什么？
怎样把左右子树的结果合并成当前节点的结果？
```

对于适合递归 DFS 的题，真正要练的不是把整棵树一次性想完，而是先定义好递归函数的职责，然后相信它能正确处理一棵更小的子树。

## 一棵二叉树长什么样

例如：

```text
        1
       / \
      2   3
     / \   \
    4   5   6
```

常用术语：

| 名称 | 含义 |
| --- | --- |
| 根节点 root | 最上面的节点，这里是 `1` |
| 父节点 parent | 直接连接在某个节点上方的节点 |
| 子节点 child | 直接连接在某个节点下方的节点 |
| 左子树 / 右子树 | 某个节点左边 / 右边的整棵子树 |
| 叶子节点 leaf | 没有左孩子也没有右孩子的节点，这里是 `4`、`5`、`6` |
| 深度 depth | 从根走到当前节点的距离 |
| 高度 height | 从当前节点向下走到最远叶子的距离 |

最重要的结构是“子树”。

对根节点 `1` 来说：

```text
以 2 为根的部分，是 1 的左子树。
以 3 为根的部分，是 1 的右子树。
```

而以 `2` 为根的部分本身又是一棵完整的二叉树。这种“整体和局部拥有相同结构”的特点，正是递归特别适合处理树的原因。

## Python 里的 TreeNode

LeetCode 通常会提供：

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

一个节点只保存三样东西：

```text
val    当前值
left   左孩子
right  右孩子
```

如果没有某一侧孩子，对应引用就是 `None`。

例如：

```python
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
```

得到：

```text
    1
   / \
  2   3
```

树和链表有一点相似：节点都通过引用连接，不支持像数组那样用下标随机访问。

区别是链表通常只有一个 `next`，二叉树的每个节点最多有 `left` 和 `right` 两个方向。

## 二叉树不等于二叉搜索树

这两个概念一定要分清。

普通二叉树只要求每个节点最多有两个孩子，不保证值的大小关系。

二叉搜索树 Binary Search Tree，简称 BST，还要求：

```text
当前节点左子树中的所有值 < 当前节点值
当前节点右子树中的所有值 > 当前节点值
```

所以普通二叉树不能因为 `target < node.val` 就只往左走。只有题目明确说明是 BST 时，才能使用这种有序性质。

## 为什么前面的树题经常使用递归 DFS

假设要计算一棵树的最大深度。

根节点的最大深度等于：

```text
1 + max(左子树最大深度, 右子树最大深度)
```

而“求左子树最大深度”与原问题完全相同，只是输入规模更小。

这就是递归：

```python
def maxDepth(root):
    if not root:
        return 0

    left_depth = maxDepth(root.left)
    right_depth = maxDepth(root.right)

    return 1 + max(left_depth, right_depth)
```

不要在第一眼就尝试同时跟踪所有递归层。先读懂这个函数的约定：

```text
maxDepth(node) 返回以 node 为根的树的最大深度。
```

只要左右递归遵守这个约定，当前节点就能用它们的结果算出自己的答案。

## 写递归前必须回答的三个问题

### 1. 这个函数的职责是什么

一定要用一句完整的话定义返回值。

例如：

```text
dfs(node) 返回以 node 为根的子树高度。
dfs(node) 返回以 node 为根的子树是否平衡。
dfs(node) 返回以 node 为根的子树中是否存在目标路径。
```

“遍历一下这棵树”不是足够清楚的函数定义，因为它没有说明递归调用之后能得到什么。

### 2. 空节点返回什么

这就是递归终止条件，也叫 base case。

常见情况：

```python
if not node:
    return 0       # 高度、节点数、总和
```

```python
if not node:
    return True    # 判断两棵空树相同、空树平衡等
```

```python
if not node:
    return None    # 查找节点、构造结果
```

返回什么不能死记，要根据函数职责决定。

### 3. 当前节点如何组合左右结果

最通用的树递归骨架是：

```python
def dfs(node):
    if not node:
        return base_value

    left_result = dfs(node.left)
    right_result = dfs(node.right)

    return combine(node, left_result, right_result)
```

不同题目的主要区别，往往只在：

```text
base_value 是什么？
left_result / right_result 表示什么？
combine 应该怎样写？
```

## 深度和高度

这两个词经常混淆。

一般概念上：

```text
节点深度：从根向下走到这个节点。
节点高度：从这个节点向下走到最远叶子。
```

不过 LeetCode 的 Maximum Depth of Binary Tree 通常按“节点数”计算：

```text
空树深度 = 0
只有根节点的树深度 = 1
```

所以代码是：

```python
return 1 + max(left_depth, right_depth)
```

做题时不要只纠结名词，先看清题目对长度的定义是计算节点还是计算边。

## DFS：深度优先搜索

DFS 会沿着一条分支尽量向下走，再回来处理其他分支。

二叉树 DFS 有三种经典顺序。顺序名称取决于“根节点什么时候处理”。

仍然使用这棵树：

```text
        1
       / \
      2   3
     / \   \
    4   5   6
```

### 前序遍历：根、左、右

```text
1, 2, 4, 5, 3, 6
```

模板：

```python
def preorder(node):
    if not node:
        return

    process(node)
    preorder(node.left)
    preorder(node.right)
```

前序遍历先知道父节点的信息，再进入孩子，适合从上向下传递状态。

常见场景：

- 复制或序列化树
- 记录从根到当前节点的路径
- 当前节点的状态依赖祖先状态
- 翻转树、构造输出

### 中序遍历：左、根、右

```text
4, 2, 5, 1, 3, 6
```

模板：

```python
def inorder(node):
    if not node:
        return

    inorder(node.left)
    process(node)
    inorder(node.right)
```

中序遍历最重要的用途是处理 BST。

BST 的中序遍历结果是递增序列：

```text
左子树较小 -> 当前节点 -> 右子树较大
```

典型题：

- Validate Binary Search Tree
- Kth Smallest Element in a BST
- Binary Search Tree Iterator

### 后序遍历：左、右、根

```text
4, 5, 2, 6, 3, 1
```

模板：

```python
def postorder(node):
    if not node:
        return

    postorder(node.left)
    postorder(node.right)
    process(node)
```

后序遍历先拿到左右子树的结果，再计算当前节点，适合从下向上汇总信息。

常见场景：

- 最大深度 / 高度
- 判断平衡二叉树
- 二叉树直径
- 删除树
- 最近公共祖先

### 怎么记住三种顺序

只看“根”放在哪里：

```text
前序：根左右
中序：左根右
后序：左右根
```

左右的相对顺序通常不变，变化的是处理根节点的时机。

## 递归代码属于哪种遍历

不一定非要看到 `print(node.val)` 才能判断遍历顺序。

例如最大深度：

```python
left_depth = dfs(node.left)
right_depth = dfs(node.right)
return 1 + max(left_depth, right_depth)
```

当前节点必须等左右结果都回来以后才能返回，因此它本质上是后序遍历。

判断方法：

```text
进入左右子树前处理当前节点：前序。
左子树结束、右子树开始前处理当前节点：中序。
左右子树都结束后处理当前节点：后序。
```

## 自顶向下和自底向上

树题还有另一种非常实用的分类。

### 自顶向下：把状态传给孩子

当前节点先根据父节点传来的信息更新状态，再继续递归。

例如记录当前深度：

```python
def dfs(node, depth):
    if not node:
        return

    # 当前节点的深度已经确定
    dfs(node.left, depth + 1)
    dfs(node.right, depth + 1)
```

适合：

- 根到叶路径
- 路径和
- 祖先信息
- 当前深度

### 自底向上：让孩子把结果返回给父亲

当前节点先等待左右子树算完，再组合结果。

```python
def dfs(node):
    if not node:
        return 0

    left = dfs(node.left)
    right = dfs(node.right)

    return 1 + max(left, right)
```

适合：

- 高度
- 平衡判断
- 直径
- 最近公共祖先

一个简单判断：

```text
信息从父节点流向孩子：自顶向下。
答案从孩子返回父节点：自底向上。
```

## BFS：广度优先搜索 / 层序遍历

BFS 按层处理节点：

```text
第 1 层：1
第 2 层：2, 3
第 3 层：4, 5, 6
```

Python 通常用 `collections.deque`：

```python
from collections import deque


def level_order(root):
    if not root:
        return []

    queue = deque([root])
    result = []

    while queue:
        level = []
        level_size = len(queue)

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result
```

为什么要先保存：

```python
level_size = len(queue)
```

因为处理当前层时会不断把下一层节点加入队列。如果直接按变化中的队列长度循环，就会把不同层混在一起。

### 为什么使用 `deque`

BFS 需要先进先出的队列：从队头取出最早加入的节点，从队尾加入新发现的节点。

Python 的 `deque` 支持：

```python
queue.append(node)  # 队尾加入，O(1)
queue.popleft()     # 队头取出，O(1)
```

普通列表的 `pop(0)` 是 O(n)，因为删除第一个元素后，后面的元素都要向前移动。

| 操作 | `list` | `deque` |
| --- | --- | --- |
| 尾部 `append` | O(1) | O(1) |
| 尾部 `pop` | O(1) | O(1) |
| 头部删除 | `pop(0)`，O(n) | `popleft()`，O(1) |
| 常见用途 | 数组、栈 | 队列、BFS |

也可以使用列表加读取下标来避免 `pop(0)`，但 BFS 的标准写法仍然是 `deque + popleft()`。

BFS 常见场景：

- 按层输出
- 找最小深度
- 找离根最近的目标
- 每层最大值 / 平均值
- 连接每层相邻节点
- 二叉树右视图

## DFS 和 BFS 怎么选

看到树题时不要先问“递归还是 `while`”，先问题目强调什么访问顺序。

| 题目信号 | 优先考虑 |
| --- | --- |
| 需要左右子树的返回值 | DFS，通常用递归实现 |
| 深度、高度、平衡、直径 | DFS，通常是后序递归 |
| 根到叶路径 | DFS + 回溯 |
| 按层处理、第 `k` 层 | BFS + queue |
| 找最浅、最近、最少层数 | BFS + queue |
| BST 第 k 小 | 中序 DFS |

DFS 和 BFS 有时都能完成同一道题，选择更贴合题意、状态更简单的写法即可。

同一种遍历策略也可以有不同实现：

| 遍历策略 | 常见实现 |
| --- | --- |
| DFS | 递归，或者 `while + stack` |
| BFS | `while + queue` |

层序遍历也能使用 DFS 并传入 `depth`，再把节点放入对应层；但实际访问顺序仍是 DFS。题目直接要求逐层处理时，BFS 更符合语义。

## 路径题与回溯

路径题经常需要维护当前路径：

```python
path = []


def dfs(node):
    if not node:
        return

    path.append(node.val)

    if not node.left and not node.right:
        # 到达叶子，使用当前路径
        result.append(path[:])

    dfs(node.left)
    dfs(node.right)

    path.pop()
```

这里的三个阶段是：

```text
做选择：path.append(node.val)
递归：进入左右子树
撤销选择：path.pop()
```

为什么保存答案时要写：

```python
result.append(path[:])
```

因为 `path` 是同一个可变列表。直接保存 `path`，后面的 `append` / `pop` 会继续改变已经放进答案里的对象。

### 叶子节点怎么判断

必须同时没有左右孩子：

```python
if not node.left and not node.right:
```

只写 `if not node.left` 不代表叶子，因为它可能还有右孩子。

## 高度、平衡和直径

这一组题非常适合学习“递归返回值”和“最终答案”的区别。

### 最大深度

递归返回值就是题目答案：

```python
def dfs(node):
    if not node:
        return 0

    left_height = dfs(node.left)
    right_height = dfs(node.right)

    return 1 + max(left_height, right_height)
```

### 判断平衡二叉树

每个节点都需要知道左右子树高度。

朴素做法会反复计算高度。更好的做法是让递归同时传递：

```text
正常高度：子树平衡。
-1：子树已经不平衡。
```

```python
def height(node):
    if not node:
        return 0

    left = height(node.left)
    if left == -1:
        return -1

    right = height(node.right)
    if right == -1:
        return -1

    if abs(left - right) > 1:
        return -1

    return 1 + max(left, right)
```

这是一个重要优化思路：把额外状态放进递归返回值，避免重复遍历。

### 二叉树直径

经过当前节点的最长路径为：

```text
左子树高度 + 右子树高度
```

但递归返回给父节点的只能是其中较长的一条向下路径：

```text
1 + max(左高度, 右高度)
```

所以这里有两个不同概念：

```text
递归返回值：父节点还能继续使用的单边高度。
全局答案：目前见过的最大直径。
```

这类题写代码前一定要分别说清楚“函数返回什么”和“最终答案是什么”。

## 二叉搜索树 BST

BST 的核心性质是有序。

### 搜索

```python
def search_bst(node, target):
    if not node or node.val == target:
        return node

    if target < node.val:
        return search_bst(node.left, target)

    return search_bst(node.right, target)
```

平衡 BST 搜索平均是 O(log n)，但如果树退化成链表，最坏仍然是 O(n)。

### 中序遍历递增

```python
def inorder(node):
    if not node:
        return

    inorder(node.left)
    values.append(node.val)
    inorder(node.right)
```

得到的 `values` 按递增顺序排列。

### 验证 BST 不能只比较父子节点

下面这棵树：

```text
        5
       / \
      1   7
         / \
        4   8
```

节点 `4 < 7`，看起来符合它与父节点的关系；但 `4` 位于根节点 `5` 的右子树中，应该大于 `5`，所以整棵树不是 BST。

因此验证 BST 时，要把祖先带来的上下界一起向下传：

```python
def valid(node, lower, upper):
    if not node:
        return True

    if not lower < node.val < upper:
        return False

    return (
        valid(node.left, lower, node.val)
        and valid(node.right, node.val, upper)
    )
```

初始调用：

```python
valid(root, float("-inf"), float("inf"))
```

左子树更新上界，右子树更新下界。

## 比较、翻转和对称

这类题通常同时递归两棵子树或两组节点。

### 判断两棵树是否相同

每一步检查：

```text
两个节点都为空：相同。
只有一个为空：不同。
值不同：不同。
左右子树也必须分别相同。
```

```python
def same(a, b):
    if not a and not b:
        return True

    if not a or not b:
        return False

    return (
        a.val == b.val
        and same(a.left, b.left)
        and same(a.right, b.right)
    )
```

### 翻转二叉树

每个节点交换左右孩子，再递归处理两边：

```python
def invert(node):
    if not node:
        return None

    node.left, node.right = invert(node.right), invert(node.left)
    return node
```

### 对称二叉树

对称不是比较：

```text
左.left 和 右.left
左.right 和 右.right
```

而是镜像比较：

```text
左.left 和 右.right
左.right 和 右.left
```

## 最近公共祖先 LCA

普通二叉树中的最近公共祖先很适合后序遍历。

递归函数可以定义为：

```text
在以 node 为根的子树中寻找 p 或 q；
如果两边分别找到，则 node 是最近公共祖先。
```

核心结构：

```python
def lowest_common_ancestor(node, p, q):
    if not node or node == p or node == q:
        return node

    left = lowest_common_ancestor(node.left, p, q)
    right = lowest_common_ancestor(node.right, p, q)

    if left and right:
        return node

    return left if left else right
```

这里也是先得到左右子树结果，再决定当前节点返回什么，因此是后序思路。

## 构造二叉树

构造题经常给两种遍历顺序。

必须记住：

```text
前序遍历第一个元素是根。
后序遍历最后一个元素是根。
中序遍历中，根左边属于左子树，根右边属于右子树。
```

例如用前序和中序构造：

```text
preorder = [3, 9, 20, 15, 7]
inorder  = [9, 3, 15, 20, 7]
```

步骤：

1. 从前序找到根 `3`。
2. 在中序中找到 `3`，左边 `[9]` 是左子树，右边 `[15, 20, 7]` 是右子树。
3. 对左右区间递归做相同的事。

构造题的核心仍然是：找到根、划分左右子树、递归构造。

## 递归返回值和全局变量

树题经常同时出现这两类状态。

### 能通过父子关系组合的结果，优先 return

例如高度：

```python
return 1 + max(left_height, right_height)
```

### 需要记录整棵树中的最大值，可以使用外部答案

例如直径：

```python
self.answer = max(self.answer, left_height + right_height)
```

但使用 `self.answer` 前，每次调用主函数都要初始化：

```python
self.answer = 0
```

否则同一个 `Solution` 对象多次调用时可能残留上一次结果。

写题前分开回答：

```text
dfs 返回给父节点什么？
题目最终要求返回什么？
```

这能避免大量递归逻辑混乱。

## 递归与显式栈

递归 DFS 的背后也使用栈，只是这个栈由 Python 调用栈管理。

递归写法：

```python
def dfs(node):
    if not node:
        return

    dfs(node.left)
    dfs(node.right)
```

迭代 DFS 会自己维护：

```python
stack = [root]

while stack:
    node = stack.pop()
```

当前阶段先把递归写熟。等你能稳定写出前序、中序、后序之后，再练迭代版本会更自然。

## 时间和空间复杂度

大多数需要访问每个节点一次的树题：

```text
时间复杂度：O(n)
```

DFS 递归空间取决于树高 `h`：

```text
平衡树：O(log n)
最坏退化成链表：O(n)
```

BFS 队列空间取决于最宽一层的节点数 `w`：

```text
空间复杂度：O(w)
最坏是 O(n)
```

不要看到递归就自动写空间 O(n)，更准确的写法是 O(h)，再补充最坏情况。

## 常见错误

### 1. 没有先定义递归函数的返回值

一边写一边决定 `return` 什么，最容易混乱。

先写一句：

```text
dfs(node) 返回 ______。
```

再开始写代码。

### 2. base case 与函数职责不匹配

空节点有时返回 `0`，有时返回 `True`，有时返回 `None`。不能统一背成一种。

### 3. 忘记接住递归返回值

错误：

```python
dfs(node.left)
dfs(node.right)
return 1
```

如果当前结果依赖子树，就应该保存：

```python
left = dfs(node.left)
right = dfs(node.right)
```

### 4. 路径回溯忘记 `pop`

进入节点时 `append`，离开节点时通常要 `pop`，否则一条分支的节点会污染另一条分支。

### 5. 把“没有左孩子”误认为叶子

叶子必须同时满足：

```python
not node.left and not node.right
```

### 6. 验证 BST 只比较当前节点和孩子

BST 的约束来自所有祖先。应使用上下界，或检查完整中序序列严格递增。

### 7. BFS 把不同层混在一起

每轮开始先保存当前层大小：

```python
level_size = len(queue)
```

### 8. 混淆节点数和边数

最大深度通常数节点；直径题通常数边。以题目定义和示例为准。

### 9. 在递归函数里重复计算同一棵子树

例如判断平衡时，对每个节点重新计算高度会退化到 O(n²)。可以让一次 DFS 同时返回高度和异常状态。

### 10. 认为二叉树一定平衡

普通二叉树可能完全向一侧倾斜：

```text
1
 \
  2
   \
    3
```

因此递归深度最坏可能是 O(n)，BST 操作最坏也可能是 O(n)。

## 看到树题时的固定思考流程

1. 输入可能是 `None` 吗？空树应该返回什么？
2. 这是普通二叉树还是 BST？能不能使用有序性质？
3. 题目要求按层处理吗？如果是，优先 BFS。
4. 如果使用 DFS，递归函数的职责是什么？
5. 信息是从父亲传给孩子，还是从孩子返回父亲？
6. 当前节点应该在递归前、中间还是递归后处理？
7. 是否需要维护路径？如果需要，离开节点时是否要回溯？
8. `dfs` 返回值和最终答案是否是同一个东西？
9. 长度计算的是节点还是边？
10. 时间复杂度是否每个节点只处理一次？

## 题型地图

### A. 基础递归与遍历

代表题：

- 104. Maximum Depth of Binary Tree
- 100. Same Tree
- 226. Invert Binary Tree
- 101. Symmetric Tree
- 144. Binary Tree Preorder Traversal
- 94. Binary Tree Inorder Traversal
- 145. Binary Tree Postorder Traversal

重点：

- base case
- 定义递归职责
- 前序 / 中序 / 后序

### B. 层序遍历

代表题：

- 102. Binary Tree Level Order Traversal
- 199. Binary Tree Right Side View
- 637. Average of Levels in Binary Tree
- 111. Minimum Depth of Binary Tree

重点：

- `deque`
- 当前层大小
- 一层处理完成后更新答案

### C. 高度和后序汇总

代表题：

- 110. Balanced Binary Tree
- 543. Diameter of Binary Tree
- 124. Binary Tree Maximum Path Sum

重点：

- 左右子树返回什么
- 当前节点如何组合结果
- 递归返回值与全局答案的区别

### D. 路径和回溯

代表题：

- 112. Path Sum
- 113. Path Sum II
- 257. Binary Tree Paths
- 437. Path Sum III

重点：

- 根到叶还是任意节点之间
- `append` / `pop`
- 保存路径时复制列表

### E. 二叉搜索树

代表题：

- 700. Search in a Binary Search Tree
- 98. Validate Binary Search Tree
- 230. Kth Smallest Element in a BST
- 235. Lowest Common Ancestor of a Binary Search Tree
- 450. Delete Node in a BST

重点：

- 左小右大
- 中序遍历递增
- 上下界来自祖先

### F. 构造与公共祖先

代表题：

- 105. Construct Binary Tree from Preorder and Inorder Traversal
- 106. Construct Binary Tree from Inorder and Postorder Traversal
- 108. Convert Sorted Array to Binary Search Tree
- 236. Lowest Common Ancestor of a Binary Tree

重点：

- 遍历顺序中根的位置
- 用中序划分左右子树
- 后序汇总左右查找结果

## 推荐刷题顺序

1. 94. Binary Tree Inorder Traversal
2. 144. Binary Tree Preorder Traversal
3. 145. Binary Tree Postorder Traversal
4. 226. Invert Binary Tree
5. 104. Maximum Depth of Binary Tree
6. 543. Diameter of Binary Tree
7. 110. Balanced Binary Tree
8. 100. Same Tree
9. 572. Subtree of Another Tree
10. 235. Lowest Common Ancestor of a Binary Search Tree
11. 701. Insert into a Binary Search Tree
12. 450. Delete Node in a BST
13. 102. Binary Tree Level Order Traversal
14. 101. Symmetric Tree
15. 112. Path Sum
16. 199. Binary Tree Right Side View
17. 98. Validate Binary Search Tree
18. 230. Kth Smallest Element in a BST
19. 236. Lowest Common Ancestor of a Binary Tree
20. 105. Construct Binary Tree from Preorder and Inorder Traversal
21. 124. Binary Tree Maximum Path Sum

前 3 题先用同一个模板掌握前序、中序和后序。

第 4 到 7 题连续练习前序修改、深度返回、全局答案和失败哨兵。

第 8 到 16 题练树的比较、子树搜索、BST 搜索与修改、BFS 和路径。

第 13 到 17 题进入 BST、公共祖先和构造树。

124 是 Hard，最后再做。

## 必背模板

### 模板 1：通用递归

```python
def dfs(node):
    if not node:
        return base_value

    left = dfs(node.left)
    right = dfs(node.right)

    return combine(node, left, right)
```

### 模板 2：最大深度

```python
def max_depth(node):
    if not node:
        return 0

    left = max_depth(node.left)
    right = max_depth(node.right)

    return 1 + max(left, right)
```

### 模板 3：层序遍历

```python
from collections import deque


def level_order(root):
    if not root:
        return []

    queue = deque([root])
    result = []

    while queue:
        level = []
        level_size = len(queue)

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result
```

### 模板 4：路径回溯

```python
def dfs(node, path):
    if not node:
        return

    path.append(node.val)

    if not node.left and not node.right:
        result.append(path[:])

    dfs(node.left, path)
    dfs(node.right, path)

    path.pop()
```

### 模板 5：验证 BST 上下界

```python
def valid(node, lower, upper):
    if not node:
        return True

    if not lower < node.val < upper:
        return False

    return (
        valid(node.left, lower, node.val)
        and valid(node.right, node.val, upper)
    )
```

## 当前学习目标

进入树专题后，先完成这些目标：

1. 能画出根、左右子树和叶子节点。
2. 能用一句话定义 `dfs(node)` 的返回值。
3. 能稳定写出最大深度递归。
4. 能说清前序、中序、后序的区别。
5. 能用 `deque` 写层序遍历。
6. 能区分自顶向下传状态和自底向上返回结果。
7. 能在路径题中正确 `append`、复制答案、`pop`。
8. 能记住 BST 中序有序，但验证 BST 需要考虑祖先边界。

树专题最重要的一句话：

```text
不要试图一次想完整棵树；先定义当前递归函数能替你解决什么子问题。
```

三种基础遍历之后，依次用 226、104、543 和 110 练习不同的递归状态：

```text
226. Invert Binary Tree
104. Maximum Depth of Binary Tree
543. Diameter of Binary Tree
110. Balanced Binary Tree
```
