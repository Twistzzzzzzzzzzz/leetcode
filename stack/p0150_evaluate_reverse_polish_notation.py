from __future__ import annotations


class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        stack: list[int] = []

        for token in tokens:
            if token in {"+", "-", "*", "/"}:
                right = stack.pop()
                left = stack.pop()

                if token == "+":
                    stack.append(left + right)
                elif token == "-":
                    stack.append(left - right)
                elif token == "*":
                    stack.append(left * right)
                else:
                    stack.append(int(left / right))
            else:
                stack.append(int(token))

        return stack[-1]


if __name__ == "__main__":
    solution = Solution()

    assert solution.evalRPN(["2", "1", "+", "3", "*"]) == 9
    assert solution.evalRPN(["4", "13", "5", "/", "+"]) == 6
    assert (
        solution.evalRPN(
            ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
        )
        == 22
    )
    assert solution.evalRPN(["-3", "2", "/"]) == -1

    print("All examples passed.")
