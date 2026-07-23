# Backtracking / 回溯基础

## 1. 回溯是什么

回溯是一种系统枚举所有可能选择的搜索方法。

它适合解决：

```text
需要一步一步做选择
+
每一步有多个候选
+
题目要求找出所有合法结果，或者判断是否存在合法结果
```

可以把回溯理解成：

```text
做一个选择
继续深入
撤销这个选择
尝试下一个选择
```

最经典的动作是：

```python
path.append(choice)
backtrack(...)
path.pop()
```

其中：

- `append`：做选择；
- 递归：沿当前选择继续搜索；
- `pop`：撤销选择，恢复现场。

## 2. 回溯不是一种独立的数据结构

回溯通常由以下内容组合而成：

```text
递归
+
DFS 深度优先搜索
+
状态修改与撤销
```

需要区分三个概念。

### 递归

递归是一种函数调用自己的实现方式。

它回答：

```text
代码如何进入下一层？
```

### DFS

DFS 是一种优先沿一条分支深入到底，再返回尝试其他分支的遍历策略。

它回答：

```text
搜索树按照什么顺序遍历？
```

### Backtracking

回溯是在 DFS 搜索过程中：

```text
尝试选择
检查约束
深入搜索
撤销选择
```

它回答：

```text
如何枚举选择，并让不同分支互不污染？
```

可以记成：

```text
递归是实现方式
DFS 是搜索顺序
Backtracking 是带选择与撤销的搜索框架
```

大多数回溯使用递归 DFS，但不是所有递归题或 DFS 题都是回溯。

例如求二叉树最大深度，虽然使用递归 DFS，却没有反复尝试和撤销选择，因此通常不称为回溯。

## 3. 把问题想成一棵决策树

回溯题最重要的抽象不是数组，而是决策树。

假设：

```text
nums = [1, 2, 3]
```

构造子集时：

```text
根节点：[]

选择 1：
    [1]
    再选择 2：
        [1, 2]
        再选择 3：
            [1, 2, 3]
    再选择 3：
        [1, 3]

选择 2：
    [2]
    再选择 3：
        [2, 3]

选择 3：
    [3]
```

决策树中的含义：

```text
节点：当前已经做出的选择
边：下一步选择了什么
深度：已经做了多少步选择
叶子：一个完整结果，或者已经无法继续
```

回溯就是深度优先遍历这棵隐式决策树。

题目通常不会真的给出这棵树；我们通过递归参数和 `path` 动态表示当前所在位置。

## 4. 每道回溯题固定先问四个问题

### 问题一：当前路径是什么

`path` 表示从决策树根节点走到当前节点时，已经选择了什么。

例如：

- 子集题：已经选中的数字；
- 排列题：当前排列；
- 分割题：已经切出的字符串片段；
- N 皇后：已经放置的皇后位置；
- 单词搜索：当前已经匹配的字符路径。

### 问题二：当前有哪些候选选择

候选可能来自：

- `nums[start:]`；
- 所有尚未使用的元素；
- 当前格子的四个方向；
- 可以放皇后的列；
- 左括号或右括号；
- 当前起点后的所有切割终点。

### 问题三：什么选择不合法

约束可能是：

- 元素不能重复使用；
- 总和不能超过目标值；
- 同一层不能选择相同数值；
- 括号不能出现右括号多于左括号；
- 格子不能重复访问；
- 皇后不能同列或同对角线；
- 当前字符串片段必须是回文。

### 问题四：什么时候得到一个结果

常见结束条件：

- 所有位置都处理完成；
- `path` 长度达到 `k`；
- `remaining == 0`；
- 字符串已经切到末尾；
- 单词所有字符已经匹配；
- 棋盘所有行都放置完成。

可以把这四问记成：

```text
路径是什么？
候选是什么？
约束是什么？
何时收集答案？
```

## 5. 回溯通用模板

```python
result = []
path = []


def backtrack(state):
    if 满足结束条件:
        result.append(path[:])
        return

    for choice in 当前候选:
        if choice 不合法:
            continue

        path.append(choice)
        更新其他状态

        backtrack(下一层状态)

        恢复其他状态
        path.pop()
```

