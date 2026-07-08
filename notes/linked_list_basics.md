# 链表基础

链表专题和数组、滑动窗口、二分查找的感觉不太一样。

它更像是指针操作题，核心不是复杂数学，而是：

```text
能不能准确控制 prev / curr / next 的关系。
能不能在修改 next 之前保存后续节点。
能不能处理 head 被删除、反转、移动的情况。
```

## 链表题在考什么

链表题主要考：

- 指针重连
- 边界处理
- dummy node
- 快慢指针
- 反转链表
- 合并链表
- 找中点
- 判断环
- 删除节点
- 递归理解

链表的核心问题是：

```text
你改一个 next 指针时，是否提前保存了后续节点。
```

## Python 里的链表节点

LeetCode 一般会给出这个定义：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

一个链表：

```text
1 -> 2 -> 3 -> None
```

在内存里不是连续数组，而是一个个节点互相指向：

```python
node1.val = 1
node1.next = node2

node2.val = 2
node2.next = node3

node3.val = 3
node3.next = None
```

如果有：

```python
head
```

它指向的是第一个节点。

## 链表和数组最大的区别

数组可以直接访问：

```python
nums[i]
```

链表不行。

链表只能从头开始一步一步走：

```python
curr = head

while curr:
    curr = curr.next
```

所以链表题通常不能随机访问。你要靠指针移动。

## 遍历模板

### 普通遍历

处理所有节点：

```python
curr = head

while curr:
    # 处理 curr
    curr = curr.next
```

### 访问当前和下一个节点

如果要安全访问 `curr.next`：

```python
curr = head

while curr and curr.next:
    # 可以安全访问 curr.next
    curr = curr.next
```

### 删除节点时的 prev / curr

删除节点通常需要知道前一个节点：

```python
prev = None
curr = head

while curr:
    # prev 是 curr 的前一个节点
    prev = curr
    curr = curr.next
```

实际删除时更常配合 dummy 使用。

## dummy node

dummy 是虚拟头节点：

```python
dummy = ListNode(0)
dummy.next = head
```

它让链表变成：

```text
dummy -> 1 -> 2 -> 3 -> None
```

最后通常返回：

```python
return dummy.next
```

## 什么时候想到 dummy

看到这些情况，优先考虑 dummy：

- 可能删除 `head`
- 需要构造新链表
- 需要在 `head` 前面插入节点
- 需要统一处理 `prev.next`
- 题目要求返回新的 `head`

典型题：

- 21. Merge Two Sorted Lists
- 19. Remove Nth Node From End of List
- 203. Remove Linked List Elements
- 24. Swap Nodes in Pairs
- 92. Reverse Linked List II
- 86. Partition List

dummy 的价值是减少对头节点的特判。

## prev / curr / nxt

反转链表时最经典的三指针是：

```python
prev = None
curr = head

while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt
```

每一步都很重要：

```python
nxt = curr.next
```

先保存后续节点。

如果直接改：

```python
curr.next = prev
```

原来的后续链表就断了。

链表反转口诀：

```text
先存 next
再改 curr.next
再移动 prev 和 curr
```

## 反转链表模板

206. Reverse Linked List 必须背熟。

```python
class Solution:
    def reverseList(self, head: ListNode | None) -> ListNode | None:
        prev = None
        curr = head

        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        return prev
```

复杂度：

- 时间复杂度：O(n)
- 空间复杂度：O(1)

这题是链表专题的核心基础，后面很多题都基于它。

## 删除节点模板

删除值等于 `val` 的节点：

```python
dummy = ListNode(0)
dummy.next = head

prev = dummy
curr = head

while curr:
    if curr.val == val:
        prev.next = curr.next
    else:
        prev = curr

    curr = curr.next

return dummy.next
```

注意：

```python
if curr.val == val:
    prev.next = curr.next
```

删除时 `prev` 不动。

因为新的 `prev.next` 可能仍然是要删除的节点。

例如：

```text
1 -> 1 -> 1
```

删除第一个 `1` 后，`prev` 还应该停在 dummy，继续检查新的 `prev.next`。

## 快慢指针

