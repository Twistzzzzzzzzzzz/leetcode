from __future__ import annotations


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next


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

    assert linked_list_to_list(solution.reverseList(build_linked_list([1, 2, 3, 4, 5]))) == [
        5,
        4,
        3,
        2,
        1,
    ]
    assert linked_list_to_list(solution.reverseList(build_linked_list([1, 2]))) == [2, 1]
    assert linked_list_to_list(solution.reverseList(build_linked_list([]))) == []

    print("All examples passed.")
