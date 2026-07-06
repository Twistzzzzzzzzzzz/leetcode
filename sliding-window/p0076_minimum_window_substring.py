from __future__ import annotations


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or len(t) > len(s):
            return ""

        freq: dict[str, int] = {}
        for char in t:
            freq[char] = freq.get(char, 0) + 1

        left = 0
        matched = 0
        target = len(freq)
        best_len = float("inf")
        best_left = 0
        best_right = 0

        for right, char in enumerate(s):
            if char in freq:
                freq[char] -= 1
                if freq[char] == 0:
                    matched += 1

            while matched == target:
                if right - left + 1 < best_len:
                    best_len = right - left + 1
                    best_left = left
                    best_right = right

                left_char = s[left]
                if left_char in freq:
                    freq[left_char] += 1
                    if freq[left_char] > 0:
                        matched -= 1
                left += 1

        return "" if best_len == float("inf") else s[best_left:best_right + 1]


if __name__ == "__main__":
    solution = Solution()

    assert solution.minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert solution.minWindow("a", "a") == "a"
    assert solution.minWindow("a", "aa") == ""
    assert solution.minWindow("aa", "aa") == "aa"
    assert solution.minWindow("ab", "b") == "b"
    assert solution.minWindow("aaflslflsldkalskaaa", "aaa") == "aaa"

    print("All examples passed.")
