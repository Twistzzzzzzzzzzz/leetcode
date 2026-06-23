from __future__ import annotations


class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        candidate = nums[0]
        vote = 0

        for num in nums:
            if vote == 0:
                candidate = num

            if num == candidate:
                vote += 1
            else:
                vote -= 1

        return candidate


if __name__ == "__main__":
    solution = Solution()

    examples = [
        ([3, 2, 3], 3),
        ([2, 2, 1, 1, 1, 2, 2], 2),
        ([1], 1),
    ]

    for nums, expected in examples:
        assert solution.majorityElement(nums) == expected

    print("All examples passed.")
