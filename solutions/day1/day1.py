import heapq
import math
from pathlib import Path
from aoc_utils import loader

if __name__ == "__main__":
    p = Path(__file__).parent / "input.txt"
    
    running_total = 0
    max_cals = -math.inf
    for line in loader.load_per_line(p):
        if line == "":
            max_cals = max(max_cals, running_total)
            running_total = 0
        else:
            running_total += int(line)

    print(max_cals)

    calories = []
    heapq.heapify(calories)
    total = 0

    for line in loader.load_per_line(p):
        if line == "":
            heapq.heappush(calories, total)
            if len(calories) > 3:
                heapq.heappop(calories)
            total = 0
        else:
            total += int(line)

    print(sum(calories))
    # calories.sort(reverse=True)
    # print(sum(calories[:3]))

    