模板中真正需要根据题目决定的是：

1. `state` 参数代表什么；
2. 当前候选从哪里开始；
3. 什么条件需要剪枝；
4. 下一层参数是 `i` 还是 `i + 1`；
5. 哪些状态需要撤销；
6. 哪个时刻收集答案。

不要只背 `append -> dfs -> pop`，必须先说明每个状态的含义。

## 6. 为什么必须撤销选择

同一个 `path` 列表会被所有递归分支复用。

例如当前：

```python
path = [1]
```

选择 2 后：

```python
path = [1, 2]
```

搜索完以 `[1, 2]` 开头的全部结果后，如果不执行：

```python
path.pop()
```

下一次选择 3 时，路径会错误地变成：

```text
[1, 2, 3]
```

但正确的新分支应该从 `[1]` 出发：

```text
[1, 3]
```

所以回溯的本质是：

```text
递归返回后，把共享状态恢复到进入这一层之前
```

## 7. 为什么保存答案时要复制路径

错误写法：

```python
result.append(path)
```

这会把同一个列表对象的引用加入 `result`。

后面继续执行：

```python
path.append(...)
path.pop()
```

已经保存的结果也会跟着变化。

正确写法：

```python
result.append(path[:])
```

也可以写：

```python
result.append(list(path))
```

需要复制的是可变路径对象。

如果保存的是不可变字符串，例如：

```python
result.append("".join(path))
```

生成的新字符串本身已经独立，不需要再复制。

## 8. 常见递归参数分别表示什么

### `start`

```python
backtrack(start)
```

表示：

```text
下一步只能从下标 start 及其右侧选择
```

适用于：

- 子集；
- 组合；
- Combination Sum；
- 字符串分割。

它可以防止：

```text
[1, 2]
[2, 1]
```

在“顺序不重要”的题里被当成两个不同结果。

### `used`

```python
used[i] = True / False
```

表示第 `i` 个输入元素是否已经被当前路径使用。

适用于排列，因为排列中的下一步可以选择任意尚未使用的元素。

### `remaining`

```python
backtrack(start, remaining)
```

表示距离目标还差多少。

适用于：

- 组合总和；
- 固定预算；
- 剩余容量；
- 剩余需要选择的数量。

### `index`

表示当前已经处理到：

- 字符串第几个字符；
- 单词第几个字符；
- 数组第几个位置。

### `row` / `(row, col)`

适用于棋盘：

- N 皇后每层处理一行；
- Word Search 从当前格子向四周搜索。

## 9. 两种常见决策树写法

### 写法一：选或不选

每个元素有两个分支：

```text
选择 nums[index]
不选择 nums[index]
```

模板：

```python
def backtrack(index):
    if index == len(nums):
        result.append(path[:])
        return

    path.append(nums[index])
    backtrack(index + 1)
    path.pop()

    backtrack(index + 1)
```

这是一棵二叉决策树。

### 写法二：for 循环枚举下一项

```python
def backtrack(start):
    result.append(path[:])

    for i in range(start, len(nums)):
        path.append(nums[i])
        backtrack(i + 1)
        path.pop()
```

这是一棵多叉决策树。

两种写法都能生成子集。

在 LeetCode 中，for 循环版本更容易扩展到：

- 组合长度限制；
- 去重；
- 剪枝；
- 元素复用。

## 10. 类型一：子集

代表题：

```text
78. Subsets
```

子集题的特点是：

```text
决策树中的每个节点都是一个合法答案
```

所以进入递归后就收集：

```python
def subsets(nums):
    result = []
    path = []

    def backtrack(start):
        result.append(path[:])

        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return result
```

这里没有“必须走到叶子才收集”的限制。

`start` 保证元素只向右选择，因此不会生成顺序不同但内容相同的结果。

## 11. 类型二：固定长度组合

代表题：

```text
77. Combinations
216. Combination Sum III
```

