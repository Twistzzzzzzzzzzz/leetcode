from __future__ import annotations


class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        """
        217. Contains Duplicate

        判断数组里是否存在重复数字。

        思路：
        - 用 seen 集合记录已经出现过的数字。
        - 如果当前数字已经在 seen 里，说明这个数字重复出现，直接返回 True。
        - 如果遍历结束都没有发现重复，返回 False。

        复杂度：
        - 时间复杂度：O(n)，最多遍历 nums 一次。
        - 空间复杂度：O(n)，最坏情况下所有数字都不同，都要放进集合。
        """
        seen: set[int] = set()

        for num in nums:
            if num in seen:
                return True
            seen.add(num)

        return False


class OneLineSolution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        """
        一行写法：

        set(nums) 会自动去重。
        如果去重后的长度变小了，说明原数组里存在重复数字。

        不建议直接比较 set(nums) 和 nums，因为它们一个是集合，一个是列表，
        类型不同；比较长度更直观。
        """
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
