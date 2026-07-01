# 42. Trapping Rain Water

## 题目

给定一个数组 `height`，每个元素表示一根柱子的高度。

下雨后，柱子之间可以存水，要求计算总共能接多少雨水。

## 核心问题

对于某一个位置 `i`，它能接多少水？

答案取决于它左右两边的最高柱子。

```text
当前位置能接的水 = min(左边最高柱子, 右边最高柱子) - 当前柱子高度
```

如果结果小于等于 `0`，说明这个位置接不到水。

也就是说，每个位置的水位由左右两边较矮的那堵墙决定。

这点和 11 Container With Most Water 有一点像：真正限制容量的是短板。

## 解法一：预处理左右最高柱子

先用两个数组记录信息：

- `max_left[i]`：位置 `i` 左边最高的柱子
- `max_right[i]`：位置 `i` 右边最高的柱子

注意这里记录的是“左边”和“右边”，不包括当前位置自己。

### 计算左边最高柱子

```python
for index in range(1, length):
    max_left[index] = max(max_left[index - 1], height[index - 1])
```

含义是：

```text
index 左边的最高柱子
= max(前一个位置左边的最高柱子, 前一个位置的高度)
```

### 计算右边最高柱子

```python
for index in range(length - 2, -1, -1):
    max_right[index] = max(max_right[index + 1], height[index + 1])
```

含义是：

```text
index 右边的最高柱子
= max(后一个位置右边的最高柱子, 后一个位置的高度)
```

### 计算每个位置的水

```python
water_level = min(max_left[index], max_right[index])
```

如果 `water_level > height[index]`，说明当前位置上方可以存水：

```python
water += water_level - height[index]
```

## 解法一代码

```python
class PrefixMaxSolution:
    def trap(self, height: list[int]) -> int:
        if not height:
            return 0

        length = len(height)
        max_left = [0] * length
        max_right = [0] * length

        for index in range(1, length):
            max_left[index] = max(max_left[index - 1], height[index - 1])

        for index in range(length - 2, -1, -1):
            max_right[index] = max(max_right[index + 1], height[index + 1])

        water = 0
        for index in range(length):
            water_level = min(max_left[index], max_right[index])
            if water_level > height[index]:
                water += water_level - height[index]

        return water
```

## 解法二：双指针优化空间

解法一的问题是用了两个数组。

但其实不一定要提前存下所有位置的 `max_left` 和 `max_right`。

我们可以一边移动指针，一边维护：

- `max_left`：从左边到当前位置见过的最高柱子
- `max_right`：从右边到当前位置见过的最高柱子

定义左右指针：

```python
left = 0
right = len(height) - 1
```

每次比较 `max_left` 和 `max_right`。

## 为什么 `max_left < max_right` 时可以处理左边

这是这题最难理解的地方。

对某个位置来说，它能接多少水取决于：

```text
min(左边最高, 右边最高)
```

如果当前 `max_left < max_right`，说明左边最高墙更矮。

这时对于左侧当前位置来说，即使右边未来还有没有看过的柱子，也不重要了。

因为右侧目前已经有一堵墙高度是 `max_right`，而且它比 `max_left` 高。

所以左侧当前位置的水位一定由 `max_left` 决定。

此时可以放心移动 `left`，并计算左边位置的水：

```python
left += 1
max_left = max(max_left, height[left])
water += max_left - height[left]
```

反过来，如果 `max_left >= max_right`，说明右边最高墙更矮。

这时右侧当前位置的水位一定由 `max_right` 决定，所以处理右边：

```python
right -= 1
max_right = max(max_right, height[right])
water += max_right - height[right]
```

## 为什么这里不用判断 `tar > 0`

你的写法里有：

```python
tar = max_left - height[left]
if tar > 0:
    res += tar
```

整理后可以直接写：

```python
max_left = max(max_left, height[left])
water += max_left - height[left]
```

因为先更新了 `max_left`。

更新后一定有：

```text
max_left >= height[left]
```

所以 `max_left - height[left]` 不会是负数。

右边同理。

## 解法二代码

```python
class Solution:
    def trap(self, height: list[int]) -> int:
        if not height:
            return 0

        left = 0
        right = len(height) - 1
        max_left = height[left]
        max_right = height[right]
        water = 0

        while left < right:
            if max_left < max_right:
                left += 1
                max_left = max(max_left, height[left])
                water += max_left - height[left]
            else:
                right -= 1
                max_right = max(max_right, height[right])
                water += max_right - height[right]

        return water
```

## 复杂度

预处理数组写法：

- 时间复杂度：O(n)
- 空间复杂度：O(n)

双指针写法：

- 时间复杂度：O(n)
- 空间复杂度：O(1)

## 心得

1. 每个位置能接多少水，取决于它左边最高柱子和右边最高柱子中较矮的那个。
2. 先写 `max_left` 和 `max_right` 数组，更容易理解这题的本质。
3. 双指针优化的关键是：哪一侧的最高墙更矮，就先处理哪一侧。
4. 如果 `max_left < max_right`，左侧位置的水位已经可以确定，因为右边已经有更高的墙兜住了。
5. 如果先更新 `max_left` 或 `max_right`，再计算水量，就不需要额外判断差值是否大于 `0`。
