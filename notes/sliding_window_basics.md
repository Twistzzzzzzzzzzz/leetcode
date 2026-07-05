# 滑动窗口基础

## 什么是滑动窗口

滑动窗口本质上是在数组或字符串里维护一个连续区间。

数组里可以理解成：

```python
nums[left:right + 1]
```

字符串里可以理解成：

```python
s[left:right + 1]
```

其中：

- `left` 是窗口左边界
- `right` 是窗口右边界

窗口会随着 `right` 向右扩张，必要时 `left` 向右收缩。

例如：

```python
s = "abcabcbb"
```

某一刻窗口可能是：

```text
a b c a b c b b
    ^     ^
   left  right
```

窗口内容是：

```text
"cabc"
```

## 滑动窗口和双指针的区别

滑动窗口可以看成双指针的一种特殊用法。

| 类型 | 核心 |
| --- | --- |
| Two Pointers | 两个指针协作移动 |
| Sliding Window | 两个指针维护一个连续区间 |

双指针不一定强调区间。

例如 167 Two Sum II：

- `left` 指向一个小数
- `right` 指向一个大数

它关注的是两个点。

滑动窗口关注的是一整段连续区间：

```python
s[left:right + 1]
```

例如最长无重复子串，窗口内要满足：

```text
不能有重复字符
```

## 滑动窗口适合什么题

滑动窗口的核心关键词是：

```text
连续子数组 / 连续子串
最长 / 最短
满足某个条件
```

看到这些词，可以优先想到滑动窗口：

- `subarray`
- `substring`
- `contiguous`
- `longest`
- `shortest`
- `minimum length`
- `maximum length`
- `at most k`
- `at least k`
- `no duplicate`
- `contains all characters`
- `sum >= target`
- `frequency`

中文就是：

- 连续
- 子数组
- 子串
- 最长
- 最短
- 至多 `k` 个
- 至少 `k` 个
- 不重复
- 包含所有字符
- 窗口内频率
- 窗口内和

## 哪些题不是普通滑动窗口

不是所有“连续子数组”都能直接滑窗。

普通滑动窗口通常要求窗口状态有某种单调性。

### 可以滑窗的情况

例如：

```text
数组全是正数，找 sum >= target 的最短子数组
```

因为：

- `right` 右移，`sum` 只会变大
- `left` 右移，`sum` 只会变小

这就适合滑动窗口。

### 不适合普通滑窗的情况

如果数组里有负数，`sum` 就不单调。

例如：

```python
nums = [2, -1, 2]
```

`right` 右移时，`sum` 可能变大，也可能变小。

这种情况下普通滑动窗口容易失效。

所以：

```text
子数组和 + 有负数
```

通常要想：

```text
前缀和 + 哈希表
```

例如之前做过的 560 Subarray Sum Equals K，就不能用普通滑动窗口。

## 两大类型

滑动窗口大致分两类：

1. 固定长度窗口
2. 可变长度窗口

## 类型 A：固定长度窗口

题目直接给定窗口长度 `k`。

常见问法：

- 长度为 `k` 的子数组最大和
- 长度为 `k` 的子数组最大平均值
- 长度为 `k` 的子串里最多有几个元音

模板：

```python
window_sum = 0
answer = 0

for right in range(len(nums)):
    window_sum += nums[right]

    if right >= k:
        window_sum -= nums[right - k]

    if right >= k - 1:
        answer = max(answer, window_sum)
```

核心：

- `right` 每次加入一个新元素
- 如果窗口长度超过 `k`，就移除最左边元素
- 当 `right >= k - 1` 时，窗口长度才真正达到 `k`

代表题：

- 643. Maximum Average Subarray I
- 1456. Maximum Number of Vowels in a Substring of Given Length

## 类型 B：可变长度窗口

窗口长度不固定，靠条件控制。

常见题：

- 最长无重复子串
- 最短和至少为 `target` 的子数组
- 最多包含 `k` 个不同字符的最长子串

基本模板：

```python
left = 0
window_state = ...

for right in range(len(nums)):
    # 1. 把 nums[right] 加进窗口

    while 窗口不合法:
        # 2. 移除 nums[left]
        left += 1

    # 3. 更新答案
```

这是接下来最需要掌握的模板。

## 最长型模板

题目问：

```text
最长的 xxx
```

通常是：

```python
left = 0
answer = 0

for right in range(len(s)):
    # 加入 s[right]

    while 窗口不合法:
        # 移除 s[left]
        left += 1

    answer = max(answer, right - left + 1)
```

