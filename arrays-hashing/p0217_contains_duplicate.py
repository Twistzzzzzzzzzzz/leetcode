from __future__ import annotations


class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        seen: set[int] = set()

        for num in nums:
            if num in seen:
                return True
            seen.add(num)

        return False


class OneLineSolution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(nums) != len(set(nums))


if __name__ == "__main__":
    solution = Solution()
    one_line_solution = OneLineSolution()

    examples = [
        ([1, 2, 3, 1], True),
        ([1, 2, 3, 4], False),
        ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),
    ]

    for nums, expected in examples:
        assert solution.containsDuplicate(nums) is expected
        assert one_line_solution.containsDuplicate(nums) is expected

    print("All examples passed.")
