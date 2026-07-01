from __future__ import annotations


class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        result: list[list[int]] = []

        for index in range(len(nums)):
            if index > 0 and nums[index] == nums[index - 1]:
                continue

            left = index + 1
            right = len(nums) - 1
            target = -nums[index]

            while left < right:
                current_sum = nums[left] + nums[right]

                if current_sum == target:
                    result.append([nums[index], nums[left], nums[right]])
                    left += 1
                    right -= 1

                    while left < right and nums[left] == nums[left - 1]:
                        left += 1

                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1

        return result


if __name__ == "__main__":
    solution = Solution()

    assert solution.threeSum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
    assert solution.threeSum([0, 1, 1]) == []
    assert solution.threeSum([0, 0, 0]) == [[0, 0, 0]]
    assert solution.threeSum([0, 0, 0, 0]) == [[0, 0, 0]]

    print("All examples passed.")
