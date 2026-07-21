from __future__ import annotations

import heapq


class KthLargest:
    def __init__(self, k: int, nums: list[int]) -> None:
        self.k = k
        self.heap: list[int] = []

        for value in nums:
            heapq.heappush(self.heap, value)

            if len(self.heap) > self.k:
                heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)

        if len(self.heap) > self.k:
            heapq.heappop(self.heap)

        return self.heap[0]


if __name__ == "__main__":
    kth_largest = KthLargest(3, [4, 5, 8, 2])
    assert kth_largest.add(3) == 4
    assert kth_largest.add(5) == 5
    assert kth_largest.add(10) == 5
    assert kth_largest.add(9) == 8
    assert kth_largest.add(4) == 8

    one_largest = KthLargest(1, [])
    assert one_largest.add(-3) == -3
    assert one_largest.add(-2) == -2
    assert one_largest.add(-4) == -2

    duplicates = KthLargest(2, [5, 5, 5])
    assert duplicates.add(5) == 5
    assert duplicates.add(6) == 5
    assert duplicates.add(7) == 6

    print("All examples passed.")
