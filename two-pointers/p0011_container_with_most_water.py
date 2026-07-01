from __future__ import annotations


class Solution:
    def maxArea(self, height: list[int]) -> int:
        left = 0
        right = len(height) - 1
        best = 0

        while left < right:
            current_height = min(height[left], height[right])
            current_width = right - left
            best = max(best, current_height * current_width)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return best


if __name__ == "__main__":
    solution = Solution()

    assert solution.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert solution.maxArea([1, 1]) == 1
    assert solution.maxArea([4, 3, 2, 1, 4]) == 16
    assert solution.maxArea([1, 2, 1]) == 2

    print("All examples passed.")
