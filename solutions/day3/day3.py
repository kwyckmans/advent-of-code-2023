from collections import defaultdict
from functools import reduce
from pathlib import Path
from typing import List, Tuple
from aoc_utils import loader

# def find_part_numbers(grid, gear_row_idx, gear_col_idx) -> Tuple[int, int]:
#     no_numbers = 0
#     for row in range(gear_row_idx - 1, gear_row_idx + 2):
#         for col in range(gear_col_idx - 1, gear_col_idx + 2):
#             if row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0]) and (row != gear_row_idx and col != gear_col_idx):
                


# def surrounded_by_2_numbers(grid, gear_row_idx, gear_col_idx) -> bool:
#     no_numbers = 0
#     for row in range(gear_row_idx - 1, gear_row_idx + 2):
#         for col in range(gear_col_idx - 1, gear_col_idx + 2):
#             if row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0]) and (row != gear_row_idx and col != gear_col_idx):
#                 print(f"Checking if {row}, {col} is digit: {grid[row][col]}")
#                 if grid[row][col].isdigit():
#                     no_numbers += 1

#     return no_numbers == 2 

def compute_ratio(gears):
    total = 0
    for gear_location, numbers in gears.items():
        if len(numbers) == 2:
            total += reduce((lambda x, y: x * y), numbers)
        
    return total

def gear_locations(grid: List[List[str]], no_row_idx: int, no_start_idx: int, no_end_idx: int) -> List[Tuple[int, int]]:
    gear_locations = []
    for row in range(no_row_idx - 1, no_row_idx + 2):
        for col in range(no_start_idx - 1, no_end_idx + 1):
            if row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0]):
                # print(f"Checking for symbols at {row}, {col}: {grid[row][col]}")

                if not grid[row][col].isdigit() and grid[row][col] == '*':
                    gear_locations.append((row, col))
    
    return gear_locations

def solve_part_2(grid:List[List[str]]) -> int:
    # Keep a hasmap of gear location to numbers. 
    # If the list of numbers is exactly 2, do the calculation

    gears = defaultdict(list)

    row_idx, col_idx = 0,0 
    total = 0

    while row_idx < len(grid):
        no_start_idx, no_end_idx = col_idx, col_idx + 1

        if grid[row_idx][col_idx].isdigit():
            number = grid[row_idx][no_start_idx]
            while no_end_idx < len(grid[0]) and grid[row_idx][no_end_idx].isdigit():
                number += grid[row_idx][no_end_idx]
                no_end_idx += 1 
            
            locations = gear_locations(grid, row_idx, no_start_idx, no_end_idx)
            if locations:
                for location in locations:
                   gears[location].append(int(number))

            col_idx = no_end_idx
        else:
            col_idx = col_idx + 1
        if col_idx == len(grid[0]):
            col_idx = 0
            row_idx += 1

    return compute_ratio(gears)

def has_symbol(grid: List[List[str]], no_row_idx: int, no_start_idx: int, no_end_idx: int) -> bool:
    for row in range(no_row_idx - 1, no_row_idx + 2):
        for col in range(no_start_idx - 1, no_end_idx + 1):
            if row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0]):
                # print(f"Checking for symbols at {row}, {col}: {grid[row][col]}")

                if not grid[row][col].isdigit() and not grid[row][col] == '.':
                    return True
    
    return False

def solve_part_1(grid: List[List[str]]) -> int:
    row_idx, col_idx = 0,0 
    total = 0

    while row_idx < len(grid):
        # print(grid[row_idx][col_idx], end=" ")

        no_start_idx, no_end_idx = col_idx, col_idx + 1
        
        if grid[row_idx][col_idx].isdigit():
            number = grid[row_idx][no_start_idx]
            while no_end_idx < len(grid[0]) and grid[row_idx][no_end_idx].isdigit():
                number += grid[row_idx][no_end_idx]
                no_end_idx += 1 
            
            if has_symbol(grid, row_idx, no_start_idx, no_end_idx):
                total += int(number)

            col_idx = no_end_idx
        else:
            col_idx = col_idx + 1
        if col_idx == len(grid[0]):
            col_idx = 0
            row_idx += 1 
        
    return total

if __name__ == "__main__":
    p = Path(__file__).parent / "input.txt"
    grid = loader.load_grid(p)

    result = solve_part_1(grid=grid)
    print(result)

    result = solve_part_2(grid=grid)
    print(result)
