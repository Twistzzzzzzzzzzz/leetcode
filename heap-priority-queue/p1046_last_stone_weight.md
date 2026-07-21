# 1046. Last Stone Weight

## 题目

每次选择当前最重的两块石头，让它们相撞。

假设两块石头重量为 `x` 和 `y`，并且 `x >= y`：

- 如果 `x == y`，两块石头都消失。
- 如果 `x > y`，留下重量为 `x - y` 的新石头。

不断重复，返回最后一块石头的重量；如果所有石头都消失，返回 0。

## 识别题型

题目反复要求：

```text
取出当前最大的两个元素
处理后可能加入一个新元素
继续取当前最大值
```

这是 Priority Queue / Heap 的直接信号。

候选集合会不断变化，而每轮只关心最大的元素，所以不需要每轮重新排序整个数组。

## 为什么需要最大堆

每次必须快速取出当前最重的两块石头，也就是两个最大值。

理想操作是：

```text
弹出最大值：O(log n)
重新加入差值：O(log n)
```

最大堆正好支持这种操作。

## Python 如何模拟最大堆

Python 3.12 的 `heapq` 基础接口是最小堆。

把重量取负后：

```text
原重量：8 > 7 > 4
取负后：-8 < -7 < -4
```

最小堆会优先弹出 `-8`，再取一次负号，就得到原来的最大重量 8：

```python
heaviest = -heapq.heappop(max_heap)
```

所以：

```text
原值最大
-> 负值最小
-> 最小堆顶
```

## 初始化最大堆

先把全部重量取负：

```python
max_heap = [-stone for stone in stones]
```

再原地建堆：

```python
heapq.heapify(max_heap)
```

`heapify` 的时间复杂度是 O(n)。

## 你的初始化写法也正确

你的版本逐个插入：

```python
heap = []

for stone in stones:
    heapq.heappush(heap, -stone)
```

它同样会得到合法最大堆，逻辑没有问题。

区别是：

- 逐个 `heappush`：O(n log n)
- 列表推导后 `heapify`：O(n)

已有全部初始数据时，`heapify` 更直接。

## 为什么循环条件是 `len(heap) > 1`

每轮循环要连续弹出两块石头：

```python
x = -heapq.heappop(heap)
y = -heapq.heappop(heap)
```

所以进入循环前必须确保至少还有两块石头：

```python
while len(heap) > 1:
```

这个条件直接描述了循环所需的数据量。

## 第一版 `len(heap) != 1` 的问题

假设只剩两块相同重量的石头：

```text
[1, 1]
```

它们相撞后全部消失，堆长度变成 0。

第一版条件：

```python
while len(heap) != 1:
```

此时：

```text
0 != 1
```

仍然是 `True`，循环会继续进入，然后从空堆中弹出元素并报错。

你修正后的条件：

```python
while heap and len(heap) != 1:
```

能够同时排除长度 0 和长度 1，所以是正确的。

不过更直接的表达是：

```python
while len(heap) > 1:
```

它明确说明每轮需要至少两个元素。

## 每轮操作

弹出两个最大重量：

```python
heaviest = -heapq.heappop(max_heap)
second_heaviest = -heapq.heappop(max_heap)
```

因为堆每次弹出当前最小的负数，所以：

```text
heaviest >= second_heaviest
```

### 两块石头相同

```python
if heaviest == second_heaviest:
```

它们全部消失，不需要向堆中加入任何内容。

### 两块石头不同

留下差值：

```python
heaviest - second_heaviest
```

因为堆中保存负数，所以重新加入时取负：

```python
heapq.heappush(
    max_heap,
    -(heaviest - second_heaviest),
)
```

## 为什么相同时不加入 0

两块相同石头会完全消失，题意不是留下重量为 0 的石头。

所以相等时什么都不做即可。

即使加入 0，很多案例最终也可能得到相同数值，但会制造一个题目中并不存在的候选，并增加后续操作。

## 返回结果

循环结束时只有两种情况：

```text
堆中剩一块石头
堆为空
```

因此：

```python
return -max_heap[0] if max_heap else 0
```

堆非空时，内部保存的是负数，需要再次取负还原原重量。

## 示例过程

```text
stones = [2, 7, 4, 1, 8, 1]
```

每轮处理：

| 最重两块 | 结果 | 剩余重量集合 |
| --- | --- | --- |
| 8 和 7 | 加入 1 | 4, 2, 1, 1, 1 |
| 4 和 2 | 加入 2 | 2, 1, 1, 1 |
| 2 和 1 | 加入 1 | 1, 1, 1 |
| 1 和 1 | 全部消失 | 1 |

最终返回 1。

表格为了方便理解把集合写成有序形式，堆的内部列表本身不保证完全有序。

## 代码

```python
import heapq


class Solution:
    def lastStoneWeight(self, stones):
        max_heap = [-stone for stone in stones]
        heapq.heapify(max_heap)

        while len(max_heap) > 1:
            heaviest = -heapq.heappop(max_heap)
            second_heaviest = -heapq.heappop(max_heap)

            if heaviest != second_heaviest:
                heapq.heappush(
                    max_heap,
                    -(heaviest - second_heaviest),
                )

        return -max_heap[0] if max_heap else 0
```

## 复杂度

设石头数量为 `n`。

- 建堆：O(n)
- 每轮最多执行两次弹出和一次插入：O(log n)
- 最多进行 `n - 1` 轮

因此：

- 时间复杂度：O(n log n)
- 空间复杂度：O(n)

## 常见错误

### 使用最小堆但不取负

那样每次弹出的是最轻石头，不符合题意。

### 循环条件允许空堆进入

每轮需要两个元素，最清楚的条件是：

```python
while len(heap) > 1:
```

### 出堆后忘记还原负号

```python
value = -heapq.heappop(max_heap)
```

### 差值重新入堆时忘记取负

```python
heapq.heappush(max_heap, -difference)
```

### 相等时加入 0

相同石头应该全部消失，不需要保存 0。

## 心得

1. 看到“反复取出当前最大的两个元素”，可以直接想到最大堆。
2. Python 3.12 使用负数把最小堆模拟成最大堆，入堆和出堆都要处理符号。
3. 每轮需要弹出两个元素，所以循环条件应该直接写成 `while len(heap) > 1`。
4. `while len(heap) != 1` 无法处理两块相同石头相撞后堆变空的情况。
5. 已有全部初始数据时，可以先取负再使用 `heapify`，以 O(n) 完成建堆。
