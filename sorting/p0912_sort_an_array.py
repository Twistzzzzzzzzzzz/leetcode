from __future__ import annotations

import random


class BruteForceSolution:
    def sortArray(self, nums: list[int]) -> list[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] > nums[j]:
                    nums[i], nums[j] = nums[j], nums[i]

        return nums


class Solution:
    def sortArray(self, nums: list[int]) -> list[int]:
        if len(nums) <= 1:
            return nums

        mid = len(nums) // 2
        left = self.sortArray(nums[:mid])
        right = self.sortArray(nums[mid:])

        return self._merge(left, right)

    def _merge(self, left: list[int], right: list[int]) -> list[int]:
        result: list[int] = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        while i < len(left):
            result.append(left[i])
            i += 1

        while j < len(right):
            result.append(right[j])
            j += 1

        return result


class QuickSortSolution:
    def sortArray(self, nums: list[int]) -> list[int]:
        if len(nums) <= 1:
            return nums

        pivot = random.choice(nums)
        left: list[int] = []
        middle: list[int] = []
        right: list[int] = []

        for num in nums:
            if num < pivot:
                left.append(num)
            elif num > pivot:
                right.append(num)
            else:
                middle.append(num)

        return self.sortArray(left) + middle + self.sortArray(right)


class CountingSortSolution:
    def sortArray(self, nums: list[int]) -> list[int]:
        offset = 50000
        counts = [0] * 100001

        for num in nums:
            counts[num + offset] += 1

        result: list[int] = []

        for index, count in enumerate(counts):
            if count > 0:
                result.extend([index - offset] * count)

        return result


if __name__ == "__main__":
    solutions = [
        BruteForceSolution(),
        Solution(),
        QuickSortSolution(),
        CountingSortSolution(),
    ]

    examples = [
        [5, 2, 3, 1],
        [5, 1, 1, 2, 0, 0],
        [-4, 0, 7, 7, -1],
        [-50000, 50000, 0, -50000],
        [],
        [1],
    ]

    for solution in solutions:
        for nums in examples:
            assert solution.sortArray(nums[:]) == sorted(nums)

    print("All examples passed.")
