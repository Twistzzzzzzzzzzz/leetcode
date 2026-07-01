# 11. Container With Most Water

## 题目

给定一个数组 `height`，每个元素表示一条竖线的高度。

任选两条线和 x 轴组成一个容器，求最多能装多少水。

## 思路

使用左右双指针：

- `left` 从最左边开始
- `right` 从最右边开始

当前容器能装的水由两个因素决定：

```text
面积 = 宽度 * 高度
```

其中：

```python
width = right - left
height = min(height[left], height[right])
```

最终能装多少水，是由两边较短的那条线决定的。

## 为什么移动较短的一边

每次移动指针，宽度都会变小。

所以如果想让面积变大，只能希望高度变大。

而当前高度由较短的一边决定。

如果移动较高的一边，短板没有变，宽度还变小了，面积不可能更好。

所以每一轮应该移动较短的一边：

- 如果 `height[left] < height[right]`，移动 `left`
- 否则移动 `right`

这就是这题使用双指针的关键。

## 代码

```python
class Solution:
    def maxArea(self, height: list[int]) -> int:
        left = 0
        right = len(height) - 1
        best = 0

        while left < right:
            current_height = min(height[left], height[right])
            current_width = right - left
            best = max(best, current_height * current_width)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return best
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

左右指针最多各移动一遍。

## 心得

1. 最终能装的水由两边较短的那条线决定。
2. 指针移动后宽度一定变小，所以只能尝试寻找更高的短板。
3. 移动较高的一边没有意义，因为短板不变，宽度还会变小。
4. 所以这题的双指针策略是：每次移动较短的一边。
