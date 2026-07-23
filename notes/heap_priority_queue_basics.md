# Heap / Priority Queue 基础

## 这个专题在解决什么问题

Heap / Priority Queue 最擅长处理一类反复出现的需求：

```text
在一批不断变化的候选元素中，反复取出当前最小值或最大值。
```

例如：

- 每次取出当前最大的石头
- 数据流中维护第 `k` 大元素
- 找距离原点最近的 `k` 个点
- 合并多个有序序列
- 每次选择最早结束的任务
- 根据频率取前 `k` 个元素

如果每加入一个新元素就把整个列表重新排序，会做很多不必要的工作。

堆只维护“谁应该在最前面”，不会维护全部元素的完整顺序。

## Heap 和 Priority Queue 是一回事吗

它们关系很近，但概念不同。

### Priority Queue：行为

Priority Queue，优先队列，描述一种抽象行为：

```text
加入一个带优先级的元素
查看当前优先级最高的元素
删除当前优先级最高的元素
```

这里的“最高优先级”可以定义成：

- 数值最小
- 数值最大
- 距离最近
- 结束时间最早
- 频率最高
- 自定义的多个排序字段

### Heap：实现

Heap，堆，是实现优先队列最常用的数据结构。

可以记成：

```text
Priority Queue 是想要的功能。
Heap 是实现这个功能的常用方法。
```

LeetCode 题目和讲解中经常混用两个词，但写代码时通常使用 Python 的 `heapq`。

## 什么是二叉堆

刷题中说的 heap 通常指 Binary Heap，二叉堆。

它同时满足两个性质。

### 性质一：完全二叉树

除最后一层外，每层都填满；最后一层从左到右连续排列。

因此不需要创建 `TreeNode`，可以直接使用列表紧凑存储。

### 性质二：堆序性质

最小堆 Min Heap：

```text
每个父节点 <= 它的孩子
```

最大堆 Max Heap：

```text
每个父节点 >= 它的孩子
```

所以：

```text
最小堆的根一定是全局最小值。
最大堆的根一定是全局最大值。
```

## 堆不是完全有序的

这是最重要的概念之一。

最小堆只保证：

```text
父节点不大于孩子
```

它不保证：

- 左孩子小于右孩子
- 同一层从左到右递增
- 底层列表整体递增

例如下面是一个合法最小堆的列表表示：

```text
[1, 3, 2, 8, 5, 4]
```

它不是排序数组，因为：

```text
3 > 2
```

但父子关系全部合法：

```text
1 <= 3, 2
3 <= 8, 5
2 <= 4
```

因此只能确定：

```python
heap[0]
```

是最小值，不能把 `heap[1]` 当成第二小值。

## 堆如何存进列表

对于列表中的下标 `i`：

```python
parent = (i - 1) // 2
left_child = 2 * i + 1
right_child = 2 * i + 2
```

例如：

```text
下标：  0  1  2  3  4  5
列表：[1, 3, 2, 8, 5, 4]
```

对应：

```text
        1
      /   \
     3     2
    / \   /
   8   5 4
```

刷题时通常不需要手写这些下标公式，因为 `heapq` 已经实现了维护逻辑。

但理解列表和树的对应关系，有助于理解为什么插入和删除是 O(log n)。

## 插入和删除为什么是 O(log n)

### 插入：向上调整

新元素先放到列表末尾，也就是完全二叉树最后的位置。

如果它破坏了父子顺序，就不断和父节点交换，直到恢复堆性质。

这个过程叫：

```text
sift up / bubble up / 向上调整
```

最多经过树高次交换，所以是 O(log n)。

### 删除堆顶：向下调整

删除根节点后，通常把列表最后一个元素移到根位置。

然后不断和更合适的孩子交换，直到恢复堆性质。

这个过程叫：

```text
sift down / 向下调整
```

同样最多经过树高次交换，所以是 O(log n)。

## Python 的 `heapq`

Python 使用标准库：

```python
import heapq
```

`heapq` 不是一个 Heap 类。

它是一组直接修改普通列表的函数：

```python
heap = []
heapq.heappush(heap, value)
value = heapq.heappop(heap)
```

