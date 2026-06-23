from __future__ import annotations


class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        groups: dict[str, list[str]] = {}

        for word in strs:
            key = "".join(sorted(word))

            if key not in groups:
                groups[key] = []
            groups[key].append(word)

        return list(groups.values())


def normalize(groups: list[list[str]]) -> list[list[str]]:
    return sorted([sorted(group) for group in groups])


if __name__ == "__main__":
    solution = Solution()

    examples = [
        (
            ["eat", "tea", "tan", "ate", "nat", "bat"],
            [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
        ),
        ([""], [[""]]),
        (["a"], [["a"]]),
    ]

    for strs, expected in examples:
        assert normalize(solution.groupAnagrams(strs)) == normalize(expected)

    print("All examples passed.")
