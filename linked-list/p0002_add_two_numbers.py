from __future__ import annotations


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next


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


def build_linked_list(values: list[int]) -> ListNode | None:
    dummy = ListNode(0)
    curr = dummy

    for value in values:
        curr.next = ListNode(value)
        curr = curr.next

    return dummy.next


def linked_list_to_list(head: ListNode | None) -> list[int]:
    values = []
    curr = head

    while curr:
        values.append(curr.val)
        curr = curr.next

    return values


if __name__ == "__main__":
    solution = Solution()

    result = solution.addTwoNumbers(build_linked_list([2, 4, 3]), build_linked_list([5, 6, 4]))
    assert linked_list_to_list(result) == [7, 0, 8]

    result = solution.addTwoNumbers(build_linked_list([0]), build_linked_list([0]))
    assert linked_list_to_list(result) == [0]

    result = solution.addTwoNumbers(
        build_linked_list([9, 9, 9, 9, 9, 9, 9]),
        build_linked_list([9, 9, 9, 9]),
    )
    assert linked_list_to_list(result) == [8, 9, 9, 9, 0, 0, 0, 1]

    print("All examples passed.")
