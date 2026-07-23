from __future__ import annotations

import heapq


class Solution:
    def carPooling(self, trips: list[list[int]], capacity: int) -> bool:
        furthest_location = max((end for _, _, end in trips), default=0)
        passenger_changes = [0] * (furthest_location + 1)

        for passengers, start, end in trips:
            passenger_changes[start] += passengers
            passenger_changes[end] -= passengers

        current_passengers = 0

        for change in passenger_changes:
            current_passengers += change

            if current_passengers > capacity:
                return False

        return True


class HeapSolution:
    def carPooling(self, trips: list[list[int]], capacity: int) -> bool:
        ordered_trips = sorted(trips, key=lambda trip: trip[1])
        active_trips: list[tuple[int, int]] = []
        current_passengers = 0

        for passengers, start, end in ordered_trips:
            while active_trips and active_trips[0][0] <= start:
                _, leaving_passengers = heapq.heappop(active_trips)
                current_passengers -= leaving_passengers

            current_passengers += passengers

            if current_passengers > capacity:
                return False

            heapq.heappush(active_trips, (end, passengers))

        return True


if __name__ == "__main__":
    test_cases = [
        ([[2, 1, 5], [3, 3, 7]], 4, False),
        ([[2, 1, 5], [3, 3, 7]], 5, True),
        ([[2, 1, 5], [3, 5, 7]], 3, True),
        ([[3, 5, 7], [2, 1, 5]], 3, True),
        ([[2, 1, 5], [2, 2, 5], [4, 5, 6]], 4, True),
        ([], 1, True),
    ]

    for solution in (Solution(), HeapSolution()):
        for trips, capacity, expected in test_cases:
            assert solution.carPooling(trips, capacity) is expected

    print("All examples passed.")
