from __future__ import annotations


class Solution:
    def calPoints(self, operations: list[str]) -> int:
        scores: list[int] = []

        for operation in operations:
            if operation == "+":
                scores.append(scores[-1] + scores[-2])
            elif operation == "D":
                scores.append(scores[-1] * 2)
            elif operation == "C":
                scores.pop()
            else:
                scores.append(int(operation))

        return sum(scores)


if __name__ == "__main__":
    solution = Solution()

    assert solution.calPoints(["5", "2", "C", "D", "+"]) == 30
    assert solution.calPoints(["5", "-2", "4", "C", "D", "9", "+", "+"]) == 27
    assert solution.calPoints(["1", "C"]) == 0

    print("All examples passed.")
