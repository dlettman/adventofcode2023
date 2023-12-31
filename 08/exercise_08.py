import math
from itertools import cycle

import pyperclip

from helpers import helpers


def parse_map(map_lines):
    mappings = {}
    for line in map_lines:
        source, dests = line.split(" = ")
        l_dest, r_dest = [item.strip("()") for item in dests.split(", ")]
        mappings[source] = {"L": l_dest, "R": r_dest}
    return mappings


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    directions = cycle(puzzle_input[0])
    mappings = parse_map(puzzle_input[2:])
    score = 0
    current_location = "AAA"
    while current_location != "ZZZ":
        direction = next(directions)
        current_location = mappings[current_location][direction]
        score += 1
    return score


def check_locations(locations):
    for location in locations:
        if location[-1] != "Z":
            return False
    return True


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    directions = cycle(puzzle_input[0])
    mappings = parse_map(puzzle_input[2:])
    score = 0
    current_locations = [location for location in mappings if location[-1] == "A"]
    cycles = {n: [] for n in range(len(current_locations))}
    while not check_locations(current_locations):
        new_locations = []
        direction = next(directions)
        for idx, location in enumerate(current_locations):
            if check_locations([location]):
                cycles[idx].append(score)
            new_locations.append(mappings[location][direction])
        score += 1
        current_locations = new_locations
        if all(cycles.values()):
            break
    return math.lcm(*[v[0] for v in cycles.values()])


if __name__ == "__main__":
    helpers.display_outupt(
        part1_func=part_one,
        part1_test=True,
        part1=True,
        part2_func=part_two,
        part2_test=True,
        part2=True,
    )
