# 706. Design HashMap

## 题目

不使用 Python 内置的 `dict`，自己实现一个 HashMap。

需要支持三个操作：

- `put(key, value)`：插入或更新一个键值对
- `get(key)`：根据 `key` 获取对应的 `value`，如果不存在返回 `-1`
- `remove(key)`：删除某个 `key`

## 思路

这题和 705 Design HashSet 很像。

区别是：

- HashSet 只需要判断 `key` 是否存在
- HashMap 需要保存 `key -> value`

所以桶里不能只存 `key`，而是要存键值对：

```python
[key, value]
```

整体结构还是：

1. 用一个数组保存很多个桶。
2. 用哈希函数把 `key` 映射到桶下标。
3. 桶里用列表保存多个 `[key, value]`，处理哈希冲突。

## 哈希函数

```python
index = key % size
```

这样可以把整数 `key` 映射到 `[0, size - 1]` 之间的下标。

## 代码

```python
class MyHashMap:
    def __init__(self) -> None:
        self.size = 1009
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def put(self, key: int, value: int) -> None:
        index = self._hash(key)

        for pair in self.buckets[index]:
            if pair[0] == key:
                pair[1] = value
                return

        self.buckets[index].append([key, value])

    def get(self, key: int) -> int:
        index = self._hash(key)

        for pair in self.buckets[index]:
            if pair[0] == key:
                return pair[1]

        return -1

    def remove(self, key: int) -> None:
        index = self._hash(key)

        for i, pair in enumerate(self.buckets[index]):
            if pair[0] == key:
                self.buckets[index].pop(i)
                return
```

## 操作解释

### put

先找到 `key` 对应的桶。

然后遍历桶里的键值对：

- 如果已经存在这个 `key`，就更新它的 `value`
- 如果不存在这个 `key`，就把 `[key, value]` 添加进桶

注意：HashMap 里同一个 `key` 只能对应一个 `value`，所以遇到旧 `key` 时应该更新，而不是追加一份新的。

### get

先找到 `key` 对应的桶。

再在桶里查找这个 `key`。

如果找到，返回对应的 `value`。

如果找不到，返回 `-1`。

### remove

先找到 `key` 对应的桶。

如果桶里存在这个 `key`，就删除对应的键值对。

删除后可以直接 `return`，因为同一个 `key` 不应该重复出现。

## 和 HashSet 的区别

HashSet 的桶里存的是：

```python
key
```

HashMap 的桶里存的是：

```python
[key, value]
```

所以 HashMap 每次查找时，都要先比较 `pair[0]` 是否等于目标 `key`。

## 复杂度

设 `k` 是某个桶里的元素数量。

- `put`：平均 O(1)，最坏 O(k)
- `get`：平均 O(1)，最坏 O(k)
- `remove`：平均 O(1)，最坏 O(k)

如果哈希分布均匀，每个桶里的元素很少，操作就接近 O(1)。

如果大量 key 进入同一个桶，就会退化成在列表中查找。

## 心得

1. HashMap 和 HashSet 的底层思路相似，都是“数组 + 桶 + 哈希函数”。
2. HashSet 只存 `key`，HashMap 要存 `[key, value]`。
3. `put` 时如果 `key` 已存在，要更新旧值；如果不存在，才追加新的键值对。
4. `get` 和 `remove` 都是先定位桶，再在桶里找目标 `key`。
5. 删除时找到后可以直接 `return`，因为同一个 `key` 不应该重复存在。
