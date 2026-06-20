from __future__ import annotations


class Solution:
    def getConcatenation(self, nums: list[int]) -> list[int]:
        return nums + nums


if __name__ == "__main__":
    solution = Solution()

    assert solution.getConcatenation([1, 2, 1]) == [1, 2, 1, 1, 2, 1]
    assert solution.getConcatenation([1, 3, 2, 1]) == [1, 3, 2, 1, 1, 3, 2, 1]

    print("All examples passed.")