当前仓库使用 Python 3.12，`heapq` 的基础公开接口按最小堆使用。

## 最常用的操作

| 操作 | Python | 复杂度 |
| --- | --- | --- |
| 建空堆 | `heap = []` | O(1) |
| 列表原地建堆 | `heapq.heapify(nums)` | O(n) |
| 插入 | `heapq.heappush(heap, x)` | O(log n) |
| 弹出最小值 | `heapq.heappop(heap)` | O(log n) |
| 查看最小值 | `heap[0]` | O(1) |
| 插入后弹出最小值 | `heapq.heappushpop(heap, x)` | O(log n) |
| 弹出最小值后插入 | `heapq.heapreplace(heap, x)` | O(log n) |

## `heappush`

```python
import heapq

heap = []

heapq.heappush(heap, 5)
heapq.heappush(heap, 2)
heapq.heappush(heap, 8)
heapq.heappush(heap, 1)
```

此时：

```python
heap[0] == 1
```

不要依赖列表中其他位置的具体顺序，只依赖堆顶和堆性质。

## `heappop`

```python
smallest = heapq.heappop(heap)
```

它会：

1. 删除并返回当前最小值。
2. 自动恢复最小堆性质。

连续弹出直到堆为空，会得到从小到大的顺序：

```python
while heap:
    print(heapq.heappop(heap))
```

但这样会清空原堆。

## 查看堆顶

```python
smallest = heap[0]
```

查看不会删除元素，时间复杂度为 O(1)。

访问前要确认堆非空：

```python
if heap:
    smallest = heap[0]
```

## `heapify`

已有普通列表时：

```python
nums = [5, 2, 8, 1, 4]
heapq.heapify(nums)
```

`heapify` 会原地把 `nums` 调整为最小堆。

注意它没有返回新列表：

```python
result = heapq.heapify(nums)
```

此时：

```python
result is None
```

正确用法是继续使用原列表 `nums`。

`heapify` 的时间复杂度是 O(n)，比把 `n` 个元素逐个 `heappush` 的 O(n log n) 更好。

直觉上，底层大量节点几乎不用移动，只有少数靠近根的节点可能移动很多层，因此总工作量可以压到 O(n)。

## `heappushpop` 和 `heapreplace`

这两个操作是进阶便利函数。

### `heappushpop(heap, x)`

逻辑上先加入 `x`，再弹出最小值：

```python
popped = heapq.heappushpop(heap, x)
```

它常用于维护固定大小的最小堆。

如果 `x` 比当前堆顶还小，`x` 自己可能直接被弹出，原堆基本保持不变。

### `heapreplace(heap, x)`

逻辑上先弹出当前最小值，再加入 `x`：

```python
popped = heapq.heapreplace(heap, x)
```

它一定会移除原来的堆顶，并把新值留下。

初学阶段不必强行使用这两个函数。先用清晰的：

```python
heapq.heappush(heap, x)

if len(heap) > k:
    heapq.heappop(heap)
```

更容易保证逻辑正确。

## Python 如何实现最大堆

Python 3.12 的 `heapq` 基础接口是最小堆。

如果需要最大堆，可以把数值取负：

```python
max_heap = []

heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -2)
heapq.heappush(max_heap, -8)
```

原值越大，负数越小：

```text
原值： 8 > 5 > 2
负值：-8 < -5 < -2
```

最小堆会把 `-8` 放在堆顶，所以取反后就是最大值：

```python
largest = -heapq.heappop(max_heap)
```

## 最大堆模板

```python
import heapq

max_heap = []

for value in nums:
    heapq.heappush(max_heap, -value)

while max_heap:
    largest = -heapq.heappop(max_heap)
```

最常见错误是：

- 入堆时忘记取负
- 出堆后忘记再取负
- 比较堆顶时忘记 `heap[0]` 保存的是负数

## 堆中保存元组

优先级不一定就是元素本身。

可以保存元组：

```python
heapq.heappush(heap, (priority, item))
```

Python 会按元组的字典序比较：

1. 先比较第一个字段 `priority`。
2. 第一个字段相同时，再比较第二个字段。
3. 仍然相同时，继续比较后续字段。

