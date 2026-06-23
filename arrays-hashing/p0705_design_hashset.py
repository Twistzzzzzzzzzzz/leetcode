from __future__ import annotations


class MyHashSet:
    def __init__(self) -> None:
        self.size = 1009
        self.buckets: list[list[int]] = [[] for _ in range(self.size)]

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


if __name__ == "__main__":
    hash_set = MyHashSet()

    hash_set.add(1)
    hash_set.add(2)
    assert hash_set.contains(1) is True
    assert hash_set.contains(3) is False

    hash_set.add(2)
    assert hash_set.contains(2) is True

    hash_set.remove(2)
    assert hash_set.contains(2) is False

    hash_set.add(1009)
    hash_set.add(2018)
    assert hash_set.contains(1009) is True
    assert hash_set.contains(2018) is True

    print("All examples passed.")
