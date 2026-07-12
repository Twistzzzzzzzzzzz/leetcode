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
    def isSubtree(
        self,
        root: TreeNode | None,
        subRoot: TreeNode | None,
    ) -> bool:
        if not subRoot:
            return True

        if not root:
            return False

        def same_tree(node_p: TreeNode | None, node_q: TreeNode | None) -> bool:
            if not node_p and not node_q:
                return True

            if not node_p or not node_q:
                return False

            if node_p.val != node_q.val:
                return False

            return same_tree(node_p.left, node_q.left) and same_tree(
                node_p.right,
                node_q.right,
            )

        if same_tree(root, subRoot):
            return True

        return self.isSubtree(root.left, subRoot) or self.isSubtree(
            root.right,
            subRoot,
        )


if __name__ == "__main__":
    solution = Solution()

    root = TreeNode(
        3,
        TreeNode(4, TreeNode(1), TreeNode(2)),
        TreeNode(5),
    )
    subtree = TreeNode(4, TreeNode(1), TreeNode(2))

    root_with_extra_node = TreeNode(
        3,
        TreeNode(4, TreeNode(1), TreeNode(2, TreeNode(0))),
        TreeNode(5),
    )

    repeated_value_root = TreeNode(1, TreeNode(1))
    repeated_value_subtree = TreeNode(1)

    assert solution.isSubtree(root, subtree) is True
    assert solution.isSubtree(root_with_extra_node, subtree) is False
    assert solution.isSubtree(repeated_value_root, repeated_value_subtree) is True
    assert solution.isSubtree(root, None) is True
    assert solution.isSubtree(None, subtree) is False

    print("All examples passed.")
