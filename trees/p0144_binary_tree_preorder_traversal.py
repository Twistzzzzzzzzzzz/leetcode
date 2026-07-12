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
    def preorderTraversal(self, root: TreeNode | None) -> list[int]:
        ans: list[int] = []

        def dfs(node: TreeNode | None) -> None:
            if not node:
                return

            ans.append(node.val)
            dfs(node.left)
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

    assert solution.preorderTraversal(root) == [1, 2, 4, 5, 3, 6]
    assert solution.preorderTraversal(TreeNode(1)) == [1]
    assert solution.preorderTraversal(None) == []

    print("All examples passed.")
