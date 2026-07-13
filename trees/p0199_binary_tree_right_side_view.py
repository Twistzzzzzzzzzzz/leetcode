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
    def rightSideView(self, root: TreeNode | None) -> list[int]:
        if not root:
            return []

        ans: list[int] = []
        queue = deque([root])

        while queue:
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()

                if i == level_size - 1:
                    ans.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return ans


if __name__ == "__main__":
    solution = Solution()

    root = TreeNode(
        1,
        TreeNode(2, right=TreeNode(5)),
        TreeNode(3, right=TreeNode(4)),
    )
    left_skewed = TreeNode(1, TreeNode(2, TreeNode(3)))
    inner_rightmost = TreeNode(
        1,
        TreeNode(2, right=TreeNode(5)),
        TreeNode(3),
    )

    assert solution.rightSideView(root) == [1, 3, 4]
    assert solution.rightSideView(left_skewed) == [1, 2, 3]
    assert solution.rightSideView(inner_rightmost) == [1, 3, 5]
    assert solution.rightSideView(TreeNode(1)) == [1]
    assert solution.rightSideView(None) == []

    print("All examples passed.")