组合只在路径长度达到 `k` 时收集：

```python
def combine(n, k):
    result = []
    path = []

    def backtrack(start):
        if len(path) == k:
            result.append(path[:])
            return

        for value in range(start, n + 1):
            path.append(value)
            backtrack(value + 1)
            path.pop()

    backtrack(1)
    return result
```

### 组合题的数量剪枝

假设：

```text
还需要 need 个元素
从当前 value 到 n 只剩 available 个元素
```

如果：

```text
available < need
```

这条分支不可能完成。

可以直接限制循环右边界：

```python
need = k - len(path)

for value in range(start, n - need + 2):
    ...
```

剪枝不是为了改变答案，而是提前跳过确定不可能成功的分支。

## 12. 类型三：排列

代表题：

```text
46. Permutations
```

排列与组合的区别：

```text
组合：[1, 2] 和 [2, 1] 是同一个选择
排列：[1, 2] 和 [2, 1] 是不同结果
```

所以排列不能使用单向 `start` 限制。

每层都要查看所有元素，只跳过当前路径已经使用的下标：

```python
def permute(nums):
    result = []
    path = []
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):
            result.append(path[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue

            used[i] = True
            path.append(nums[i])

            backtrack()

            path.pop()
            used[i] = False

    backtrack()
    return result
```

这里需要同时撤销：

```python
path.pop()
used[i] = False
```

## 13. 组合和：元素是否可以复用

### 可以重复使用当前元素

代表题：

```text
39. Combination Sum
```

选择 `candidates[i]` 后，下一层仍可从 `i` 开始：

```python
backtrack(i, remaining - candidates[i])
```

### 每个下标只能使用一次

代表题：

```text
40. Combination Sum II
```

选择后下一层从 `i + 1` 开始：

```python
backtrack(i + 1, remaining - candidates[i])
```

核心区别：

```text
下一层传 i     -> 当前元素可以再次选择
下一层传 i + 1 -> 当前下标不能再次选择
```

这是回溯题最常见的参数差异之一。

## 14. Combination Sum 模板

```python
def combination_sum(candidates, target):
    candidates.sort()
    result = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            value = candidates[i]

            if value > remaining:
                break

            path.append(value)
            backtrack(i, remaining - value)
            path.pop()

    backtrack(0, target)
    return result
```

排序后，如果：

```python
value > remaining
```

后面的值只会更大，因此可以使用 `break`，而不只是 `continue`。

## 15. 去重：先区分“同层”与“同一条路径”

有重复输入时，去重最容易混乱。

需要区分：

```text
同一树层：多个选择会生成相同开头
同一树枝：路径中是否允许再次选择相同数值
```

### 同层去重

对于排序后的数组：

```python
if i > start and nums[i] == nums[i - 1]:
    continue
```

含义是：

```text
在当前递归层中，相同数值只作为下一步选择一次
```

`i > start` 非常重要。

它只跳过同层的重复候选，不会禁止更深层再次使用另一个相同值。

### 为什么必须先排序

只有排序后，相同值才会相邻：

```text
[2, 1, 2] -> [1, 2, 2]
```

才能通过比较 `nums[i] == nums[i - 1]` 跳过重复。

## 16. Subsets II / Combination Sum II 去重模板

```python
nums.sort()


def backtrack(start):
    result.append(path[:])

    for i in range(start, len(nums)):
        if i > start and nums[i] == nums[i - 1]:
            continue

        path.append(nums[i])
        backtrack(i + 1)
        path.pop()
```

这个模板适合：

- 90. Subsets II；
- 40. Combination Sum II 的同层去重部分。

不要在答案生成后使用：

```python
if path not in result:
```

更好的方式是提前阻止重复分支产生。

## 17. Permutations II 的去重

代表题：

```text
47. Permutations II
```

排列题既要使用 `used`，又要处理相同数值：

