# 121. Best Time to Buy and Sell Stock

## 题目

给定每天的股票价格 `prices`。

只能买入一次、卖出一次，求最大利润。

如果不能赚钱，返回 `0`。

## 思路

这题只能交易一次，所以需要找到：

```text
某一天买入，后面某一天卖出，使差价最大
```

遍历价格时，维护两个值：

- `lowest_price`：目前为止见过的最低价格
- `max_profit`：目前为止能得到的最大利润

每看到一个新价格 `price`：

1. 如果 `price` 更低，就更新最低买入价。
2. 否则就计算 `price - lowest_price`，尝试更新最大利润。

## 代码

```python
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
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

## 心得

1. 只能交易一次时，关键是维护“当前之前的最低买入价”。
2. 每一天都把它当成可能的卖出日，看看用历史最低价买入能赚多少。
3. 这题更像数组遍历中维护状态：如果遇到更低价格，就更新未来可能用到的候选买入点。
