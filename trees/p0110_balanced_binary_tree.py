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
    def isBalanced(self, root: TreeNode | None) -> bool:
        def check_balance(node: TreeNode | None) -> int:
            if not node:
                return 0

            left_depth = check_balance(node.left)
            if left_depth == -1:
                return -1

            right_depth = check_balance(node.right)
            if right_depth == -1:
                return -1

            if abs(left_depth - right_depth) > 1:
                return -1

            return 1 + max(left_depth, right_depth)

        return check_balance(root) != -1


if __name__ == "__main__":
    solution = Solution()

    balanced = TreeNode(
        3,
        TreeNode(9),
        TreeNode(20, TreeNode(15), TreeNode(7)),
    )
    unbalanced = TreeNode(
        1,
        TreeNode(
            2,
            TreeNode(3, TreeNode(4), TreeNode(4)),
            TreeNode(3),
        ),
        TreeNode(2),
    )

    assert solution.isBalanced(balanced) is True
    assert solution.isBalanced(unbalanced) is False
    assert solution.isBalanced(TreeNode(1)) is True
    assert solution.isBalanced(None) is True

    print("All examples passed.")