链表里的快慢指针很常见。

模板：

```python
slow = head
fast = head

while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
```

含义：

- `slow` 每次走一步
- `fast` 每次走两步

常用于：

- 找中点
- 判断是否有环
- 找环入口
- 删除倒数第 n 个节点
- 回文链表

## 找链表中点

模板：

```python
slow = head
fast = head

while fast and fast.next:
    slow = slow.next
    fast = fast.next.next

return slow
```

对于：

```text
1 -> 2 -> 3 -> 4 -> 5
```

返回 `3`。

对于：

```text
1 -> 2 -> 3 -> 4
```

返回第二个中点 `3`。

如果想返回第一个中点，可以改成：

```python
while fast.next and fast.next.next:
```

中点题要先确认题目需要第一个中点还是第二个中点。

## 判断链表是否有环

141. Linked List Cycle

```python
class Solution:
    def hasCycle(self, head: ListNode | None) -> bool:
        slow = head
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False
```

如果没有环，`fast` 会走到 `None`。

如果有环，`fast` 会在环里追上 `slow`。

## 找环入口

142. Linked List Cycle II

步骤：

1. 用 `slow` / `fast` 判断是否相遇。
2. 相遇后，让一个指针回到 `head`。
3. 两个指针每次都走一步。
4. 再次相遇的位置就是环入口。

代码：

```python
class Solution:
    def detectCycle(self, head: ListNode | None) -> ListNode | None:
        slow = head
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                pointer = head

                while pointer != slow:
                    pointer = pointer.next
                    slow = slow.next

                return pointer

        return None
```

### 数学证明

设：

```text
a = 从 head 到环入口的距离
b = 从环入口到第一次相遇点的距离
c = 环的总长度
```

那么从相遇点继续走到环入口的距离是：

```text
c - b
```

第一次相遇时，`slow` 走了：

```text
a + b
```

因为 `fast` 每次走两步，所以 `fast` 走了：

```text
2(a + b)
```

它们在同一个节点相遇，说明 `fast` 比 `slow` 多走的路程正好是环长度的整数倍：

```text
2(a + b) - (a + b) = k c
```

化简：

```text
a + b = k c
```

所以：

```text
a = k c - b
a = (k - 1)c + (c - b)
```

其中：

```text
c - b = 从相遇点走到环入口的距离
```

这说明：

```text
从 head 出发走 a 步，会到环入口。
从相遇点出发走 a 步，也会到环入口。
```

因为从相遇点出发走 `c - b` 步先到环入口，剩下的 `(k - 1)c` 步只是绕完整圈。

所以第一次相遇后：

```python
pointer = head

while pointer != slow:
    pointer = pointer.next
    slow = slow.next
```

两个指针最终一定会在环入口相遇。

## 删除倒数第 n 个节点

19. Remove Nth Node From End of List

核心：

1. 让 `fast` 先走 `n` 步。
2. 然后 `slow` 和 `fast` 一起走。
3. 当 `fast` 到尾部时，`slow` 正好在要删除节点的前一个位置。

因为可能删除 `head`，所以用 dummy。

```python
class Solution:
    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        dummy = ListNode(0)
        dummy.next = head

        slow = dummy
        fast = dummy

        for _ in range(n):
            fast = fast.next

        while fast.next:
            slow = slow.next
            fast = fast.next

        slow.next = slow.next.next

        return dummy.next
```

这里用：

```python
while fast.next:
```

是为了让循环结束时，`slow.next` 正好是要删除的节点。

## 合并两个有序链表

21. Merge Two Sorted Lists

这是 dummy 构造新链表的典型题。

```python
class Solution:
    def mergeTwoLists(
        self, list1: ListNode | None, list2: ListNode | None
    ) -> ListNode | None:
        dummy = ListNode(0)
        curr = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                curr.next = list1
                list1 = list1.next
            else:
                curr.next = list2
                list2 = list2.next

            curr = curr.next

        if list1:
            curr.next = list1
        else:
            curr.next = list2

        return dummy.next
```

核心：

- `curr` 永远指向新链表的尾巴
- 每次接一个更小的节点
- 最后把剩余链表接上

