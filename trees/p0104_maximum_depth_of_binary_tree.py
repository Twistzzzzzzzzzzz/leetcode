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
    def maxDepth(self, root: TreeNode | None) -> int:
        def dfs(node: TreeNode | None) -> int:
            if not node:
                return 0

            left_depth = dfs(node.left)
            right_depth = dfs(node.right)

            return 1 + max(left_depth, right_depth)

        return dfs(root)


if __name__ == "__main__":
    solution = Solution()

    root = TreeNode(
        3,
        TreeNode(9),
        TreeNode(20, TreeNode(15), TreeNode(7)),
    )
    skewed = TreeNode(
        1,
        right=TreeNode(2, right=TreeNode(3, right=TreeNode(4))),
    )

    assert solution.maxDepth(root) == 3
    assert solution.maxDepth(skewed) == 4
    assert solution.maxDepth(TreeNode(1)) == 1
    assert solution.maxDepth(None) == 0

    print("All examples passed.")
