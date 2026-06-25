# 122. Best Time to Buy and Sell Stock II

## 题目

给定每天的股票价格 `prices`。

可以完成多次交易，但同一时间最多只能持有一股。

求最大利润。

## 思路

这题和 121 的区别是：可以交易多次。

所以只要今天价格比昨天高，就可以把这段上涨利润拿到手：

```text
prices[i] - prices[i - 1]
```

例如：

```text
[1, 2, 3, 4, 5]
```

从 `1` 买入、`5` 卖出的利润是 `4`。

每天都吃上涨差价：

```text
(2 - 1) + (3 - 2) + (4 - 3) + (5 - 4) = 4
```

结果一样。

所以可以把所有上涨的小段利润加起来。

## 代码

```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        profit = 0

        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                profit += prices[i] - prices[i - 1]

        return profit
```

## 你的写法

也可以维护一个 `start`，表示前一天价格：

```python
class StartPriceSolution:
    def maxProfit(self, prices: list[int]) -> int:
        profit = 0
        start = prices[0]

        for price in prices[1:]:
            if price > start:
                profit += price - start
            start = price

        return profit
```

这里的 `start` 每轮都会更新成当前价格，所以本质上就是比较今天和昨天。

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

## 心得

1. 121 只能交易一次，所以要维护历史最低买入价。
2. 122 可以交易多次，所以不需要找全局最低点和最高点。
3. 只要今天比昨天涨，就把这段涨幅加入利润。
4. 多次交易题可以理解为：把一整段上涨拆成很多个相邻上涨小段，利润总和不变。
