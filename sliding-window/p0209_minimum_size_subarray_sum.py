from __future__ import annotations


class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        answer = float("inf")
        left = 0
        window_sum = 0

        for right, num in enumerate(nums):
            window_sum += num

            while window_sum >= target:
                answer = min(answer, right - left + 1)
                window_sum -= nums[left]
                left += 1

        return 0 if answer == float("inf") else answer


if __name__ == "__main__":
    solution = Solution()

    assert solution.minSubArrayLen(7, [2, 3, 1, 2, 4, 3]) == 2
    assert solution.minSubArrayLen(4, [1, 4, 4]) == 1
    assert solution.minSubArrayLen(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0
    assert solution.minSubArrayLen(11, [1, 2, 3, 4, 5]) == 3
    assert solution.minSubArrayLen(15, [1, 2, 3, 4, 5]) == 5

    print("All examples passed.")
