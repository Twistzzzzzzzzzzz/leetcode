from __future__ import annotations


class Solution:
    def isAlienSorted(self, words: list[str], order: str) -> bool:
        rank_by_char: dict[str, int] = {}

        for index in range(len(order)):
            rank_by_char[order[index]] = index

        for index in range(1, len(words)):
            first_word = words[index - 1]
            second_word = words[index]
            common_length = min(len(first_word), len(second_word))
            found_difference = False

            for char_index in range(common_length):
                first_char = first_word[char_index]
                second_char = second_word[char_index]

                if first_char == second_char:
                    continue

                found_difference = True

                if rank_by_char[first_char] > rank_by_char[second_char]:
                    return False

                break

            if not found_difference and len(first_word) > len(second_word):
                return False

        return True


if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        (
            ["hello", "leetcode"],
            "hlabcdefgijkmnopqrstuvwxyz",
            True,
        ),
        (
            ["word", "world", "row"],
            "worldabcefghijkmnpqstuvxyz",
            False,
        ),
        (
            ["apple", "app"],
            "abcdefghijklmnopqrstuvwxyz",
            False,
        ),
        (
            ["app", "apple"],
            "abcdefghijklmnopqrstuvwxyz",
            True,
        ),
        (
            ["same", "same"],
            "abcdefghijklmnopqrstuvwxyz",
            True,
        ),
        (
            ["single"],
            "abcdefghijklmnopqrstuvwxyz",
            True,
        ),
    ]

    for words, order, expected in test_cases:
        assert solution.isAlienSorted(words, order) is expected

    print("All examples passed.")
