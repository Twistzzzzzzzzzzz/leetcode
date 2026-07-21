from __future__ import annotations

import heapq


class Solution:
    def lastStoneWeight(self, stones: list[int]) -> int:
        max_heap = [-stone for stone in stones]
        heapq.heapify(max_heap)

        while len(max_heap) > 1:
            heaviest = -heapq.heappop(max_heap)
            second_heaviest = -heapq.heappop(max_heap)

            if heaviest != second_heaviest:
                heapq.heappush(
                    max_heap,
                    -(heaviest - second_heaviest),
                )

        return -max_heap[0] if max_heap else 0


if __name__ == "__main__":
    solution = Solution()

    assert solution.lastStoneWeight([2, 7, 4, 1, 8, 1]) == 1
    assert solution.lastStoneWeight([1]) == 1
    assert solution.lastStoneWeight([1, 1]) == 0
    assert solution.lastStoneWeight([3, 3, 3]) == 3
    assert solution.lastStoneWeight([10, 4, 2, 10]) == 2
    assert solution.lastStoneWeight([]) == 0

    print("All examples passed.")