例如任务按结束时间排序：

```python
heapq.heappush(heap, (end_time, task_name))
```

堆顶就是结束时间最早的任务。

## 多字段优先级

如果要求：

```text
频率高的优先
频率相同时，字典序小的优先
```

就要把规则翻译为可比较的元组。

最小堆希望更优元素对应更小的元组，例如某些场景可以使用：

```python
(-frequency, word)
```

含义是：

- 频率越高，`-frequency` 越小
- 频率相同时，单词按正常字典序比较

写元组前必须明确每一位代表什么，以及升序还是降序。

## 优先级相同时的对象比较问题

假设 `item` 是自定义对象：

```python
heapq.heappush(heap, (priority, item))
```

当两个 `priority` 相同时，Python 会继续比较两个 `item`。

如果对象不支持大小比较，会出现 `TypeError`。

可以加入一个唯一的顺序号：

```python
from itertools import count

sequence = count()

heapq.heappush(
    heap,
    (priority, next(sequence), item),
)
```

这样优先级相同时，会比较不会重复的整数顺序号，而不会直接比较对象。

## 模式一：反复取当前最小值或最大值

如果题目反复执行：

```text
加入元素
取出当前最小 / 最大元素
继续处理
```

这是最直接的堆信号。

例如“每次取出最大的两块石头”：

```python
max_heap = [-stone for stone in stones]
heapq.heapify(max_heap)

while len(max_heap) > 1:
    first = -heapq.heappop(max_heap)
    second = -heapq.heappop(max_heap)

    if first != second:
        heapq.heappush(max_heap, -(first - second))
```

对应入门题：[1046. Last Stone Weight](../heap-priority-queue/p1046_last_stone_weight.md)。

## 模式二：保留最大的 `k` 个元素

这是最重要、也最反直觉的模板。

要保留最大的 `k` 个元素，通常维护：

```text
大小为 k 的最小堆
```

模板：

```python
heap = []

for value in nums:
    heapq.heappush(heap, value)

    if len(heap) > k:
        heapq.heappop(heap)
```

处理结束后，堆里是最大的 `k` 个元素。

堆顶：

```python
heap[0]
```

是这 `k` 个大元素中最小的一个，也就是整个数组的第 `k` 大元素。

## 为什么保留最大值却用最小堆

假设目标是保留最大的 3 个元素。

真正需要快速找到的是：

```text
当前保留集合中最弱的那个元素
```

因为当更大的新元素到来时，应该淘汰这个最弱元素。

最小堆的根正好是保留集合中的最小值，也就是淘汰门槛。

可以记成：

```text
保留最大的 k 个 -> 小顶堆负责淘汰最小者
```

## 模式三：保留最小的 `k` 个元素

对称地，保留最小的 `k` 个元素时，需要快速淘汰当前保留集合中最大的元素。

因此维护：

```text
大小为 k 的最大堆
```

Python 用负数实现：

```python
max_heap = []

for value in nums:
    heapq.heappush(max_heap, -value)

    if len(max_heap) > k:
        heapq.heappop(max_heap)
```

堆顶负数对应“当前保留的 `k` 个小元素中最大的那个”。

核心对照：

```text
保留最大的 k 个 -> 大小 k 的最小堆
保留最小的 k 个 -> 大小 k 的最大堆
```

对应入门题：[973. K Closest Points to Origin](../heap-priority-queue/p0973_k_closest_points_to_origin.md)。

## 模式四：第 `k` 大元素

```python
def find_kth_largest(nums, k):
    heap = []

    for value in nums:
        heapq.heappush(heap, value)

        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]
```

复杂度：

```text
时间：O(n log k)
空间：O(k)
```

当 `k` 远小于 `n` 时，它比完整排序后取下标更节省维护工作。

对应入门题：[215. Kth Largest Element in an Array](../heap-priority-queue/p0215_kth_largest_element_in_an_array.md)。

## 模式五：Top K Frequent

第一步使用 HashMap / Counter 统计频率：

```python
from collections import Counter

frequency = Counter(nums)
```

第二步维护大小为 `k` 的最小堆：

