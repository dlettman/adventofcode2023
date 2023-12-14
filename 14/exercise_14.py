import time
from functools import cache

import pyperclip
from numpy import add

from helpers import helpers

N = (0, -1)


def rotate_map(map):
    rotated = tuple(
        [tuple([line[n] for line in map[::-1]]) for n in range(len(map[0]))]
    )
    return rotated


@cache
def slide_rocks(map, direction=N):
    for y, row in enumerate(map):
        new_map = [list(item) for item in map]
        for x, char in enumerate(row):
            if char == "O":
                coord = (x, y)
                while True:
                    new_coord = tuple(add(coord, direction))
                    if (not helpers.out_of_bounds(new_coord, map)) and (
                        map[new_coord[1]][new_coord[0]] == "."
                    ):
                        new_map[new_coord[1]][new_coord[0]] = "O"
                        new_map[coord[1]][coord[0]] = "."
                        coord = new_coord
                    else:
                        break
        map = new_map
    return tuple([tuple(item) for item in map])


def part_one(input_filename):
    score = 0
    input = helpers.parse_input(input_filename)
    map = tuple([tuple(item) for item in input])
    map = slide_rocks(map, N)
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == "O":
                score += len(map) - y
    return score


def part_two_cyclo_mode(input_filename):
    input = helpers.parse_input(input_filename)
    map = tuple([tuple(item) for item in input])
    state_cache = {}
    offset = None
    for n in range(1000000000):
        for _ in "NWSE":
            map = slide_rocks(map)
            map = rotate_map(map)
        if map in state_cache and len(state_cache[map]) > 1:
            cycle_time = state_cache[map][1] - state_cache[map][0]
            break
        if map in state_cache:
            if not offset:
                offset = n
            state_cache[map].append((n + 1))  # start after round 1
        elif not map in state_cache:
            state_cache[map] = [(n + 1)]  # start after round 1
    offset = offset - cycle_time
    remainder = ((1000000000 - 1) - offset) % cycle_time
    for n in range(remainder):
        for _ in ["N", "W", "S", "E"]:
            map = slide_rocks(map)
            map = rotate_map(map)
    score = 0
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == "O":
                score += len(map) - y
    return score


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    onestart = time.time()
    p1result = part_one("input.txt")
    oneend = time.time()
    print(f"REAL RESULT = {p1result}")
    print(f"Time = {oneend - onestart}")
    print("\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two_cyclo_mode('inputtest.txt')}\n")
    twostart = time.time()
    p2result = part_two_cyclo_mode("input.txt")
    twoend = time.time()
    print(f"REAL RESULT = {p2result}")
    print(f"Time = {twoend - twostart}")
    if p1result:
        pyperclip.copy(p1result)
    elif p2result:
        pyperclip.copy(p2result)
