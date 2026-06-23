from __future__ import annotations


class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        write_index = 0

        for num in nums:
            if num != val:
                nums[write_index] = num
                write_index += 1

        return write_index


if __name__ == "__main__":
    solution = Solution()

    nums = [3, 2, 2, 3]
    length = solution.removeElement(nums, 3)
    assert length == 2
    assert nums[:length] == [2, 2]

    nums = [0, 1, 2, 2, 3, 0, 4, 2]
    length = solution.removeElement(nums, 2)
    assert length == 5
    assert sorted(nums[:length]) == [0, 0, 1, 3, 4]

    nums = []
    length = solution.removeElement(nums, 1)
    assert length == 0
    assert nums[:length] == []

    print("All examples passed.")