```python
heap = []

for value, count_value in frequency.items():
    heapq.heappush(heap, (count_value, value))

    if len(heap) > k:
        heapq.heappop(heap)
```

这里的堆元素含义是：

```text
(频率, 原值)
```

堆顶是当前入选元素中频率最低的，超过 `k` 时优先淘汰它。

所以 Top K Frequent 通常是：

```text
HashMap 统计频率
+
大小为 k 的最小堆维护候选
```

## 模式六：K 路归并

如果有多个已经有序的序列，要合并成一个有序序列：

```text
每个序列只把当前最小的候选放进堆
```

示例模板：

```python
heap = []

for list_index, values in enumerate(lists):
    if values:
        heapq.heappush(
            heap,
            (values[0], list_index, 0),
        )

result = []

while heap:
    value, list_index, element_index = heapq.heappop(heap)
    result.append(value)

    next_index = element_index + 1

    if next_index < len(lists[list_index]):
        heapq.heappush(
            heap,
            (
                lists[list_index][next_index],
                list_index,
                next_index,
            ),
        )
```

堆里每次最多保存每个序列的一个候选。

如果有 `k` 个序列，总元素数为 `n`：

```text
时间复杂度：O(n log k)
堆空间：O(k)
```

K 路归并不一定真的生成完整合并结果。如果只需要前若干个最优元素，可以在得到足够答案后立即停止。对应设计题：[355. Design Twitter](../heap-priority-queue/p0355_design_twitter.md)。

## 模式七：调度与最早结束时间

很多调度题会反复问：

- 当前最早结束的会议是什么？
- 哪台机器最早空闲？
- 哪个任务下一次最先执行？

可以把堆元素设计成：

```python
(end_time, resource_id)
```

堆顶始终是最早可以处理的候选。

有些调度题需要同时区分两类状态：

```text
最大堆：当前可以执行的任务，按剩余次数选择
冷却队列：当前不能执行的任务，按恢复时间等待
```

此时 cooldown 只负责判断任务是否可执行；真正的执行优先级由最大堆决定。对应练习：[621. Task Scheduler](../heap-priority-queue/p0621_task_scheduler.md)。

如果限制只是“刚使用的字符不能在下一轮再次使用”，可以把上一轮字符临时留在堆外，用一个变量代替完整冷却队列。对应练习：[767. Reorganize String](../heap-priority-queue/p0767_reorganize_string.md)。

如果堆顶候选只是在当前局部状态下不合法，可以临时使用第二候选，再把未使用的堆顶原样放回。对应练习：[1405. Longest Happy String](../heap-priority-queue/p1405_longest_happy_string.md)。

如果任务具有预先给定的到达时间，可以先按到达时间排序，用指针维护尚未到达的任务，再用堆维护当前可执行任务；CPU 空闲时直接跳到下一项任务的到达时刻。对应练习：[1834. Single-Threaded CPU](../heap-priority-queue/p1834_single_threaded_cpu.md)。

区间按起点进入、按终点离开时，可以排序起点并用最小堆维护最早终点；如果只关心边界净变化且坐标范围很小，差分数组可能更优。对应练习：[1094. Car Pooling](../heap-priority-queue/p1094_car_pooling.md)。

这类题的难点通常不是调用 `heapq`，而是先明确：

```text
堆中每个元组代表什么状态？
第一优先级和第二优先级分别是什么？
```

## 模式八：两个堆维护中位数

数据流中位数是进阶经典题。

通常维护：

```text
small：最大堆，保存较小的一半
large：最小堆，保存较大的一半
```

并维持：

```text
两边大小之差不超过 1
small 中所有值 <= large 中所有值
```

中位数只与两个堆顶有关。

这部分先知道思路即可，等做到 295. Find Median from Data Stream 时再详细整理。

## Heap、排序和线性扫描怎么选

### 只求一次最小值或最大值

直接扫描：

```python
min(nums)
max(nums)
```

时间 O(n)，不需要堆。

### 需要完整排序结果

直接排序通常更简单：

```python
nums.sort()
```

时间 O(n log n)。

### 只需要前 `k` 个，且 `k` 很小

大小为 `k` 的堆通常合适：

```text
O(n log k)
```

