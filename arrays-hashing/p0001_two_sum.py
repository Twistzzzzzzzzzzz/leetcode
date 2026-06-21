from __future__ import annotations


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        needed: dict[int, int] = {}

        for index, num in enumerate(nums):
            if num in needed:
                return [needed[num], index]
            needed[target - num] = index

        return []


if __name__ == "__main__":
    solution = Solution()

    examples = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
    ]

    for nums, target, expected in examples:
        assert solution.twoSum(nums, target) == expected

    print("All examples passed.")
