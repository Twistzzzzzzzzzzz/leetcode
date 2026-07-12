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
    def diameterOfBinaryTree(self, root: TreeNode | None) -> int:
        self.ans = 0

        def dfs(node: TreeNode | None) -> int:
            if not node:
                return 0

            left_depth = dfs(node.left)
            right_depth = dfs(node.right)

            self.ans = max(self.ans, left_depth + right_depth)

            return 1 + max(left_depth, right_depth)

        dfs(root)
        return self.ans


if __name__ == "__main__":
    solution = Solution()

    root = TreeNode(
        1,
        TreeNode(2, TreeNode(4), TreeNode(5)),
        TreeNode(3),
    )
    skewed = TreeNode(
        1,
        right=TreeNode(2, right=TreeNode(3, right=TreeNode(4))),
    )

    assert solution.diameterOfBinaryTree(root) == 3
    assert solution.diameterOfBinaryTree(skewed) == 3
    assert solution.diameterOfBinaryTree(TreeNode(1)) == 0
    assert solution.diameterOfBinaryTree(None) == 0

    print("All examples passed.")
