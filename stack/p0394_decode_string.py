from __future__ import annotations


class Solution:
    def decodeString(self, s: str) -> str:
        stack: list[tuple[str, int]] = []
        repeat = 0
        current = ""

        for char in s:
            if char.isdigit():
                repeat = repeat * 10 + int(char)
            elif char == "[":
                stack.append((current, repeat))
                repeat = 0
                current = ""
            elif char == "]":
                previous, count = stack.pop()
                current = previous + current * count
            else:
                current += char

        return current


if __name__ == "__main__":
    solution = Solution()

    assert solution.decodeString("3[a]2[bc]") == "aaabcbc"
    assert solution.decodeString("3[a2[c]]") == "accaccacc"
    assert solution.decodeString("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert solution.decodeString("abc3[cd]xyz") == "abccdcdcdxyz"
    assert solution.decodeString("10[a]") == "aaaaaaaaaa"

    print("All examples passed.")
