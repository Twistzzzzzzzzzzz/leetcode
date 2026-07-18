# Trie 前缀树基础

## Trie 是什么

Trie 通常叫：

```text
前缀树
字典树
```

它是一种专门保存字符串的多叉树。

普通树的节点通常保存一个完整数值，而 Trie 会把字符串拆成一个个字符，按照字符顺序形成路径。

例如插入：

```text
app
apple
apply
bat
```

可以理解成：

```text
root
├── a
│   └── p
│       └── p  <- app 结束
│           └── l
│               ├── e  <- apple 结束
│               └── y  <- apply 结束
└── b
    └── a
        └── t  <- bat 结束
```

`app`、`apple` 和 `apply` 共享前缀 `app`，所以这段路径只需要保存一次。

## Trie 解决什么问题

Trie 最适合处理：

- 多次插入字符串
- 多次查询完整单词
- 多次查询某个前缀是否存在
- 自动补全
- 搜索建议
- 通配符单词搜索
- 大量字符串共享前缀

它的核心优势不是“完整单词查找一定比 HashSet 更快”。

HashSet 也能高效判断一个完整单词是否存在，但它不直接保存字符串之间的前缀关系。

例如：

```python
words = {"apple", "apply", "app"}
```

HashSet 很适合：

```text
"apple" 是否存在？
```

Trie 除了能回答完整单词是否存在，还能自然回答：

```text
是否存在以 "appl" 开头的单词？
以 "app" 开头的单词有哪些？
```

## Trie 不是二叉树

二叉树节点最多有两个孩子：

```text
left
right
```

Trie 节点可能有很多孩子，每个孩子对应一个字符：

```text
a
b
c
...
```

所以 Trie 是多叉树。

它的基础操作通常只沿一条字符路径移动，直接使用循环即可，不一定需要递归。

这再次说明：

```text
树是数据结构
DFS / BFS 是遍历策略
递归 / while / for 是实现方式
```

## Trie 节点保存什么

最常见的节点定义：

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
```

每个节点保存两个核心字段。

### `children`

```python
self.children = {}
```

字典含义是：

```text
下一个字符 -> 对应的 TrieNode
```

例如：

```python
node.children = {
    "a": node_a,
    "b": node_b,
}
```

表示从当前节点可以沿字符 `a` 或 `b` 继续向下。

字符通常保存在父节点到孩子节点的边上，可以简单理解为孩子节点代表“走完这个字符后到达的位置”。

### `is_end`

```python
self.is_end = False
```

表示当前节点是不是某个完整单词的结尾。

这个字段非常重要，因为：

```text
路径存在
```

和：

```text
完整单词存在
```

不是同一件事。

例如只插入了：

```text
apple
```

此时 `app` 的路径已经存在，但 `app` 没有被作为完整单词插入：

```text
search("app") == False
startsWith("app") == True
```

## 根节点为什么不保存字符

```python
self.root = TrieNode()
```

根节点只是所有单词的共同起点，本身不代表任何字符。

第一个字符保存在：

```python
root.children
```

这样所有字符串都能从同一个空节点开始处理，不需要特殊判断第一个字符。

## 节点代表什么

理解 Trie 时，可以给每个节点一个明确含义：

> 从根节点走到当前节点的整条路径，代表一个字符串前缀。

例如：

```text
root -> a -> p -> p
```

当前节点代表前缀：

```text
app
```

如果当前节点：

```python
is_end is True
```

说明 `app` 还是一个被完整插入过的单词。

如果是 `False`，说明它只是其他更长单词的前缀。

## 操作一：插入单词

从根节点开始遍历单词中的每个字符：

```python
node = self.root

for char in word:
    if char not in node.children:
        node.children[char] = TrieNode()

    node = node.children[char]

