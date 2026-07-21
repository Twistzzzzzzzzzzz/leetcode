# 973. K Closest Points to Origin

## 题目

给定平面上的一组点：

```text
[x, y]
```

返回距离原点 `(0, 0)` 最近的 `k` 个点。

答案顺序可以任意。

## 识别题型

题目要求：

```text
距离最小的 k 个元素
```

这是 Top K 问题。

如果不需要完整排序，只需要保留最优的 `k` 个候选，可以维护固定大小堆：

```text
保留最小的 k 个
-> 大小为 k 的最大堆
```

## 为什么保留最近的点却使用最大堆

这一点和 703 正好相反。

堆中只保留当前最近的 `k` 个点。

当新点加入后，如果候选数量变成 `k + 1`，需要淘汰的是：

```text
这些候选中距离最远的点
```

所以我们需要让“最远候选”位于堆顶，以便 O(log k) 删除。

这就是最大堆。

可以记成：

```text
保留最小的 k 个 -> 最大堆负责淘汰最大者
```

## 与 703 的对照

| 目标 | 保留内容 | 需要快速淘汰 | 使用的堆 |
| --- | --- | --- | --- |
| 第 `k` 大 / 最大的 `k` 个 | 最大的 `k` 个 | 最小候选 | 最小堆 |
| 最近的 `k` 个 / 最小的 `k` 个 | 最小的 `k` 个 | 最大候选 | 最大堆 |

选择堆方向时，不要只看题目写“最大”还是“最小”。

应该问：

```text
当候选超过 k 个时，我需要最快淘汰谁？
```

## 为什么不需要开平方

点 `(x, y)` 到原点的欧几里得距离是：

```text
sqrt(x² + y²)
```

但平方根函数是单调递增的：

```text
a < b
-> sqrt(a) < sqrt(b)
```

所以比较距离时，直接比较平方距离即可：

```python
distance_squared = x * x + y * y
```

这样避免了不必要的浮点数和开平方计算。

## Python 如何模拟最大堆

Python 3.12 的 `heapq` 基础接口是最小堆。

把平方距离取负：

```python
negative_distance_squared = -(x * x + y * y)
```

距离越远，平方距离越大，取负后越小：

```text
平方距离：25 > 10 > 2
取负后： -25 < -10 < -2
```

最小堆会把 `-25` 放在堆顶，它对应原本距离最远的点。

所以每次：

```python
heapq.heappop(max_heap)
```

删除的就是当前候选中最远的点。

## 堆元素保存什么

```python
(negative_distance_squared, point)
```

第一项控制优先级：

```text
最远的点对应最小的负距离
```

第二项保存最终需要返回的原始点：

```python
[x, y]
```

因此加入堆：

```python
heapq.heappush(
    max_heap,
    (negative_distance_squared, point),
)
```

## 必须维持的不变量

处理每个点之后：

1. `max_heap` 按负距离维护为合法最小堆，也就是逻辑上的最大堆。
2. `len(max_heap) <= k`。
3. 堆中保存目前处理过的点里距离最小的 `k` 个。

加入新点后：

```python
if len(max_heap) > k:
    heapq.heappop(max_heap)
```

最远候选会被淘汰，不变量重新成立。

## 示例过程

```text
points = [[1, 3], [-2, 2]]
k = 1
```

平方距离：

```text
[1, 3]  -> 1² + 3² = 10
[-2, 2] -> 2² + 2² = 8
```

先加入 `[1, 3]`：

```text
堆中保存距离 10
```

再加入 `[-2, 2]`：

```text
候选距离为 10 和 8
堆大小超过 1
最大堆淘汰距离 10
```

最终留下 `[-2, 2]`。

## 为什么第一版 `return heap` 不符合返回类型

堆中保存的是：

```python
(negative_distance_squared, point)
```

所以直接：

```python
return heap
```

会得到类似：

```python
[
    (-8, [-2, 2]),
    (-10, [1, 3]),
]
```

但题目要求返回：

```python
[
    [-2, 2],
    [1, 3],
]
```

需要把元组中的点提取出来：

```python
return [point for distance, point in heap]
```

距离变量没有使用时，可以写成：

```python
return [point for _, point in heap]
```

下划线表示这个字段只用于占位，不会在表达式中使用。

## 返回结果为什么不需要排序

题目允许任意顺序返回最近的 `k` 个点。

堆内部不是完整排序结构，但它已经保存了正确的 `k` 个点，所以直接提取即可。

如果题目要求按照距离从近到远返回，还需要额外排序答案或按正确方向弹出。

## 相同距离如何比较

当前堆元素是：

```python
(negative_distance_squared, point)
```

两个点距离相同时，Python 会继续比较第二项 `point`。

本题中的点是两个整数构成的列表，能够按字典序比较，因此代码可以正常运行。

如果第二项是不能比较的自定义对象，可以加入唯一序号：

```python
(negative_distance_squared, index, point)
```

避免优先级相同时直接比较对象。

## 代码

```python
import heapq


class Solution:
    def kClosest(self, points, k):
        max_heap = []

        for point in points:
            x, y = point
            negative_distance_squared = -(x * x + y * y)

            heapq.heappush(
                max_heap,
                (negative_distance_squared, point),
            )

            if len(max_heap) > k:
                heapq.heappop(max_heap)

        return [point for _, point in max_heap]
```

## 另一种思路：全部放进最小堆

也可以把所有点按正常正距离放进最小堆：

```python
min_heap = []

for point in points:
    x, y = point
    distance_squared = x * x + y * y
    heapq.heappush(min_heap, (distance_squared, point))
```

然后弹出 `k` 次最小值。

这种写法更直观，但需要保存全部 `n` 个点：

- 时间复杂度：O(n + k log n)，如果使用 `heapify`
- 空间复杂度：O(n)

固定大小最大堆只保存 `k` 个点：

- 时间复杂度：O(n log k)
- 空间复杂度：O(k)

当 `k` 远小于 `n` 时，固定大小堆更合适。

## 复杂度

设点的数量为 `n`。

- 时间复杂度：O(n log k)
- 空间复杂度：O(k)

每个点执行一次插入，堆大小最多为 `k + 1`；超过 `k` 时再执行一次弹出。

## 常见错误

### 使用最小堆保存最近的 `k` 个

固定大小候选超过 `k` 时需要淘汰最远点，因此堆顶必须是最大距离。

### 计算了平方根

比较远近只需要平方距离，不需要 `sqrt`。

### 返回了堆中的完整元组

题目只需要点，需要从 `(distance, point)` 中提取 `point`。

### 认为堆中结果按距离排好序

堆只保证根的优先级，题目允许任意顺序，所以这里不需要排序。

### 固定大小判断写成 `>= k`

应该只在超过 `k` 时弹出：

```python
if len(heap) > k:
```

## 心得

1. 看到“距离最近的 `k` 个”，可以想到固定大小 Top K 堆。
2. 保留最小的 `k` 个元素时，需要最大堆快速淘汰当前最远候选。
3. Python 使用负平方距离把最小堆模拟成最大堆。
4. 距离比较不需要开平方，直接使用 `x * x + y * y`。
5. 堆中保存 `(优先级, 最终数据)` 时，返回答案要提取真正需要的数据，而不是直接返回整个堆。
6. 选择堆方向时要问“超过 k 个后要淘汰谁”，而不是只看题目写最大还是最小。
