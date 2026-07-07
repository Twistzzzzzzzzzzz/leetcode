# 二分查找基础

## 二分查找到底在做什么

二分查找不只是“在排序数组里找 `target`”。

更本质地说，二分查找是在：

```text
一个有单调性的搜索空间里，不断砍掉一半不可能的答案。
```

所以二分的核心不是数组，而是：

```text
单调性
```

只要能判断：

```text
某个位置或某个答案 x 的左边都不满足，右边都满足
```

或者反过来：

```text
左边都满足，右边都不满足
```

就可能使用二分。

## 题型触发词

看到这些条件，可以考虑二分查找：

1. `sorted array` / 排序数组
2. 要求 `O(log n)`
3. 找 `target`
4. 找第一个 `>= target`
5. 找最后一个 `<= target`
6. 找插入位置
7. 找最小可行答案
8. 找最大可行答案
9. 答案范围很大，但可以判断某个答案是否可行
10. `rotated sorted array`
11. `peak` / 山峰
12. 矩阵每行每列有序

最重要的一句：

```text
如果题目要求 O(log n)，大概率就是二分。
```

## 三大类型

### 类型一：普通找 target

代表题：

- 704. Binary Search

目标：

```text
在有序数组中找 target，找到返回下标，否则返回 -1。
```

这是最基础的二分。

### 类型二：找边界

边界题比普通查找更重要。

常见问题：

- 找第一个 `>= target` 的位置
- 找第一个 `> target` 的位置
- 找最后一个 `< target` 的位置
- 找最后一个 `<= target` 的位置
- 找 `target` 的左边界
- 找 `target` 的右边界

这类题的核心不是“找到就返回”，而是继续收缩边界。

### 类型三：二分答案

这类题不是在数组里找，而是在“答案范围”里找。

代表题：

- 875. Koko Eating Bananas
- 1011. Capacity To Ship Packages Within D Days
- 410. Split Array Largest Sum
- 1482. Minimum Number of Days to Make m Bouquets

例如 Koko 吃香蕉：

```text
速度越大，越容易在 h 小时内吃完。
速度越小，越难吃完。
```

这就是单调性。

于是可以二分：

```text
最小可行速度是多少？
```

## 当前阶段先统一的模板

建议当前先统一掌握两个模板：

1. 闭区间普通查找
2. 左边界 / 最小可行答案

先不要同时混学 `[left, right]`、`[left, right)`、`while left < right`、`while left <= right` 的所有变体。

## 模板 A：普通找 target

适用于：

- 704. Binary Search
- 374. Guess Number Higher or Lower
- 33. Search in Rotated Sorted Array 的部分逻辑
- 74. Search a 2D Matrix

```python
def binary_search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

这个模板使用的是闭区间：

```text
[left, right]
```

所以：

```python
right = len(nums) - 1
while left <= right
```

当 `left == right` 时，区间里还有一个元素，仍然要检查。

记忆点：

```text
while left <= right
找到就 return
left = mid + 1
right = mid - 1
```

### 例子：Guess Number Higher or Lower

374. Guess Number Higher or Lower 也是普通闭区间二分。

`guess(num)` 的返回值含义是：

```text
0  表示猜中了
1  表示 num 猜小了，答案更大
-1 表示 num 猜大了，答案更小
```

所以：

```python
if guess(num) == 1:
    left = num + 1
elif guess(num) == -1:
    right = num - 1
else:
    return num
```

这题要特别注意方向：

```text
返回 1 不是往左，而是说明要猜更大的数。
```

## 模板 B：找第一个满足条件的位置

这是最重要的模板。

目标：

```text
找最左边的 valid 位置。
```

也可以理解为：

```text
找第一个 condition(mid) == True 的位置。
```

以 `lower_bound` 为例：

```python
def lower_bound(nums, target):
    left = 0
    right = len(nums)

    while left < right:
        mid = (left + right) // 2

        if nums[mid] >= target:
            right = mid
        else:
            left = mid + 1

    return left