node.is_end = True
```

每个字符有两种情况。

### 对应孩子已经存在

直接复用已有前缀：

```python
node = node.children[char]
```

### 对应孩子不存在

先创建新节点，再移动过去：

```python
node.children[char] = TrieNode()
node = node.children[char]
```

全部字符处理完后，才标记单词结束：

```python
node.is_end = True
```

不能在遍历过程中把每个节点都标记为结束，否则一个单词的全部前缀都会被错误地当成完整单词。

## 操作二：搜索完整单词

```python
node = self.root

for char in word:
    if char not in node.children:
        return False

    node = node.children[char]

return node.is_end
```

判断过程分两步：

1. 单词中的每个字符路径必须存在。
2. 最后到达的节点必须是完整单词的结尾。

所以遍历结束后不能直接：

```python
return True
```

必须：

```python
return node.is_end
```

## 操作三：搜索前缀

```python
node = self.root

for char in prefix:
    if char not in node.children:
        return False

    node = node.children[char]

return True
```

前缀查询只要求整条路径存在，不要求最后节点是一个完整单词的结尾。

因此不需要检查：

```python
node.is_end
```

## 三种基础操作对比

| 操作 | 遍历字符路径 | 创建缺失节点 | 最后检查 `is_end` |
| --- | --- | --- | --- |
| `insert(word)` | 是 | 是 | 设置为 `True` |
| `search(word)` | 是 | 否 | 是 |
| `startsWith(prefix)` | 是 | 否 | 否 |

## 208 基础模板

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True

    def search(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                return False

            node = node.children[char]

        return node.is_end

    def startsWith(self, prefix):
        node = self.root

        for char in prefix:
            if char not in node.children:
                return False

            node = node.children[char]

        return True
```

详细题解见 [208. Implement Trie](../trees/p0208_implement_trie_prefix_tree.md)。

## 可以抽取共同的查找函数吗

`search` 和 `startsWith` 的路径查找部分完全相同，可以抽取：

```python
def _find_node(self, text):
    node = self.root

    for char in text:
        if char not in node.children:
            return None

        node = node.children[char]

    return node
```

然后：

```python
def search(self, word):
    node = self._find_node(word)
    return node is not None and node.is_end

def startsWith(self, prefix):
    return self._find_node(prefix) is not None
```

这个抽取能减少重复，但第一次学习时分别写出两个循环更容易看清结束条件的区别。

只有当抽取后逻辑仍然清楚时才需要这样重构。

## 通配符为什么让搜索变难

208 中的普通字符会确定唯一的下一条边：

```text
当前字符是 a
-> 只能走 children["a"]
```

211 中允许出现通配符 `.`：

```text
. 可以匹配任意一个字符
-> 当前节点的所有孩子都可能成为下一步
```

搜索从单一路径变成了多个候选分支，因此需要 DFS。

## 通配符搜索的递归定义

定义：

```python
dfs(index, node)
```

表示：

> 从 Trie 的当前节点 `node` 出发，能否匹配搜索字符串中从 `index` 开始的剩余部分。

### 所有字符匹配完成

```python
if index == len(word):
    return node.is_end
```

必须检查 `is_end`，确保匹配的是完整单词。

### 普通字符

```python
if char not in node.children:
    return False

return dfs(index + 1, node.children[char])
```

普通字符只走对应的一条路径。

### 通配符

```python
for child_node in node.children.values():
    if dfs(index + 1, child_node):
        return True

return False
```

任意一个孩子成功就返回 `True`。

只有所有孩子都失败后，才能返回 `False`。

## 211 通配符搜索模板

```python
def search(self, word):
    def dfs(index, node):
        if index == len(word):
            return node.is_end

        char = word[index]

        if char == ".":
            for child_node in node.children.values():
                if dfs(index + 1, child_node):
                    return True

            return False

        if char not in node.children:
            return False

        return dfs(index + 1, node.children[char])

    return dfs(0, self.root)
```

详细题解见 [211. Design Add and Search Words](../trees/p0211_design_add_and_search_words_data_structure.md)。

## DFS 和回溯的关系