核心：

```text
每次窗口合法后，更新最长长度。
```

## 最短型模板

题目问：

```text
最短的 xxx
```

通常是：

```python
left = 0
answer = float("inf")

for right in range(len(nums)):
    # 加入 nums[right]

    while 窗口已经满足条件:
        answer = min(answer, right - left + 1)

        # 尝试缩小窗口
        left += 1
```

核心：

```text
满足条件后，边收缩 left，边更新最短长度。
```

这里答案更新的位置很重要：

```python
while window_sum >= target:
    answer = min(answer, right - left + 1)
    window_sum -= nums[left]
    left += 1
```

要先更新答案，再移除左端元素。

因为移除前的窗口已经满足条件，是一个合法答案。

## 什么时候移动 left

这是滑动窗口的关键。

要先问自己：

```text
当前窗口什么时候不合法？
```

### 例子 1：最长无重复子串

窗口要求：

```text
不能有重复字符
```

不合法条件是：

```text
某个字符出现次数 > 1
```

于是：

```python
while count[s[right]] > 1:
    count[s[left]] -= 1
    left += 1
```

### 例子 2：最短和至少为 target 的子数组

窗口要求：

```text
sum >= target
```

问最短，所以一旦满足，就开始缩小：

```python
while window_sum >= target:
    answer = min(answer, right - left + 1)
    window_sum -= nums[left]
    left += 1
```

## 常用窗口状态

你需要维护窗口里的某种信息。

| 题目条件 | 维护什么 |
| --- | --- |
| 窗口和 | `window_sum` |
| 字符频率 | `dict` / `Counter` |
| 是否重复 | `set` 或 `dict count` |
| 元音数量 | `vowel_count` |
| 最多 `k` 个不同字符 | `freq + len(freq)` |
| 包含目标字符 | `need/window` 两个字典 |

## 刷题常用模板

### 模板 1：可变窗口，求最长

适合问：

```text
最长连续子数组 / 最长连续子串
```

核心流程：

```python
left = 0
answer = 0
window_state = ...

for right in range(n):
    # 1. 加入右端元素
    add(nums[right])

    # 2. 窗口不合法时，持续移除左端元素
    while 窗口不合法:
        remove(nums[left])
        left += 1

    # 3. 此时窗口已经合法，更新最大长度
    answer = max(answer, right - left + 1)
```

记忆点：

```text
最长型：先修合法，再更新最大值。
```

### 模板 2：可变窗口，求最短

适合问：

```text
满足条件的最短连续子数组 / 最短连续子串
```

核心流程：

```python
left = 0
answer = float("inf")
window_state = ...

for right in range(n):
    # 1. 加入右端元素
    add(nums[right])

    # 2. 窗口满足条件后，尝试继续缩小
    while 窗口满足条件:
        answer = min(answer, right - left + 1)
        remove(nums[left])
        left += 1

return answer if answer != float("inf") else 0
```

记忆点：

```text
最短型：一旦满足条件，就边收缩边更新最小值。
```

### 模板 3：固定长度窗口

适合题目直接给窗口长度 `k`。

核心流程：

```python
window_sum = 0
answer = 0

for right in range(n):
    window_sum += nums[right]

    if right >= k:
        window_sum -= nums[right - k]

    if right >= k - 1:
        answer = max(answer, window_sum)
```

记忆点：

```text
固定窗口：右边进一个，长度超了左边出一个。
```

### 模板 4：无重复字符窗口

适合问：

```text
最长无重复子串
```

核心流程：

```python
seen = set()
left = 0
answer = 0

for right, char in enumerate(s):
    while char in seen:
        seen.remove(s[left])
        left += 1

    seen.add(char)
    answer = max(answer, right - left + 1)
```

记忆点：

```text
无重复窗口：当前字符重复了，就从左边删到不重复为止。
```

### 模板 5：最多替换 k 次窗口

适合问：

```text
最多替换 k 次后，最长能变成同一种字符的子串
```

核心公式：

```python
window_len = right - left + 1
max_freq = max(freq.values())

window_len - max_freq <= k
```

核心流程：

```python
freq = {}
left = 0
answer = 0

for right, char in enumerate(s):
    freq[char] = freq.get(char, 0) + 1
    max_freq = max(freq.values())

    while right - left + 1 - max_freq > k:
        freq[s[left]] -= 1
        left += 1
        max_freq = max(freq.values())

    answer = max(answer, right - left + 1)
```

