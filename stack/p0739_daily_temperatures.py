from __future__ import annotations


class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        answer = [0] * len(temperatures)
        stack: list[int] = []

        for index, temperature in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < temperature:
                previous_index = stack.pop()
                answer[previous_index] = index - previous_index

            stack.append(index)

        return answer


if __name__ == "__main__":
    solution = Solution()

    assert solution.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [
        1,
        1,
        4,
        2,
        1,
        1,
        0,
        0,
    ]
    assert solution.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert solution.dailyTemperatures([30, 60, 90]) == [1, 1, 0]
    assert solution.dailyTemperatures([90, 80, 70]) == [0, 0, 0]

    print("All examples passed.")