通配符搜索会尝试多个分支，因此具有回溯搜索的思想。

不过当前代码没有修改共享的路径、计数器或访问状态，只是把新的 `index` 和子节点传给下一层。

所以递归返回后不需要显式执行：

```python
path.pop()
```

它可以直接理解为：

```text
Trie 上的 DFS 分支搜索
```

后续 Trie 与棋盘搜索组合时，通常会修改棋盘访问状态，那时就需要真正的“做选择、递归、撤销选择”。

## 字典和固定数组怎么选

### 使用字典

```python
self.children = {}
```

优点：

- 写法直观
- 只保存实际存在的孩子
- 容易支持不同字符集合

缺点：

- 每个节点都包含哈希表开销

### 使用长度为 26 的数组

如果题目保证只有小写英文字母：

```python
self.children = [None] * 26
```

字符转下标：

```python
index = ord(char) - ord("a")
```

优点：

- 下标访问直接
- 不需要哈希

缺点：

- 每个节点固定预留 26 个位置
- Python 代码更长

当前阶段优先使用字典版本，先把结构与状态理解清楚。

## 时间复杂度

设字符串长度为 `L`。

### 插入

```text
时间复杂度：O(L)
最坏新增空间：O(L)
```

### 普通完整搜索

```text
时间复杂度：O(L)
额外空间：O(1)
```

如果使用递归搜索，调用栈为 O(L)。

### 前缀搜索

```text
时间复杂度：O(L)
额外空间：O(1)
```

### 通配符搜索

设每个节点最多有 `B` 个孩子。

如果很多位置都是 `.`，最坏可能探索：

```text
O(B^L)
```

实际访问量受到 Trie 中真实节点数量限制。

递归深度最多为 `L`，所以调用栈空间为 O(L)。

## 整棵 Trie 的空间

假设插入的全部单词长度之和为：

```text
S
```

完全没有共享前缀时，节点数量最多接近：

```text
O(S)
```

共享前缀越多，实际创建的节点越少。

空间不能简单理解成“单词数量”，因为一个长度为 `L` 的全新单词最多会创建 `L` 个节点。

## 如何识别 Trie 题

看到以下信号，可以优先考虑 Trie：

1. 需要动态插入许多字符串。
2. 需要反复查询完整单词。
3. 需要反复查询前缀。
4. 题目出现自动补全或搜索建议。
5. 大量字符串共享前缀。
6. 搜索过程可以按字符逐层缩小候选集合。
7. 单词搜索中出现通配符或多个字符分支。

可以用一句话概括：

```text
大量字符串 + 多次前缀相关操作 -> 考虑 Trie
```

## 哪些情况不必使用 Trie

Trie 不是所有字符串题的默认答案。

以下情况可能用普通结构更简单：

- 只判断一次完整单词是否存在：使用 `set`
- 只统计字符频率：使用 HashMap / Counter
- 只比较两个字符串：使用普通遍历
- 只需要排序后的字符串分组：使用 HashMap
- 数据量很小，没有多次查询

先确认题目是否真正需要维护前缀层级。

## 常见错误

### 忘记移动 `node`

错误：

```python
for char in word:
    if char not in node.children:
        node.children[char] = TrieNode()
```

创建孩子后还必须：

```python
node = node.children[char]
```

否则所有字符都会错误地挂在同一个节点下。

### 提前设置 `is_end`

只有完整单词的最后一个节点才能设置：

```python
node.is_end = True
```

### `search` 遍历完直接返回 `True`

路径存在可能只是其他单词的前缀，必须返回：

```python
node.is_end
```

### `startsWith` 检查 `is_end`

前缀不要求是完整单词，只需要路径存在。

### 把 `.` 当作普通键

通配符不应该查找：

```python
node.children["."]
```

而应该遍历所有孩子。

### 第一个通配符分支失败就返回 `False`

一个孩子失败不代表其他孩子也失败。

`return False` 必须放在所有孩子尝试完成之后。

