import math
import time

import pyperclip

from helpers import helpers


def parse_lines(input):
    times, distances = [
        [int(item) for item in input[n].split(": ")[1].strip().split()]
        for n in range(2)
    ]
    return times, distances


def part_one(input_filename):
    scores = []
    puzzle_input = helpers.parse_input(input_filename)
    times, distances = parse_lines(puzzle_input)
    for time, distance in zip(times, distances):
        scores.append(sum([1 for n in range(time) if (((time - n) * n) > distance)]))
    return math.prod(scores)


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    time, distance = [
        int("".join(puzzle_input[n].split(": ")[1].strip().split())) for n in range(2)
    ]
    score = sum([1 for n in range(time) if (((time - n) * n) > distance)])
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
