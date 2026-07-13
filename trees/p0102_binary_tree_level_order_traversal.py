from __future__ import annotations

from collections import deque


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
    def levelOrder(self, root: TreeNode | None) -> list[list[int]]:
        if not root:
            return []

        ans: list[list[int]] = []
        queue = deque([root])

        while queue:
            level: list[int] = []
            level_size = len(queue)

            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            ans.append(level)

        return ans


if __name__ == "__main__":
    solution = Solution()

    root = TreeNode(
        3,
        TreeNode(9),
        TreeNode(20, TreeNode(15), TreeNode(7)),
    )
    skewed = TreeNode(1, right=TreeNode(2, right=TreeNode(3)))

    assert solution.levelOrder(root) == [[3], [9, 20], [15, 7]]
    assert solution.levelOrder(skewed) == [[1], [2], [3]]
    assert solution.levelOrder(TreeNode(1)) == [[1]]
    assert solution.levelOrder(None) == []

    print("All examples passed.")
