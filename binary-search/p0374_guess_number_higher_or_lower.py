from __future__ import annotations


_PICK = 1


def guess(num: int) -> int:
    # Local test stub. LeetCode provides this API.
    if num == _PICK:
        return 0
    if num < _PICK:
        return 1
    return -1


class Solution:
    def guessNumber(self, n: int) -> int:
        lower = 1
        upper = n

        while lower <= upper:
            num = (lower + upper) // 2
            result = guess(num)

            if result == 0:
                return num
            if result == 1:
                lower = num + 1
            else:
                upper = num - 1

        return -1


if __name__ == "__main__":
    solution = Solution()

    for n, pick in ((10, 6), (1, 1), (2, 1), (2, 2), (100, 73)):
        _PICK = pick
        assert solution.guessNumber(n) == pick

    print("All examples passed.")
