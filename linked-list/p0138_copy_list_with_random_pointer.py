from __future__ import annotations


class Node:
    def __init__(
        self,
        x: int,
        next: Node | None = None,
        random: Node | None = None,
    ) -> None:
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: Node | None) -> Node | None:
        old_to_new: dict[Node | None, Node | None] = {None: None}

        curr = head
        while curr:
            old_to_new[curr] = Node(curr.val)
            curr = curr.next

        curr = head
        while curr:
            old_to_new[curr].next = old_to_new[curr.next]
            old_to_new[curr].random = old_to_new[curr.random]
            curr = curr.next

        return old_to_new[head]


def build_random_list(values: list[list[int | None]]) -> Node | None:
    if not values:
        return None

    nodes = [Node(value) for value, _ in values]

    for index, node in enumerate(nodes):
        if index + 1 < len(nodes):
            node.next = nodes[index + 1]

        random_index = values[index][1]
        if random_index is not None:
            node.random = nodes[random_index]

    return nodes[0]


def collect_nodes(head: Node | None) -> list[Node]:
    nodes = []
    curr = head

    while curr:
        nodes.append(curr)
        curr = curr.next

    return nodes


def random_list_to_list(head: Node | None) -> list[list[int | None]]:
    nodes = collect_nodes(head)
    index_by_node = {node: index for index, node in enumerate(nodes)}
    result = []

    for node in nodes:
        random_index = index_by_node.get(node.random)
        result.append([node.val, random_index])

    return result


if __name__ == "__main__":
    solution = Solution()

    head = build_random_list([[7, None], [13, 0], [11, 4], [10, 2], [1, 0]])
    copied = solution.copyRandomList(head)
    assert random_list_to_list(copied) == [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]

    original_nodes = collect_nodes(head)
    copied_nodes = collect_nodes(copied)
    assert len(original_nodes) == len(copied_nodes)
    assert all(old is not new for old, new in zip(original_nodes, copied_nodes))

    head = build_random_list([[1, 1], [2, 1]])
    copied = solution.copyRandomList(head)
    assert random_list_to_list(copied) == [[1, 1], [2, 1]]

    assert solution.copyRandomList(None) is None

    print("All examples passed.")
