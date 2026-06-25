from __future__ import annotations


class NumMatrix:
    def __init__(self, matrix: list[list[int]]) -> None:
        height = len(matrix)
        width = len(matrix[0])
        self.prefix = [[0] * (width + 1) for _ in range(height + 1)]

        for row in range(height):
            for col in range(width):
                self.prefix[row + 1][col + 1] = (
                    matrix[row][col]
                    + self.prefix[row][col + 1]
                    + self.prefix[row + 1][col]
                    - self.prefix[row][col]
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self.prefix[row2 + 1][col2 + 1]
            - self.prefix[row1][col2 + 1]
            - self.prefix[row2 + 1][col1]
            + self.prefix[row1][col1]
        )


if __name__ == "__main__":
    matrix = [
        [3, 0, 1, 4, 2],
        [5, 6, 3, 2, 1],
        [1, 2, 0, 1, 5],
        [4, 1, 0, 1, 7],
        [1, 0, 3, 0, 5],
    ]

    num_matrix = NumMatrix(matrix)

    assert num_matrix.sumRegion(2, 1, 4, 3) == 8
    assert num_matrix.sumRegion(1, 1, 2, 2) == 11
    assert num_matrix.sumRegion(1, 2, 2, 4) == 12
    assert num_matrix.sumRegion(0, 0, 0, 0) == 3
    assert num_matrix.sumRegion(0, 0, 4, 4) == 58

    print("All examples passed.")
