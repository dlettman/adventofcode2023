from typing import List

import pyperclip
from numpy import add

from helpers import helpers

CONNECTIONS = {
    "|": [(0, 1), (0, -1)],
    "-": [(1, 0), (-1, 0)],
    "L": [(0, -1), (1, 0)],
    "J": [(0, -1), (-1, 0)],
    "7": [(-1, 0), (0, 1)],
    "F": [(0, 1), (1, 0)],
    ".": [],
    "S": [],
}


def find_loop(pipes):
    for y, line in enumerate(pipes):
        for x, char in enumerate(line):
            if char == "S":
                coord = (x, y)
                break
    start_coord = coord
    pipes_seen = set(coord)
    next_steps = [([coord], add(coord, mod)) for mod in helpers.NEIGHBORS_ORTH]
    while next_steps:
        step = next_steps.pop()
        coord = step[1]
        if helpers.out_of_bounds(coord, pipes) or pipes[coord[1]][coord[0]] == ".":
            continue  # path dies
        else:
            new_char = pipes[coord[1]][coord[0]]
            for new_coord in [tuple(add(coord, mod)) for mod in CONNECTIONS[new_char]]:
                if pipes[new_coord[1]][new_coord[0]] == "S" and (len(step[0]) > 1):
                    step[0] += [tuple(coord)]
                    return step[0], start_coord
                if new_coord not in pipes_seen:
                    next_steps.append([step[0] + [tuple(coord)], new_coord])
        pipes_seen.add(tuple(coord))


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    return (len(find_loop(puzzle_input)[0]) + 1) // 2


FLIPPERS = "JL|"  # puzzled out by drawing a bunch of diagrams, these are the symbols on the loop that will transition you from outside to inside and vice versa when scanning left to right


def get_s_shape(s_coord, loop_coords: List):
    connections = set([loop_coords[1], loop_coords[-1]])
    for shape in CONNECTIONS:
        if not len(CONNECTIONS[shape]) == 2:
            continue
        mod1, mod2 = CONNECTIONS[shape]
        modded_coords = {tuple(add(s_coord, mod1)), tuple(add(s_coord, mod2))}
        if modded_coords == set(connections):
            return shape
    raise Exception("We haven't invented a shape like that yet, sir")


def engage_scanners(pipes, exterior, s_shape):
    score = 0
    exterior = set(exterior)
    for y, line in enumerate(pipes):
        inside = False
        for x, char in enumerate(line):
            if (x, y) in exterior:
                if char == "S":
                    char = s_shape
                if char in FLIPPERS:
                    inside = not inside
            elif inside:
                score += 1
    return score


def part_two(input_filename):
    pipes = helpers.parse_input(input_filename)
    exterior, s_coord = find_loop(pipes)
    s_shape = get_s_shape(s_coord, exterior)
    score = engage_scanners(pipes, exterior, s_shape)
    return score


if __name__ == "__main__":
    helpers.display_outupt(
        part1_func=part_one,
        part1_test=True,
        part1=True,
        part2_func=part_two,
        part2_test=True,
        part2=True,
    )
