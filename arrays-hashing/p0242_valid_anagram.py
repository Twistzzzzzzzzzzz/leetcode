from __future__ import annotations


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        count: dict[str, int] = {}

        for char in s:
            count[char] = count.get(char, 0) + 1

        for char in t:
            if char not in count:
                return False
            count[char] -= 1

        for value in count.values():
            if value != 0:
                return False

        return True


if __name__ == "__main__":
    solution = Solution()

    examples = [
        ("anagram", "nagaram", True),
        ("rat", "car", False),
        ("a", "ab", False),
        ("", "", True),
    ]

    for s, t, expected in examples:
        assert solution.isAnagram(s, t) is expected

    print("All examples passed.")
