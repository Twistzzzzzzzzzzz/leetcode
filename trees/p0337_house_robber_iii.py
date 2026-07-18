from __future__ import annotations


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rob(self, root: TreeNode | None) -> int:
        def dfs(node: TreeNode | None) -> tuple[int, int]:
            if not node:
                return 0, 0

            left_rob, left_not_rob = dfs(node.left)
            right_rob, right_not_rob = dfs(node.right)

            rob_current = node.val + left_not_rob + right_not_rob
            not_rob_current = max(left_rob, left_not_rob) + max(
                right_rob,
                right_not_rob,
            )

            return rob_current, not_rob_current

        rob_root, not_rob_root = dfs(root)
        return max(rob_root, not_rob_root)


if __name__ == "__main__":
    solution = Solution()

    first = TreeNode(
        3,
        TreeNode(2, right=TreeNode(3)),
        TreeNode(3, right=TreeNode(1)),
    )
    second = TreeNode(
        3,
        TreeNode(4, TreeNode(1), TreeNode(3)),
        TreeNode(5, right=TreeNode(1)),
    )
    chain = TreeNode(2, TreeNode(1, TreeNode(4)))
    expensive_root = TreeNode(10, TreeNode(1), TreeNode(2))

    assert solution.rob(first) == 7
    assert solution.rob(second) == 9
    assert solution.rob(chain) == 6
    assert solution.rob(expensive_root) == 10
    assert solution.rob(TreeNode(5)) == 5
    assert solution.rob(None) == 0

    print("All examples passed.")
