from __future__ import annotations


class Solution:
    def reverseString(self, s: list[str]) -> None:
        left = 0
        right = len(s) - 1

        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1


if __name__ == "__main__":
    solution = Solution()

    chars = ["h", "e", "l", "l", "o"]
    solution.reverseString(chars)
    assert chars == ["o", "l", "l", "e", "h"]

    chars = ["H", "a", "n", "n", "a", "h"]
    solution.reverseString(chars)
    assert chars == ["h", "a", "n", "n", "a", "H"]

    chars = ["a"]
    solution.reverseString(chars)
    assert chars == ["a"]

    print("All examples passed.")
