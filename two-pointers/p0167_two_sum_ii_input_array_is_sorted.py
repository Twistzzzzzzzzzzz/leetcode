from __future__ import annotations


class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]

            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                return [left + 1, right + 1]

        return []


if __name__ == "__main__":
    solution = Solution()

    assert solution.twoSum([2, 7, 11, 15], 9) == [1, 2]
    assert solution.twoSum([2, 3, 4], 6) == [1, 3]
    assert solution.twoSum([-1, 0], -1) == [1, 2]
    assert solution.twoSum([1, 2, 3, 4, 4, 9], 8) == [4, 5]

    print("All examples passed.")
