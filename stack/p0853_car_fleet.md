# 853. Car Fleet

## 题目

有一组车，每辆车有：

- `position[i]`：当前位置
- `speed[i]`：速度

所有车都向同一个终点 `target` 行驶。

如果后面的车追上前面的车，它们会形成一个车队，并且之后以较慢车的速度一起行驶。

要求计算最终会有多少个车队到达终点。

## 思路

先把 `position` 和 `speed` 合并起来：

```python
cars = sorted(zip(position, speed), reverse=True)
```

这样每辆车就变成：

```python
(position, speed)
```

并且按位置从靠近终点到远离终点排序。

然后从离终点最近的车开始往后看。

对于每辆车，计算它自己到达终点需要的时间：

```python
time = (target - car_position) / car_speed
```

如果后面的车到达时间小于等于前面车队的时间，说明它能追上前面的车队，会合并进去。

如果后面的车到达时间更长，说明它追不上前面的车队，只能形成新的车队。

## 为什么从离终点最近的车开始看

车只能向前开，后面的车只能追前面的车。

所以要先知道前方车队的到达时间。

按位置从大到小排序后：

```text
离 target 最近的车在前面
离 target 更远的车在后面
```

这样遍历时，当前车只需要和前方最近形成的车队比较。

## 为什么可以只维护一个 `slowest_time`

`slowest_time` 表示前方最近一个车队到达终点需要的时间。

如果当前车的时间：

```python
time <= slowest_time
```

说明当前车更快或刚好一样快，能追上前方车队。

它不会形成新车队。

如果：

```python
time > slowest_time
```

说明当前车太慢，追不上前方车队。

它会形成一个新车队，并成为新的 `slowest_time`。

## 和单调栈的关系

这题可以理解成单调栈思想的简化版。

如果显式写栈，可以把每个车队的到达时间压入栈。

但因为我们从前往后扫描时，只需要比较最近的前方车队时间，所以可以用一个变量 `slowest_time` 代替栈顶。

也就是说：

```text
slowest_time 就是压缩后的栈顶信息
```

如果一道题的单调栈过程中只需要看栈顶，而不需要保留整个栈，就可以把栈压缩成一个变量。

这题里真正需要关心的只有：

```text
前方最近车队的到达时间
```

所以不需要显式维护一个栈，只用 `slowest_time` 就够了。

## `zip` 的用法

这题的 `position` 和 `speed` 是两个互相关联的列表。

同一个下标表示同一辆车：

```python
position[i]
speed[i]
```

这种情况下可以用 `zip` 把它们打包：

```python
cars = list(zip(position, speed))
```

例如：

```python
position = [10, 8, 0]
speed = [2, 4, 1]

list(zip(position, speed))
```

结果是：

```python
[(10, 2), (8, 4), (0, 1)]
```

之后就可以按位置排序：

```python
cars.sort(reverse=True)
```

或者直接写：

```python
cars = sorted(zip(position, speed), reverse=True)
```

一开始可能会担心排序把两个数组的对应关系打乱。

但只要先用 `zip` 把同一辆车的 `position` 和 `speed` 打包成元组，再排序，二者的关系就不会乱。

## 代码

```python
class Solution:
    def carFleet(self, target: int, position: list[int], speed: list[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)
        fleets = 0
        slowest_time = 0.0

        for car_position, car_speed in cars:
            time = (target - car_position) / car_speed

            if time > slowest_time:
                fleets += 1
                slowest_time = time

        return fleets
```

## 复杂度

- 时间复杂度：O(n log n)
- 空间复杂度：O(n)

主要成本来自排序。

## 心得

1. 这题可以看作单调栈思想：后车如果能追上前车队，就会被前车队合并。
2. 从离终点最近的车开始处理，只需要维护前方车队的到达时间。
3. `zip(position, speed)` 可以把两个互相关联的列表按下标打包，方便一起排序。
4. 如果当前车到达时间小于等于前方车队时间，就会合并；如果更长，就形成新车队。
5. 如果只需要栈顶，就可以压缩成一个变量；依旧是单调栈思想，但实现上更简单。
6. 遇到“追上”“合并”“被前面挡住”这类描述，可以考虑单调栈。
7. 两个数组之间也可以先排序再做题，只要用 `zip` 先把相关元素绑定起来。
8. 能合并到已有状态时，不更新主状态；形成新状态时，才更新主状态。
