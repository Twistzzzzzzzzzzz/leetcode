from __future__ import annotations


class MyHashMap:
    def __init__(self) -> None:
        self.size = 1009
        self.buckets: list[list[list[int]]] = [[] for _ in range(self.size)]

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


if __name__ == "__main__":
    hash_map = MyHashMap()

    hash_map.put(1, 1)
    hash_map.put(2, 2)
    assert hash_map.get(1) == 1
    assert hash_map.get(3) == -1

    hash_map.put(2, 1)
    assert hash_map.get(2) == 1

    hash_map.remove(2)
    assert hash_map.get(2) == -1

    hash_map.put(1009, 10)
    hash_map.put(2018, 20)
    assert hash_map.get(1009) == 10
    assert hash_map.get(2018) == 20

    print("All examples passed.")