```python
nums.sort()


def backtrack():
    if len(path) == len(nums):
        result.append(path[:])
        return

    for i in range(len(nums)):
        if used[i]:
            continue

        if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
            continue

        used[i] = True
        path.append(nums[i])

        backtrack()

        path.pop()
        used[i] = False
```

条件：

```python
not used[i - 1]
```

表示前一个相同元素在当前路径中没有被使用。

此时选择后一个相同元素作为当前层开头，会生成重复分支，因此跳过。

可以理解为规定：

```text
相同元素在同一层只能按照原下标顺序被选择
```

## 18. 类型四：字符串分割

代表题：

```text
131. Palindrome Partitioning
```

状态通常是：

```text
start：下一段从哪里开始切
path：已经切出的合法片段
```

模板：

```python
def partition(s):
    result = []
    path = []

    def is_palindrome(left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    def backtrack(start):
        if start == len(s):
            result.append(path[:])
            return

        for end in range(start, len(s)):
            if not is_palindrome(start, end):
                continue

            path.append(s[start : end + 1])
            backtrack(end + 1)
            path.pop()

    backtrack(0)
    return result
```

每一层枚举：

```text
当前片段在哪里结束
```

只有片段合法时才继续深入。

## 19. 类型五：受约束字符串构造

代表题：

```text
22. Generate Parentheses
```

路径中可以放左括号或右括号，但选择受计数约束：

```python
def generate_parenthesis(n):
    result = []
    path = []

    def backtrack(open_count, close_count):
        if len(path) == 2 * n:
            result.append("".join(path))
            return

        if open_count < n:
            path.append("(")
            backtrack(open_count + 1, close_count)
            path.pop()

        if close_count < open_count:
            path.append(")")
            backtrack(open_count, close_count + 1)
            path.pop()

    backtrack(0, 0)
    return result
```

剪枝规则：

```text
左括号总数不能超过 n
任何前缀中，右括号数量不能超过左括号
```

这类题不是先生成所有字符串再检查，而是在生成过程中始终维持合法状态。

## 20. 类型六：棋盘搜索

代表题：

```text
79. Word Search
51. N-Queens
```

棋盘题的共享状态通常不是 `path` 列表，而是：

- 棋盘格是否访问；
- 哪些列已经占用；
- 哪些对角线已经占用；
- 当前处理到第几行或第几个字符。

## 21. Word Search 模板

```python
def exist(board, word):
    rows = len(board)
    cols = len(board[0])

    def backtrack(row, col, index):
        if index == len(word):
            return True

        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or board[row][col] != word[index]
        ):
            return False

        original = board[row][col]
        board[row][col] = "#"

        found = (
            backtrack(row + 1, col, index + 1)
            or backtrack(row - 1, col, index + 1)
            or backtrack(row, col + 1, index + 1)
            or backtrack(row, col - 1, index + 1)
        )

        board[row][col] = original
        return found
```

把格子临时改成 `"#"` 表示当前路径已经使用它。

递归结束后必须恢复：

```python
board[row][col] = original
```

否则其他起点或其他路径无法正常使用该格子。

## 22. N-Queens 的状态设计

每一层递归处理一行：

```python
backtrack(row)
```

需要维护：

```text
columns：已经占用的列
positive_diagonals：row + col
negative_diagonals：row - col
```

模板：

```python
columns = set()
positive_diagonals = set()
negative_diagonals = set()


def backtrack(row):
    if row == n:
        result.append(["".join(line) for line in board])
        return

    for col in range(n):
        if (
            col in columns
            or row + col in positive_diagonals
            or row - col in negative_diagonals
        ):
            continue

        board[row][col] = "Q"
        columns.add(col)
        positive_diagonals.add(row + col)
        negative_diagonals.add(row - col)

        backtrack(row + 1)

        board[row][col] = "."
        columns.remove(col)
        positive_diagonals.remove(row + col)
        negative_diagonals.remove(row - col)
```

这里要恢复四类共享状态：

- 棋盘字符；
- 列集合；
- 两个对角线集合。

## 23. 什么状态需要显式恢复

### 可变共享对象

通常需要恢复：