```

这个返回的是：

```text
第一个 nums[i] >= target 的下标。
```

这里使用左闭右开区间：

```text
[left, right)
```

所以：

```python
right = len(nums)
while left < right
```

## lower_bound

`lower_bound(target)` 表示：

```text
找第一个 >= target 的位置。
```

例如：

```python
nums = [1, 2, 2, 2, 4, 5]
target = 2
```

第一个 `>= 2` 的位置是：

```text
index = 1
```

如果：

```python
target = 3
```

第一个 `>= 3` 的位置是：

```text
index = 4
```

对应：

```python
nums[4] = 4
```

如果：

```python
target = 6
```

没有任何数 `>= 6`，返回：

```python
len(nums)
```

这就是插入位置。

35. Search Insert Position 本质就是 `lower_bound`：

```text
如果 target 存在，返回它的位置。
如果 target 不存在，返回第一个 >= target 的位置，也就是插入位置。
```

## upper_bound

`upper_bound(target)` 表示：

```text
找第一个 > target 的位置。
```

模板：

```python
def upper_bound(nums, target):
    left = 0
    right = len(nums)

    while left < right:
        mid = (left + right) // 2

        if nums[mid] > target:
            right = mid
        else:
            left = mid + 1

    return left
```

例如：

```python
nums = [1, 2, 2, 2, 4, 5]
target = 2
```

第一个 `> 2` 的位置是：

```text
index = 4
```

## 左闭右开区间

左闭右开区间写成：

```text
[left, right)
```

意思是包含 `left`，不包含 `right`。

所以常见初始化是：

```python
left = 0
right = len(arr)
```

此时 `right` 可以等于 `len(arr)`，因为它不是会被访问的真实下标。

循环条件通常是：

```python
while left < right:
```

如果判断后答案在左边，也就是新范围应该变成：

```text
[left, mid)
```

那么更新应该写：

```python
right = mid
```

而不是：

```python
right = mid - 1
```

因为在左闭右开里，`right` 本来就不包含，`right = mid` 已经排除了 `mid`。

和闭区间对比：

| 模板 | 区间含义 | 循环 | 右边界更新 |
| --- | --- | --- | --- |
| 闭区间 | `[left, right]` | `while left <= right` | `right = mid - 1` |
| 左闭右开 | `[left, right)` | `while left < right` | `right = mid` |

## 例子：Time Based Key-Value Store

981. Time Based Key-Value Store 是 HashMap + 二分边界。

外层结构是：

```text
key -> [(timestamp, value), ...]
```

因为时间戳是顺序添加的，所以每个 `key` 对应的列表天然按 `timestamp` 有序。

`get(key, timestamp)` 要找的是：

```text
最后一个 <= timestamp 的记录
```

可以转化成：

```text
找第一个 > timestamp 的位置，然后答案是它前一个位置。
```

也就是：

```python
left = 0
right = len(values)

while left < right:
    mid = (left + right) // 2

    if values[mid][0] <= timestamp:
        left = mid + 1
    else:
        right = mid

index = left - 1
```

## 用 lower_bound / upper_bound 找 target 范围

代表题：

- 34. Find First and Last Position of Element in Sorted Array

可以这样想：

```text
左边界 = 第一个 >= target 的位置
右边界 = 第一个 > target 的位置 - 1
```

代码：

```python
class Solution:
    def searchRange(self, nums: list[int], target: int) -> list[int]:
        def lower_bound(target: int) -> int:
            left = 0
            right = len(nums)

            while left < right:
                mid = (left + right) // 2

                if nums[mid] >= target:
                    right = mid
                else:
                    left = mid + 1

            return left

        left_pos = lower_bound(target)
        right_pos = lower_bound(target + 1) - 1

        if left_pos < len(nums) and nums[left_pos] == target:
            return [left_pos, right_pos]

        return [-1, -1]
```

更通用地说：

```text
first target = lower_bound(target)
first greater than target = upper_bound(target)
last target = upper_bound(target) - 1
```

## 为什么有时 right = len(nums)，有时 right = len(nums) - 1

### 普通查找模板

```python
left = 0
right = len(nums) - 1

while left <= right:
```

含义：

```text
搜索区间是闭区间 [left, right]。
```

所以最后一个有效下标是：

```python
len(nums) - 1
```

### lower_bound 模板

```python
left = 0
right = len(nums)

while left < right:
```

含义：

```text
搜索区间是左闭右开 [left, right)。
```

所以 `right` 可以等于 `len(nums)`，表示插入到最后。

## 二分答案模板：找最小可行答案

很多 Medium 题使用这个模板。

目标：

```text
找最小可行答案。
```

模板：

```python
def binary_search_min_answer():
    left = 最小可能答案
    right = 最大可能答案

    while left < right:
        mid = (left + right) // 2

        if check(mid):
            right = mid
        else:
            left = mid + 1

    return left
```

核心：

```text
check(mid) == True 表示 mid 可行。
```

如果 `mid` 可行，尝试更小答案：

```python
right = mid
```

如果 `mid` 不可行，只能变大：

```python
left = mid + 1
```

## 二分答案题真正难在哪里

二分答案题的循环本体通常很固定。

找最小可行答案时，基本就是：

```python
while left < right:
    mid = (left + right) // 2

    if check(mid):
        right = mid
    else:
        left = mid + 1

