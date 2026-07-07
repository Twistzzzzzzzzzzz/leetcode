# 981. Time Based Key-Value Store

## 题目

设计一个基于时间的键值存储结构，支持两个操作：

```python
set(key, value, timestamp)
get(key, timestamp)
```

`set` 会在某个时间戳存入一个值。

`get` 要返回这个 `key` 在不超过 `timestamp` 的最近一次记录。

如果不存在符合条件的记录，返回空字符串。

## 思路

这题可以拆成两层：

1. 外层用 HashMap，根据 `key` 找到对应的所有历史记录。
2. 内层因为 `timestamp` 是顺序添加的，所以每个 `key` 对应的记录列表天然有序，可以用二分查找。

数据结构可以设计成：

```python
self.data = {
    "foo": [(1, "bar"), (4, "bar2")]
}
```

也就是：

```text
key -> [(timestamp, value), ...]
```

`set` 时直接追加：

```python
self.data[key].append((timestamp, value))
```

`get` 时要找：

```text
最后一个 timestamp <= 查询时间
```

这本质上是一个边界二分。

## 二分写法

可以换一种等价说法：

```text
找第一个 timestamp > 查询时间的位置，然后答案是它前一个位置。
```

所以二分条件写成：

```python
if values[mid][0] <= timestamp:
    left = mid + 1
else:
    right = mid
```

循环结束后：

```python
left
```

指向第一个 `timestamp > 查询时间` 的位置。

那么：

```python
left - 1
```

就是最后一个 `timestamp <= 查询时间` 的位置。

## 左闭右开区间

这里用的是左闭右开区间：

```python
left = 0
right = len(values)
```

含义是：

```text
[left, right)
```

也就是包含 `left`，不包含 `right`。

所以 `right = len(values)` 不会越界，因为 `right` 本来就不是搜索范围里的真实下标。

循环条件是：

```python
while left < right:
```

当想把右边界缩到 `mid` 时，要写：

```python
right = mid
```

而不是：

```python
right = mid - 1
```

因为在 `[left, right)` 里，`right` 本来就不包含。

如果写 `right = mid`，新范围是：

```text
[left, mid)
```

这个范围已经排除了 `mid`。

## 代码

```python
class TimeMap:
    def __init__(self) -> None:
        self.data: dict[str, list[tuple[int, str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.data:
            self.data[key] = []

        self.data[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.data:
            return ""

        values = self.data[key]
        index = self._last_timestamp_not_after(values, timestamp)

        if index < 0:
            return ""

        return values[index][1]

    def _last_timestamp_not_after(
        self, values: list[tuple[int, str]], timestamp: int
    ) -> int:
        left = 0
        right = len(values)

        while left < right:
            mid = (left + right) // 2

            if values[mid][0] <= timestamp:
                left = mid + 1
            else:
                right = mid

        return left - 1
```

## 复杂度

设某个 `key` 下有 `m` 条记录。

`set` 时间复杂度：O(1)

`get` 时间复杂度：O(log m)

空间复杂度：O(n)，其中 `n` 是所有 `set` 操作存下来的记录总数。

## 心得

时间戳是顺序添加的，所以每个 `key` 下面可以直接放一个列表，列表元素是 `(timestamp, value)` 元组。

这题的二分重点是左闭右开区间：

```text
[left, right)
```

在左闭右开区间中，`right` 本来就不属于搜索范围，所以缩右边界时写：

```python
right = mid
```

不是：

```python
right = mid - 1
```

可以这样记：

| 模板 | 区间含义 | 循环 | 右边界更新 |
| --- | --- | --- | --- |
| 闭区间 | `[left, right]` | `while left <= right` | `right = mid - 1` |
| 左闭右开 | `[left, right)` | `while left < right` | `right = mid` |

一句话：

左闭右开里，`right` 本来就不包含，所以 `right = mid` 已经把 `mid` 排除掉了。
