from __future__ import annotations


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        freq: dict[str, int] = {}
        left = 0
        answer = 0

        for right, char in enumerate(s):
            freq[char] = freq.get(char, 0) + 1
            max_freq = max(freq.values())

            while right - left + 1 - max_freq > k:
                freq[s[left]] -= 1
                left += 1
                max_freq = max(freq.values())

            answer = max(answer, right - left + 1)

        return answer


if __name__ == "__main__":
    solution = Solution()

    assert solution.characterReplacement("ABAB", 2) == 4
    assert solution.characterReplacement("AABABBA", 1) == 4
    assert solution.characterReplacement("AAAA", 2) == 4
    assert solution.characterReplacement("ABCDE", 1) == 2
    assert solution.characterReplacement("BAAA", 0) == 3

    print("All examples passed.")
