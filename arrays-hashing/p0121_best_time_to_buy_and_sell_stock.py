from __future__ import annotations


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        lowest_price = prices[0]
        max_profit = 0

        for price in prices[1:]:
            if price < lowest_price:
                lowest_price = price
            else:
                max_profit = max(max_profit, price - lowest_price)

        return max_profit


if __name__ == "__main__":
    solution = Solution()

    examples = [
        ([7, 1, 5, 3, 6, 4], 5),
        ([7, 6, 4, 3, 1], 0),
        ([1, 2], 1),
    ]

    for prices, expected in examples:
        assert solution.maxProfit(prices) == expected

    print("All examples passed.")
