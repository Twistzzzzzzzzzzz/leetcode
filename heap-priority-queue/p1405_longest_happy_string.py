from __future__ import annotations

import heapq
from collections import Counter


class Solution:
    def longestDiverseString(self, a: int, b: int, c: int) -> str:
        max_heap: list[tuple[int, str]] = []
        answer: list[str] = []

        for count, char in ((a, "a"), (b, "b"), (c, "c")):
            if count > 0:
                heapq.heappush(max_heap, (-count, char))

        while max_heap:
            first_count, first_char = heapq.heappop(max_heap)

            if (
                len(answer) >= 2
                and answer[-1] == first_char
                and answer[-2] == first_char
            ):
                if not max_heap:
                    break

                second_count, second_char = heapq.heappop(max_heap)
                answer.append(second_char)
                second_count += 1

                if second_count < 0:
                    heapq.heappush(max_heap, (second_count, second_char))

                heapq.heappush(max_heap, (first_count, first_char))
            else:
                answer.append(first_char)
                first_count += 1

                if first_count < 0:
                    heapq.heappush(max_heap, (first_count, first_char))

        return "".join(answer)


def is_happy_string(result: str, a: int, b: int, c: int) -> bool:
    limits = {"a": a, "b": b, "c": c}
    used = Counter(result)

    return all(used[char] <= limit for char, limit in limits.items()) and all(
        not (result[index] == result[index - 1] == result[index - 2])
        for index in range(2, len(result))
    )


if __name__ == "__main__":
    solution = Solution()
    test_cases = [
        (1, 1, 7, 8),
        (7, 1, 0, 5),
        (2, 2, 1, 5),
        (4, 4, 3, 11),
        (1, 1, 1, 3),
        (0, 0, 0, 0),
    ]

    for a_count, b_count, c_count, expected_length in test_cases:
        result = solution.longestDiverseString(a_count, b_count, c_count)
        assert is_happy_string(result, a_count, b_count, c_count)
        assert len(result) == expected_length

    print("All examples passed.")
