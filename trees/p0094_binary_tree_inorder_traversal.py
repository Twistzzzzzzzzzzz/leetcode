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
    def inorderTraversal(self, root: TreeNode | None) -> list[int]:
        ans: list[int] = []

        def dfs(node: TreeNode | None) -> None:
            if not node:
                return

            dfs(node.left)
            ans.append(node.val)
            dfs(node.right)

        dfs(root)
        return ans


if __name__ == "__main__":
    solution = Solution()

    root = TreeNode(
        1,
        TreeNode(2, TreeNode(4), TreeNode(5)),
        TreeNode(3, right=TreeNode(6)),
    )

    assert solution.inorderTraversal(root) == [4, 2, 5, 1, 3, 6]
    assert solution.inorderTraversal(TreeNode(1)) == [1]
    assert solution.inorderTraversal(None) == []

    print("All examples passed.")
