from __future__ import annotations


class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        prefix_count = {0: 1}
        prefix_sum = 0
        count = 0

        for num in nums:
            prefix_sum += num
            need = prefix_sum - k

            count += prefix_count.get(need, 0)
            prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

        return count


if __name__ == "__main__":
    solution = Solution()

    examples = [
        ([1, 1, 1], 2, 2),
        ([1, 2, 3], 3, 2),
        ([1, -1, 0], 0, 3),
        ([1, -1, 1, 1, 1, 1], 3, 4),
        ([], 0, 0),
    ]

    for nums, k, expected in examples:
        assert solution.subarraySum(nums, k) == expected

    print("All examples passed.")
