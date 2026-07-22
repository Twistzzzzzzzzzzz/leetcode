# 1834. Single-Threaded CPU

## 题目

每个任务表示为：

```text
tasks[i] = [enqueueTime, processingTime]
```

含义是：

- `enqueueTime`：任务从什么时候开始可以被 CPU 处理；
- `processingTime`：CPU 完成该任务需要多长时间；
- `i`：任务的原始下标，也是最终答案要返回的值。

CPU 每次选择任务时遵守：

1. 只能从已经到达的任务中选择。
2. 优先选择处理时间最短的任务。
3. 处理时间相同时，选择原始下标更小的任务。
4. 一旦开始处理任务，就必须完整执行，不能中途切换。

返回 CPU 实际处理任务的下标顺序。

## 识别题型

题目中同时存在：

```text
任务到达时间
+
当前可执行任务的优先级
+
CPU 时间不断向前推进
```

这是典型的：

```text
排序 + 优先队列 + 时间模拟
```

需要把任务分成两类状态：

```text
尚未到达：enqueueTime > current_time
已经到达：enqueueTime <= current_time
```

尚未到达的任务不能参与 CPU 选择；已经到达的任务才进入处理堆。

## 两种不同的排序规则

这题最重要的是不要把两种顺序混在一起。

### 尚未到达的任务

需要知道：

```text
下一批任务什么时候进入系统？
```

所以按照：

```text
(enqueueTime, ...)
```

排序。

### 已经到达的任务

需要知道：

```text
当前可执行任务中，CPU 应该先处理谁？
```

所以堆元素设计成：

```python
(processing_time, original_index)
```

Python 元组会先比较处理时间，相同时自动比较原始下标，正好符合题目规则。

## 你的双堆思路

你的总体框架是正确的：

```text
enqueue_heap：按进入时间保存尚未到达的任务
process_heap：按处理时间和下标保存当前可执行任务
```

两个堆分别回答不同问题：

```text
enqueue_heap -> 下一项任务何时到达？
process_heap -> 当前应该执行哪项任务？
```

修正索引和时间跳跃后，它的时间复杂度为 O(n log n)，可以通过题目。

## 原代码中的二维数组索引问题

### `tasks[0]` 不是第 `i` 个任务的进入时间

```python
tasks[0]
```

表示整个第一个任务，例如：

```text
[enqueueTime, processingTime]
```

第 `i` 个任务的进入时间应写为：

```python
tasks[i][0]
```

所以到达堆中保存：

```python
(tasks[i][0], i)
```

### `tasks[1]` 不是当前任务的处理时间

从到达堆弹出原始下标 `index` 后，对应处理时间是：

```python
tasks[index][1]
```

不能写成 `tasks[1]`，因为那表示整个第二项任务。

二维数组字段可以固定记成：

```python
tasks[index][0]  # enqueueTime
tasks[index][1]  # processingTime
```

## CPU 空闲时必须跳跃时间

假设：

```text
current_time = 1
下一项任务 enqueueTime = 1_000_000_000
```

如果每轮只执行：

```python
time += 1
```

会进行接近十亿次无意义循环。

当处理堆为空时，CPU 没有其他选择，可以直接把时间跳到下一项任务的到达时间：

```python
time = next_enqueue_time
```

这是一类时间模拟题的重要优化：

```text
系统当前无事可做时，直接跳到下一个事件发生的时刻
```

## 为什么到达堆可以换成排序数组

所有任务以及它们的到达时间在程序开始时就已经全部给出。

这意味着“未来任务的到达顺序”是静态信息，可以一次排序：

```python
ordered_tasks = sorted(
    (enqueue_time, processing_time, index)
    for index, (enqueue_time, processing_time) in enumerate(tasks)
)
```

然后使用指针 `next_task` 依次读取：

```text
ordered_tasks[0 : next_task] -> 已经处理过到达状态
ordered_tasks[next_task :]    -> 仍然尚未加入候选堆
```

因此主解只需要：

```text
一个排序数组 + 一个处理堆 + 一个指针
```

渐进复杂度仍然是 O(n log n)，但状态更少、代码更直接，也避免了到达堆的额外弹入弹出。

## 主解的执行流程

### 第一步：保存原始下标并排序

```python
ordered_tasks = sorted(
    (enqueue_time, processing_time, index)
    for index, (enqueue_time, processing_time) in enumerate(tasks)
)
```

原始下标必须在排序前保存，否则排序后会丢失题目要求返回的编号。

### 第二步：CPU 空闲时跳到下一个事件

```python
if not available_tasks and time < ordered_tasks[next_task][0]:
    time = ordered_tasks[next_task][0]
```

只有候选堆为空时才能这样跳跃；如果已有可执行任务，CPU 必须立即选择其中一个执行。

### 第三步：加入所有已经到达的任务

```python
while (
    next_task < len(ordered_tasks)
    and ordered_tasks[next_task][0] <= time
):
    _, processing_time, index = ordered_tasks[next_task]
    heapq.heappush(available_tasks, (processing_time, index))
    next_task += 1
```

这里必须使用 `while`，因为 CPU 完成一项任务后，可能已经有多项任务在这段时间内到达。

