from __future__ import annotations


class PrefixMaxSolution:
    def trap(self, height: list[int]) -> int:
        if not height:
            return 0

        length = len(height)
        max_left = [0] * length
        max_right = [0] * length

        for index in range(1, length):
            max_left[index] = max(max_left[index - 1], height[index - 1])

        for index in range(length - 2, -1, -1):
            max_right[index] = max(max_right[index + 1], height[index + 1])

        water = 0
        for index in range(length):
            water_level = min(max_left[index], max_right[index])
            if water_level > height[index]:
                water += water_level - height[index]

        return water


class Solution:
    def trap(self, height: list[int]) -> int:
        if not height:
            return 0

        left = 0
        right = len(height) - 1
        max_left = height[left]
        max_right = height[right]
        water = 0

        while left < right:
            if max_left < max_right:
                left += 1
                max_left = max(max_left, height[left])
                water += max_left - height[left]
            else:
                right -= 1
                max_right = max(max_right, height[right])
                water += max_right - height[right]

        return water


if __name__ == "__main__":
    test_cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        ([1, 2, 3], 0),
        ([3, 2, 1], 0),
        ([2, 0, 2], 2),
        ([], 0),
    ]

    for solution_class in (PrefixMaxSolution, Solution):
        solution = solution_class()
        for heights, expected in test_cases:
            assert solution.trap(heights) == expected

    print("All examples passed.")
