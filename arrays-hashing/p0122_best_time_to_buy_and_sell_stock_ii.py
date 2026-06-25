from __future__ import annotations


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        profit = 0

        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                profit += prices[i] - prices[i - 1]

        return profit


class StartPriceSolution:
    def maxProfit(self, prices: list[int]) -> int:
        profit = 0
        start = prices[0]

        for price in prices[1:]:
            if price > start:
                profit += price - start
            start = price

        return profit


if __name__ == "__main__":
    solutions = [
        Solution(),
        StartPriceSolution(),
    ]

    examples = [
        ([7, 1, 5, 3, 6, 4], 7),
        ([1, 2, 3, 4, 5], 4),
        ([7, 6, 4, 3, 1], 0),
        ([1, 2], 1),
    ]

    for solution in solutions:
        for prices, expected in examples:
            assert solution.maxProfit(prices) == expected

    print("All examples passed.")