```python
path.append(value)
path.pop()

used[i] = True
used[i] = False

board[row][col] = "#"
board[row][col] = original

selected.add(value)
selected.remove(value)
```

### 不可变参数

通常不需要恢复：

```python
backtrack(remaining - value)
backtrack(index + 1)
backtrack(open_count + 1, close_count)
```

整数和字符串是不可变对象，每一层递归拥有自己的局部绑定。

因此没有必要写：

```python
remaining += value
```

前提是你没有在当前层直接修改共享变量，而是把新值作为参数传入下一层。

## 24. 收集答案的位置为什么不同

### 子集：每个节点都收集

```python
result.append(path[:])
```

因为任意长度路径都是合法子集。

### 固定长度组合：达到长度时收集

```python
if len(path) == k:
```

### 目标和：剩余值为 0 时收集

```python
if remaining == 0:
```

### 排列：使用完全部元素时收集

```python
if len(path) == len(nums):
```

### 分割：起点到达字符串末尾时收集

```python
if start == len(s):
```

所以不能机械地把 `result.append` 放在所有模板的同一个位置。

## 25. `return`、`continue` 和 `break` 的区别

### `return`

结束当前递归调用，回到父节点。

适用于：

- 已经收集完整结果；
- 当前状态确定不可能继续；
- 判断题已经找到答案。

### `continue`

当前候选不合法，但同一层后面还有其他候选需要尝试。

例如：

```python
if used[i]:
    continue
```

### `break`

当前候选以及后续所有候选都不可能合法。

通常需要排序提供单调性：

```python
if candidates[i] > remaining:
    break
```

不能在没有证明后续都失败时随意使用 `break`。

## 26. 剪枝是什么

剪枝是在进入递归前证明：

```text
这一整棵子树不可能产生答案
```

然后跳过它。

常见剪枝：

### 数值超过目标

```python
if value > remaining:
    break
```

### 剩余元素数量不足

```text
剩余候选数 < 还需要选择的数量
```

### 当前前缀已经不合法

```text
右括号数量 > 左括号数量
```

### 棋盘冲突

```text
列或对角线已被占用
```

### 当前字符不匹配

Word Search 中立即返回 `False`。

好的剪枝必须保证不会删除任何可能成功的分支。

## 27. 回溯的复杂度为什么经常是指数级

回溯需要枚举大量可能结果。

### 子集

每个元素选或不选：

```text
2^n 个子集
```

复制每个路径还需要最多 O(n)，总复杂度常写为：

```text
O(n * 2^n)
```

### 排列

排列数量：

```text
n!
```

复制结果需要 O(n)，总复杂度：

```text
O(n * n!)
```

### 组合

固定选择 `k` 个：

```text
C(n, k) 个结果
```

包含复制成本时约为：

```text
O(k * C(n, k))
```

### 棋盘搜索

Word Search 的宽松上界常写成：

```text
O(rows * cols * 4^L)
```

其中 `L` 是单词长度。

第一步以后不能立即返回原格子，实际分支常小于 4，但宽松分析用 `4^L` 更直观。

回溯复杂度往往至少与输出数量成正比。题目要求返回所有答案时，不可能完全避免枚举这些答案。

## 28. 空间复杂度看什么

主要包括：

1. 递归调用栈深度；
2. 当前路径；
3. `used` / 集合 / 棋盘标记；
4. 返回结果本身。

例如排列：

- 递归深度 O(n)；
- `path` O(n)；
- `used` O(n)；
- 不计算输出时额外空间 O(n)；
- 输出本身需要 O(n * n!)。

分析时最好说明是否把返回结果空间计算在内。

## 29. 回溯与动态规划怎么区分

### 优先考虑回溯

题目要求：

- 返回所有组合；
- 返回所有排列；
- 返回所有合法分割；
- 返回具体棋盘方案；
- 判断是否存在一条满足约束的路径；
- 输入规模较小，可以枚举。

### 优先考虑动态规划

题目只要求：

- 最优值；
- 方案数量；
- 是否可达；
- 子问题大量重复；
- 不需要输出每个具体方案。

