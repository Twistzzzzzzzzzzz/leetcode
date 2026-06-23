from __future__ import annotations


class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        if not strs:
            return ""

        shortest = min(strs, key=len)

        for index in range(len(shortest)):
            for word in strs:
                if shortest[index] != word[index]:
                    return shortest[:index]

        return shortest


if __name__ == "__main__":
    solution = Solution()

    examples = [
        (["flower", "flow", "flight"], "fl"),
        (["dog", "racecar", "car"], ""),
        (["interspecies", "interstellar", "interstate"], "inters"),
        (["a"], "a"),
        ([], ""),
    ]

    for strs, expected in examples:
        assert solution.longestCommonPrefix(strs) == expected

    print("All examples passed.")
