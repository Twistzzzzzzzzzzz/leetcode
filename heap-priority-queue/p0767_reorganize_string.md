# 767. Reorganize String

## 题目

给定字符串 `s`，重新排列其中的字符，使任意两个相邻字符都不相同。

如果存在合法排列，返回任意一个；如果无法完成，返回空字符串 `""`。

例如：

```text
s = "aab"
```

可以返回：

```text
"aba"
```

而：

```text
s = "aaab"
```

无法让三个 `a` 都互不相邻，因此返回空字符串。

## 识别题型

题目同时出现：

```text
按照出现次数安排字符
+
高频字符最难放置
+
刚使用的字符下一轮不能再使用
```

可以想到：

```text
频率统计 + 最大堆 + 暂存上一轮字符
```

最大堆负责优先选择剩余次数最多的字符，暂存状态负责阻止同一个字符连续出现。

## 第一步：统计完整频率

可以手写字典：

```python
frequency = {}

for char in s:
    frequency[char] = frequency.get(char, 0) + 1
```

也可以使用：

```python
frequency = Counter(s)
```

堆中的一个元素代表一种字符及其剩余次数，而不是一个单独字符实例。

## 遍历字典时为什么需要 `.items()`

直接遍历字典：

```python
for item in frequency:
```

得到的只有键，也就是字符。

如果要同时取得字符和频率，必须写：

```python
for char, count in frequency.items():
```

原来的：

```python
for key, value in frequency:
```

会尝试把每一个字典键拆成两个值，并不是在遍历 `(key, value)`。

## 为什么使用最大堆

剩余次数最多的字符最难安排。如果一直推迟它，最后可能只剩下许多个相同字符，无法用其他字符隔开。

所以每轮优先选择：

```text
当前仍可使用的字符中，剩余次数最多者
```

Python 的 `heapq` 是最小堆，因此存入负频率：

```python
max_heap = [
    (-count, char)
    for char, count in Counter(s).items()
]
heapq.heapify(max_heap)
```

例如：

```text
a: 3
b: 2
c: 1
```

堆中保存：

```text
(-3, "a"), (-2, "b"), (-1, "c")
```

最小的负数 `-3` 位于堆顶，对应原频率最大的字符 `a`。

## 只使用最大堆为什么还不够

假设弹出 `a`，使用一次后马上把它重新压回堆：

```text
a 剩余次数仍然最多
```

下一轮可能又会弹出 `a`，产生：

```text
aa
```

所以最大堆只解决了：

```text
应该优先选择谁？
```

还需要额外解决：

```text
刚刚使用的字符下一轮没有资格参与选择
```

## 核心机制：上一轮字符暂时留在堆外

维护：

```python
previous_count = 0
previous_char = ""
```

每轮顺序固定为：

```text
1. 从堆中弹出当前字符。
2. 把当前字符加入答案，并减少剩余次数。
3. 将上一轮暂存的字符放回堆。
4. 把当前字符保存为新的 previous，继续留在堆外一轮。
```

代码：

```python
count, char = heapq.heappop(max_heap)
answer.append(char)
count += 1

if previous_count < 0:
    heapq.heappush(max_heap, (previous_count, previous_char))

previous_count = count
previous_char = char
```

因为当前字符直到下一轮选择结束前都不在堆中，所以它不可能连续被选中。

## 负频率为什么执行一次后是 `+ 1`

例如字符还剩 3 次，堆中保存：

```text
-3
```

使用一次后剩 2 次：

```text
-3 + 1 = -2
```

因此：

```python
count += 1
```

负频率应不断向 0 靠近，而不是继续减小。

## 为什么放回 previous 必须有条件

第一次循环前：

```python
previous_count = 0
previous_char = ""
```

如果无条件压回：

```python
heapq.heappush(max_heap, (previous_count, previous_char))
```

就会把不存在的占位记录 `(0, "")` 放入堆中。

只有上一轮字符仍有剩余时，才放回：

```python
if previous_count < 0:
```

负频率等于 0 说明该字符已经全部使用完。

## 为什么当前字符必须无条件更新为 previous

即使当前字符刚好用完，也必须执行：

```python
previous_count = count
previous_char = char
```

如果只在 `count < 0` 时更新，旧的 `previous` 可能被错误保留，并在后续再次压入堆，造成重复计数。

是否需要重新进入堆，由下一轮的：

```python
if previous_count < 0:
```

统一判断。

## 如何判断无解

循环结束时可能出现：

```text
最大堆已经为空
但 previous 字符仍有剩余
```

这说明只剩下与答案最后一个字符相同的字符，没有其他字符可以把它隔开。

