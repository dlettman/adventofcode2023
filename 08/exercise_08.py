import math
import sys

sys.path.append("..")
from helpers import helpers
import pyperclip
from itertools import cycle


def parse_map(map_lines):
    map = {}
    for line in map_lines:
        source, dests = line.split(" = ")
        l_dest, r_dest = [item.strip("()") for item in dests.split(", ")]
        map[source] = {"L": l_dest, "R": r_dest}
    return map


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    directions = cycle(input[0])
    map = parse_map(input[2:])
    score = 0
    current_location = "AAA"
    while current_location != "ZZZ":
        direction = next(directions)
        current_location = map[current_location][direction]
        score += 1
    return score


def check_locations(locations):
    for location in locations:
        if location[-1] != "Z":
            return False
    return True


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    directions = cycle(input[0])
    map = parse_map(input[2:])
    score = 0
    current_locations = [location for location in map if location[-1] == "A"]
    cycles = {n: [] for n in range(len(current_locations))}
    while not check_locations(current_locations):
        new_locations = []
        direction = next(directions)
        for idx, location in enumerate(current_locations):
            if check_locations([location]):
                cycles[idx].append(score)
            new_locations.append(map[location][direction])
        score += 1
        current_locations = new_locations
        if all(cycles.values()):
            break
    return math.lcm(*[v[0] for v in cycles.values()])


if __name__ == "__main__":
    # print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    p1result = part_one("input.txt")
    print(f"REAL RESULT = {p1result}\n\n")
    # print("*** PART TWO ***\n")
    # print(f"Test result = {part_two('inputtest.txt')}\n")
    p2result = part_two("input.txt")
    print(f"REAL RESULT = {p2result}")
    if p2result:
        pyperclip.copy(p2result)
    elif p1result:
        pyperclip.copy(p1result)
