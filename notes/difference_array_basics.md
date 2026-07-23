# 差分数组基础

## 1. 差分数组解决什么问题

差分数组适合处理：

```text
多次对连续区间进行增加或减少
+
最后需要知道每个位置的累计状态
```

典型描述包括：

- 在区间 `[left, right]` 全部增加某个值；
- 某批乘客在 `start` 上车，在 `end` 下车；
- 某段时间内同时进行若干活动；
- 多个区间覆盖后，求每个位置的总覆盖量；
- 只在事件开始和结束位置发生状态变化。

核心思想是：

```text
不逐个修改区间内部所有位置
只记录区间开始和结束处的变化
```

## 2. 它与前缀和的关系

前缀和把原数组累加起来：

```python
prefix[i] = prefix[i - 1] + nums[i]
```

差分数组记录相邻位置之间的变化：

```python
difference[i] = nums[i] - nums[i - 1]
```

对差分数组做前缀累加，就能还原原数组：

```python
current += difference[i]
```

所以可以这样记：

```text
前缀和：把状态累加起来
差分数组：先记录状态在哪里发生改变
```

## 3. 半开区间模板 `[start, end)`

如果区间 `[start, end)` 内全部增加 `value`：

```python
changes[start] += value
changes[end] -= value
```

之后做前缀累加：

```python
current = 0

for change in changes:
    current += change
```

为什么在 `end` 减去？

因为 `end` 不属于区间，从该位置开始，之前增加的影响需要取消。

## 4. 闭区间模板 `[left, right]`

如果题目使用闭区间 `[left, right]`：

```python
changes[left] += value
changes[right + 1] -= value
```

这里必须为 `right + 1` 预留数组空间。

对比：

```text
[start, end)  -> 在 end 撤销
[left, right] -> 在 right + 1 撤销
```

区间端点定义是差分数组最常见的错误来源。

## 5. 示例

长度为 6 的数组初始全是 0：

```text
[0, 0, 0, 0, 0, 0]
```

希望让半开区间 `[1, 4)` 增加 3：

```python
changes[1] += 3
changes[4] -= 3
```

差分变化为：

```text
[0, 3, 0, 0, -3, 0]
```

前缀累加后：

```text
[0, 3, 3, 3, 0, 0]
```

中间位置不需要逐个更新。

## 6. Car Pooling 如何使用差分

一段行程：

```text
[passengers, start, end]
```

表示乘客占用座位的区间为 `[start, end)`：

```python
changes[start] += passengers
changes[end] -= passengers
```

扫描地点并累加：

```python
current_passengers = 0

for change in changes:
    current_passengers += change

    if current_passengers > capacity:
        return False
```

对应题解：[1094. Car Pooling](../heap-priority-queue/p1094_car_pooling.md)。

## 7. 为什么它也叫扫描线思想

可以想象一条线从左向右扫描坐标：

```text
遇到 start -> 状态增加
遇到 end   -> 状态减少
```

差分数组适合坐标范围较小、可以直接分配数组的情况。

如果坐标很大但事件数量较少，可以改用事件字典：

```python
events = {}

events[start] = events.get(start, 0) + value
events[end] = events.get(end, 0) - value

current = 0

for position in sorted(events):
    current += events[position]
```

这仍然是边界变化加扫描线，只是不再为每个坐标创建数组。

## 8. 什么时候优先想到差分数组

看到以下组合时应考虑：

```text
区间增加 / 减少
+
操作很多
+
只关心最终累计状态
+
变化只发生在左右边界
```

进一步检查：

1. 区间是闭区间还是半开区间？
2. 坐标范围是否足够小？
3. 是最后统一查询，还是每次更新后立即查询？
4. 是否只需要聚合数量，而不需要知道具体对象是谁？

如果每次更新后都需要立即查询，普通离线差分数组通常不够，需要考虑树状数组、线段树等动态结构。

## 9. Difference Array、Heap 与排序怎么选

### Difference Array

```text
不关心具体对象
只关心每个位置的净变化
坐标范围可扫描
```

### Heap

```text
维护具体动态候选
反复取当前最小值或最大值
```

### 排序事件

```text
坐标很大
事件点较少
只需按事件发生顺序扫描
```

以 Car Pooling 为例：

```text
Heap：维护当前车上的具体行程，反复取最早下车者
Difference Array：只维护每个地点人数净变化
Event Sorting：只保存出现过变化的地点并排序
```

## 10. 复杂度

设操作数量为 `n`，坐标范围为 `M`：

- 建立差分：O(n)
- 前缀扫描：O(M)
- 总时间：O(n + M)
- 空间：O(M)

如果 `M` 是题目固定小常数，可以相对于 `n` 视为 O(1) 空间；一般分析仍建议明确写出 O(M)。

## 11. 常见错误

### 忘记撤销区间影响

只在起点增加，没有在结束边界减少。

### 混淆闭区间和半开区间

需要先明确在 `right` 还是 `right + 1` 撤销。

### 把变化量当成实际状态

差分数组必须通过前缀累加才能得到实际值。

### 数组长度不足

闭区间更新需要访问 `right + 1`，必须预留额外位置。

### 坐标巨大仍直接开数组

此时应改用事件排序或坐标压缩。

### 在线问题误用离线差分

普通差分适合先完成全部更新，再统一还原；更新和查询交错时需要其他结构。

## 12. 基础模板

### 半开区间

```python
changes = [0] * (size + 1)

for value, start, end in updates:
    changes[start] += value
    changes[end] -= value

current = 0
result = []

for index in range(size):
    current += changes[index]
    result.append(current)
```

### 闭区间

```python
changes = [0] * (size + 1)

for value, left, right in updates:
    changes[left] += value
    changes[right + 1] -= value
```

## 13. 当前阶段需要掌握什么

1. 知道差分数组记录的是边界变化。
2. 能区分 `[start, end)` 和 `[left, right]` 的撤销位置。
3. 会通过一次前缀累加还原状态。
4. 看到区间增减和小坐标范围时想到差分。
5. 坐标很大时知道改用事件排序或坐标压缩。
6. 能区分差分维护聚合变化，堆维护具体动态候选。

现阶段不需要中断其他专题大量刷差分题。先把 1094 作为模板记住，之后遇到区间边界增减题再回来看这份笔记即可。
