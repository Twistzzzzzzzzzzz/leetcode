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
    def isSameTree(self, p: TreeNode | None, q: TreeNode | None) -> bool:
        def check(node_p: TreeNode | None, node_q: TreeNode | None) -> bool:
            if not node_p and not node_q:
                return True

            if not node_p or not node_q:
                return False

            if node_p.val != node_q.val:
                return False

            return check(node_p.left, node_q.left) and check(
                node_p.right,
                node_q.right,
            )

        return check(p, q)


if __name__ == "__main__":
    solution = Solution()

    first = TreeNode(1, TreeNode(2), TreeNode(3))
    same = TreeNode(1, TreeNode(2), TreeNode(3))
    different_structure = TreeNode(1, right=TreeNode(2))
    different_values = TreeNode(1, TreeNode(3), TreeNode(2))

    assert solution.isSameTree(first, same) is True
    assert solution.isSameTree(first, different_structure) is False
    assert solution.isSameTree(first, different_values) is False
    assert solution.isSameTree(None, None) is True
    assert solution.isSameTree(first, None) is False

    print("All examples passed.")