### 元素动态加入，并反复查询极值

堆非常合适：

```text
插入 O(log n)
查看堆顶 O(1)
弹出堆顶 O(log n)
```

## Heap 不擅长什么

堆擅长访问根，不擅长访问任意元素。

例如：

- 判断某个任意值是否存在，最坏要 O(n)
- 删除指定的任意元素并不直接
- 查找第 37 个位置没有意义
- 不能把内部列表当作排序结果

需要快速成员查找时用 `set` / HashMap。

需要完整有序遍历时通常用排序。

某些需要删除任意任务的进阶题，会采用“堆 + HashMap + 延迟删除”，后续遇到再学习。

## 题型识别信号

看到以下描述，可以优先考虑 Heap / Priority Queue：

- 第 `k` 大 / 第 `k` 小
- Top K
- 最常见的 `k` 个
- 最近的 `k` 个
- 每次取当前最大值 / 最小值
- 元素不断加入，持续查询极值
- 合并多个有序列表或有序序列
- 最早结束、最早空闲、下一次最先发生
- 候选集合不断变化，每轮选择优先级最高者
- 只关心最优的一小部分，而不是完整排序

一句话：

```text
动态候选集合 + 反复取极值 -> 考虑堆
```

## 堆元素设计

写堆题前，必须先明确堆中保存什么。

常见设计：

```text
value
(-value)
(frequency, value)
(distance, x, y)
(end_time, room_id)
(node.val, list_index, node)
```

每个字段都应该能回答：

1. 它代表什么？
2. 为什么放在这个位置？
3. 是升序还是通过取负实现降序？
4. 优先级相同时如何打破平局？

如果这四个问题没有说明白，代码很容易在符号或元组顺序上出错。

## 常见错误

### 认为整个堆是有序的

只能依赖 `heap[0]` 是最小值，其他位置不保证顺序。

### 最大堆忘记取负

入堆和出堆要成对处理：

```python
heapq.heappush(heap, -value)
value = -heapq.heappop(heap)
```

### `heapify` 的返回值用错

```python
heap = heapq.heapify(nums)
```

会让 `heap` 变成 `None`。`heapify` 修改的是原列表。

### 空堆直接访问 `heap[0]`

先判断：

```python
if heap:
```

### Top K 的堆方向写反

记住淘汰对象：

```text
保留最大 k 个，需要淘汰最小者 -> 最小堆
保留最小 k 个，需要淘汰最大者 -> 最大堆
```

### 固定大小堆出现 off-by-one

清晰模板是：

```python
heappush(...)

if len(heap) > k:
    heappop(...)
```

不是 `>= k`。

### 元组优先级相同时比较了不可比较对象

增加唯一顺序号：

```python
(priority, order, item)
```

### 把弹出的负数当成原值

最大堆弹出后记得还原符号。

### 一边遍历一边手动修改堆内部下标

不要直接删除 `heap[i]` 后期待堆仍然合法。优先使用 `heappush`、`heappop` 和 `heapify`。

## 固定思考流程

看到可能使用堆的题时，按这个顺序思考：

1. 候选集合里保存的是什么？
2. 每一步需要最快得到最小值还是最大值？
3. 需要完整排序，还是只需要 Top K / 一个极值？
4. 堆应该保存原值、负值还是元组？
5. 元组中每一位的优先级规则是什么？
6. 堆需要保存全部元素，还是只保留 `k` 个？
7. 超过大小后应该淘汰谁？
8. 优先级相同时是否会比较不可比较对象？
9. 最终答案在堆顶、整个堆中，还是弹出顺序中？

## 题型地图

### A. 基础最大堆 / 最小堆模拟

代表题：

- 1046. Last Stone Weight
- 2558. Take Gifts From the Richest Pile

重点：

- Python 最小堆
- 负数模拟最大堆
- 反复弹出和重新加入

### B. 第 K 大与固定大小堆

代表题：

- 703. Kth Largest Element in a Stream
- 215. Kth Largest Element in an Array
- 973. K Closest Points to Origin

重点：

- 大小固定为 `k`
- 保留最大 `k` 个使用最小堆
- 堆顶是当前淘汰门槛