### 忘记精确匹配长度

通配符 `.` 只能匹配一个字符。

搜索结束时检查 `is_end`，可以同时保证完整单词和长度正确。

## 固定思考流程

看到 Trie 题时，按这个顺序思考：

1. 每个节点需要保存什么？
2. `children` 的键和值分别代表什么？
3. 是否需要区分完整单词和普通前缀？
4. 当前操作只走一条字符路径，还是会产生多个分支？
5. 普通字符不存在时应返回什么？
6. 所有字符处理完后，是检查 `is_end`，还是只要求路径存在？
7. 如果出现通配符，什么时候能提前返回 `True`？
8. 是否修改了共享状态，需要在递归后撤销？

## 题型地图

### A. Trie 基础操作

代表题：

- 208. Implement Trie (Prefix Tree)

需要掌握：

- 节点结构
- 插入
- 完整单词搜索
- 前缀搜索
- `search` 与 `startsWith` 的区别

### B. Trie + DFS

代表题：

- 211. Design Add and Search Words Data Structure

需要掌握：

- 普通字符走单个孩子
- 通配符枚举所有孩子
- `dfs(index, node)` 的定义
- 任意分支成功与所有分支失败

### C. Trie + 字符串替换或统计

代表题：

- 648. Replace Words
- 677. Map Sum Pairs
- 720. Longest Word in Dictionary
- 1268. Search Suggestions System

可能需要在节点中额外保存：

- 前缀对应的值
- 经过当前节点的单词数量
- 当前节点对应的完整单词
- 搜索建议列表

### D. Trie + 棋盘回溯

代表题：

- 212. Word Search II

核心组合：

```text
Trie：快速判断当前路径是不是某些单词的前缀
回溯：在棋盘中探索上下左右路径
```

这是进阶题，先掌握 208 和 211 后再做。

## 推荐刷题顺序

1. 208. Implement Trie (Prefix Tree)
2. 211. Design Add and Search Words Data Structure
3. 648. Replace Words
4. 677. Map Sum Pairs
5. 720. Longest Word in Dictionary
6. 1268. Search Suggestions System
7. 212. Word Search II

前两题先掌握 Trie 节点、单路径搜索和通配符分支搜索。

中间四题练习把额外信息保存在 Trie 节点中。

212 是 Trie 与棋盘回溯的综合 Hard 题，最后再做。

## 必背模板

### 模板一：Trie 节点

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
```

### 模板二：插入

```python
def insert(self, word):
    node = self.root

    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()

        node = node.children[char]

    node.is_end = True
```

### 模板三：完整单词搜索

```python
def search(self, word):
    node = self.root

    for char in word:
        if char not in node.children:
            return False

        node = node.children[char]

    return node.is_end
```

### 模板四：前缀搜索

```python
def startsWith(self, prefix):
    node = self.root

    for char in prefix:
        if char not in node.children:
            return False

        node = node.children[char]

    return True
```

### 模板五：通配符搜索

```python
def dfs(index, node):
    if index == len(word):
        return node.is_end

    char = word[index]

    if char == ".":
        for child in node.children.values():
            if dfs(index + 1, child):
                return True

        return False

    if char not in node.children:
        return False

    return dfs(index + 1, node.children[char])
```

## 当前学习目标

当前阶段应该能够：

1. 解释 Trie 为什么能共享字符串前缀。
2. 写出 `children + is_end` 的节点结构。
3. 独立完成插入、完整单词搜索和前缀搜索。
4. 说明 `search` 为什么必须检查 `is_end`。
5. 说明 `startsWith` 为什么不检查 `is_end`。
6. 遇到通配符时，能把单路径搜索改成 DFS 分支搜索。
7. 正确定义 `dfs(index, node)` 的职责。
8. 知道 Trie 适合多次前缀相关操作，而不是所有字符串题。

先把 208 和 211 反复写熟，再进入 Trie 与回溯、统计信息的组合题。
