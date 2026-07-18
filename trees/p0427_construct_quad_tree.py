from __future__ import annotations


class Node:
    def __init__(
        self,
        val: bool,
        isLeaf: bool,
        topLeft: Node | None = None,
        topRight: Node | None = None,
        bottomLeft: Node | None = None,
        bottomRight: Node | None = None,
    ) -> None:
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


class Solution:
    def construct(self, grid: list[list[int]]) -> Node | None:
        if not grid:
            return None

        def build(row: int, col: int, size: int) -> Node:
            first_value = grid[row][col]
            is_same = True

            for i in range(row, row + size):
                for j in range(col, col + size):
                    if grid[i][j] != first_value:
                        is_same = False
                        break
                if not is_same:
                    break

            if is_same:
                return Node(bool(first_value), True)

            half = size // 2

            top_left = build(row, col, half)
            top_right = build(row, col + half, half)
            bottom_left = build(row + half, col, half)
            bottom_right = build(row + half, col + half, half)

            return Node(
                True,
                False,
                top_left,
                top_right,
                bottom_left,
                bottom_right,
            )

        return build(0, 0, len(grid))


if __name__ == "__main__":
    solution = Solution()

    one = solution.construct([[1]])
    assert one is not None
    assert one.isLeaf is True
    assert one.val is True

    zero = solution.construct([[0, 0], [0, 0]])
    assert zero is not None
    assert zero.isLeaf is True
    assert zero.val is False

    quadrants = solution.construct(
        [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
    )
    assert quadrants is not None
    assert quadrants.isLeaf is False
    assert quadrants.topLeft is not None and quadrants.topLeft.val is True
    assert quadrants.topRight is not None and quadrants.topRight.val is False
    assert quadrants.bottomLeft is not None and quadrants.bottomLeft.val is True
    assert quadrants.bottomRight is not None and quadrants.bottomRight.val is True

    mixed = solution.construct([[0, 1], [1, 0]])
    assert mixed is not None
    assert mixed.isLeaf is False
    assert mixed.topLeft is not None and mixed.topLeft.val is False
    assert mixed.topRight is not None and mixed.topRight.val is True
    assert mixed.bottomLeft is not None and mixed.bottomLeft.val is True
    assert mixed.bottomRight is not None and mixed.bottomRight.val is False

    assert solution.construct([]) is None

    print("All examples passed.")
