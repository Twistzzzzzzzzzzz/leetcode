from __future__ import annotations

from collections import deque


class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        decreasing: deque[int] = deque()
        answer: list[int] = []

        for right, num in enumerate(nums):
            while decreasing and nums[decreasing[-1]] <= num:
                decreasing.pop()

            decreasing.append(right)

            left = right - k + 1
            if decreasing[0] < left:
                decreasing.popleft()

            if right >= k - 1:
                answer.append(nums[decreasing[0]])

        return answer


if __name__ == "__main__":
    solution = Solution()

    assert solution.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert solution.maxSlidingWindow([1], 1) == [1]
    assert solution.maxSlidingWindow([1, -1], 1) == [1, -1]
    assert solution.maxSlidingWindow([9, 11], 2) == [11]
    assert solution.maxSlidingWindow([4, 3, 2, 1], 2) == [4, 3, 2]
    assert solution.maxSlidingWindow([1, 3, 1, 2, 0, 5], 3) == [3, 3, 2, 5]

    print("All examples passed.")
