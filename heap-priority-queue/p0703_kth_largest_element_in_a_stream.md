# 703. Kth Largest Element in a Stream

## 题目

设计一个类，在初始化时接收整数 `k` 和一个初始数组。

之后每次调用：

```python
add(val)
```

都把 `val` 加入数据流，并返回目前所有元素中的第 `k` 大元素。

注意题目问的是：

```text
第 k 大元素
```

不是：

```text
第 k 个不同的元素
```

重复值需要正常参与排名。

## 识别题型

题目同时出现：

```text
数据流不断加入新元素
+
每次都要查询第 k 大
```

这是固定大小堆的经典信号。

如果每次 `add` 后都重新排序全部历史元素，会重复处理大量旧数据。

我们真正需要保留的只有：

```text
截至目前最大的 k 个元素
```

## 为什么使用最小堆

这一点确实反直觉：

```text
题目要求第 k 大
却使用最小堆
```

假设当前最大的 3 个数是：

```text
10, 9, 8
```

第 3 大是：

```text
8
```

也就是这 3 个大数中最小的那个。

所以只要维护最大的 `k` 个元素：

```text
最小堆的堆顶
= 这 k 个元素中的最小值
= 所有元素中的第 k 大
```

## 最小堆是淘汰机制

堆里不需要保存全部历史数据，只保存当前最大的 `k` 个候选。

当新元素加入后，如果堆大小超过 `k`：

```python
heapq.heappop(self.heap)
```

最小堆会删除候选中最小的那个元素。

这意味着：

```text
更小、无法进入前 k 名的元素被淘汰
最大的 k 个元素继续留在堆中
```

堆顶就是当前入选集合中最弱的候选，因此同时也是第 `k` 大元素和下一轮的淘汰门槛。

可以记成：

```text
保留最大的 k 个 -> 大小为 k 的最小堆
```

## 为什么不用最大堆

最大堆能够快速找到所有候选中的最大值。

但本题为了维护最大的 `k` 个元素，超过大小后需要删除的是：

```text
这 k + 1 个候选中最小的那个
```

最大堆的堆顶是最大值，无法直接告诉我们应该淘汰哪个最小值。

最小堆正好把淘汰对象放在根节点，所以更合适。

对称地：

```text
保留最小的 k 个 -> 大小为 k 的最大堆
```

## 必须维持的三个不变量

每次初始化或 `add` 完成后，都应该满足：

1. `self.heap` 是合法最小堆。
2. `len(self.heap) <= k`。
3. 堆中保存目前见过的最大 `k` 个元素；如果总元素不足 `k`，就保存全部元素。

当至少有 `k` 个元素时：

```python
self.heap[0]
```

就是第 `k` 大元素。

## 初始化

```python
self.heap = []
self.k = k

for value in nums:
    heapq.heappush(self.heap, value)

    if len(self.heap) > self.k:
        heapq.heappop(self.heap)
```

每加入一个初始值，就立即把堆恢复到最多 `k` 个元素。

所以初始化结束时，不论 `nums` 有多长，堆最多只有 `k` 个元素。

## 你的初始化写法为什么也正确

你的版本先把全部元素加入：

```python
for value in nums:
    heapq.heappush(self.heap, value)
```

然后统一删除多余的最小值：

```python
while len(self.heap) > self.k:
    heapq.heappop(self.heap)
```

最终同样只会留下最大的 `k` 个元素，因此逻辑完全正确。

整理后的版本选择在每次插入后立即裁剪：

```python
if len(self.heap) > self.k:
    heapq.heappop(self.heap)
```

这样中间堆的大小也不会超过 `k + 1`，初始化时间为 O(n log k)，额外空间为 O(k)。

## 为什么初始化用 `if`，你的版本用 `while`

如果每插入一个元素后立刻检查，堆大小最多只会从 `k` 变成 `k + 1`。

所以弹出一次就够了：

```python
if len(heap) > k:
    heappop(heap)
```

如果先把所有元素一次性加入，堆可能比 `k` 大很多，因此需要不断弹出：

```python
while len(heap) > k:
    heappop(heap)
```

两者的区别来自检查时机，而不是 `if` 或 `while` 本身谁更正确。

## `add` 操作

先让新元素进入候选集合：

```python
heapq.heappush(self.heap, val)
```

如果候选超过 `k` 个，就删除最小者：

```python
if len(self.heap) > self.k:
    heapq.heappop(self.heap)
```

最后返回堆顶：

```python
return self.heap[0]
```

## 为什么必须先加入，再淘汰

新元素也可能进入最大的 `k` 个。

必须先让它参与比较，再由最小堆决定谁被淘汰。

例如当前：

```text
k = 3
heap 中保存 5, 8, 10
```

加入 9 后，候选是：

```text
5, 8, 9, 10
```

弹出最小值 5，留下：

```text
8, 9, 10
```

新的第 3 大就是 8。

如果新元素是 2，加入后最小值就是 2，它会立即被弹出，原来的最大 3 个不变。

## 执行示例

```text
k = 3
nums = [4, 5, 8, 2]
```

初始化后保留最大的三个元素：

```text
4, 5, 8
```

堆顶是 4，所以当前第 3 大是 4。

后续：

| 操作 | 加入后保留的最大 3 个 | 返回值 |
| --- | --- | --- |
| `add(3)` | `4, 5, 8` | 4 |
| `add(5)` | `5, 5, 8` | 5 |
| `add(10)` | `5, 8, 10` | 5 |
| `add(9)` | `8, 9, 10` | 8 |
| `add(4)` | `8, 9, 10` | 8 |

表格中的集合为了方便理解写成了有序形式，堆内部列表本身不保证完全有序。

## 代码

```python
import heapq


class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = []

        for value in nums:
            heapq.heappush(self.heap, value)

            if len(self.heap) > self.k:
                heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)

        if len(self.heap) > self.k:
            heapq.heappop(self.heap)

        return self.heap[0]
```

## 复杂度

设初始数组长度为 `n`。

### 初始化

- 时间复杂度：O(n log k)
- 空间复杂度：O(k)

每次插入和可能的弹出都在大小最多为 `k + 1` 的堆上进行。

### 每次 `add`

- 时间复杂度：O(log k)
- 额外空间复杂度：O(1)

整个对象持续保存 O(k) 个元素。

## 常见错误

### 使用最大堆

最大堆方便得到第一大，却不方便淘汰最大的 `k` 个候选中最小的那个。

### 保存全部数据

题目只需要第 `k` 大，不需要保留所有无法进入前 `k` 名的历史元素。

### 写成 `len(heap) >= k`

```python
if len(heap) >= k:
    heappop(heap)
```

会导致最终只保留 `k - 1` 个元素。

正确条件是：

```python
if len(heap) > k:
```

### 认为整个堆已经排序

只能确定：

```python
heap[0]
```

是堆中最小值，不能依赖其他下标顺序。

### 忘记重复值也参与排名

例如：

```text
[5, 5, 5]
```

第 2 大仍然是 5，不需要使用集合去重。

## 心得

1. 第 `k` 大使用最小堆确实反直觉，关键是堆只保存最大的 `k` 个元素。
2. 堆顶是这 `k` 个候选中最小的，因此正好是整个数据流的第 `k` 大。
3. 最小堆还负责快速淘汰无法留在前 `k` 名的最弱候选。
4. 每次先加入新元素，再在堆大小超过 `k` 时弹出最小值。
5. 固定大小堆不需要保存全部历史数据，单次更新只需 O(log k)。
6. 看到“数据流 + 持续查询第 k 大”，可以直接想到大小为 `k` 的最小堆。
