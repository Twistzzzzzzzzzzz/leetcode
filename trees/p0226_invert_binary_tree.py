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
    def invertTree(self, root: TreeNode | None) -> TreeNode | None:
        def invert(node: TreeNode | None) -> None:
            if not node:
                return

            node.left, node.right = node.right, node.left

            invert(node.left)
            invert(node.right)

        invert(root)
        return root


def tree_to_tuple(
    root: TreeNode | None,
) -> tuple[int, object, object] | None:
    if not root:
        return None

    return (
        root.val,
        tree_to_tuple(root.left),
        tree_to_tuple(root.right),
    )


if __name__ == "__main__":
    solution = Solution()

    root = TreeNode(
        4,
        TreeNode(2, TreeNode(1), TreeNode(3)),
        TreeNode(7, TreeNode(6), TreeNode(9)),
    )

    inverted = solution.invertTree(root)

    assert tree_to_tuple(inverted) == (
        4,
        (7, (9, None, None), (6, None, None)),
        (2, (3, None, None), (1, None, None)),
    )
    assert solution.invertTree(None) is None

    print("All examples passed.")
