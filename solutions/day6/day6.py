from pathlib import Path
from aoc_utils import loader


def solve_part_1(input_file: Path) -> int:
    times = []
    distances = []

    for line in loader.load_per_line(input_file):
        if line.startswith("Time"):
            for timing in line.split(':')[1].split():
                times.append(int(timing))
        else:
            for distance in line.split(':')[1].split():
                distances.append(int(distance))

    result = 1
    for time, distance in zip(times, distances):
        no_of_winning_strategies = 0
        # TODO: You only need to run half the range, it's symmetric
        for t in range(time + 1):
            distance_travelled = t * (time - t)
            if distance_travelled > distance:
                no_of_winning_strategies += 1
        
        result *= no_of_winning_strategies
    
    return result


def solve_part_2(input_file: Path) -> int:
    for line in loader.load_per_line(input_file):
        if line.startswith("Time"):
            time = int(line.split(':')[1].replace(" ", ""))
        else:
            distance = int(line.split(':')[1].replace(" ", ""))

    no_of_winning_strategies = 0
    # TODO: You only need to run half the range, it's symmetric
    for t in range(time + 1):
        distance_travelled = t * (time - t)
        if distance_travelled > distance:
            no_of_winning_strategies += 1


    return no_of_winning_strategies


if __name__ == "__main__":
    p = Path(__file__).parent / "input.txt"

    result = solve_part_1(p)
    print(result)

    p = Path(__file__).parent / "input.txt"

    result = solve_part_2(p)
    print(result)
