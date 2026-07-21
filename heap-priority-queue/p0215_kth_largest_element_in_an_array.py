from __future__ import annotations

import heapq


class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        min_heap: list[int] = []

        for num in nums:
            heapq.heappush(min_heap, num)

            if len(min_heap) > k:
                heapq.heappop(min_heap)

        return min_heap[0]


if __name__ == "__main__":
    solution = Solution()

    assert solution.findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5
    assert solution.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert solution.findKthLargest([-1, -1], 2) == -1
    assert solution.findKthLargest([1], 1) == 1

    print("All examples passed.")
