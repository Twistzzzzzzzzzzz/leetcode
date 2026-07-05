# 658. Find K Closest Elements

## 题目

给定一个已经升序排列的数组 `arr`，返回其中最接近 `x` 的 `k` 个元素。

结果也需要按升序返回。

## 思路

这题比较特别，是“二分查找 + 固定长度窗口”。

因为最终答案一定是 `arr` 里的连续一段，长度固定为 `k`：

```python
arr[left:left + k]
```

所以问题可以转化成：

```text
在所有长度为 k 的窗口里，找到最适合作为答案的窗口左边界 left。
```

左边界最小可以是 `0`。

左边界最大可以是：

```python
len(arr) - k
```

因为窗口长度是 `k`，如果左边界再往右，窗口就会越界。

## 二分判断

假设当前窗口左边界是 `mid`：

```python
arr[mid:mid + k]
```

二分时真正要问的问题是：

```text
对于候选窗口 arr[mid:mid + k]，
它是应该继续留在左边，还是应该往右移动？
```

我们比较两个边界外侧的候选：

```python
arr[mid]
arr[mid + k]
```

具体来说：

当前候选窗口是：

```python
arr[mid:mid + k]
```

它的左边界元素是：

```python
arr[mid]
```

它右边外面第一个候选元素是：

```python
arr[mid + k]
```

然后比较：

```python
x - arr[mid]
```

和：

```python
arr[mid + k] - x
```

如果：

```python
x - arr[mid] > arr[mid + k] - x
```

说明左边界元素 `arr[mid]` 比右边外面第一个候选元素 `arr[mid + k]` 离 `x` 更远。

也就是说，当前窗口太靠左了，应该整体右移：


```python
left = mid + 1
```

否则，窗口不应该右移，当前 `mid` 以及更左边仍然可能是答案：

```python
right = mid
```

## 代码

```python
class Solution:
    def findClosestElements(self, arr: list[int], k: int, x: int) -> list[int]:
        left = 0
        right = len(arr) - k

        while left < right:
            mid = (left + right) // 2

            if x - arr[mid] > arr[mid + k] - x:
                left = mid + 1
            else:
                right = mid

        return arr[left:left + k]
```

## 为什么比较 `arr[mid]` 和 `arr[mid + k]`

窗口长度是 `k`。

如果窗口从 `mid` 开始：

```python
arr[mid:mid + k]
```

那么 `arr[mid]` 是当前窗口最左边的元素。

而 `arr[mid + k]` 是如果窗口右移一格后，可能新进入窗口的元素。

所以这两个数决定了：

```text
窗口应该留在左边，还是应该往右移动。
```

## 注意

这题不是直接二分查找最接近 `x` 的某个下标。

更准确地说，它是在二分查找：

```text
最优长度为 k 的窗口左边界。
```

这也是它看起来像“二分滑动窗口”的原因。

可以把 `mid` 理解成：

```text
候选窗口的左边界
```

而不是：

```text
最接近 x 的元素下标
```

## 不要用窗口 sum 判断接近程度

这题不要用窗口和 `sum(window)` 来判断哪个窗口更接近 `x`。

原因是题目要求的是：

```text
窗口里的每个元素 individually 更接近 x
```

不是要求：

```text
窗口总和更接近 k * x
```

窗口和可能看起来很接近 `k * x`，但里面可能包含一个特别小和一个特别大的数，它们只是互相抵消了。

这不代表这些元素本身更接近 `x`。

所以这题应该比较窗口边界：

```python
x - arr[mid]
arr[mid + k] - x
```

而不是比较窗口总和。

## 复杂度

- 时间复杂度：O(log(n - k) + k)
- 空间复杂度：O(1)

二分窗口左边界需要 `O(log(n - k))`，最后切片返回长度为 `k` 的结果需要 `O(k)`。

## 心得

1. 这题很新奇，是二分查找和固定长度窗口结合起来的题。
2. 最终答案一定是长度为 `k` 的连续窗口，所以可以二分窗口左边界。
3. 更准确地说，不是二分查找最接近 `x` 的单个下标，而是二分查找最优窗口起点。
4. 判断窗口是否应该右移，核心比较是：`x - arr[mid] > arr[mid + k] - x`。
5. 如果距离相等，题目要求优先选择更小的元素，所以保留左边窗口，也就是 `right = mid`。
6. 不要用窗口 `sum` 判断接近程度，因为总和接近不代表窗口里的每个元素都更接近 `x`。
