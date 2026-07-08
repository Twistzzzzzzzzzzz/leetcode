from __future__ import annotations


class ListNode:
    def __init__(self, x: int) -> None:
        self.val = x
        self.next: ListNode | None = None


class Solution:
    def hasCycle(self, head: ListNode | None) -> bool:
        fast = head
        slow = head

        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next

            if fast == slow:
                return True

        return False


def build_linked_list(values: list[int]) -> ListNode | None:
    dummy = ListNode(0)
    curr = dummy

    for value in values:
        curr.next = ListNode(value)
        curr = curr.next

    return dummy.next


def build_cycle_list(values: list[int], pos: int) -> ListNode | None:
    dummy = ListNode(0)
    curr = dummy
    cycle_entry = None

    for index, value in enumerate(values):
        curr.next = ListNode(value)
        curr = curr.next

        if index == pos:
            cycle_entry = curr

    if pos != -1:
        curr.next = cycle_entry

    return dummy.next


if __name__ == "__main__":
    solution = Solution()

    assert solution.hasCycle(build_cycle_list([3, 2, 0, -4], 1)) is True
    assert solution.hasCycle(build_cycle_list([1, 2], 0)) is True
    assert solution.hasCycle(build_cycle_list([1], -1)) is False
    assert solution.hasCycle(build_linked_list([])) is False

    print("All examples passed.")
