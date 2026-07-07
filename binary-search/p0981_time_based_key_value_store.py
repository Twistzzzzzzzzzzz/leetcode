from __future__ import annotations


class TimeMap:
    def __init__(self) -> None:
        self.data: dict[str, list[tuple[int, str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.data:
            self.data[key] = []

        self.data[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.data:
            return ""

        values = self.data[key]
        index = self._last_timestamp_not_after(values, timestamp)

        if index < 0:
            return ""

        return values[index][1]

    def _last_timestamp_not_after(
        self, values: list[tuple[int, str]], timestamp: int
    ) -> int:
        left = 0
        right = len(values)

        while left < right:
            mid = (left + right) // 2

            if values[mid][0] <= timestamp:
                left = mid + 1
            else:
                right = mid

        return left - 1


if __name__ == "__main__":
    time_map = TimeMap()

    time_map.set("foo", "bar", 1)
    assert time_map.get("foo", 1) == "bar"
    assert time_map.get("foo", 3) == "bar"

    time_map.set("foo", "bar2", 4)
    assert time_map.get("foo", 4) == "bar2"
    assert time_map.get("foo", 5) == "bar2"
    assert time_map.get("foo", 0) == ""
    assert time_map.get("missing", 10) == ""

    time_map.set("love", "high", 10)
    time_map.set("love", "low", 20)
    assert time_map.get("love", 5) == ""
    assert time_map.get("love", 10) == "high"
    assert time_map.get("love", 15) == "high"
    assert time_map.get("love", 20) == "low"
    assert time_map.get("love", 25) == "low"

    print("All examples passed.")
