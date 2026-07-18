# 211. Design Add and Search Words Data Structure

## 题目

设计一个支持以下操作的数据结构：

```text
addWord(word)：添加一个单词
search(word)：搜索一个单词
```

搜索字符串中可以包含通配符 `.`，它能够匹配任意一个字母。

例如已经添加：

```text
bad, dad, mad
```

那么：

```python
search("bad")   # True
search("pad")   # False
search(".ad")   # True
search("b..")   # True
```

## 与 208 Trie 的关系

添加单词的部分与 208 完全相同：

```text
字符存在 -> 复用对应孩子
字符不存在 -> 创建新 TrieNode
单词结束 -> 标记 is_end
```

真正的新难点只在搜索：

```text
普通字符：只可能沿一个指定孩子继续
通配符 .：当前节点的任何孩子都可能匹配
```

208 的搜索始终只有一条确定路径，因此可以直接使用循环。

211 遇到 `.` 时会出现多个候选分支，所以需要 DFS 尝试这些分支。

## Trie 节点

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
```

含义仍然是：

```text
children：字符 -> 子节点
is_end：当前节点是否为完整单词的结尾
```

## `addWord`

```python
def addWord(self, word):
    node = self.root

    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()

        node = node.children[char]

    node.is_end = True
```

多个单词会共享已有前缀，只有缺失的字符路径才创建新节点。

## DFS 函数的职责

定义：

```python
dfs(index, node)
```

表示：

> 从当前 Trie 节点 `node` 出发，能否匹配搜索字符串中从 `index` 开始的剩余部分 `word[index:]`。

这里的两个状态分别是：

```text
index：下一步需要匹配 word 中的哪个字符
node：当前位于 Trie 的哪个节点
```

每次成功匹配一个字符后：

```text
index 向后移动一位
node 移动到匹配的孩子
```

## 结束条件为什么返回 `node.is_end`

```python
if index == len(word):
    return node.is_end
```

`index == len(word)` 只说明搜索字符串中的字符已经全部匹配完。

还必须确认当前 Trie 节点是某个完整单词的结尾。

例如只添加了：

```text
apple
```

搜索 `app` 时，所有字符路径都能走完，但第三个 `p` 的 `is_end` 仍为 `False`，因此不能返回 `True`。

这个结束条件还保证了单词长度必须匹配。添加 `bad` 后：

```text
search("..")   == False
search("...")  == True
search("....") == False
```

每个 `.` 只匹配恰好一个字符，不是零个或任意多个字符。

## 普通字符：只走一条路径

```python
if char not in node.children:
    return False

return dfs(index + 1, node.children[char])
```

普通字符已经确定了下一条边：

- 对应孩子不存在：当前路径匹配失败。
- 对应孩子存在：进入该孩子，继续匹配下一个字符。

## 通配符：尝试所有孩子

```python
if char == ".":
    for child_node in node.children.values():
        if dfs(index + 1, child_node):
            return True

    return False
```

`.` 可以代表任意一个字符，所以不关心字典中的键，只需要遍历所有孩子节点：

```python
node.children.values()
```

只要其中一个分支能够匹配剩余字符串，就可以立即返回 `True`。

只有所有孩子都尝试失败后，才能返回 `False`。

## 为什么不能在第一个失败分支后返回 `False`

错误结构：

```python
for child in node.children.values():
    if dfs(index + 1, child):
        return True
    else:
        return False
```

第一个孩子失败，不代表其他孩子也会失败。

正确逻辑是：

```text
任意一个成功 -> True
所有分支都失败 -> False
```

因此 `return False` 必须放在 `for` 循环结束之后。

## 这算回溯吗

这段代码会在 `.` 处尝试多个候选分支，因此具有回溯搜索的思想。

不过它没有修改共享的路径列表、计数器或访问状态，所以不需要显式执行：

```python
path.pop()
```

每次递归只传入新的 `index` 和另一个子节点。递归返回后，自然会继续尝试下一个孩子。

更准确地说，它是：

```text
Trie 上的 DFS 分支搜索
```

## 代码

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True

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

## 执行示例

已经添加：

```text
bad, dad, mad
```

搜索：

```text
.ad
```

根节点遇到 `.`，会依次尝试：

```text
b 分支 -> 剩余 ad -> 找到 bad -> True
d 分支 -> 剩余 ad -> 找到 dad -> True
m 分支 -> 剩余 ad -> 找到 mad -> True
```

实际程序在第一个成功分支就会短路返回，不会继续做无意义搜索。

## 复杂度

设单词长度为 `L`。

### `addWord`

- 时间复杂度：O(L)
- 最坏新增空间：O(L)

### 没有通配符的 `search`

- 时间复杂度：O(L)
- 递归栈空间：O(L)

### 包含通配符的 `search`

设每个节点最多有 `B` 个孩子。

最坏情况下，每一位都是 `.`，可能探索：

```text
O(B^L)
```

对于只包含小写字母的题，`B` 最多为 26。实际访问量还受到 Trie 中真实节点数量限制。

递归深度最多为 `L`，所以递归栈空间是 O(L)。

## 如何识别这种题

看到以下组合，可以想到 Trie + DFS：

```text
维护大量单词
+
根据字符逐层匹配
+
搜索中存在通配符或多个可能分支
```

普通 Trie 搜索只有一条路径；一旦某个字符可以匹配多个孩子，就需要分支搜索。

## 常见错误

1. 把 `.` 当成字典中的普通键查找。
2. 字符全部处理完后直接返回 `True`，忘记检查 `is_end`。
3. 通配符的第一个孩子失败后就提前返回 `False`。
4. 普通字符匹配后忘记把 `index` 加一。
5. 把 `.` 理解为能匹配零个或多个字符；本题中它只能匹配一个字符。

## 心得

1. 211 的插入操作与 208 完全相同，变化只发生在搜索阶段。
2. `dfs(index, node)` 表示从当前 Trie 节点能否匹配 `word[index:]`。
3. 普通字符只走对应的一条路径，`.` 要尝试当前节点的全部孩子。
4. 任意分支成功就返回 `True`，所有分支失败后才能返回 `False`。
5. 字符全部匹配完仍要检查 `node.is_end`，保证匹配的是完整单词。
6. Trie 搜索出现通配符时，可以考虑 Trie + DFS 分支搜索。
