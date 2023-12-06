from collections import defaultdict
from pathlib import Path
from typing import List, Set, Tuple
from aoc_utils import loader

def convert_input_to_winning_numbers(line: str) -> Tuple[int, Set[int], List[int]]:
    left_side, right_side = line.strip().split("|")
    numbers_i_have = [int(n) for n in right_side.split()]
    winning_numbers = set(int(n) for n in left_side.split(":")[1].split())
    card_id = int(left_side.split(":")[0].split()[1])
    return card_id, winning_numbers, numbers_i_have

def find_no_of_matches(winning_numbers: Set[int], numbers_i_have: List[int]):
    matches = 0
    for num in numbers_i_have:
        if num in winning_numbers:
            matches += 1
    
    return matches

def calculate_score(winning_numbers: Set[int], numbers_i_have: List[int]):
    no_of_matches = find_no_of_matches(winning_numbers=winning_numbers, numbers_i_have=numbers_i_have)
    return 2 ** (no_of_matches  -1) if no_of_matches > 0 else 0

def solve_part_1(input_file: Path) -> int:
    total = 0 
    for line in loader.load_per_line(input_file):
        _, winning_numbers, numbers_i_have = convert_input_to_winning_numbers(line)
        total += calculate_score(winning_numbers=winning_numbers, numbers_i_have=numbers_i_have)
        
    return total

def solve_part_2(input_file: Path) -> int:
    copies = defaultdict(int)
    
    for line in loader.load_per_line(input_file):
        card_id, winning_numbers, numbers_i_have = convert_input_to_winning_numbers(line)
        no_of_matches = find_no_of_matches(winning_numbers=winning_numbers, numbers_i_have=numbers_i_have)
        no_of_copies = copies[card_id]

        # for card 2: add copy to 3 and 4
        for card in range(card_id + 1 , card_id + no_of_matches + 1):
            # There's 2 versions of 2, the original, and the copy, so we should add to 3 and 4 twice.
            # Add a card for the original
            copies[card] = copies[card] + 1
            # Add a card for each copy.
            for _ in range(no_of_copies):
                copies[card] = copies[card] + 1

    return len(copies.keys()) + sum(copies.values())

if __name__ == "__main__":
    p = Path(__file__).parent / "input.txt"
    
    print(solve_part_1(p))
    print(solve_part_2(p))