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
    def postorderTraversal(self, root: TreeNode | None) -> list[int]:
        ans: list[int] = []

        def dfs(node: TreeNode | None) -> None:
            if not node:
                return

            dfs(node.left)
            dfs(node.right)
            ans.append(node.val)

        dfs(root)
        return ans


if __name__ == "__main__":
    solution = Solution()

    root = TreeNode(
        1,
        TreeNode(2, TreeNode(4), TreeNode(5)),
        TreeNode(3, right=TreeNode(6)),
    )

    assert solution.postorderTraversal(root) == [4, 5, 2, 6, 3, 1]
    assert solution.postorderTraversal(TreeNode(1)) == [1]
    assert solution.postorderTraversal(None) == []

    print("All examples passed.")
