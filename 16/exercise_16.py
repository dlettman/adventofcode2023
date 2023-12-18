import time
from collections import deque

import pyperclip

from helpers import helpers
from helpers.helpers import Coordinate

from functools import cache

DIRECTIONS = {
    "N": Coordinate(0, -1),
    "S": Coordinate(0, 1),
    "W": Coordinate(-1, 0),
    "E": Coordinate(1, 0),
}

FORWARD_SLASH_DIRECTION_CHANGE = {
    DIRECTIONS["N"]: DIRECTIONS["E"],
    DIRECTIONS["S"]: DIRECTIONS["W"],
    DIRECTIONS["W"]: DIRECTIONS["S"],
    DIRECTIONS["E"]: DIRECTIONS["N"],
}

BACKSLASH_DIRECTION_CHANGE = {
    DIRECTIONS["N"]: DIRECTIONS["W"],
    DIRECTIONS["S"]: DIRECTIONS["E"],
    DIRECTIONS["W"]: DIRECTIONS["N"],
    DIRECTIONS["E"]: DIRECTIONS["S"],
}


class Beam(object):
    def __init__(self, location=Coordinate(0, 0), direction=DIRECTIONS["E"]):
        self.location = location
        self.direction = direction

    def __repr__(self):
        return f"{self.location}, dir = {self.direction}"

    def __hash__(self):
        return hash(tuple([self.location, self.direction]))

    def __eq__(self, other):
        return self.location == other.location and self.direction == other.direction


@cache
def do_beams(beams, puzzle_input):
    energized = set()
    location_direction_record = set()
    while beams:
        beam = beams.popleft()
        energized.add(beam.location)
        location_direction_record.add(
            Beam(location=beam.location, direction=beam.direction)
        )
        if puzzle_input[beam.location.y][beam.location.x] == "/":
            beam.direction = FORWARD_SLASH_DIRECTION_CHANGE[beam.direction]
        elif puzzle_input[beam.location.y][beam.location.x] == "\\":
            beam.direction = BACKSLASH_DIRECTION_CHANGE[beam.direction]
        elif puzzle_input[beam.location.y][beam.location.x] == "|":
            if beam.direction in [DIRECTIONS["E"], DIRECTIONS["W"]]:  # beam splits
                beam.direction = DIRECTIONS["N"]
                if not helpers.out_of_bounds(
                    beam.location + DIRECTIONS["S"], puzzle_input
                ):
                    if (
                        not Beam(
                            location=beam.location + DIRECTIONS["E"],
                            direction=DIRECTIONS["E"],
                        )
                        in location_direction_record
                    ):
                        beams.append(
                            Beam(
                                location=beam.location + DIRECTIONS["S"],
                                direction=DIRECTIONS["S"],
                            )
                        )
        elif puzzle_input[beam.location.y][beam.location.x] == "-":
            if beam.direction in [DIRECTIONS["N"], DIRECTIONS["S"]]:  # beam splits
                beam.direction = DIRECTIONS["W"]
                if not helpers.out_of_bounds(
                    beam.location + DIRECTIONS["E"], puzzle_input
                ):
                    if (
                        not Beam(
                            location=beam.location + DIRECTIONS["E"],
                            direction=DIRECTIONS["E"],
                        )
                        in location_direction_record
                    ):
                        beams.append(
                            Beam(
                                location=beam.location + DIRECTIONS["E"],
                                direction=DIRECTIONS["E"],
                            )
                        )
        beam.location = beam.location + beam.direction
        if not helpers.out_of_bounds(beam.location, puzzle_input):
            if beam not in location_direction_record:
                beams.append(beam)
    return energized


def part_one(input_filename):
    beams = deque([Beam()])
    puzzle_input = helpers.parse_input(input_filename)
    energized = do_beams(beams, puzzle_input)
    return energized


def part_two(input_filename):  # it's not THAT MUCH brute force
    puzzle_input = helpers.parse_input(input_filename)
    max_energized = 0
    for n in range(len(puzzle_input)):
        max_energized = max(
            do_beams(deque([Beam(Coordinate(0, n), DIRECTIONS["E"])]), puzzle_input),
            max_energized,
        )
        max_energized = max(
            do_beams(
                deque([Beam(Coordinate(len(puzzle_input[0]) - 1, n), DIRECTIONS["W"])]),
                puzzle_input,
            ),
            max_energized,
        )
    for n in range(len(puzzle_input[0])):
        max_energized = max(
            do_beams(deque([Beam(Coordinate(n, 0), DIRECTIONS["S"])]), puzzle_input),
            max_energized,
        )
        max_energized = max(
            do_beams(
                deque([Beam(Coordinate(n, len(puzzle_input) - 1), DIRECTIONS["N"])]),
                puzzle_input,
            ),
            max_energized,
        )
    return max_energized


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
