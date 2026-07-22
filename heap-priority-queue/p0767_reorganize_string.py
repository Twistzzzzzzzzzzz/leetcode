from __future__ import annotations

import heapq
from collections import Counter


class Solution:
    def reorganizeString(self, s: str) -> str:
        max_heap = [(-count, char) for char, count in Counter(s).items()]
        heapq.heapify(max_heap)

        answer: list[str] = []
        previous_count = 0
        previous_char = ""

        while max_heap:
            count, char = heapq.heappop(max_heap)
            answer.append(char)
            count += 1

            if previous_count < 0:
                heapq.heappush(max_heap, (previous_count, previous_char))

            previous_count = count
            previous_char = char

        if previous_count < 0:
            return ""

        return "".join(answer)


def is_valid_reorganization(source: str, result: str) -> bool:
    return (
        Counter(source) == Counter(result)
        and all(result[index] != result[index - 1] for index in range(1, len(result)))
    )


if __name__ == "__main__":
    solution = Solution()

    for source in ("aab", "vvvlo", "aaabbc", "a", "baaba"):
        result = solution.reorganizeString(source)
        assert is_valid_reorganization(source, result)

    assert solution.reorganizeString("aaab") == ""
    assert solution.reorganizeString("aaaaabc") == ""

    print("All examples passed.")
