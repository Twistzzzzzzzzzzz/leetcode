from __future__ import annotations


class StockSpanner:
    def __init__(self) -> None:
        self.stack: list[tuple[int, int]] = []

    def next(self, price: int) -> int:
        span = 1

        while self.stack and price >= self.stack[-1][0]:
            span += self.stack.pop()[1]

        self.stack.append((price, span))
        return span


if __name__ == "__main__":
    stock_spanner = StockSpanner()

    prices = [100, 80, 60, 70, 60, 75, 85]
    expected = [1, 1, 1, 2, 1, 4, 6]

    result = [stock_spanner.next(price) for price in prices]
    assert result == expected

    print("All examples passed.")
