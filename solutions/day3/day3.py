from dataclasses import dataclass
from pathlib import Path
from typing import List
from aoc_utils import loader

def solve_part_1(grid: List[List[chr]]) -> int:
    for row in grid:
        for char in row:
            if char.is_digit():
                print(char)
    

if __name__ == "__main__":
    p = Path(__file__).parent / "input.txt"
    grid = loader.load_grid(p)