return left
```

真正的题目差异通常在两件事：

1. 看出来答案具有单调性。
2. 写出 `check(mid)` / `can_finish(mid)` / `can_load(mid)` 函数。

可以这样理解：

```text
二分答案题 = 二分模板 + 判定函数
```

模板负责缩小搜索范围。

判定函数负责告诉我们 `mid` 可不可行。

更准确地说，难点是把题目翻译成：

```text
False False False True True True
                  ^
              找第一个 True
```

或者：

```text
True True True False False False
            ^
       找最后一个 True
```

## check 函数的固定思考方式

以后遇到二分答案题，先问自己：

1. `mid` 代表什么？

   是速度、容量、天数、最大子数组和，还是距离？

2. 给定 `mid`，能不能验证它可不可行？

3. `mid` 越大，是越容易满足，还是越难满足？

4. 要找第一个 `True`，还是最后一个 `True`？

这几个问题答出来，二分答案题基本就成型了。

## 二分答案例子：Koko Eating Bananas

代表题：

- 875. Koko Eating Bananas
- 1011. Capacity To Ship Packages Within D Days

题意：

```text
给 piles 和 h。
Koko 每小时吃 speed 根香蕉。
问最小 speed，使她能在 h 小时内吃完。
```

单调性：

```text
speed 越大，越容易吃完。
speed 越小，越难吃完。
```

所以问题是：

```text
找最小可行 speed。
```

代码：

```python
class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        def can_finish(speed: int) -> bool:
            hours = 0

            for pile in piles:
                hours += (pile + speed - 1) // speed

            return hours <= h

        left = 1
        right = max(piles)

        while left < right:
            mid = (left + right) // 2

            if can_finish(mid):
                right = mid
            else:
                left = mid + 1

        return left
```

这里最重要的是向上取整：

```python
(pile + speed - 1) // speed
```

例如：

```text
pile = 10
speed = 3
10 / 3 = 3.333...
```

实际需要 4 小时，所以要向上取整。

1011 Capacity To Ship Packages Within D Days 也是同一类：

```text
找最小可行容量。
```

搜索范围：

```python
left = max(weights)
right = sum(weights)
```

原因：

```text
容量至少要装得下最重包裹。
容量等于所有包裹重量之和时，一天就能运完，一定可行。
```

`check(capacity)` 的含义是：

```text
按顺序装包裹，容量为 capacity 时，能否在 days 天内运完。
```

## 找最大可行答案

有些题是：

```text
找最大满足条件的答案。
```

模板：

```python
def binary_search_max_answer():
    left = 最小可能答案
    right = 最大可能答案

    while left < right:
        mid = (left + right + 1) // 2

        if check(mid):
            left = mid
        else:
            right = mid - 1

    return left
```

注意这里：

```python
mid = (left + right + 1) // 2
```

这是为了防止死循环。

如果找最大可行答案时写：

```python
mid = (left + right) // 2
left = mid
```

当：

```python
left + 1 == right
```

就会有：

```python
mid == left
```

导致 `left` 不变，进入死循环。

所以最大化模板用右中位数：

```python
mid = (left + right + 1) // 2
```

### 例子：Sqrt(x)

69. Sqrt(x) 要返回：

```text
floor(sqrt(x))
```

等价于：

```text
找最大的 mid，使得 mid * mid <= x。
```

所以这是最大可行答案二分。

```python
def my_sqrt(x):
    left = 0
    right = x

    while left < right:
        mid = (left + right + 1) // 2

        if mid * mid <= x:
            left = mid
        else:
            right = mid - 1

    return left
```

核心记忆：

```text
找最大可行答案：
while left < right
mid 取右中位数
True 时 left = mid
False 时 right = mid - 1
```

## 二分的核心判断

每次写二分，都先问自己三个问题：

1. 我搜索的是什么？
2. `mid` 代表什么？
3. `check(mid)` 为 `True` 时，答案应该在左边还是右边？

### lower_bound 的例子

搜索的是：

```text
第一个 >= target 的位置。
```

`mid` 代表：

```text
当前检查的下标。
```

如果：

```python
nums[mid] >= target
```

说明 `mid` 可能是答案，但左边也可能有答案：

```python
right = mid
```

如果：

```python
nums[mid] < target
```

说明 `mid` 以及左边都不可能是答案：

```python
left = mid + 1
```

### Koko 的例子

搜索的是：

```text
最小可行速度。
```

`mid` 代表：

```text
吃香蕉速度。
```

如果：

```python
can_finish(mid) is True
```

说明 `mid` 可行，但可能还能更小。

同时，`mid` 本身也可能就是答案，所以不能排除 `mid`：

```python
right = mid
```

如果：

```python
can_finish(mid) is False
```

说明速度太慢，`mid` 以及更小的速度都不可能是答案，所以可以排除 `mid`：

```python
left = mid + 1
```

不能写成：

```python
right = mid - 1
left = mid
```

因为找最小可行答案时，True 的 `mid` 可能就是答案，不能丢；False 的 `mid` 已经不可能是答案，必须用 `mid + 1` 排除，避免死循环。

## 常见坑

### 坑 1：死循环

错误例子：

```python
while left < right:
    mid = (left + right) // 2
    if check(mid):
        left = mid
    else:
        right = mid - 1
