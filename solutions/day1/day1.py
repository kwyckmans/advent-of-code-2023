from pathlib import Path
from aoc_utils import loader

digits = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

def find_calibration_values(s: str) -> int:
    digits = [c for c in s if c.isdigit()]
    return int(digits[0] + digits[-1])

def find_calibration_values_with_text(s: str) -> int:
    first_idx = 10000
    last_idx = -1
    for i, c in enumerate(s):
        if c.isdigit():
            first_idx = min(first_idx, i)
            last_idx = max(last_idx, i)

    lowest_digit = s[first_idx] if first_idx < 10000 else 10000
    highest_digit = s[last_idx] if last_idx >= 0 else -1

    for key, val in digits.items():
        idx = s.find(key)
        ridx = s.rfind(key)
        if idx > -1 and idx < first_idx:
            first_idx = idx
            lowest_digit = val
        
        if ridx != -1 and ridx  > last_idx:
            last_idx = ridx 
            highest_digit = val

    return int(str(lowest_digit) + str(highest_digit))

if __name__ == "__main__":
    p = Path(__file__).parent / "input.txt"
    result = sum(list(map(find_calibration_values ,loader.load_per_line(p))))
    print(result)

    result = sum(list(map(find_calibration_values_with_text, loader.load_per_line(p))))
    print(result)

