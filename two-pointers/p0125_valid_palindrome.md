# 125. Valid Palindrome

## 题目

给定一个字符串 `s`，判断它是不是回文串。

判断时需要：

- 忽略非字母和数字的字符
- 忽略大小写

## 思路

这题适合使用左右双指针。

定义：

- `left` 指向左边当前要比较的位置
- `right` 指向右边当前要比较的位置

每一轮做三件事：

1. 从左边跳过无效字符。
2. 从右边跳过无效字符。
3. 比较 `s[left].lower()` 和 `s[right].lower()`。

如果不同，说明不是回文，直接返回 `False`。

如果相同，就继续向中间移动。

## 如何识别这类题

看到“回文”时，可以先想到左右双指针。

因为回文的本质是：

```text
第一个有效字符 == 最后一个有效字符
第二个有效字符 == 倒数第二个有效字符
...
```

所以自然可以从两端开始比较。

这题和 344 Reverse String 很像，都是从两端向中间处理。区别是：

- 344 是直接交换
- 125 是跳过无效字符后比较

## 代码

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1

        while left < right:
            while left < right and not s[left].isalnum():
                left += 1

            while left < right and not s[right].isalnum():
                right -= 1

            if s[left].lower() != s[right].lower():
                return False

            left += 1
            right -= 1

        return True
```

## 为什么内层 `while` 也要写 `left < right`

内层 `while` 的作用是移动指针，跳过无效字符。

移动过程中，`left` 和 `right` 可能会相遇，甚至交叉。

所以内层循环也要写：

```python
while left < right and not s[left].isalnum():
```

如果不加 `left < right`，指针可能在跳过字符时越过边界，或者在已经没有必要比较时继续访问字符串。

这类写法可以理解成：

```text
只要两个指针还没有完成比较任务，才继续移动。
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

每个字符最多被左右指针访问常数次。

## 心得

1. 看到“回文”可以先想到左右双指针。
2. 有无效字符时，先用内层 `while` 把指针移动到有效字符上。
3. 内层 `while` 也要加 `left < right`，因为移动过程中两个指针可能相遇或交叉。
