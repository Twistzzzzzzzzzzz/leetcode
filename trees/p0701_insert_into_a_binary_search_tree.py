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
    def insertIntoBST(self, root: TreeNode | None, val: int) -> TreeNode:
        if not root:
            return TreeNode(val)

        if val < root.val:
            root.left = self.insertIntoBST(root.left, val)
        else:
            root.right = self.insertIntoBST(root.right, val)

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
        TreeNode(7),
    )

    result = solution.insertIntoBST(root, 5)
    assert result is root
    assert tree_to_tuple(result) == (
        4,
        (2, (1, None, None), (3, None, None)),
        (7, (5, None, None), None),
    )

    result = solution.insertIntoBST(result, 0)
    assert result is root
    assert result.left is not None
    assert result.left.left is not None
    assert result.left.left.left is not None
    assert result.left.left.left.val == 0

    new_root = solution.insertIntoBST(None, 1)
    assert tree_to_tuple(new_root) == (1, None, None)

    print("All examples passed.")
