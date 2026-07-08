from __future__ import annotations


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next


class Solution:
    def reverseBetween(
        self, head: ListNode | None, left: int, right: int
    ) -> ListNode | None:
        if left == right:
            return head

        dummy = ListNode(0)
        dummy.next = head

        node_before_left = dummy
        for _ in range(left - 1):
            node_before_left = node_before_left.next

        right_node = dummy
        for _ in range(right):
            right_node = right_node.next

        node_left = node_before_left.next
        node_after_right = right_node.next
        right_node.next = None

        prev = None
        curr = node_left

        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        node_before_left.next = prev
        node_left.next = node_after_right

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
    assert linked_list_to_list(solution.reverseBetween(head, 2, 4)) == [1, 4, 3, 2, 5]

    head = build_linked_list([5])
    assert linked_list_to_list(solution.reverseBetween(head, 1, 1)) == [5]

    head = build_linked_list([1, 2, 3, 4, 5])
    assert linked_list_to_list(solution.reverseBetween(head, 1, 5)) == [5, 4, 3, 2, 1]

    head = build_linked_list([1, 2, 3])
    assert linked_list_to_list(solution.reverseBetween(head, 1, 2)) == [2, 1, 3]

    print("All examples passed.")
