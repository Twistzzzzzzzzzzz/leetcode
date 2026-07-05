from __future__ import annotations


class Solution:
    def findClosestElements(self, arr: list[int], k: int, x: int) -> list[int]:
        left = 0
        right = len(arr) - k

        while left < right:
            mid = (left + right) // 2

            if x - arr[mid] > arr[mid + k] - x:
                left = mid + 1
            else:
                right = mid

        return arr[left:left + k]


if __name__ == "__main__":
    solution = Solution()

    assert solution.findClosestElements([1, 2, 3, 4, 5], 4, 3) == [1, 2, 3, 4]
    assert solution.findClosestElements([1, 2, 3, 4, 5], 4, -1) == [1, 2, 3, 4]
    assert solution.findClosestElements([1, 1, 2, 3, 4, 5], 4, -1) == [1, 1, 2, 3]
    assert solution.findClosestElements([1, 2, 3, 4, 5], 4, 6) == [2, 3, 4, 5]
    assert solution.findClosestElements([0, 1, 2, 2, 2, 3, 6, 8, 8, 9], 5, 9) == [3, 6, 8, 8, 9]

    print("All examples passed.")
