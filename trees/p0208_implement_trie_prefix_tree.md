# 208. Implement Trie (Prefix Tree)

## 题目

实现一个 Trie，也叫前缀树或字典树，支持三种操作：

```text
insert(word)       插入完整单词
search(word)       判断完整单词是否存在
startsWith(prefix) 判断是否存在以 prefix 开头的单词
```

## Trie 是什么

Trie 是一棵按照字符逐层展开的多叉树。

例如依次插入：

```text
app
apple
apply
```

可以画成：

```text
root
  |
  a
  |
  p
  |
  p  <- app 结束
 / \
l   ...
|
e    <- apple 结束
\
 y   <- apply 结束
```

更准确地说，`apple` 和 `apply` 会共享 `appl` 这一段路径。相同前缀只保存一次，这就是 Trie 的核心价值。

## 节点保存什么

每个 Trie 节点需要两个字段：

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
```

### `children`

```python
self.children = {}
```

字典含义是：

```text
字符 -> 对应的下一个 TrieNode
```

例如当前节点有：

```python
node.children = {
    "a": node_a,
    "b": node_b,
}
```

表示从当前节点沿字符 `a` 或 `b` 可以继续向下走。

### `is_end`

```python
self.is_end = False
```

表示当前节点是不是某个完整单词的结尾。

它不能省略，因为：

```text
路径存在
```

不一定代表：

```text
完整单词存在
```

插入 `apple` 后，路径 `a -> p -> p` 已经存在，但如果没有单独插入 `app`：

```text
startsWith("app") == True
search("app") == False
```

区别就由第三个 `p` 节点的 `is_end` 决定。

## 根节点为什么不保存字符

```python
self.root = TrieNode()
```

根节点只是所有单词的共同起点，本身不对应任何字符。

第一个字符保存在：

```python
root.children
```

这样所有单词都可以从同一个空根节点开始处理，代码不需要特殊判断第一个字符。

## `insert`：插入单词

从根节点开始，依次处理每个字符：

```python
node = self.root

for char in word:
    if char not in node.children:
        node.children[char] = TrieNode()

    node = node.children[char]
```

每一步分两种情况：

- 字符对应的孩子已经存在：复用已有前缀。
- 字符对应的孩子不存在：创建新节点。

无论是否新建，最后都要移动到这个孩子：

```python
node = node.children[char]
```

所有字符处理完后，标记完整单词结束：

```python
node.is_end = True
```

不能在遍历每个字符时都标记 `is_end`，否则单词的所有前缀都会被错误地当成完整单词。

## `search`：搜索完整单词

首先沿着字符路径向下走：

```python
for char in word:
    if char not in node.children:
        return False

    node = node.children[char]
```

任何一个字符路径不存在，完整单词就不存在。

所有字符都能走完时，还不能直接返回 `True`，必须检查：

```python
return node.is_end
```

因为走完只证明该字符串是某个已插入单词的前缀；`is_end` 才能证明它本身被完整插入过。

## `startsWith`：搜索前缀

前缀查询同样沿字符路径向下走。

区别是：只要所有字符路径存在，就已经找到一个有效前缀：

```python
return True
```

这里不需要检查 `node.is_end`，因为前缀本来就不要求是完整单词。

## `search` 与 `startsWith` 的区别

| 操作 | 路径必须存在 | 最后要求 `is_end` |
| --- | --- | --- |
| `search(word)` | 是 | 是 |
| `startsWith(prefix)` | 是 | 否 |

插入 `apple` 后：

```python
search("apple")       # True
search("app")         # False
startsWith("app")     # True
```

再插入 `app` 后：

```python
search("app")         # True
```

路径没有变化，只是第三个 `p` 节点的 `is_end` 从 `False` 变成了 `True`。

## 代码

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

## 为什么这里没有使用递归

Trie 是树结构，但三种基础操作只需要按照字符串从上到下走一条路径。

用循环依次处理字符最直接：

```python
for char in word:
```

这再次说明：

```text
树是数据结构
递归只是实现方式之一
```

后续遇到通配符搜索、列出全部匹配单词等需要探索多个分支的题时，才更可能在 Trie 上使用 DFS。

## 为什么使用字典保存孩子

字典只为实际出现的字符创建孩子，写法直观，也能支持不同字符集合。

如果题目只包含 26 个小写字母，也可以使用固定长度数组：

```python
self.children = [None] * 26
```

下标由字符计算：

```python
index = ord(char) - ord("a")
```

两种方式的取舍：

| 实现 | 优点 | 缺点 |
| --- | --- | --- |
| 字典 | 简洁，只存实际孩子 | 有哈希表额外开销 |
| 长度 26 的数组 | 下标访问稳定直接 | 每个节点固定占 26 个位置 |

Python 刷题时，字典版本通常更清楚。

## 复杂度

设字符串长度为 `L`。

### 插入

- 时间复杂度：O(L)
- 最坏新增空间：O(L)

### 搜索完整单词

- 时间复杂度：O(L)
- 额外空间复杂度：O(1)

### 搜索前缀

- 时间复杂度：O(L)
- 额外空间复杂度：O(1)

字典查找按平均 O(1) 计算。

整棵 Trie 的节点数最多接近所有插入字符串长度之和，但共享前缀会减少实际节点数量。

## 如何识别 Trie 题

看到以下需求，可以考虑 Trie：

- 反复插入和查询字符串。
- 判断某个单词或前缀是否存在。
- 自动补全、搜索建议。
- 大量单词共享前缀。
- 根据字符逐层缩小候选集合。

如果只查询一次，普通集合或字符串方法可能更简单。Trie 更适合需要维护许多单词并进行多次前缀查询的场景。

## 常见错误

### 忘记移动当前节点

创建或找到孩子后必须执行：

```python
node = node.children[char]
```

否则每个字符都会错误地从根节点处理。

### `search` 遍历完直接返回 `True`

这只能证明路径存在，不能证明完整单词存在。必须返回：

```python
node.is_end
```

### `startsWith` 检查 `is_end`

前缀不要求是完整单词。只要路径存在就应返回 `True`。

### 提前标记 `is_end`

只有完整单词的最后一个节点才能标记为结束节点。

## 心得

1. Trie 用树结构保存字符串前缀，相同前缀只保存一次。
2. 每个节点的 `children` 表示“字符到下一个节点”的映射。
3. `is_end` 用来区分“路径存在”和“完整单词存在”。
4. `search` 最后必须检查 `is_end`；`startsWith` 只需要确认路径存在。
5. Trie 的基础操作只沿一条路径移动，使用循环即可，不需要递归。
6. 看到大量字符串插入、完整单词查询和前缀查询，可以考虑 Trie。
