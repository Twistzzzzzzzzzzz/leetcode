from __future__ import annotations


class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        nums.sort()
        result: list[list[int]] = []
        length = len(nums)

        for first in range(length):
            if first > 0 and nums[first] == nums[first - 1]:
                continue

            for second in range(first + 1, length):
                if second > first + 1 and nums[second] == nums[second - 1]:
                    continue

                left = second + 1
                right = length - 1
                two_sum_target = target - nums[first] - nums[second]

                while left < right:
                    current_sum = nums[left] + nums[right]

                    if current_sum == two_sum_target:
                        result.append(
                            [nums[first], nums[second], nums[left], nums[right]]
                        )

                        left += 1
                        right -= 1

                        while left < right and nums[left] == nums[left - 1]:
                            left += 1

                        while left < right and nums[right] == nums[right + 1]:
                            right -= 1
                    elif current_sum < two_sum_target:
                        left += 1
                    else:
                        right -= 1

        return result


def normalize(items: list[list[int]]) -> list[list[int]]:
    return sorted(items)


if __name__ == "__main__":
    solution = Solution()

    assert normalize(solution.fourSum([1, 0, -1, 0, -2, 2], 0)) == normalize(
        [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
    )
    assert solution.fourSum([2, 2, 2, 2, 2], 8) == [[2, 2, 2, 2]]
    assert solution.fourSum([], 0) == []
    assert normalize(solution.fourSum([-3, -1, 0, 2, 4, 5], 2)) == normalize(
        [[-3, -1, 2, 4]]
    )

    print("All examples passed.")
