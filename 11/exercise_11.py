import time

import pyperclip

from helpers import helpers


def get_manhattan_distance(a, b):
    return sum(abs(val1 - val2) for val1, val2 in zip(a, b))


def get_empty_rows(map):
    empty_rows = []
    empty_colums = []
    for y, row in enumerate(map):
        if not "#" in row:
            empty_rows.append(y)
    for x in range(len(map[0])):
        if not "#" in [row[x] for row in map]:
            empty_colums.append(x)
    return empty_colums, empty_rows


def expansion_coordinate(coordinate, empty_columns, empty_rows, expansion_factor=1):
    new_x = coordinate[0] + sum(
        [expansion_factor for n in empty_columns if n < coordinate[0]]
    )
    new_y = coordinate[1] + sum(
        [expansion_factor for n in empty_rows if n < coordinate[1]]
    )
    return (new_x, new_y)


def parse_grid(map, empty_columns, empty_rows, expansion_factor=1):
    galaxy_coords = []
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == "#":
                galaxy_coords.append(
                    expansion_coordinate(
                        (x, y), empty_columns, empty_rows, expansion_factor
                    )
                )
    return galaxy_coords


def get_pair_distances(galaxies):
    pairs_distances = []
    for n1, galaxy1 in enumerate(galaxies):
        for n2, galaxy2 in enumerate(galaxies[n1 + 1 :]):
            pairs_distances.append(get_manhattan_distance(galaxy1, galaxy2))
    return pairs_distances


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    empty_columns, empty_rows = get_empty_rows(puzzle_input)
    galaxies = parse_grid(puzzle_input, empty_columns, empty_rows)
    distances = get_pair_distances(galaxies)
    return sum(distances)


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    empty_columns, empty_rows = get_empty_rows(puzzle_input)
    galaxies = parse_grid(puzzle_input, empty_columns, empty_rows, expansion_factor=(999999))
    distances = get_pair_distances(galaxies)
    return sum(distances)


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
    print(f"Test result = {part_two('inputtest.txt')}\n")
    twostart = time.time()
    p2result = part_two("input.txt")
    twoend = time.time()
    print(f"REAL RESULT = {p2result}")
    print(f"Time = {twoend - twostart}")
    if p1result:
        pyperclip.copy(p1result)
    elif p2result:
        pyperclip.copy(p2result)
