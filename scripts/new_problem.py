from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
    return slug or "problem"


def method_name(title: str) -> str:
    parts = slugify(title).split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


def build_solution(number: int, title: str, method: str) -> str:
    return f'''from __future__ import annotations


class Solution:
    """{number}. {title}

    Time: TODO
    Space: TODO
    """

    def {method}(self):
        raise NotImplementedError
'''


def build_test(difficulty: str, stem: str, method: str) -> str:
    module = f"problems.{difficulty}.{stem}"
    return f'''import pytest

from {module} import Solution


def test_{stem}_examples() -> None:
    solution = Solution()

    pytest.skip("Add example assertions for solution.{method}().")
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a LeetCode solution and test file.")
    parser.add_argument("number", type=int, help="Problem number, for example: 1")
    parser.add_argument("difficulty", choices=["easy", "medium", "hard"])
    parser.add_argument("title", help='Problem title, for example: "Two Sum"')
    parser.add_argument("--method", help="LeetCode method name, for example: twoSum")
    args = parser.parse_args()

    stem = f"p{args.number:04d}_{slugify(args.title)}"
    method = args.method or method_name(args.title)

    solution_path = ROOT / "problems" / args.difficulty / f"{stem}.py"
    test_path = ROOT / "tests" / f"test_{stem}.py"

    for path in (solution_path, test_path):
        if path.exists():
            raise FileExistsError(f"{path} already exists")

    solution_path.write_text(build_solution(args.number, args.title, method), encoding="utf-8")
    test_path.write_text(build_test(args.difficulty, stem, method), encoding="utf-8")

    print(f"Created {solution_path.relative_to(ROOT)}")
    print(f"Created {test_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

