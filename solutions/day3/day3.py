from dataclasses import dataclass
from pathlib import Path
from aoc_utils import loader


if __name__ == "__main__":
    p = Path(__file__).parent / "input.txt"

    print(loader.load_grid(p))
