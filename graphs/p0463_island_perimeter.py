from __future__ import annotations


class Solution:
    def islandPerimeter(self, grid: list[list[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])
        perimeter = 0

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 0:
                    continue

                if row == 0 or grid[row - 1][col] == 0:
                    perimeter += 1
                if row == rows - 1 or grid[row + 1][col] == 0:
                    perimeter += 1
                if col == 0 or grid[row][col - 1] == 0:
                    perimeter += 1
                if col == cols - 1 or grid[row][col + 1] == 0:
                    perimeter += 1

        return perimeter


class DirectionSolution:
    def islandPerimeter(self, grid: list[list[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])
        perimeter = 0
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 0:
                    continue

                for row_change, col_change in directions:
                    next_row = row + row_change
                    next_col = col + col_change

                    is_outside = (
                        next_row < 0
                        or next_row >= rows
                        or next_col < 0
                        or next_col >= cols
                    )

                    if is_outside or grid[next_row][next_col] == 0:
                        perimeter += 1

        return perimeter


if __name__ == "__main__":
    test_cases = [
        (
            [
                [0, 1, 0, 0],
                [1, 1, 1, 0],
                [0, 1, 0, 0],
                [1, 1, 0, 0],
            ],
            16,
        ),
        ([[1]], 4),
        ([[1, 0]], 4),
        ([[1, 1]], 6),
        ([[1, 1], [1, 1]], 8),
    ]

    for solution in (Solution(), DirectionSolution()):
        for grid, expected in test_cases:
            assert solution.islandPerimeter(grid) == expected

    print("All examples passed.")
