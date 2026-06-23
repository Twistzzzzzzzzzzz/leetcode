# 705. Design HashSet

## 题目

不使用 Python 内置的 `set`，自己实现一个 HashSet。

需要支持三个操作：

- `add(key)`：添加一个值
- `remove(key)`：删除一个值
- `contains(key)`：判断一个值是否存在

## 思路

HashSet 的核心是：

1. 用一个数组保存很多个桶。
2. 通过哈希函数把 `key` 转成桶的下标。
3. 如果多个 `key` 落到同一个桶里，就在这个桶里继续用列表保存。

这里使用：

```python
index = key % size
```

这样就可以把任意整数 `key` 映射到 `[0, size - 1]` 之间的某个位置。

## 冲突处理

不同的 `key` 可能算出同一个下标。

例如当 `size = 1009` 时：

```text
1009 % 1009 = 0
2018 % 1009 = 0
```

它们都会进入第 `0` 个桶。

所以每个桶不能只保存一个数字，而是保存一个列表：

```python
self.buckets = [[] for _ in range(self.size)]
```

这种做法叫链地址法。

## 代码

```python
class MyHashSet:
    def __init__(self) -> None:
        self.size = 1009
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def add(self, key: int) -> None:
        index = self._hash(key)

        if key not in self.buckets[index]:
            self.buckets[index].append(key)

    def remove(self, key: int) -> None:
        index = self._hash(key)

        if key in self.buckets[index]:
            self.buckets[index].remove(key)

    def contains(self, key: int) -> bool:
        index = self._hash(key)
        return key in self.buckets[index]
```

## 操作解释

### add

先通过 `_hash(key)` 找到桶。

如果桶里还没有这个 `key`，就添加进去。

这里要先判断：

```python
if key not in self.buckets[index]:
```

因为 HashSet 不能保存重复元素。

### remove

先通过 `_hash(key)` 找到桶。

如果桶里有这个 `key`，就删除。

如果桶里没有这个 `key`，什么都不用做。

### contains

先通过 `_hash(key)` 找到桶。

然后判断 `key` 是否在这个桶里。

## 复杂度

设 `k` 是某个桶里的元素数量。

- `add`：平均 O(1)，最坏 O(k)
- `remove`：平均 O(1)，最坏 O(k)
- `contains`：平均 O(1)，最坏 O(k)

如果哈希分布比较均匀，每个桶里的元素很少，操作就接近 O(1)。

如果很多元素都进入同一个桶，就会退化成在列表里查找。

## 心得

1. HashSet 可以理解为“数组 + 桶”。
2. 哈希函数负责把 `key` 转成桶的下标。
3. `key % size` 可以把整数映射到固定范围内。
4. 不同的 `key` 可能进入同一个桶，所以桶里用列表处理冲突。
5. `add` 时要先检查桶里有没有这个 `key`，因为 HashSet 不保存重复元素。
