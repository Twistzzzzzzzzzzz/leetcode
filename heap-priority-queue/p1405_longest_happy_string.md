# 1405. Longest Happy String

## 题目

给定三个整数 `a`、`b`、`c`，分别表示最多可以使用多少个字符：

```text
"a"、"b"、"c"
```

构造一个尽可能长的字符串，并满足：

```text
不能出现 "aaa"
不能出现 "bbb"
不能出现 "ccc"
```

可以不使用完所有字符，只需要返回任意一个长度最大的合法字符串。

例如：

```text
a = 1, b = 1, c = 7
```

可以构造：

```text
"ccaccbcc"
```

仍可能剩下一个 `c`，但继续添加就会产生三个连续的 `c`，所以长度已经达到最大。

## 识别题型

题目同时出现：

```text
每种字符有剩余数量
+
高频字符最难安排
+
选择当前最多的字符可能违反局部连续限制
```

可以想到：

```text
最大堆 + 贪心 + 备用候选
```

最大堆负责优先消耗剩余数量最多的字符；当堆顶字符会形成三个连续字符时，临时改用第二多的字符打断它。

## 为什么优先使用剩余最多的字符

剩余数量最多的字符最难安排。

如果一直推迟它，其他字符可能很快被用完，最后只剩大量相同字符，无法继续添加。

因此贪心选择是：

```text
在不破坏合法性的前提下，优先使用剩余次数最多的字符
```

这与 767. Reorganize String、621. Task Scheduler 的核心直觉相同：高频元素应该尽早穿插处理。

## 最大堆如何保存字符

Python 的 `heapq` 是最小堆，所以保存负频率：

```python
(-remaining_count, char)
```

例如：

```text
a: 2
b: 5
c: 1
```

堆中保存：

```text
(-2, "a"), (-5, "b"), (-1, "c")
```

最小值 `-5` 位于堆顶，对应剩余次数最多的 `b`。

只把数量大于 0 的字符加入堆：

```python
for count, char in ((a, "a"), (b, "b"), (c, "c")):
    if count > 0:
        heapq.heappush(max_heap, (-count, char))
```

## 正常情况：直接使用第一候选

先弹出剩余次数最多的字符：

```python
first_count, first_char = heapq.heappop(max_heap)
```

如果添加它不会形成三个连续字符，就直接使用：

```python
answer.append(first_char)
first_count += 1
```

负频率执行一次后向 0 靠近。例如：

```text
-4 + 1 = -3
```

如果仍有剩余，再放回堆：

```python
if first_count < 0:
    heapq.heappush(max_heap, (first_count, first_char))
```

## 特殊情况：第一候选会形成三个连续字符

判断：

```python
len(answer) >= 2
and answer[-1] == first_char
and answer[-2] == first_char
```

如果成立，说明答案末尾已经是：

```text
first_char, first_char
```

此时不能再添加 `first_char`，即使它的剩余次数最多。

需要弹出第二候选：

```python
second_count, second_char = heapq.heappop(max_heap)
```

使用一次第二候选：

```python
answer.append(second_char)
second_count += 1
```

第二候选仍有剩余时，将它放回堆。

第一候选本轮没有使用，所以频率不能改变，并且必须原样放回：

```python
heapq.heappush(max_heap, (first_count, first_char))
```

下一轮因为答案最后一个字符已经变成 `second_char`，第一候选通常又可以继续使用。

## 为什么没有第二候选时必须停止

如果第一候选会形成三个连续字符，同时堆中没有其他字符：

```python
if not max_heap:
    break
```

说明当前状态是：

```text
答案末尾已经有两个相同字符
剩余字符也全部是这一种
```

无论如何都不能继续追加，剩余字符允许不用完，因此当前答案就是最长合法答案。

这里不能返回空字符串，因为前面已经构造出的部分仍然合法。

## 为什么不是像 767 那样总把当前字符留在堆外

[767. Reorganize String](p0767_reorganize_string.md) 要求相邻字符不能相同，因此一个字符使用后，下一轮一定不能再选它。

本题只禁止三个连续相同字符：

```text
"aa" 合法
"aaa" 非法
```

所以当前字符使用一次后可以立即放回堆。只有答案末尾已经连续出现两次时，才需要改用第二候选。

可以对比：

```text
767：限制连续 2 个相同 -> 当前字符固定等待一轮
1405：限制连续 3 个相同 -> 根据答案末尾两个字符动态判断
```