### 第四步：执行当前最优任务

```python
processing_time, index = heapq.heappop(available_tasks)
time += processing_time
answer.append(index)
```

任务执行期间新到达的任务不能打断当前任务；它们会在下一轮统一加入候选堆。

## 执行示例

```text
tasks = [[1, 2], [2, 4], [3, 2], [4, 1]]
```

任务信息：

| 下标 | 到达时间 | 处理时间 |
| --- | --- | --- |
| 0 | 1 | 2 |
| 1 | 2 | 4 |
| 2 | 3 | 2 |
| 3 | 4 | 1 |

模拟过程：

| 当前时间 | 已到达候选 `(处理时间, 下标)` | 执行任务 | 完成时间 |
| --- | --- | --- | --- |
| 1 | `(2, 0)` | 0 | 3 |
| 3 | `(4, 1), (2, 2)` | 2 | 5 |
| 5 | `(4, 1), (1, 3)` | 3 | 6 |
| 6 | `(4, 1)` | 1 | 10 |

答案为：

```text
[0, 2, 3, 1]
```

## 主解代码

```python
import heapq


class Solution(object):
    def getOrder(self, tasks):
        ordered_tasks = sorted(
            (enqueue_time, processing_time, index)
            for index, (enqueue_time, processing_time) in enumerate(tasks)
        )

        available_tasks = []
        answer = []
        time = 0
        next_task = 0

        while next_task < len(ordered_tasks) or available_tasks:
            if not available_tasks and time < ordered_tasks[next_task][0]:
                time = ordered_tasks[next_task][0]

            while (
                next_task < len(ordered_tasks)
                and ordered_tasks[next_task][0] <= time
            ):
                _, processing_time, index = ordered_tasks[next_task]
                heapq.heappush(available_tasks, (processing_time, index))
                next_task += 1

            processing_time, index = heapq.heappop(available_tasks)
            time += processing_time
            answer.append(index)

        return answer
```

## 保留双堆思路的版本

```python
import heapq


class Solution(object):
    def getOrder(self, tasks):
        arrival_heap = [
            (enqueue_time, index)
            for index, (enqueue_time, _) in enumerate(tasks)
        ]
        heapq.heapify(arrival_heap)

        available_tasks = []
        answer = []
        time = 0

        while arrival_heap or available_tasks:
            if not available_tasks:
                time = max(time, arrival_heap[0][0])

            while arrival_heap and arrival_heap[0][0] <= time:
                _, index = heapq.heappop(arrival_heap)
                heapq.heappush(
                    available_tasks,
                    (tasks[index][1], index),
                )

            processing_time, index = heapq.heappop(available_tasks)
            time += processing_time
            answer.append(index)

        return answer
```

## 是否已经是最优解

你的双堆版本修正后：

- 时间复杂度：O(n log n)
- 空间复杂度：O(n)

排序加单堆版本同样是：

- 时间复杂度：O(n log n)
- 空间复杂度：O(n)

所以从渐进复杂度看，双堆版本已经达到这道题的标准高效解法。

排序加单堆的优势主要是：

- 状态更少；
- 未来任务只需顺序读取；
- 常数开销更低；
- 更符合“静态数据先排序，动态候选用堆”的常见模式。

## 与 621. Task Scheduler 的区别

[621. Task Scheduler](p0621_task_scheduler.md) 也使用堆和时间模拟，但两题维护的“不可执行原因”不同：

```text
621：任务已经执行过，正在等待 cooldown 结束
1834：任务的 enqueueTime 还没有到达
```

共同点是：

```text
先维护哪些任务当前有资格执行
再用堆决定有资格的任务中先选谁
```

## 常见错误

### 把进入时间也放进处理优先级

任务一旦已经到达，CPU 的选择规则只比较：

```text
processingTime
originalIndex
```

进入时间只决定是否有资格进入候选堆。

### 时间每次只增加 1

CPU 空闲且下一任务很晚才到达时，必须直接跳到下一事件时间。

### 只加入一项已经到达的任务

同一时间可能有多项任务可执行，必须使用 `while` 全部加入候选堆后再选择。

### 忘记保存原始下标

排序会改变任务位置，必须在排序元组中提前携带原始下标。

### 忘记处理时间相同的规则

堆元素应为：

```python
(processing_time, index)
```

这样元组的第二字段会自动处理下标较小者优先。

### CPU 执行过程中加入新任务并抢占

本题 CPU 是非抢占式的。一项任务开始后，必须先完成；新任务只能等待下一次选择。

## 心得

1. 这题有两个不同状态：尚未到达的任务，以及已经到达的可执行任务。
2. 进入时间负责决定资格，处理时间和原始下标负责决定执行优先级。
3. 所有到达时间预先已知时，可以先排序，再用指针代替一个到达堆。
4. CPU 空闲时不要逐秒增加时间，应直接跳到下一项任务的到达时刻。
5. CPU 完成任务后，要用 `while` 将这段时间内到达的所有任务加入候选堆。
6. Python 元组 `(processing_time, index)` 可以直接表达题目的两级优先级。
7. 双堆方案在渐进复杂度上已经正确且高效；单堆方案主要优化状态数量和实现清晰度。