### C. 频率 + Heap

代表题：

- 347. Top K Frequent Elements
- 692. Top K Frequent Words
- 451. Sort Characters By Frequency

重点：

- Counter / HashMap 先统计频率
- 元组优先级
- 频率相同时的规则

### D. K 路归并

代表题：

- 23. Merge k Sorted Lists
- 373. Find K Pairs with Smallest Sums
- 378. Kth Smallest Element in a Sorted Matrix

重点：

- 每个来源只放一个当前候选
- 弹出候选后，加入同一来源的下一个元素
- 堆大小通常与来源数量有关

### E. 调度与贪心

代表题：

- 621. Task Scheduler
- 767. Reorganize String
- 1834. Single-Threaded CPU

重点：

- 堆中状态的含义
- 多字段优先级
- 每轮选择当前最合适的任务

### F. 双堆

代表题：

- 295. Find Median from Data Stream
- 480. Sliding Window Median

重点：

- 最大堆维护较小一半
- 最小堆维护较大一半
- 平衡两个堆的大小

## 推荐刷题顺序

1. 1046. Last Stone Weight
2. 703. Kth Largest Element in a Stream
3. 215. Kth Largest Element in an Array
4. 347. Top K Frequent Elements
5. 973. K Closest Points to Origin
6. 692. Top K Frequent Words
7. 23. Merge k Sorted Lists
8. 355. Design Twitter
9. 621. Task Scheduler
10. 1834. Single-Threaded CPU
11. 1094. Car Pooling
12. 767. Reorganize String
13. 1405. Longest Happy String
14. 295. Find Median from Data Stream

前 3 题先练最小堆、最大堆和固定大小堆。

第 4 到 6 题练频率、距离和元组优先级。

第 7 到 8 题练 K 路归并和状态设计。

第 9 到 13 题练调度、区间与贪心。

295 是双堆综合题，最后再做。

## 必背模板

### 模板一：最小堆

```python
import heapq

heap = []

for value in nums:
    heapq.heappush(heap, value)

while heap:
    smallest = heapq.heappop(heap)
```

### 模板二：最大堆

```python
import heapq

max_heap = []

for value in nums:
    heapq.heappush(max_heap, -value)

while max_heap:
    largest = -heapq.heappop(max_heap)
```

### 模板三：第 `k` 大

```python
heap = []

for value in nums:
    heapq.heappush(heap, value)

    if len(heap) > k:
        heapq.heappop(heap)

answer = heap[0]
```

对应入门题：[703. Kth Largest Element in a Stream](../heap-priority-queue/p0703_kth_largest_element_in_a_stream.md)。

### 模板四：Top K Frequent

```python
from collections import Counter

frequency = Counter(nums)
heap = []

for value, count_value in frequency.items():
    heapq.heappush(heap, (count_value, value))

    if len(heap) > k:
        heapq.heappop(heap)

answer = [value for count_value, value in heap]
```

### 模板五：K 路归并候选

```python
heap = []

for source_index, source in enumerate(sources):
    if source:
        heapq.heappush(
            heap,
            (source[0], source_index, 0),
        )

while heap:
    value, source_index, item_index = heapq.heappop(heap)

    next_index = item_index + 1

    if next_index < len(sources[source_index]):
        heapq.heappush(
            heap,
            (
                sources[source_index][next_index],
                source_index,
                next_index,
            ),
        )
```

## 当前学习目标

当前阶段应该能够：

1. 解释 Priority Queue 和 Heap 的区别。
2. 说明最小堆只保证堆顶最小，不保证整个列表有序。
3. 使用 `heapify`、`heappush`、`heappop` 和 `heap[0]`。
4. 使用负数在 Python 3.12 中模拟最大堆。
5. 解释为什么保留最大的 `k` 个元素要使用大小为 `k` 的最小堆。
6. 明确堆中元组每个字段的含义和优先级。
7. 识别 Top K、反复取极值、K 路归并和调度题。
8. 区分什么时候使用堆、排序、线性扫描或 HashMap。
9. 写出固定大小堆和 K 路归并的基础模板。

先把 1046、703 和 215 写熟，再进入频率、归并和双堆题。
