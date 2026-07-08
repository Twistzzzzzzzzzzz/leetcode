# 2. Add Two Numbers

## 题目

给定两个非空链表，分别表示两个非负整数。

数字是倒序存储的，每个节点只存一位数字。

例如：

```text
l1 = 2 -> 4 -> 3
l2 = 5 -> 6 -> 4
```

表示：

```text
342 + 465 = 807
```

返回：

```text
7 -> 0 -> 8
```

## 思路

这题是 dummy 构造新链表 + 进位 `carry`。

因为数字是倒序存储的，所以链表头部就是个位，可以直接从头开始相加。

每一轮取：

```python
val1 = l1.val if l1 else 0
val2 = l2.val if l2 else 0
```

然后加上上一轮的进位：

```python
total = val1 + val2 + carry
```

当前位是：

```python
digit = total % 10
```

新的进位是：

```python
carry = total // 10
```

把当前位接到新链表后面：

```python
curr.next = ListNode(digit)
curr = curr.next
```

循环条件要写：

```python
while l1 or l2 or carry:
```

因为即使两个链表都走完了，也可能还有最后一个进位。

## 为什么倒序存储更方便

这题的链表是倒序的：

```text
个位 -> 十位 -> 百位
```

所以可以从头到尾直接模拟竖式加法。

如果是正序存储：

```text
百位 -> 十位 -> 个位
```

就不能直接从头开始加，因为进位是从低位往高位传的。

正序版本会麻烦很多，通常需要：

- 使用栈
- 或者先反转链表

所以你这里的判断是对的：reverse 这个顺序反而让题目简单。

## 代码

```python
class Solution:
    def addTwoNumbers(
        self, l1: ListNode | None, l2: ListNode | None
    ) -> ListNode | None:
        dummy = ListNode(0)
        curr = dummy
        carry = 0

        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            total = val1 + val2 + carry
            carry = total // 10
            digit = total % 10

            curr.next = ListNode(digit)
            curr = curr.next

            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

        return dummy.next
```

## 复杂度

设两个链表长度分别为 `m` 和 `n`。

时间复杂度：O(max(m, n))

空间复杂度：O(max(m, n))

空间复杂度来自新建的结果链表。

## 心得

这题的核心状态是 `carry`。

每一位都做三件事：

1. 取两个链表当前节点的值，没有节点就当作 0。
2. 加上 `carry`。
3. 用 `% 10` 得到当前位，用 `// 10` 得到新的进位。

循环条件里的 `or carry` 很重要，用来处理最后还剩一个进位的情况。

因为输入链表是倒序存储的，所以可以直接从头开始加；如果是正序存储，就需要栈或反转链表。