例如：

```text
返回所有能组成 target 的组合 -> 回溯
只问组成 target 的方案数量   -> 可能更适合 DP
```

有些题两者都能做，选择取决于输出要求和重复子问题规模。

## 30. 回溯与普通 DFS 怎么区分

### 普通图遍历

如果只是判断从起点能否访问某个节点，`visited` 通常永久标记：

```text
访问过就不再访问
```

### 路径枚举

如果同一个节点可以出现在不同候选路径中，`visited` 只属于当前路径：

```text
进入路径时标记
离开路径时撤销
```

Word Search 就属于第二种。

所以看到 `visited` 时要先问：

```text
它表示全局已经处理过，还是当前路径正在使用？
```

## 31. 回溯与贪心怎么区分

贪心每一步选择一个当前最优选项，通常不会回来修改。

回溯会尝试多个候选：

```text
这个选择可能成功，也可能失败
失败后撤销并尝试另一个
```

如果无法证明一个局部最优选择一定属于全局最优答案，就不能只靠贪心跳过其他分支。

## 32. 看到题目时的固定思考顺序

以后遇到疑似回溯题，可以按以下顺序：

### 第一步：题目是否要求枚举

关键词：

- all；
- every；
- combinations；
- permutations；
- partitions；
- arrangements；
- generate；
- construct；
- 所有方案；
- 任意合法路径；
- 是否存在一条路径。

### 第二步：画出前两层决策树

不要一开始就写代码。

先问：

```text
第一步有哪些选择？
选择其中一个后，第二步还剩哪些选择？
```

### 第三步：写清 `path`

用一句话说明：

```text
path 表示什么？
```

### 第四步：选择状态参数

- 顺序不重要：`start`；
- 顺序重要：`used`；
- 有目标总和：`remaining`；
- 处理字符串：`index` / `start`；
- 棋盘：`row`、`col`、占用集合。

### 第五步：写结束条件

先写 base case，再写循环。

### 第六步：写选择和撤销

```python
做选择
递归
撤销选择
```

### 第七步：最后考虑剪枝和去重

先保证决策树正确，再压缩无效分支。

## 33. 调试回溯时记录什么

可以临时打印：

```python
print(
    "start =", start,
    "path =", path,
    "remaining =", remaining,
)
```

重点观察：

1. 进入下一层前路径增加了什么；
2. 返回后路径是否恢复；
3. `start` 是否正确前进；
4. 同一层重复值是否被跳过；
5. 收集答案时路径是否完整；
6. 无解分支是否正确停止。

如果逻辑很绕，手动画三列：

| 递归层 | 当前路径 | 剩余候选 |
| --- | --- | --- |
| 0 | `[]` | `[1, 2, 3]` |
| 1 | `[1]` | `[2, 3]` |
| 2 | `[1, 2]` | `[3]` |

回溯题画决策树通常比盯着代码更有效。

## 34. 常见错误

### 忘记 `path.pop()`

不同分支共享了错误状态。

### 保存 `path` 本身

所有答案引用同一个列表，最终内容异常。

### `start` 传错

- 应该复用却传 `i + 1`；
- 不应复用却传 `i`；
- 排列题误用 `start`，漏掉顺序。

### `used` 没有恢复

后续分支无法使用已经退出当前路径的元素。

### 收集答案后忘记 `return`

如果路径已经完整却继续深入，可能越界或生成无效结果。

### 结束条件放错位置

子集需要每个节点收集，排列只在叶子收集。

### 去重条件写成 `i > 0`

组合型同层去重通常需要：

```python
i > start
```

否则会错误跳过更深层合法使用的相同值。

### 没有先排序就比较相邻重复值

相同元素不相邻，去重条件失效。

### 棋盘标记没有恢复

一条失败路径污染其他路径或其他起点。

### 在循环中修改候选列表

`pop`、删除元素会改变后续下标，通常更推荐使用 `start` 或 `used` 表示状态。

### 盲目使用全局集合去重答案

