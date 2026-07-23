# 953. Verifying an Alien Dictionary

## 题目

给定：

- 一个单词列表 `words`；
- 外星语言中 26 个小写字母的顺序 `order`。

判断 `words` 是否已经按照这套外星字典序排列。

例如：

```text
words = ["hello", "leetcode"]
order = "hlabcdefgijkmnopqrstuvwxyz"
```

因为 `h` 在 `l` 前面，所以 `"hello"` 应该排在 `"leetcode"` 前面，答案为 `True`。

## 为什么放在 Graph 专题

按照当前学习路线，这道题归档在 `graphs`，作为 269. Alien Dictionary 的前置热身题。

不过需要区分“目录归属”和“当前题目的实际算法”：

953 已经直接给出了完整的字母顺序，所以当前解法仍然是：

```text
建立字符排名
+
按照字典序比较相邻字符串
```

它本身不需要建图，但可以提前练习 Alien Dictionary 中同样重要的两个规则：

```text
第一个不同字符决定两个单词的相对顺序
较短前缀必须排在较长单词前面
```

之后学习 269. Alien Dictionary 时，区别是：

- 953：顺序已知，验证单词列表；
- 269：顺序未知，需要从单词列表中推导字母依赖关系，再使用拓扑排序。

因此可以记成：

```text
953 = Alien Dictionary 的比较规则热身
269 = 根据比较规则建图 + Topological Sort
```

## 第一步：把字母顺序转换成排名

`order` 是一个字符串，直接查某个字母的位置并不方便。

先建立 HashMap：

```python
rank_by_char = {}

for index in range(len(order)):
    rank_by_char[order[index]] = index
```

例如：

```text
order = "hlabc..."

rank_by_char["h"] = 0
rank_by_char["l"] = 1
rank_by_char["a"] = 2
```

排名越小，字母在外星字典中越靠前。

这样字符顺序比较就从线性查找变成平均 O(1) 的 HashMap 查找。

## 第二步：只比较相邻单词

如果整个列表已经有序，那么每一对相邻单词都必须满足：

```text
words[i - 1] <= words[i]
```

因此只需检查：

```text
第 0 个和第 1 个
第 1 个和第 2 个
第 2 个和第 3 个
...
```

不需要两两比较所有单词。

## 如何比较两个单词

比较：

```text
first_word
second_word
```

从左到右寻找第一个不同字符。

### 找到了不同字符

第一个不同字符直接决定两个单词的字典序。

例如：

```text
first_word  = "hello"
second_word = "leetcode"
               ^
```

第一位就不同，只需要比较 `h` 和 `l` 的外星排名。

如果：

```python
rank_by_char[first_char] > rank_by_char[second_char]
```

说明前面的单词反而更大，整个列表无序，返回 `False`。

如果前面的字符排名更小，这一对单词已经确定有序，可以停止继续比较后面的字符。

## 特殊情况：前缀关系

如果比较完较短单词的所有字符都没有发现不同字符，说明其中一个单词是另一个单词的前缀。

正确顺序必须是：

```text
"app"
"apple"
```

错误顺序是：

```text
"apple"
"app"
```

因此需要额外判断：

```python
if not found_difference and len(first_word) > len(second_word):
    return False
```

这是本题最容易漏掉的边界。

## 整理后的代码

```python
class Solution:
    def isAlienSorted(self, words: list[str], order: str) -> bool:
        rank_by_char = {}

        for index in range(len(order)):
            rank_by_char[order[index]] = index

        for index in range(1, len(words)):
            first_word = words[index - 1]
            second_word = words[index]
            common_length = min(len(first_word), len(second_word))
            found_difference = False

            for char_index in range(common_length):
                first_char = first_word[char_index]
                second_char = second_word[char_index]

                if first_char == second_char:
                    continue

                found_difference = True

                if rank_by_char[first_char] > rank_by_char[second_char]:
                    return False

                break

            if not found_difference and len(first_word) > len(second_word):
                return False

        return True
```

## 为什么发现正确顺序后也要 `break`

假设：

```text
first_word  = "abcx"
second_word = "abda"
```

第一个不同位置是：

```text
c 和 d
```

只要 `c` 排在 `d` 前面，就已经能确定第一个单词更小。

后面的：

```text
x 和 a
```

不再影响这两个单词的字典序。

所以找到第一个不同字符后，无论顺序正确还是错误，都不应该继续比较后续字符。

## 为什么只比较相邻单词就够了

假设：

```text
word1 <= word2
word2 <= word3
```

字典序具有传递性，因此：

```text
word1 <= word3
```

只要所有相邻关系都正确，整个列表就是有序的。

## 复杂度

设所有相邻单词比较过程中，一共检查了 `C` 个字符：

- 建立排名表：O(26)
- 比较单词：O(C)
- 总时间复杂度：O(C)
- 额外空间复杂度：O(26)

通常也可以把时间写成 O(S)，其中 `S` 是所有单词的字符总数。

因为字母表大小固定为 26，额外空间相对于输入规模可以视为 O(1)。

## 易错点

### 直接使用普通字母顺序

不能写：

```python
first_char > second_char
```

Python 比较的是正常英文字母顺序，不是题目给出的外星顺序。

### 忘记前缀规则

`"apple"` 不能排在 `"app"` 前面，即使所有能够比较的位置都相同。

### 找到第一个不同字符后仍继续比较

字典序只由第一个不同字符决定，后面的字符不再参与当前这对单词的顺序判断。

### 两两比较所有单词

只需比较相邻单词。全部两两比较会增加不必要的逻辑和复杂度。

### 把 953 当成拓扑排序

本题已经给出 `order`，不用推导字符依赖关系，也不需要建图。

## 心得

1. 自定义字母顺序可以先转换成 `字符 -> 排名` 的 HashMap。
2. 验证整个列表是否有序，只需要逐对比较相邻元素。
3. 比较两个字符串时，第一个不同字符决定字典序，之后的字符不再重要。
4. 如果没有不同字符，必须检查前缀情况：较短单词应该排在较长单词前面。
5. 看到 Alien Dictionary 不要立刻认定是 Graph；先判断题目是“已知顺序进行验证”，还是“根据关系推导顺序”。
