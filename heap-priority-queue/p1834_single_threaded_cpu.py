from __future__ import annotations

import heapq


class Solution:
    def getOrder(self, tasks: list[list[int]]) -> list[int]:
        ordered_tasks = sorted(
            (enqueue_time, processing_time, index)
            for index, (enqueue_time, processing_time) in enumerate(tasks)
        )

        available_tasks: list[tuple[int, int]] = []
        answer: list[int] = []
        time = 0
        next_task = 0

        while next_task < len(ordered_tasks) or available_tasks:
            if not available_tasks and time < ordered_tasks[next_task][0]:
                time = ordered_tasks[next_task][0]

            while (
                next_task < len(ordered_tasks)
                and ordered_tasks[next_task][0] <= time
            ):
                _, processing_time, index = ordered_tasks[next_task]
                heapq.heappush(available_tasks, (processing_time, index))
                next_task += 1

            processing_time, index = heapq.heappop(available_tasks)
            time += processing_time
            answer.append(index)

        return answer


class DoubleHeapSolution:
    def getOrder(self, tasks: list[list[int]]) -> list[int]:
        arrival_heap = [
            (enqueue_time, index)
            for index, (enqueue_time, _) in enumerate(tasks)
        ]
        heapq.heapify(arrival_heap)

        available_tasks: list[tuple[int, int]] = []
        answer: list[int] = []
        time = 0

        while arrival_heap or available_tasks:
            if not available_tasks:
                time = max(time, arrival_heap[0][0])

            while arrival_heap and arrival_heap[0][0] <= time:
                _, index = heapq.heappop(arrival_heap)
                heapq.heappush(available_tasks, (tasks[index][1], index))

            processing_time, index = heapq.heappop(available_tasks)
            time += processing_time
            answer.append(index)

        return answer


if __name__ == "__main__":
    test_cases = [
        (
            [[1, 2], [2, 4], [3, 2], [4, 1]],
            [0, 2, 3, 1],
        ),
        (
            [[7, 10], [7, 12], [7, 5], [7, 4], [7, 2]],
            [4, 3, 2, 0, 1],
        ),
        (
            [[1_000_000_000, 1], [1, 2]],
            [1, 0],
        ),
        (
            [[1, 10], [1, 10], [1, 1]],
            [2, 0, 1],
        ),
    ]

    for solution in (Solution(), DoubleHeapSolution()):
        for task_list, expected in test_cases:
            assert solution.getOrder(task_list) == expected

    print("All examples passed.")