## 执行示例

```text
a = 1, b = 1, c = 7
```

一种执行过程：

| 步骤 | 堆顶首选 | 是否会形成三个连续字符 | 实际选择 | 答案 |
| --- | --- | --- | --- | --- |
| 1 | `c` | 否 | `c` | `c` |
| 2 | `c` | 否 | `c` | `cc` |
| 3 | `c` | 是 | 第二候选 `a` | `cca` |
| 4 | `c` | 否 | `c` | `ccac` |
| 5 | `c` | 否 | `c` | `ccacc` |
| 6 | `c` | 是 | 第二候选 `b` | `ccaccb` |
| 7 | `c` | 否 | `c` | `ccaccbc` |
| 8 | `c` | 否 | `c` | `ccaccbcc` |

最后仍剩一个 `c`，但答案以 `cc` 结尾且没有其他字符可用，所以停止。

## 代码

```python
import heapq


class Solution(object):
    def longestDiverseString(self, a, b, c):
        heap = []
        answer = []

        if a > 0:
            heapq.heappush(heap, (-a, "a"))
        if b > 0:
            heapq.heappush(heap, (-b, "b"))
        if c > 0:
            heapq.heappush(heap, (-c, "c"))

        while heap:
            first_count, first_char = heapq.heappop(heap)

            if (
                len(answer) >= 2
                and answer[-1] == first_char
                and answer[-2] == first_char
            ):
                if not heap:
                    break

                second_count, second_char = heapq.heappop(heap)
                answer.append(second_char)
                second_count += 1

                if second_count < 0:
                    heapq.heappush(heap, (second_count, second_char))

                heapq.heappush(heap, (first_count, first_char))
            else:
                answer.append(first_char)
                first_count += 1

                if first_count < 0:
                    heapq.heappush(heap, (first_count, first_char))

        return "".join(answer)
```

## 为什么返回结果不唯一

题目允许返回任意最长合法字符串。

当两个字符剩余次数相同时，选择哪一个都可能得到不同但同样正确的结果。Python 元组会使用字符作为第二排序字段，因此当前实现的结果是确定的，但不需要与示例字符串完全相同。

验证时应检查：

- 是否只使用 `a`、`b`、`c`；
- 每个字符使用次数是否超过给定数量；
- 是否存在三个连续相同字符；
- 最终长度是否达到最大。

## 正确性直觉

每轮有两种情况：

1. 最高频字符合法：立即使用它，有助于避免高频字符在最后堆积。
2. 最高频字符不合法：只有使用另一个字符才能继续，因此选择剩余次数第二多的字符最有利于后续安排。

如果最高频字符不合法且不存在第二候选，那么任何字符都无法合法追加，算法停止的位置必然已经达到最大长度。

## 复杂度

设最终构造的字符串长度为 `L`。

- 时间复杂度：O(L log 3)，也就是 O(L)
- 堆空间复杂度：O(3)，也就是 O(1)
- 答案空间复杂度：O(L)

堆中最多只有 `a`、`b`、`c` 三类字符。

## 常见错误

### 相邻两个字符相同就禁止继续使用

本题允许两个连续相同字符，只禁止三个连续字符。必须检查答案末尾两个位置是否都等于候选字符。

### 第一候选不合法时直接丢弃

第一候选只是本轮暂时不能使用，数量没有减少，必须原样放回堆。

### 第二候选使用后没有减少频率

第二候选也真实加入了答案，所以负频率需要 `+ 1`。

### 没有第二候选时继续弹堆

此时已经不存在合法扩展，应直接 `break`。

### 要求使用完所有字符

题目只要求最长合法字符串，并不保证所有字符都能使用。剩余字符无法合法追加时可以停止。

### 比较具体字符串答案

合法最长答案可能有多个，测试不应只接受某一个固定字符串。

## 心得

1. 高频字符优先是一种贪心策略，但每次选择前仍要检查局部连续限制。
2. 堆顶候选暂时不合法时，可以弹出第二候选打断连续状态，再把第一候选原样放回。
3. 第一候选没有使用就不能减少频率；第二候选实际使用后必须更新频率。
4. 没有第二候选且堆顶会违规时，说明任何字符都无法继续追加，当前答案已经最长。
5. 1405 允许连续两个相同字符，也允许不使用完所有字符，这是它与 767 的关键区别。
6. 当堆只包含固定三种字符时，堆操作可以视为常数时间，但这种写法能推广到更多字符类型。
