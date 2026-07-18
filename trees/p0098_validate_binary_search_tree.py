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
    def isValidBST(self, root: TreeNode | None) -> bool:
        def check(
            node: TreeNode | None,
            lower: float | int,
            upper: float | int,
        ) -> bool:
            if not node:
                return True

            if node.val <= lower or node.val >= upper:
                return False

            return check(node.left, lower, node.val) and check(
                node.right,
                node.val,
                upper,
            )

        return check(root, float("-inf"), float("inf"))


if __name__ == "__main__":
    solution = Solution()

    valid = TreeNode(2, TreeNode(1), TreeNode(3))
    invalid_descendant = TreeNode(
        5,
        TreeNode(1),
        TreeNode(4, TreeNode(3), TreeNode(6)),
    )
    duplicate = TreeNode(2, TreeNode(2), TreeNode(3))
    invalid_left = TreeNode(5, TreeNode(7))

    assert solution.isValidBST(valid) is True
    assert solution.isValidBST(invalid_descendant) is False
    assert solution.isValidBST(duplicate) is False
    assert solution.isValidBST(invalid_left) is False
    assert solution.isValidBST(TreeNode(1)) is True
    assert solution.isValidBST(None) is True

    print("All examples passed.")