这会掩盖决策树本身的重复分支，并增加额外比较和存储。

### 过早优化

模板还没正确就加入复杂剪枝，导致难以判断是搜索逻辑还是剪枝条件出错。

## 35. 必背模板

### 模板一：子集 / 组合

```python
result = []
path = []


def backtrack(start):
    result.append(path[:])

    for i in range(start, len(nums)):
        path.append(nums[i])
        backtrack(i + 1)
        path.pop()
```

### 模板二：排列

```python
result = []
path = []
used = [False] * len(nums)


def backtrack():
    if len(path) == len(nums):
        result.append(path[:])
        return

    for i in range(len(nums)):
        if used[i]:
            continue

        used[i] = True
        path.append(nums[i])

        backtrack()

        path.pop()
        used[i] = False
```

### 模板三：同层去重

```python
nums.sort()


def backtrack(start):
    for i in range(start, len(nums)):
        if i > start and nums[i] == nums[i - 1]:
            continue

        path.append(nums[i])
        backtrack(i + 1)
        path.pop()
```

### 模板四：目标和

```python
def backtrack(start, remaining):
    if remaining == 0:
        result.append(path[:])
        return

    for i in range(start, len(candidates)):
        value = candidates[i]

        if value > remaining:
            break

        path.append(value)
        backtrack(i, remaining - value)
        path.pop()
```

### 模板五：棋盘

```python
def backtrack(row, col, state):
    if 越界或不合法:
        return False

    if 完成目标:
        return True

    标记当前位置

    for next_position in 相邻位置:
        if backtrack(next_position, next_state):
            恢复当前位置
            return True

    恢复当前位置
    return False
```

## 36. 推荐刷题顺序

| 顺序 | 题号 | 题目 | 重点 |
| --- | --- | --- | --- |
| 1 | 78 | Subsets | `start`、每个节点收集 |
| 2 | 77 | Combinations | 固定长度、数量剪枝 |
| 3 | 46 | Permutations | `used` 数组 |
| 4 | 17 | Letter Combinations of a Phone Number | 每层候选来自映射 |
| 5 | 39 | Combination Sum | `remaining`、元素复用 |
| 6 | 22 | Generate Parentheses | 构造过程保持合法 |
| 7 | 131 | Palindrome Partitioning | 字符串切割 |
| 8 | 79 | Word Search | 棋盘标记与恢复 |
| 9 | 90 | Subsets II | 排序 + 同层去重 |
| 10 | 40 | Combination Sum II | 不复用 + 同层去重 |
| 11 | 47 | Permutations II | `used` + 排列去重 |
| 12 | 51 | N-Queens | 多集合约束与棋盘恢复 |

建议不要一开始就做 N-Queens。

先把以下三种基本状态练熟：

```text
start
used
remaining
```

再进入重复元素和棋盘约束。

## 37. 当前阶段的学习目标

完成 Backtracking 入门后，应能：

1. 把问题画成决策树。
2. 用一句话定义 `path` 和递归函数职责。
3. 区分组合使用 `start`、排列使用 `used`。
4. 正确写出“选择、递归、撤销”。
5. 保存结果时复制可变路径。
6. 根据题意决定当前元素能否复用。
7. 使用排序和 `i > start` 完成同层去重。
8. 根据剩余数量、目标值和局部合法性剪枝。
9. 在棋盘题中正确标记并恢复状态。
10. 区分回溯、普通 DFS、动态规划和贪心。

## 38. 最后总结

回溯的核心不是背代码，而是管理决策树中的状态：

```text
当前走到了哪里？
已经选择了什么？
下一步可以选什么？
什么选择不合法？
什么时候得到答案？
返回上一层时要恢复什么？
```

最重要的基础模板是：

```python
for choice in choices:
    if invalid(choice):
        continue

    make_choice(choice)
    backtrack(next_state)
    undo_choice(choice)
```

可以记住一句话：

```text
回溯 = 枚举选择 + 约束剪枝 + 递归深入 + 恢复现场
```
