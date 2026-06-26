from __future__ import annotations


class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        result: list[str] = []
        index1 = 0
        index2 = 0

        while index1 < len(word1) and index2 < len(word2):
            result.append(word1[index1])
            result.append(word2[index2])
            index1 += 1
            index2 += 1

        if index1 < len(word1):
            result.append(word1[index1:])

        if index2 < len(word2):
            result.append(word2[index2:])

        return "".join(result)


if __name__ == "__main__":
    solution = Solution()

    assert solution.mergeAlternately("abc", "pqr") == "apbqcr"
    assert solution.mergeAlternately("ab", "pqrs") == "apbqrs"
    assert solution.mergeAlternately("abcd", "pq") == "apbqcd"
    assert solution.mergeAlternately("", "abc") == "abc"

    print("All examples passed.")
