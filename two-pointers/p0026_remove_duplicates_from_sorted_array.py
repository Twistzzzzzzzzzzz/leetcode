from __future__ import annotations


class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        if not nums:
            return 0

        slow = 0

        for fast in range(1, len(nums)):
            if nums[fast] != nums[slow]:
                slow += 1
                nums[slow] = nums[fast]

        return slow + 1


if __name__ == "__main__":
    solution = Solution()

    nums = [1, 1, 2]
    length = solution.removeDuplicates(nums)
    assert length == 2
    assert nums[:length] == [1, 2]

    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    length = solution.removeDuplicates(nums)
    assert length == 5
    assert nums[:length] == [0, 1, 2, 3, 4]

    nums = [1]
    length = solution.removeDuplicates(nums)
    assert length == 1
    assert nums[:length] == [1]

    nums = []
    length = solution.removeDuplicates(nums)
    assert length == 0

    print("All examples passed.")
