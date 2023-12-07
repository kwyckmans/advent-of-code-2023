from dataclasses import dataclass, field
from functools import cache
import math
from pathlib import Path
from typing import List, Optional, Tuple
from aoc_utils import loader


@dataclass
class Mapping:
    start_indices: List[int] = field(default_factory=list)
    dest_indices: List[int] = field(default_factory=list)
    range_lengths: List[int] = field(default_factory=list)
    next_map: Optional[str] = None

    def add(self, source_idx, dest_idx, range_len):
        self.start_indices.append(source_idx)
        self.dest_indices.append(dest_idx)
        self.range_lengths.append(range_len)

    def get_dest(self, source_id):
        for i in range(len(self.start_indices)):
            if (
                self.start_indices[i]
                <= source_id
                < self.start_indices[i] + self.range_lengths[i]
            ):
                dest = self.dest_indices[i] + (source_id - self.start_indices[i])
                return dest

        return source_id


MAPPINGS = {}


@cache
def find_mapping_from_seed_to_location_number(seed_id: int) -> int:
    soil_id = MAPPINGS["seed-to-soil"].get_dest(seed_id)
    fertilizer_id = MAPPINGS["soil-to-fertilizer"].get_dest(soil_id)
    water_id = MAPPINGS["fertilizer-to-water"].get_dest(fertilizer_id)
    light_id = MAPPINGS["water-to-light"].get_dest(water_id)
    temperature_id = MAPPINGS["light-to-temperature"].get_dest(light_id)
    humidity_id = MAPPINGS["temperature-to-humidity"].get_dest(temperature_id)
    location_id = MAPPINGS["humidity-to-location"].get_dest(humidity_id)

    # print(f"seed {seed_id} to soil {soil_id} to fertilizer {fertilizer_id} to water {water_id} to light {light_id}")
    return location_id


def solve_part_1(input_file: Path) -> int:
    seeds_to_be_planted = []
    # MAPPINGS = {}
    for block in loader.load_per_newline_block(input_file):
        # print(block)
        if block.startswith("seeds"):
            seeds_to_be_planted = [int(i) for i in block.split(":")[1].split()]
        else:
            lines = block.strip().split("\n")

            map_name = lines[0].split()[0]
            mapping = None
            match map_name:
                case "seed-to-soil":
                    mapping = Mapping(next_map="soil-to-fertilizer")
                case "soil-to-fertilizer":
                    mapping = Mapping(next_map="fertilizer-to-water")
                case "fertilizer-to-water":
                    mapping = Mapping(next_map="water-to-light")
                case "water-to-light":
                    mapping = Mapping(next_map="light-to-temperature")
                case "light-to-temperature":
                    mapping = Mapping(next_map="temperature-to-humidity")
                case "temperature-to-humidity":
                    mapping = Mapping(next_map="humidity-to-location")
                case "humidity-to-location":
                    mapping = Mapping(next_map=None)

            for idx in range(1, len(lines)):
                dest_start, source_start, range_len = [
                    int(i) for i in lines[idx].split()
                ]
                mapping.add(source_start, dest_start, range_len)

            MAPPINGS[map_name] = mapping

    lowest_location = math.inf
    for seed_id in seeds_to_be_planted:
        lowest_location = min(
            lowest_location, find_mapping_from_seed_to_location_number(seed_id)
        )

    return lowest_location


def merge_intervals(intervals):
    merged = []

    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])

    return merged


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


mappers = []


def map_seed(seed: int) -> Tuple[int, int]:
    global mappers

    step = math.inf
    for mapper in mappers:
        was_mapped = False
        for src, dest, count in mapper:
            # Loop over all intervals in this mapper, to see if we find a match
            # Stop looping this specific mapper if one is found. Replace the old id with
            #  its match, and go to the next mapper.
            if seed >= src and seed < src + count:
                # print(f"We found a match for {seed} in the {src, dest, count} interval")
                # All entries remaining in this interval will map to a larger number
                step = min(step, src + count - seed)
                seed = dest + seed - src
                # print(f"step: {step}, new seed: {seed}")
                was_mapped = True
                break
        if not was_mapped:
            # We have an idx that didn't have a match in this mapping layer
            # We don't have to update our seed index, but we may need 
            # to reduce the amount of seeds we skip.
            #
            # Say we have id 10, and the interval in this mapping level starts at 14,
            # all seed_ids between 10 and 14 will be larger.
            # print(f"We couldn't map {seed} in {mapper}")
            closest = math.inf
            for src, dest, count in mapper:
                # print(f"Comparing interval starts {src} to current idx: {seed}")
                if src > seed:
                    closest = min(closest, src - seed)
                    # print(f"Closest match is {closest}")
            # print(f"We can jump {step} seeds")
            step = min(step, closest)
    return seed, step


def solve_part_2(input_file: Path) -> int:
    seeds_to_be_planted = []
    for block in loader.load_per_newline_block(input_file):
        if block.startswith("seeds"):
            seeds_to_be_planted = [int(i) for i in block.split(":")[1].split()]
        else:
            lines = block.strip().split("\n")
            interval = []
            for idx in range(1, len(lines)):
                dest_start, source_start, range_len = [
                    int(i) for i in lines[idx].split()
                ]
                interval.append((source_start, dest_start, range_len))

            mappers.append(interval)
    # print(mappers)

    best_location = math.inf
    for seed, seed_count in pairwise(seeds_to_be_planted):
        # print(seed, seed_count)
        cur_seed = seed
        while cur_seed < seed + seed_count:
            # print(f"Looking at {cur_seed}")
            location, step = map_seed(cur_seed)
            best_location = min(location, best_location)
            cur_seed += step

    return best_location


if __name__ == "__main__":
    p = Path(__file__).parent / "input.txt"

    result = solve_part_1(p)
    print(result)

    p = Path(__file__).parent / "input.txt"

    result = solve_part_2(p)
    print(result)
