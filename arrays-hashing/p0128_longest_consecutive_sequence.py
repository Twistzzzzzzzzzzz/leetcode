from __future__ import annotations


class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        nums_set = set(nums)
        longest = 0

        for num in nums_set:
            if num - 1 in nums_set:
                continue

            current = num
            length = 1

            while current + 1 in nums_set:
                current += 1
                length += 1

            longest = max(longest, length)

        return longest


if __name__ == "__main__":
    solution = Solution()

    examples = [
        ([100, 4, 200, 1, 3, 2], 4),
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
        ([], 0),
        ([1, 2, 0, 1], 3),
    ]

    for nums, expected in examples:
        assert solution.longestConsecutive(nums) == expected

    print("All examples passed.")
