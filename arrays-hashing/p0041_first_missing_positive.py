from __future__ import annotations


class SetSolution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        nums_set = set(nums)
        candidate = 1

        while candidate in nums_set:
            candidate += 1

        return candidate


class Solution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        n = len(nums)

        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                target_index = nums[i] - 1
                nums[i], nums[target_index] = nums[target_index], nums[i]

        for i in range(n):
            if nums[i] != i + 1:
                return i + 1

        return n + 1


class NegativeMarkingSolution:
    def firstMissingPositive(self, nums: list[int]) -> int:
        n = len(nums)

        for i in range(n):
            if nums[i] <= 0 or nums[i] > n:
                nums[i] = n + 1

        for i in range(n):
            value = abs(nums[i])

            if 1 <= value <= n:
                index = value - 1
                if nums[index] > 0:
                    nums[index] = -nums[index]

        for i in range(n):
            if nums[i] > 0:
                return i + 1

        return n + 1


if __name__ == "__main__":
    solutions = [
        SetSolution(),
        Solution(),
        NegativeMarkingSolution(),
    ]

    examples = [
        ([1, 2, 0], 3),
        ([3, 4, -1, 1], 2),
        ([7, 8, 9, 11, 12], 1),
        ([1], 2),
        ([2, 1], 3),
        ([1, 1], 2),
        ([], 1),
    ]

    for solution in solutions:
        for nums, expected in examples:
            assert solution.firstMissingPositive(nums[:]) == expected

    print("All examples passed.")
