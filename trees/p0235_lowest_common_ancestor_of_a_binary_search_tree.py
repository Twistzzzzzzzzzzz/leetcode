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
    def lowestCommonAncestor(
        self,
        root: TreeNode | None,
        p: TreeNode,
        q: TreeNode,
    ) -> TreeNode | None:
        if not root:
            return None

        if p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestor(root.left, p, q)

        if p.val > root.val and q.val > root.val:
            return self.lowestCommonAncestor(root.right, p, q)

        return root


if __name__ == "__main__":
    solution = Solution()

    node_0 = TreeNode(0)
    node_3 = TreeNode(3)
    node_5 = TreeNode(5)
    node_4 = TreeNode(4, node_3, node_5)
    node_2 = TreeNode(2, node_0, node_4)
    node_7 = TreeNode(7)
    node_9 = TreeNode(9)
    node_8 = TreeNode(8, node_7, node_9)
    root = TreeNode(6, node_2, node_8)

    assert solution.lowestCommonAncestor(root, node_2, node_8) is root
    assert solution.lowestCommonAncestor(root, node_2, node_4) is node_2
    assert solution.lowestCommonAncestor(root, node_3, node_5) is node_4

    print("All examples passed.")
