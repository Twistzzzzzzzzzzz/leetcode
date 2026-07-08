from __future__ import annotations


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next


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

    merged = solution.mergeTwoLists(build_linked_list([1, 2, 4]), build_linked_list([1, 3, 4]))
    assert linked_list_to_list(merged) == [1, 1, 2, 3, 4, 4]

    merged = solution.mergeTwoLists(build_linked_list([]), build_linked_list([]))
    assert linked_list_to_list(merged) == []

    merged = solution.mergeTwoLists(build_linked_list([]), build_linked_list([0]))
    assert linked_list_to_list(merged) == [0]

    print("All examples passed.")
