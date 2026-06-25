from __future__ import annotations


class DivisionSolution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        product = 1
        zero_count = 0

        for num in nums:
            if num == 0:
                zero_count += 1
            else:
                product *= num

        if zero_count >= 2:
            return [0] * len(nums)

        result: list[int] = []

        for num in nums:
            if num == 0:
                result.append(product)
            elif zero_count == 0:
                result.append(product // num)
            else:
                result.append(0)

        return result


class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        result = [1] * len(nums)

        for i in range(1, len(nums)):
            result[i] = result[i - 1] * nums[i - 1]

        right_product = 1

        for i in range(len(nums) - 1, -1, -1):
            result[i] *= right_product
            right_product *= nums[i]

        return result


if __name__ == "__main__":
    solutions = [
        DivisionSolution(),
        Solution(),
    ]

    examples = [
        ([1, 2, 3, 4], [24, 12, 8, 6]),
        ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
        ([0, 0], [0, 0]),
        ([2, 3], [3, 2]),
    ]

    for solution in solutions:
        for nums, expected in examples:
            assert solution.productExceptSelf(nums[:]) == expected

    print("All examples passed.")