记忆点：

```text
要替换的数量 = 窗口长度 - 窗口内最高频字符次数。
```

### 模板 6：固定长度频率窗口

适合问：

```text
一个字符串是否包含另一个字符串的排列 / anagram
```

核心流程：

```python
freq = {}
k = len(target)

for char in target:
    freq[char] = freq.get(char, 0) + 1

left = 0

for right, char in enumerate(s):
    if char in freq:
        freq[char] -= 1

    while right - left + 1 > k:
        if s[left] in freq:
            freq[s[left]] += 1
        left += 1

    if right - left + 1 == k and all(value == 0 for value in freq.values()):
        return True

return False
```

记忆点：

```text
排列长度不变，所以窗口长度固定；字符频率完全抵消，就说明找到一个排列。
```

### 模板 7：二分固定窗口左边界

适合问：

```text
有序数组里找长度为 k 的最优连续窗口
```

核心流程：

```python
left = 0
right = len(arr) - k

while left < right:
    mid = (left + right) // 2

    if 窗口应该整体右移:
        left = mid + 1
    else:
        right = mid

return arr[left:left + k]
```

以 658 Find K Closest Elements 为例：

```python
if x - arr[mid] > arr[mid + k] - x:
    left = mid + 1
else:
    right = mid
```

这里比较的是：

```text
当前窗口左边界 arr[mid]
右边外面第一个候选元素 arr[mid + k]
```

如果左边界更远，说明窗口太靠左，应该右移。

记忆点：

```text
不是二分某个元素下标，而是二分长度为 k 的窗口左边界。
```

二分时要问：

```text
对于候选窗口 arr[mid:mid + k]，
它应该继续留在左边，还是应该往右移动？
```

这类题不要随便用窗口 `sum` 判断窗口好坏。

例如找最接近 `x` 的 `k` 个元素时，比较的是元素离 `x` 的距离，不是窗口总和离 `k * x` 的距离。

## 容易混淆的点

### 1. `right` 负责扩张，`left` 负责收缩

不要两个指针乱跳。

- `right` 每轮固定向右走一步
- `left` 只在窗口不合法或需要缩小时移动

### 2. 更新答案的位置很关键

最长型：

```python
while 不合法:
    left += 1

answer = max(answer, right - left + 1)
```

最短型：

```python
while 已经满足条件:
    answer = min(answer, right - left + 1)
    left += 1
```

### 3. 窗口长度是 `right - left + 1`

固定记住：

```python
length = right - left + 1
```

不是：

```python
right - left
```

因为左右端点都包含。

### 4. 移动 left 前，要先移除窗口状态

例如：

```python
count[s[left]] -= 1
left += 1
```

顺序不能反。

要先把左端元素从窗口状态里删掉，再移动 `left`。

## 建议刷题顺序

| 顺序 | 题号 | 题名 | 类型 |
| --- | --- | --- | --- |
| 1 | 643 | Maximum Average Subarray I | 固定窗口 |
| 2 | 3 | Longest Substring Without Repeating Characters | 可变窗口 / 无重复 |
| 3 | 209 | Minimum Size Subarray Sum | 可变窗口 / 最短 |
| 4 | 424 | Longest Repeating Character Replacement | 可变窗口 / 最多替换 k 次 |
| 5 | 567 | Permutation in String | 固定窗口 + 频率 |
| 6 | 438 | Find All Anagrams in a String | 固定窗口 + 频率 |
| 7 | 76 | Minimum Window Substring | Hard，后期做 |

现在先别碰 76。

先把 643、3、209、424 吃透。

## 判断流程

以后看题先问这几个问题：

1. 题目是不是在找连续子数组或连续子串？
2. 有没有最长、最短、满足条件？
3. 这个条件能不能随着 `left/right` 移动来维护？
4. 窗口是否合法，可以用什么状态判断？
5. 是固定长度，还是可变长度？

如果答案是：

```text
连续 + 最长/最短 + 可维护状态
```

大概率就是滑动窗口。

## 总结口诀

```text
滑动窗口 = 连续区间 + 双指针 + 维护窗口状态
```

- `right` 负责扩张窗口。
- `left` 负责收缩窗口。
- 窗口状态负责判断是否合法。
- 最长题：合法后更新最大值。
- 最短题：满足条件后边收缩边更新最小值。
