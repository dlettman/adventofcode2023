import time

import pyperclip

from helpers import helpers


def get_grids(input):
    grids = []
    cur_grid = []
    for line in input:
        if not line:
            grids.append(cur_grid.copy())
            cur_grid = []
        else:
            cur_grid.append(line)
    grids.append(cur_grid)
    return grids


def rotate_grid(map):
    rotated = ["".join([line[n] for line in map]) for n in range(len(map[0]))]
    return rotated


def get_potential_reflections(reflection_point, map):
    left = [row[reflection_point - 1 :: -1] for row in map]
    right = [row[reflection_point:] for row in map]
    num_to_compare = min(len(left[0]), len(right[0]))
    left = [item[:num_to_compare] for item in left]
    right = [item[:num_to_compare] for item in right]
    return left, right


def find_vert_reflection(map):
    for reflection_point in range(len(map[0])):
        left, right = get_potential_reflections(reflection_point, map)
        if left == right:
            return reflection_point
    return 0


def find_horiz_reflection(map):
    rotated = rotate_grid(map)
    return find_vert_reflection(rotated)


class TooManySmudgesError(Exception):
    pass


def find_smudge(left, right, reflection_point):
    smudge = None
    try:
        for row_idx, row in enumerate(left):
            for idx, char in enumerate(row):
                if right[row_idx][idx] != char:
                    if smudge is None:
                        smudge = reflection_point
                    else:
                        raise TooManySmudgesError
    except TooManySmudgesError:
        return 0
    return smudge if smudge else 0


def find_vert_smudge(grid):
    for reflection_point in range(len(grid[0])):
        left, right = get_potential_reflections(reflection_point, grid)
        smudge = find_smudge(left, right, reflection_point)
        if smudge:
            return smudge
    return 0


def find_horiz_smudge(grid):
    rotated = rotate_grid(grid)
    return find_vert_smudge(rotated)


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    grids = get_grids(puzzle_input)
    score = 0
    for idx, grid in enumerate(grids):
        score += find_vert_reflection(grid)
        score += 100 * find_horiz_reflection(grid)
    return score


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    grids = get_grids(puzzle_input)
    score = 0
    for idx, map in enumerate(grids):
        score += find_vert_smudge(map)
        score += 100 * find_horiz_smudge(map)
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