```

当：

```python
left = 3
right = 4
mid = 3
```

如果执行：

```python
left = mid
```

`left` 仍然是 3，会死循环。

解决：

```python
mid = (left + right + 1) // 2
```

这个写法用于“找最大可行答案”。

### 坑 2：混用循环条件

当前阶段先这样记：

```text
普通找 target：while left <= right
找边界 / 找最小可行答案：while left < right
```

这不是唯一写法，但最适合先稳定下来。

### 坑 3：边界题找到 target 就直接 return

如果题目问：

```text
第一个 target
最后一个 target
```

那么看到：

```python
nums[mid] == target
```

不能直接 `return`。

因为还要继续找边界。

### 坑 4：忘记处理不存在

例如 34. Find First and Last Position。

用 `lower_bound` 找到位置后，还要检查：

```python
if pos < len(nums) and nums[pos] == target:
```

否则 `target` 不存在时会误判。

### 坑 5：`mid + 1` 越界

有些题会访问：

```python
nums[mid + 1]
```

那就要保证：

```python
mid + 1 < len(nums)
```

比如 peak element 或 rotated array 题，要特别注意边界。

## 二分和滑动窗口的区别

### 滑动窗口

适合：

```text
连续子数组 / 子串
right 向右扩
left 向右缩
维护一个窗口状态
```

典型题：

- 3
- 209
- 424
- 567
- 76

### 二分查找

适合：

```text
搜索某个位置 / 某个答案
每次砍掉一半搜索空间
```

典型题：

- 704
- 35
- 34
- 875
- 1011

区别：

```text
滑动窗口：线性移动边界。
二分查找：每次跳到中间，砍掉一半。
```

## 题型地图

### A. 基础数组查找

先做：

- 704. Binary Search
- 35. Search Insert Position
- 278. First Bad Version
- 374. Guess Number Higher or Lower

目标：

```text
熟悉 left / right / mid 的移动。
```

### B. 边界查找

然后做：

- 34. Find First and Last Position of Element in Sorted Array
- 69. Sqrt(x)
- 367. Valid Perfect Square

目标：

```text
理解 lower_bound。
```

### C. 旋转排序数组

之后做：

- 33. Search in Rotated Sorted Array
- 153. Find Minimum in Rotated Sorted Array
- 154. Find Minimum in Rotated Sorted Array II
- 81. Search in Rotated Sorted Array II

目标：

```text
学会判断哪一边有序。
```

33. Search in Rotated Sorted Array 是旋转排序数组里查找具体 `target`。

普通二分依赖整个数组有序，但旋转数组整体不一定有序。

不过每次取出 `mid` 后，左半边和右半边至少有一边是有序的。

所以流程是：

1. 先检查 `nums[mid] == target`。
2. 再判断左半边有序还是右半边有序。
3. 判断 `target` 是否落在有序的那一边。

左半边有序：

```python
if nums[left] <= nums[mid]:
```

如果 `target` 在左半边：

```python
if nums[left] <= target < nums[mid]:
    right = mid - 1
else:
    left = mid + 1
```

右半边有序：

```python
else:
    if nums[mid] < target <= nums[right]:
        left = mid + 1
    else:
        right = mid - 1
```

这里的等号要特别注意：

```text
left 和 right 是还没排除的边界，所以 target 可能等于 nums[left] 或 nums[right]。
mid 已经被单独检查过，所以后面的范围判断不再包含 nums[mid]。
```

所以范围判断是：

```python
nums[left] <= target < nums[mid]
nums[mid] < target <= nums[right]
```

81. Search in Rotated Sorted Array II 和 33 的区别是允许重复元素。

重复元素会让有序半边的判断失效。

例如：

```python
nums[left] == nums[mid] == nums[right]
```

这时无法判断左半边有序还是右半边有序。

但如果前面已经检查过：

```python
if nums[mid] == target:
    return True
