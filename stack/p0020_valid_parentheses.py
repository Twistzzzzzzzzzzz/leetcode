from __future__ import annotations


class Solution:
    def isValid(self, s: str) -> bool:
        stack: list[str] = []
        pairs = {
            "]": "[",
            "}": "{",
            ")": "(",
        }

        for char in s:
            if char in "([{":
                stack.append(char)
            else:
                if not stack:
                    return False

                if stack.pop() != pairs[char]:
                    return False

        return not stack


if __name__ == "__main__":
    solution = Solution()

    assert solution.isValid("()") is True
    assert solution.isValid("()[]{}") is True
    assert solution.isValid("(]") is False
    assert solution.isValid("([])") is True
    assert solution.isValid("([)]") is False
    assert solution.isValid("(") is False
    assert solution.isValid("]") is False

    print("All examples passed.")