## 回文链表

234. Palindrome Linked List

核心步骤：

1. 快慢指针找中点。
2. 反转后半段。
3. 从头和后半段逐个比较。

```python
class Solution:
    def isPalindrome(self, head: ListNode | None) -> bool:
        if not head or not head.next:
            return True

        slow = head
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        prev = None
        curr = slow

        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        left = head
        right = prev

        while right:
            if left.val != right.val:
                return False
            left = left.next
            right = right.next

        return True
```

这题不一定需要恢复链表，除非题目明确要求。

## 链表里的递归

当前阶段优先掌握迭代。

递归反转链表可以先做到能读懂：

```python
class Solution:
    def reverseList(self, head: ListNode | None) -> ListNode | None:
        if not head or not head.next:
            return head

        new_head = self.reverseList(head.next)

        head.next.next = head
        head.next = None

        return new_head
```

这版理解难度高于迭代，后面再重点补。

## 常见 bug

### 忘记保存 next

错误写法：

```python
curr.next = prev
curr = curr.next
```

这样 `curr` 会回到 `prev`，原链表后面丢了。

正确写法：

```python
nxt = curr.next
curr.next = prev
curr = nxt
```

### 返回了错误的 head

如果用了 dummy，通常返回：

```python
return dummy.next
```

如果是反转链表，返回：

```python
return prev
```

不是返回原来的 `head`。

### 删除 head 没处理

例如：

```text
1 -> 2 -> 3
```

如果要删除值为 `1` 的节点，不用 dummy 很容易漏掉头节点。

所以删除类题优先 dummy。

### `while curr.next` 和 `while curr` 混淆

如果写：

```python
while curr.next:
```

最后一个节点不会被处理。

如果要处理所有节点，用：

```python
while curr:
```

如果需要看下一个节点是否存在，用：

```python
while curr and curr.next:
```

### 链表断了

修改某个节点的 `next` 前，先问：

```text
后面的节点我有没有保存？
```

## 固定思考流程

每道链表题先问：

1. 会不会改变 `head`？
   如果会，优先 dummy。
2. 是遍历、删除、反转、合并、找中点，还是找环？
3. 需要几个指针？
   `prev / curr / nxt`、`slow / fast`、`dummy / tail`？
4. 修改 `curr.next` 前，是否保存了 `curr.next`？
5. 最后应该返回谁？
   `head`、`dummy.next`、`prev`、还是 `new_head`？

## 题型地图

### A. 基础遍历 / 删除

代表题：

- 203. Remove Linked List Elements
- 83. Remove Duplicates from Sorted List
- 82. Remove Duplicates from Sorted List II

重点：

- dummy
- `prev / curr`
- 删除节点时 `prev` 是否移动

### B. 反转链表

代表题：

- 206. Reverse Linked List
- 92. Reverse Linked List II
- 25. Reverse Nodes in k-Group
- 24. Swap Nodes in Pairs

重点：

- 保存 `next`
- 改变 `curr.next`
- 返回新的 `head`

92. Reverse Linked List II 是局部反转链表。

如果反转区间是：

```text
A -> B -> C -> D -> None
```

反转结束后：

```text
D -> C -> B -> A -> None
```

此时：

```text
prev = D
curr = None
原来的头 A 变成反转后的尾巴
```

所以在局部反转中要提前保存：

```python
node_before_left
node_left
right_node
node_after_right
```

反转后接回原链表：

```python
node_before_left.next = prev
node_left.next = node_after_right
```

不能用 `curr.next = node_after_right`，因为反转结束时 `curr` 已经是 `None`。

### C. 快慢指针

代表题：

- 141. Linked List Cycle
- 142. Linked List Cycle II
- 876. Middle of the Linked List
- 19. Remove Nth Node From End of List
- 234. Palindrome Linked List
- 287. Find the Duplicate Number

重点：

- `fast` 每次两步
- `slow` 每次一步
- `while fast and fast.next`

287. Find the Duplicate Number 虽然输入是数组，但可以把数组看成隐式链表。

如果题目给出：

```text
nums[i] 在 1..len(nums) - 1 范围内
```

