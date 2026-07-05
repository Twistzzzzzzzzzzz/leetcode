from __future__ import annotations


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        freq: dict[str, int] = {}
        k = len(s1)

        for char in s1:
            freq[char] = freq.get(char, 0) + 1

        left = 0

        for right, char in enumerate(s2):
            if char in freq:
                freq[char] -= 1

            while right - left + 1 > k:
                if s2[left] in freq:
                    freq[s2[left]] += 1
                left += 1

            if right - left + 1 == k and all(value == 0 for value in freq.values()):
                return True

        return False


if __name__ == "__main__":
    solution = Solution()

    assert solution.checkInclusion("ab", "eidbaooo") is True
    assert solution.checkInclusion("ab", "eidboaoo") is False
    assert solution.checkInclusion("adc", "dcda") is True
    assert solution.checkInclusion("a", "a") is True
    assert solution.checkInclusion("abc", "bbbca") is True
    assert solution.checkInclusion("abcd", "abc") is False

    print("All examples passed.")
