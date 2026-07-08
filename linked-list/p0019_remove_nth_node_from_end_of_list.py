from __future__ import annotations


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        dummy = ListNode(0)
        dummy.next = head

        slow = dummy
        fast = dummy

        for _ in range(n):
            fast = fast.next

        while fast.next:
            fast = fast.next
            slow = slow.next

        slow.next = slow.next.next

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

    head = build_linked_list([1, 2, 3, 4, 5])
    assert linked_list_to_list(solution.removeNthFromEnd(head, 2)) == [1, 2, 3, 5]

    head = build_linked_list([1])
    assert linked_list_to_list(solution.removeNthFromEnd(head, 1)) == []

    head = build_linked_list([1, 2])
    assert linked_list_to_list(solution.removeNthFromEnd(head, 1)) == [1]

    head = build_linked_list([1, 2])
    assert linked_list_to_list(solution.removeNthFromEnd(head, 2)) == [2]

    print("All examples passed.")
