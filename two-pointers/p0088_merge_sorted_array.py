from __future__ import annotations


class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        index1 = m - 1
        index2 = n - 1
        write_index = m + n - 1

        while index1 >= 0 and index2 >= 0:
            if nums1[index1] <= nums2[index2]:
                nums1[write_index] = nums2[index2]
                index2 -= 1
            else:
                nums1[write_index] = nums1[index1]
                index1 -= 1

            write_index -= 1

        while index2 >= 0:
            nums1[write_index] = nums2[index2]
            index2 -= 1
            write_index -= 1


if __name__ == "__main__":
    solution = Solution()

    nums1 = [1, 2, 3, 0, 0, 0]
    solution.merge(nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6]

    nums1 = [1]
    solution.merge(nums1, 1, [], 0)
    assert nums1 == [1]

    nums1 = [0]
    solution.merge(nums1, 0, [1], 1)
    assert nums1 == [1]

    nums1 = [4, 5, 6, 0, 0, 0]
    solution.merge(nums1, 3, [1, 2, 3], 3)
    assert nums1 == [1, 2, 3, 4, 5, 6]

    print("All examples passed.")
