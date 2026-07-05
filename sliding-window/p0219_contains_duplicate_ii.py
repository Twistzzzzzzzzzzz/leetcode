from __future__ import annotations


class Solution:
    def containsNearbyDuplicate(self, nums: list[int], k: int) -> bool:
        window: set[int] = set()

        for index, num in enumerate(nums):
            if num in window:
                return True

            window.add(num)

            if len(window) > k:
                window.remove(nums[index - k])

        return False


class HashMapSolution:
    def containsNearbyDuplicate(self, nums: list[int], k: int) -> bool:
        last_seen: dict[int, int] = {}

        for index, num in enumerate(nums):
            if num in last_seen and index - last_seen[num] <= k:
                return True

            last_seen[num] = index

        return False


if __name__ == "__main__":
    test_cases = [
        ([1, 2, 3, 1], 3, True),
        ([1, 0, 1, 1], 1, True),
        ([1, 2, 3, 1, 2, 3], 2, False),
        ([1, 2], 0, False),
        ([], 3, False),
    ]

    for solution_class in (Solution, HashMapSolution):
        solution = solution_class()
        for nums, k, expected in test_cases:
            assert solution.containsNearbyDuplicate(nums, k) is expected

    print("All examples passed.")