因此：

```python
if previous_count < 0:
    return ""
```

也可以通过最终答案长度判断：

```python
if len(answer) != len(s):
    return ""
```

## 执行示例

```text
s = "aaabbc"
```

初始频率：

```text
a: 3
b: 2
c: 1
```

一种过程：

| 轮次 | 弹出字符 | 放回上一轮字符 | 答案 |
| --- | --- | --- | --- |
| 1 | `a` | 无 | `a` |
| 2 | `b` | `a` | `ab` |
| 3 | `a` | `b` | `aba` |
| 4 | `b` | `a` | `abab` |
| 5 | `a` | 无 | `ababa` |
| 6 | `c` | 无 | `ababac` |

每轮弹出时，上一轮字符仍在堆外，所以相邻字符一定不同。

## 代码

```python
import heapq
from collections import Counter


class Solution(object):
    def reorganizeString(self, s):
        max_heap = [
            (-count, char)
            for char, count in Counter(s).items()
        ]
        heapq.heapify(max_heap)

        answer = []
        previous_count = 0
        previous_char = ""

        while max_heap:
            count, char = heapq.heappop(max_heap)
            answer.append(char)
            count += 1

            if previous_count < 0:
                heapq.heappush(
                    max_heap,
                    (previous_count, previous_char),
                )

            previous_count = count
            previous_char = char

        if previous_count < 0:
            return ""

        return "".join(answer)
```

## 为什么使用列表和 `join`

字符串不可变。在循环中不断：

```python
answer += char
```

可能反复创建新字符串。

更适合的方式是：

```python
answer = []
answer.append(char)
return "".join(answer)
```

`join` 的调用方向是：

```python
separator.join(iterable)
```

所以：

```python
answer = answer.join(char)
```

并不是向 `answer` 末尾追加字符。

## 与 621. Task Scheduler 的联系

[621. Task Scheduler](p0621_task_scheduler.md) 使用最大堆和冷却队列。

本题可以理解为一个更简单的冷却限制：

```text
同一个字符不能出现在相邻位置
=
刚使用的字符必须等待一个其他字符
```

所以无需保存完整的恢复时间队列，只需把上一轮字符留在堆外一次。

共同结构是：

```text
堆负责从当前有资格的候选中选择
额外状态负责暂时隔离没有资格的候选
```

## 可行性的数学条件

如果最高频字符出现 `max_count` 次，字符串长度为 `n`，存在合法排列必须满足：

```text
max_count <= (n + 1) // 2
```

原因是最高频字符需要被其他字符隔开。最多可以占据下标：

```text
0, 2, 4, ...
```

共 `(n + 1) // 2` 个位置。

可以在建堆前使用这个条件提前返回，也可以像当前实现一样，让堆模拟在结尾自然检测失败。

## 复杂度

设字符串长度为 `n`，不同字符数量为 `u`。

- 时间复杂度：O(n log u)
- 空间复杂度：O(n + u)

答案列表占 O(n)，频率表和堆占 O(u)。如果不计算返回结果占用的空间，额外空间为 O(u)。

## 原代码中的关键问题

### 循环条件写反

```python
while not heap:
```

表示只有堆为空时才进入循环，随后弹出必然失败。正确条件是：

```python
while heap:
```

### `heapq` 没有 `pop`

应使用：

```python
heapq.heappop(heap)
```

### 错误理解 `join`

`join` 使用调用它的字符串作为分隔符连接一个可迭代对象，不会原地追加内容。

### 当前字符立即重新入堆

这样同一个高频字符可能连续两轮位于堆顶，违反相邻字符不能相同的要求。

### 无条件压入占位 previous

初始 `(0, "")` 不代表真实字符，不能进入堆。

### 只在仍有剩余时更新 previous

这会让更早的旧状态残留。当前字符无论是否用完，都必须覆盖 previous 状态。

### 未使用变量

原代码中的：

```python
n = len(s)
waiting = None
```

没有参与逻辑，应删除以避免干扰阅读。

## 心得

1. 频率字典要通过 `.items()` 同时遍历键和值。
2. 最大堆只能决定当前优先选谁，不能自动保证相邻字符不同。
3. 刚使用的字符需要暂时留在堆外，等另一个字符被选中后才能重新参与竞争。
4. 负频率使用一次后要 `+ 1`，让它向 0 靠近。
5. previous 是否重新入堆要有条件，但当前字符更新为 previous 必须无条件进行。
6. 堆为空而 previous 仍有剩余，说明只剩同一种字符，无法继续排列。
7. 循环构造字符串时优先使用列表收集，最后通过 `"".join(answer)` 合并。
