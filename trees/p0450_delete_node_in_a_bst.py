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
    def deleteNode(self, root: TreeNode | None, key: int) -> TreeNode | None:
        def delete_current(node: TreeNode) -> TreeNode | None:
            if not node.left:
                return node.right

            if not node.right:
                return node.left

            new_root = node.right
            leftmost = new_root

            while leftmost.left:
                leftmost = leftmost.left

            leftmost.left = node.left
            return new_root

        if not root:
            return None

        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            return delete_current(root)

        return root


def build_sample_tree() -> TreeNode:
    return TreeNode(
        5,
        TreeNode(3, TreeNode(2), TreeNode(4)),
        TreeNode(6, right=TreeNode(7)),
    )


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

    deleted_internal = solution.deleteNode(build_sample_tree(), 3)
    assert tree_to_tuple(deleted_internal) == (
        5,
        (4, (2, None, None), None),
        (6, None, (7, None, None)),
    )

    deleted_root = solution.deleteNode(build_sample_tree(), 5)
    assert tree_to_tuple(deleted_root) == (
        6,
        (3, (2, None, None), (4, None, None)),
        (7, None, None),
    )

    one_child = TreeNode(2, TreeNode(1))
    assert tree_to_tuple(solution.deleteNode(one_child, 2)) == (1, None, None)

    unchanged = build_sample_tree()
    before = tree_to_tuple(unchanged)
    result = solution.deleteNode(unchanged, 100)
    assert result is unchanged
    assert tree_to_tuple(result) == before

    assert solution.deleteNode(None, 1) is None

    print("All examples passed.")
