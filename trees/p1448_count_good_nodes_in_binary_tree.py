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
    def goodNodes(self, root: TreeNode | None) -> int:
        def dfs(node: TreeNode | None, path_maximum: float | int) -> int:
            if not node:
                return 0

            is_good = int(node.val >= path_maximum)
            new_maximum = max(path_maximum, node.val)

            return (
                is_good
                + dfs(node.left, new_maximum)
                + dfs(node.right, new_maximum)
            )

        return dfs(root, float("-inf"))


if __name__ == "__main__":
    solution = Solution()

    root = TreeNode(
        3,
        TreeNode(1, TreeNode(3)),
        TreeNode(4, TreeNode(1), TreeNode(5)),
    )
    decreasing = TreeNode(3, TreeNode(2, TreeNode(1)))
    negative = TreeNode(-1, TreeNode(-1), TreeNode(-2, right=TreeNode(0)))

    assert solution.goodNodes(root) == 4
    assert solution.goodNodes(decreasing) == 1
    assert solution.goodNodes(negative) == 3
    assert solution.goodNodes(TreeNode(7)) == 1
    assert solution.goodNodes(None) == 0

    print("All examples passed.")
