from __future__ import annotations

import heapq
from collections import Counter, deque


class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        max_heap = [-count for count in Counter(tasks).values()]
        heapq.heapify(max_heap)

        cooldown: deque[tuple[int, int]] = deque()
        time = 0

        while max_heap or cooldown:
            time += 1

            while cooldown and cooldown[0][0] <= time:
                _, remaining_count = cooldown.popleft()
                heapq.heappush(max_heap, remaining_count)

            if max_heap:
                remaining_count = heapq.heappop(max_heap) + 1

                if remaining_count < 0:
                    ready_time = time + n + 1
                    cooldown.append((ready_time, remaining_count))

        return time


if __name__ == "__main__":
    solution = Solution()

    assert solution.leastInterval(["A", "A", "A", "B", "B", "B"], 2) == 8
    assert solution.leastInterval(["A", "A", "A", "B", "B", "B"], 0) == 6
    assert solution.leastInterval(["A", "A", "A", "B", "B", "B"], 3) == 10
    assert solution.leastInterval(["A", "C", "A", "B", "D", "B"], 1) == 6
    assert solution.leastInterval(["A"], 100) == 1

    print("All examples passed.")
