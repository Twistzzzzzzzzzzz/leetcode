# 680. Valid Palindrome II

## 题目

给定一个字符串 `s`，判断最多删除一个字符后，它能不能变成回文串。

注意是“最多删除一个”，所以本来就是回文也要返回 `True`。

## 思路

这题仍然是左右双指针。

先从两端开始比较：

- 如果 `s[left] == s[right]`，说明当前这一对字符没问题，继续向中间移动。
- 如果 `s[left] != s[right]`，说明出现了第一次冲突。

因为最多只能删除一个字符，所以第一次冲突时只有两种选择：

1. 删除左边字符，检查 `left + 1` 到 `right` 是否为回文。
2. 删除右边字符，检查 `left` 到 `right - 1` 是否为回文。

只要其中一种可以成立，答案就是 `True`。

## 不是递归，而是分支检查

这里的 `is_palindrome_range` 不是递归。

它只是一个辅助函数，用来检查某一段区间是不是回文。

真正关键的地方是：

```text
第一次不匹配时，把“删左边”或“删右边”两种情况都试一下
```

因为不能只靠一个 `count` 继续往下走。

当 `s[left] != s[right]` 时，并不知道应该删除左边字符还是右边字符。这个选择会影响后面的比较。

所以更稳的写法是直接检查两个剩余区间。

## 代码

```python
class Solution:
    def validPalindrome(self, s: str) -> bool:
        def is_palindrome_range(left: int, right: int) -> bool:
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1

            return True

        left = 0
        right = len(s) - 1

        while left < right:
            if s[left] != s[right]:
                return is_palindrome_range(left + 1, right) or is_palindrome_range(
                    left, right - 1
                )

            left += 1
            right -= 1

        return True
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

主循环最多走一遍。第一次不匹配时，最多额外检查两段区间，所以整体仍然是 O(n)。

## 心得

1. 这题和 125 一样，看到“回文”可以先想到左右双指针。
2. 一开始思路已经接近正确：如果左右字符不一样，就尝试移动一边指针。
3. 更关键的是，第一次不匹配时不能确定删左边还是删右边，所以要分别检查两种情况。
4. `is_palindrome_range` 不是递归，而是把剩下的区间交给辅助函数再检查一次。
