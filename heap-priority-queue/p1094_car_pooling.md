# 1094. Car Pooling

## 题目

每段行程表示为：

```text
[numPassengers, from, to]
```

含义是：

- 在地点 `from` 有 `numPassengers` 名乘客上车；
- 在地点 `to` 这些乘客下车；
- 乘客实际占用座位的区间是 `[from, to)`。

给定车辆容量 `capacity`，判断能否完成所有行程且任意时刻都不超载。

## 你的堆解法为什么值得肯定

你一遍通过的关键不是碰巧，而是正确抓住了三个状态：

1. 先按上车地点排序，让车辆沿路线向前处理。
2. 用最小堆按照下车地点管理仍在车上的行程。
3. 到达当前地点时先让到站乘客下车，再让新乘客上车。

这就是：

```text
按开始位置扫描
+
用堆维护最早结束的活动区间
```

尤其是同一地点的处理顺序：

```python
while heap and heap[0][0] <= start:
    # 先下车

# 再上车
```

保证了地点 5 下车释放的座位，可以立即被地点 5 上车的乘客使用。

## 更清晰的堆不变量

整理后的堆解法让堆只保存：

```text
已经上车，但还没有下车的行程
```

堆元素为：

```python
(end, passengers)
```

堆顶是当前车上所有行程中最早下车的一批乘客。

每处理一段新行程：

```text
1. 弹出所有 end <= start 的旧行程，并减去乘客。
2. 加上当前行程上车人数。
3. 检查容量。
4. 把当前行程按 end 加入堆。
```

你的原版提前把所有行程的结束位置放进堆，在题目 `from < to` 且已经按 `from` 排序的前提下也能工作；但“堆只存当前有效行程”的不变量更直观，也更容易推广。

## 堆解法代码

```python
import heapq


class HeapSolution(object):
    def carPooling(self, trips, capacity):
        ordered_trips = sorted(trips, key=lambda trip: trip[1])
        active_trips = []
        current_passengers = 0

        for passengers, start, end in ordered_trips:
            while active_trips and active_trips[0][0] <= start:
                _, leaving_passengers = heapq.heappop(active_trips)
                current_passengers -= leaving_passengers

            current_passengers += passengers

            if current_passengers > capacity:
                return False

            heapq.heappush(active_trips, (end, passengers))

        return True
```

## 堆解法复杂度

设行程数量为 `n`：

- 排序：O(n log n)
- 每段行程最多入堆、出堆各一次：O(n log n)
- 总时间复杂度：O(n log n)
- 空间复杂度：O(n)

这是正确而且通用的区间扫描解法。

## 为什么本题还能进一步优化

本题额外给出了很强的条件：地点范围很小。

如果最大地点不超过 1000，我们不必保存每一段具体行程，只需要知道：

```text
每个地点，车上人数净变化了多少
```

这就可以使用差分数组。

## 差分数组思路

对于一段行程：

```text
[passengers, start, end]
```

只记录两个边界：

```python
changes[start] += passengers
changes[end] -= passengers
```

之后从左到右累加：

```python
current_passengers += changes[location]
```

就能得到经过每个地点后的车上人数。

行程对应半开区间 `[start, end)`，所以在 `end` 位置减去乘客，表示到达该地点后这些乘客已经不再占座位。

## 同一地点先下车再上车如何体现

假设地点 5 同时发生：

```text
3 人下车
2 人上车
```

差分数组在该位置记录：

```text
-3 + 2 = -1
```

也就是车上人数净减少 1。

它不需要显式写“先下车再上车”，边界变化合并后的净结果已经与题意一致。

## 差分数组主解

```python
class Solution(object):
    def carPooling(self, trips, capacity):
        furthest_location = max((end for _, _, end in trips), default=0)
        passenger_changes = [0] * (furthest_location + 1)

        for passengers, start, end in trips:
            passenger_changes[start] += passengers
            passenger_changes[end] -= passengers

        current_passengers = 0

        for change in passenger_changes:
            current_passengers += change

            if current_passengers > capacity:
                return False

        return True
```

## 差分数组复杂度

设：

- `n` 为行程数量；
- `M` 为最远地点。

复杂度为：

- 时间：O(n + M)
- 空间：O(M)

本题中 `M <= 1000`，因此常被写作：

```text
时间 O(n)
空间 O(1)
```

这里的 O(1) 是相对于输入行程数量 `n` 而言，因为地点上限是题目固定常数。推广到任意坐标范围时，仍应写成 O(M)。

## 差分数组属于哪个专题

差分数组通常归入：

```text
Arrays
-> Prefix Sum
-> Difference Array
-> Interval Updates / Sweep Line
```

它可以看作前缀和的反向使用：

```text
差分数组先记录边界变化
前缀累加再还原每个位置的实际状态
```

从知识依赖看，它通常比 Heap 更基础；但题单常把它分散放在 Prefix Sum、Intervals 或 Sweep Line 中，所以现在第一次系统遇到很正常。

完整入门笔记见：[差分数组基础](../notes/difference_array_basics.md)。

## 如何判断 Heap 还是差分数组

### 优先考虑 Heap

当题目符合：

```text
候选集合动态变化
+
需要反复取得当前最小值或最大值
```

例如本题的堆视角：

```text
当前有多段未结束行程
需要反复找到最早下车的位置
```

### 优先考虑差分数组

当题目符合：

```text
每个操作作用于一个连续区间
+
只关心边界处增加和减少
+
最后按坐标顺序扫描
+
坐标范围可承受
```

例如本题的差分视角：

```text
不关心每批乘客是谁
只关心每个地点人数变化多少
```

差分数组利用了更强的题目结构，所以在本题约束下优于堆。

## 与 1834 的联系

[1834. Single-Threaded CPU](p1834_single_threaded_cpu.md) 中：

```text
任务按到达时间加入动态候选集合
CPU 反复取处理时间最短者
```

因此堆是核心数据结构。

1094 虽然也能用堆维护活动区间，但因为只需要累计人数且坐标范围很小，可以进一步压缩成边界变化。

这说明：

```text
能用堆，不等于堆一定是最终最优方法
```

## 常见错误

### 在同一地点先上车再下车

会错误地认为车辆短暂超载。堆解法必须先弹出所有 `end <= start` 的行程。

### 把区间当成 `[start, end]`

乘客在 `end` 地点已经下车，实际占用区间是 `[start, end)`。

### 差分数组忘记在终点减去人数

只写起点增加会让乘客永远留在车上。

### 差分变化后没有做前缀累加

`changes[location]` 表示变化量，不是当前位置的实际乘客数。

### 坐标巨大时仍创建完整数组

如果坐标可能达到十亿，O(M) 数组不可行。此时应考虑排序事件、坐标压缩或堆。

## 心得

1. 按上车地点排序，再用最小堆管理最早下车行程，是正确的通用区间扫描建模。
2. 同一地点必须先释放已经结束行程的座位，再处理新乘客上车。
3. 动态候选集合中反复取得最早结束位置，是 Heap 的识别信号。
4. 如果不关心具体行程，只关心区间边界的净变化，可以进一步想到差分数组。
5. 差分数组属于 Arrays / Prefix Sum 的延伸，不需要中断 Heap 专题单独深挖，但应记住其识别模板。
6. 混合刷题时先问题目真正需要维护“具体对象”还是“聚合变化”，能够帮助选择堆或差分数组。
