from __future__ import annotations


class Solution:
    def simplifyPath(self, path: str) -> str:
        stack: list[str] = []

        for part in path.split("/"):
            if part == "..":
                if stack:
                    stack.pop()
            elif part == "." or part == "":
                continue
            else:
                stack.append(part)

        return "/" + "/".join(stack)


if __name__ == "__main__":
    solution = Solution()

    assert solution.simplifyPath("/home/") == "/home"
    assert solution.simplifyPath("/home//foo/") == "/home/foo"
    assert solution.simplifyPath("/home/user/Documents/../Pictures") == "/home/user/Pictures"
    assert solution.simplifyPath("/../") == "/"
    assert solution.simplifyPath("/.../a/../b/c/../d/./") == "/.../b/d"

    print("All examples passed.")
