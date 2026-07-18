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
    def removeLeafNodes(
        self,
        root: TreeNode | None,
        target: int,
    ) -> TreeNode | None:
        def dfs(node: TreeNode | None) -> TreeNode | None:
            if not node:
                return None

            node.left = dfs(node.left)
            node.right = dfs(node.right)

            if node.val == target and not node.left and not node.right:
                return None

            return node

        return dfs(root)


def tree_to_tuple(node: TreeNode | None):
    if not node:
        return None

    return (
        node.val,
        tree_to_tuple(node.left),
        tree_to_tuple(node.right),
    )


if __name__ == "__main__":
    solution = Solution()

    cascading = TreeNode(
        1,
        TreeNode(2, TreeNode(2)),
        TreeNode(3, TreeNode(2), TreeNode(4)),
    )
    target_with_child = TreeNode(2, TreeNode(1))
    unchanged = TreeNode(1, TreeNode(2), TreeNode(3))

    result = solution.removeLeafNodes(cascading, 2)
    assert tree_to_tuple(result) == (1, None, (3, None, (4, None, None)))

    result = solution.removeLeafNodes(target_with_child, 2)
    assert tree_to_tuple(result) == (2, (1, None, None), None)

    result = solution.removeLeafNodes(unchanged, 4)
    assert tree_to_tuple(result) == (
        1,
        (2, None, None),
        (3, None, None),
    )

    assert solution.removeLeafNodes(TreeNode(2), 2) is None
    assert solution.removeLeafNodes(None, 2) is None

    print("All examples passed.")
