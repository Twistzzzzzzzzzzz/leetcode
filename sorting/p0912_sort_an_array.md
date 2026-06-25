# 912. Sort an Array

## 题目

给定一个整数数组 `nums`，返回按升序排列后的数组。

这道题是排序算法练习题，适合用来对比不同排序写法。

## 朴素交换排序

最直接的写法是两层循环。

如果发现前面的数比后面的数大，就交换它们。

```python
class BruteForceSolution:
    def sortArray(self, nums: list[int]) -> list[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] > nums[j]:
                    nums[i], nums[j] = nums[j], nums[i]

        return nums
```

这个写法容易理解，但时间复杂度是 O(n²)，数据量大时会很慢。

## 归并排序

归并排序的核心是“分治”：

1. 把数组从中间切成左右两半。
2. 分别递归排序左右两半。
3. 把两个已经有序的数组合并成一个有序数组。

递归部分是：

```python
mid = len(nums) // 2
left = self.sortArray(nums[:mid])
right = self.sortArray(nums[mid:])
return self._merge(left, right)
```

这几行可以理解为：

- 先把大问题拆成两个小问题
- 小问题继续拆
- 拆到长度为 0 或 1 时天然有序
- 再一层层合并回来

## 归并排序代码

```python
class Solution:
    def sortArray(self, nums: list[int]) -> list[int]:
        if len(nums) <= 1:
            return nums

        mid = len(nums) // 2
        left = self.sortArray(nums[:mid])
        right = self.sortArray(nums[mid:])

        return self._merge(left, right)

    def _merge(self, left: list[int], right: list[int]) -> list[int]:
        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        while i < len(left):
            result.append(left[i])
            i += 1

        while j < len(right):
            result.append(right[j])
            j += 1

        return result
```

## 快速排序

快速排序的核心是选一个 `pivot`，然后把数组分成三部分：

- 小于 `pivot` 的放到 `left`
- 等于 `pivot` 的放到 `middle`
- 大于 `pivot` 的放到 `right`

最后递归排序左右两边：

```python
return self.sortArray(left) + middle + self.sortArray(right)
```

## 快速排序代码

```python
class QuickSortSolution:
    def sortArray(self, nums: list[int]) -> list[int]:
        if len(nums) <= 1:
            return nums

        pivot = random.choice(nums)
        left = []
        middle = []
        right = []

        for num in nums:
            if num < pivot:
                left.append(num)
            elif num > pivot:
                right.append(num)
            else:
                middle.append(num)

        return self.sortArray(left) + middle + self.sortArray(right)
```

这个版本比较直观，但会额外创建 `left`、`middle`、`right` 三个数组。

后续可以再补一个原地指针版快速排序。

## 计数排序

如果题目给了明确的数值范围，就可以考虑计数排序。

这道题的数字范围是：

```text
-50000 <= nums[i] <= 50000
```

所以可以创建一个长度为 `100001` 的数组 `counts`，用来统计每个数字出现了几次。

因为数组下标不能是负数，所以用 `offset = 50000` 做偏移：

```text
真实数字 num -> counts[num + 50000]
数组下标 index -> index - 50000
```

## 计数排序代码

```python
class CountingSortSolution:
    def sortArray(self, nums: list[int]) -> list[int]:
        offset = 50000
        counts = [0] * 100001

        for num in nums:
            counts[num + offset] += 1

        result = []

        for index, count in enumerate(counts):
            if count > 0:
                result.extend([index - offset] * count)

        return result
```

这个版本不是通用排序，它依赖题目给出的数字范围。

如果数字范围特别大，计数数组会很浪费空间。

## 复杂度

朴素交换排序：

- 时间复杂度：O(n²)
- 空间复杂度：O(1)

归并排序：

- 时间复杂度：O(n log n)
- 空间复杂度：O(n)

快速排序：

- 平均时间复杂度：O(n log n)
- 最坏时间复杂度：O(n²)
- 空间复杂度：O(n)

这里的快速排序因为用了额外数组，所以空间复杂度是 O(n)。

计数排序：

- 时间复杂度：O(n + k)
- 空间复杂度：O(k)

其中 `k` 是数字范围大小。这道题里 `k = 100001`。

## 心得

1. 归并排序主要是熟能生巧，重点是记住递归部分：先拆左右，再递归排序，最后 merge。
2. 递归出口是 `len(nums) <= 1`，因为长度为 0 或 1 的数组天然有序。
3. 快速排序目前先写了额外数组版本，逻辑直观；后续还可以补原地指针版。
4. 朴素交换排序适合理解“比较和交换”，但数据量大时不适合。
5. 计数排序适合数字范围明确且不大的题。它不是靠比较大小排序，而是先统计每个数字出现次数，再按数字顺序还原结果。