```

那么三端相等且 `nums[mid]` 不是 `target` 时，`nums[left]` 和 `nums[right]` 也不是 `target`。

所以可以安全收缩：

```python
left += 1
right -= 1
```

剩下的逻辑和 33 一样。

注意：因为重复元素可能导致每次只能收缩一格，所以最坏时间复杂度会退化到 O(n)。

153. Find Minimum in Rotated Sorted Array 是旋转排序数组里的结构二分。

它不是在找某个 `target`，而是在找旋转点，也就是最小值的位置。

常用判断是比较：

```python
nums[mid]
nums[right]
```

如果：

```python
nums[mid] > nums[right]
```

说明 `mid` 在左边较大的那段里，最小值一定在 `mid` 右边：

```python
left = mid + 1
```

否则：

```python
right = mid
```

因为 `mid` 仍然可能就是最小值，不能直接排除。

这类题看起来代码量比普通二分少，是因为没有 `nums[mid] == target` 的分支，本质是在判断最小值落在哪一侧。

### D. 二分答案

重点 Medium：

- 875. Koko Eating Bananas
- 1011. Capacity To Ship Packages Within D Days
- 1482. Minimum Number of Days to Make m Bouquets
- 410. Split Array Largest Sum
- 1552. Magnetic Force Between Two Balls

目标：

```text
把“找答案”转化成“判断 mid 是否可行”。
```

### E. 矩阵二分

代表题：

- 74. Search a 2D Matrix
- 240. Search a 2D Matrix II

注意：

```text
74 可以二分。
240 通常从右上角走，不是普通二分最优。
```

74 的矩阵满足整体有序，可以直接把二维矩阵看成一维数组。

一维下标和二维坐标的映射是：

```python
row = mid // cols
col = mid % cols
```

也可以先二分行首，找到候选行，再在这一行里做普通二分。

### F. 特殊二分

代表题：

- 162. Find Peak Element
- 658. Find K Closest Elements
- 852. Peak Index in a Mountain Array
- 540. Single Element in a Sorted Array

这些题不一定是普通 `target` 查找，而是利用结构单调性或局部关系。

## 推荐刷题顺序

1. 704. Binary Search
2. 35. Search Insert Position
3. 278. First Bad Version
4. 34. Find First and Last Position
5. 69. Sqrt(x)
6. 367. Valid Perfect Square
7. 33. Search in Rotated Sorted Array
8. 153. Find Minimum in Rotated Sorted Array
9. 74. Search a 2D Matrix
10. 875. Koko Eating Bananas
11. 1011. Capacity To Ship Packages Within D Days
12. 1482. Minimum Number of Days to Make m Bouquets
13. 162. Find Peak Element
14. 658. Find K Closest Elements
15. 410. Split Array Largest Sum

前 6 题把模板打稳。

第 7 到 9 题练结构判断。

第 10 题之后练“二分答案”。

## 应该背下来的三个模板

### 模板 1：普通查找

```python
def search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

### 模板 2：第一个 >= target

```python
def lower_bound(nums, target):
    left = 0
    right = len(nums)

    while left < right:
        mid = (left + right) // 2

        if nums[mid] >= target:
            right = mid
        else:
            left = mid + 1

    return left
```

### 模板 3：最小可行答案

```python
def binary_search_min_answer():
    left = 最小可能答案
    right = 最大可能答案

    while left < right:
        mid = (left + right) // 2

        if check(mid):
            right = mid
        else:
            left = mid + 1

    return left
```

## 做题固定思考流程

每一道二分题，都按这 5 个问题想：

1. 搜索空间是什么？

   是下标？是答案值？是速度？是容量？是天数？

2. `left` 和 `right` 分别是多少？

   最小可能值和最大可能值是什么？

3. `mid` 代表什么？

   下标？速度？容量？天数？

4. `check(mid)` 的含义是什么？

   `mid` 是否可行？`nums[mid]` 是否满足某个关系？

5. 如果 `check(mid)` 为 `True`，应该往左找还是往右找？

只要这 5 个问题能回答，代码基本就能写出来。

## 当前阶段学习目标

现在先不要追求所有二分变体都秒杀。

当前目标是：

1. 普通二分不写错边界。
2. `lower_bound` 能独立写出来。
3. 能解释 `left` / `right` / `mid` 的含义。
4. 能判断什么时候用 `while left <= right`，什么时候用 `while left < right`。
5. 能看出二分答案题的单调性。

下一题建议从：

```text
704. Binary Search
```

开始。