那么 `nums[i]` 可以当作下一个下标：

```python
next_index = nums[index]
```

这就相当于链表里的：

```python
node = node.next
```

重复值会让两个位置指向同一个下标，从而形成环。

重复数字本身就是这个环的入口。

所以可以用 Floyd 快慢指针：

```python
slow = nums[slow]
fast = nums[nums[fast]]
```

第二阶段从 `0` 和相遇点同时出发，最后相遇的位置就是重复数字。

### D. 合并链表

代表题：

- 21. Merge Two Sorted Lists
- 23. Merge k Sorted Lists
- 2. Add Two Numbers
- 445. Add Two Numbers II

重点：

- dummy + tail
- 构造新链表
- 处理 carry

2. Add Two Numbers 是 dummy 构造新链表 + `carry`。

因为题目给的是倒序存储：

```text
个位 -> 十位 -> 百位
```

所以可以从链表头部开始直接相加。

每一轮：

```python
total = val1 + val2 + carry
carry = total // 10
digit = total % 10
```

循环条件要保留 `carry`：

```python
while l1 or l2 or carry:
```

如果数字是正序存储，进位方向和遍历方向相反，就会麻烦很多，通常要用栈或先反转链表。

### E. 复杂指针 / 哈希表

代表题：

- 138. Copy List with Random Pointer
- 160. Intersection of Two Linked Lists

重点：

- HashMap 映射原节点到新节点
- 双指针同步长度差

138. Copy List with Random Pointer 可以用两遍遍历：

1. 第一遍复制所有节点，建立 `old_node -> new_node` 的映射。
2. 第二遍根据映射补上新节点的 `next` 和 `random`。

常用初始化：

```python
old_to_new = {None: None}
```

这样当 `curr.next` 或 `curr.random` 是 `None` 时，也可以直接写：

```python
old_to_new[curr].next = old_to_new[curr.next]
old_to_new[curr].random = old_to_new[curr.random]
```

不用额外判断空指针。

## 推荐刷题顺序

1. 206. Reverse Linked List
2. 21. Merge Two Sorted Lists
3. 203. Remove Linked List Elements
4. 83. Remove Duplicates from Sorted List
5. 876. Middle of the Linked List
6. 141. Linked List Cycle
7. 19. Remove Nth Node From End of List
8. 234. Palindrome Linked List
9. 2. Add Two Numbers
10. 160. Intersection of Two Linked Lists
11. 24. Swap Nodes in Pairs
12. 92. Reverse Linked List II
13. 142. Linked List Cycle II
14. 138. Copy List with Random Pointer
15. 25. Reverse Nodes in k-Group

前 8 题是基础核心。

9 到 13 是 Medium 主线。

14 和 15 难度更高，后面再做。

## 必背模板

### 模板 1：普通遍历

```python
curr = head

while curr:
    # process curr
    curr = curr.next
```

### 模板 2：dummy 删除

```python
dummy = ListNode(0)
dummy.next = head

prev = dummy
curr = head

while curr:
    if should_delete(curr):
        prev.next = curr.next
    else:
        prev = curr

    curr = curr.next

return dummy.next
```

### 模板 3：反转链表

```python
prev = None
curr = head

while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt

return prev
```

### 模板 4：快慢指针

```python
slow = head
fast = head

while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
```

### 模板 5：dummy 构造新链表

```python
dummy = ListNode(0)
tail = dummy

while condition:
    tail.next = some_node
    tail = tail.next

return dummy.next
```

## 当前学习目标

现在进入链表专题，先不要追 Hard。

当前目标是：

1. 能熟练画出节点变化。
2. 能稳定写出反转链表。
3. 能知道什么时候用 dummy。
4. 能区分 `prev / curr / next`。
5. 能写快慢指针。
6. 能处理 `head` 被删除或改变的情况。
7. 能解释最后为什么返回 `dummy.next` / `prev`。

最关键的一句话：

```text
链表题必须画图。
```

尤其是反转、交换、删除、局部反转题，不画图很容易乱。

第一题建议从：

```text
206. Reverse Linked List
```

开始。
