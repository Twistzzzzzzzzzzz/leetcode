from __future__ import annotations


class Solution:
    def findDuplicate(self, nums: list[int]) -> int:
        slow = 0
        fast = 0

        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]

            if slow == fast:
                break

        finder = 0

        while finder != slow:
            finder = nums[finder]
            slow = nums[slow]

        return finder


if __name__ == "__main__":
    solution = Solution()

    assert solution.findDuplicate([1, 3, 4, 2, 2]) == 2
    assert solution.findDuplicate([3, 1, 3, 4, 2]) == 3
    assert solution.findDuplicate([3, 3, 3, 3, 3]) == 3
    assert solution.findDuplicate([1, 1]) == 1

    print("All examples passed.")
