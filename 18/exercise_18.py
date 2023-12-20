import time
from collections import deque

import pyperclip

from helpers import helpers
from helpers.helpers import Coordinate

DIRECTIONS = {
    "R": Coordinate(1, 0),
    "L": Coordinate(-1, 0),
    "U": Coordinate(0, -1),
    "D": Coordinate(0, 1),
}


def parse_input(puzzle_input):
    return [line.split() for line in puzzle_input]


def visualize_it(dug_locations, seen):
    min_x = min([coord.x for coord in dug_locations])
    min_y = min([coord.y for coord in dug_locations])
    max_x = max([coord.x for coord in dug_locations])
    max_y = max([coord.y for coord in dug_locations])
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            if Coordinate(x, y) in dug_locations and Coordinate(x, y) in seen:
                line += "!"
            elif Coordinate(x, y) in dug_locations:
                line += "#"
            elif Coordinate(x, y) in seen:
                line += "x"
            else:
                line += "."
        print(line)
    print("len seen:")
    print(len(seen))
    print("len dug locations:")
    print(len(dug_locations))
    return len(seen) + len(dug_locations)


def part_one(input_filename):  # Naive approach
    puzzle_input = helpers.parse_input(input_filename)
    parsed_input = parse_input(puzzle_input)
    digger_location = Coordinate(0, 0)
    dug_locations = {}
    for line in parsed_input:
        direction, magnitude, color = line
        for n in range(int(magnitude)):
            digger_location = digger_location + DIRECTIONS[direction]
            dug_locations[digger_location] = color
    for start_neighbor in helpers.NEIGHBORS:
        test_coordinate = Coordinate(0, 0) + start_neighbor
        if test_coordinate in dug_locations:
            continue
        else:  # do a bfs
            start = test_coordinate
            seen = set()
            queue = deque([start])
            outside = False
            found_it = True
            while queue:
                cur_move = queue.popleft()
                for neighbor in helpers.NEIGHBORS_ORTH:
                    if (cur_move + neighbor) in seen or (
                        cur_move + neighbor
                    ) in dug_locations:
                        continue
                    else:
                        seen.add(cur_move + neighbor)
                        queue.append(cur_move + neighbor)
                    if len(seen) > 100000:  # arbitrary break condition
                        outside = True
                        break
                if outside:
                    found_it = False
                    break
            if found_it:
                return len(seen) + len(dug_locations)
    return "dang"


HEX_DIRECTIONS = {
    "0": Coordinate(1, 0),
    "2": Coordinate(-1, 0),
    "3": Coordinate(0, -1),
    "1": Coordinate(0, 1),
}


def parse_hex(line):
    hex = line.split()[2][2:-1]
    magnitude = int(hex[0:5], 16)
    direction = HEX_DIRECTIONS[hex[5]]
    return magnitude, direction


def shoelace_formula(vertices):
    return abs(
        sum(
            (vertices[i][0] - vertices[i - 1][0])
            * (vertices[i][1] + vertices[i - 1][1])
            for i in range(1, len(vertices))
        )
        / 2
    )


def picks_theorem(int_area, ext_points):
    return int(int_area + (ext_points // 2) + 1)


def part_two(input_filename):  # Use geometry
    puzzle_input = helpers.parse_input(input_filename)
    for line in puzzle_input:
        parse_hex(line)
    digger_location = Coordinate(0, 0)
    corners = [digger_location]
    total_magnitude = 0
    for line in puzzle_input:
        magnitude, direction = parse_hex(line)
        digger_location = (
            Coordinate(direction.x * magnitude, direction.y * magnitude)
            + digger_location
        )
        corners.append(digger_location)
        total_magnitude += magnitude
    corners = [(coord.x, coord.y) for coord in corners]
    int_area = shoelace_formula(corners)
    total_area = picks_theorem(int_area, total_magnitude)
    return total_area


if __name__ == "__main__":
    helpers.display_outupt(
        part1_func=part_one,
        part1_test=True,
        part1=True,
        part2_func=part_two,
        part2_test=True,
        part2=True,
    )
