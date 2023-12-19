import heapq
import time
from collections import namedtuple

import pyperclip

from helpers import helpers


def create_grid(puzzle_input, max_moves=3):
    coord_risk_dict = {}
    for y, row in enumerate(puzzle_input):
        for x, value in enumerate(row):
            for neighbor in helpers.NEIGHBORS_ORTH:
                for n in range(1, max_moves + 1):
                    coord_risk_dict[
                        (x, y, neighbor, n)
                    ] = value  # x, y, last dir, num moves in that dir
    return coord_risk_dict


Move = namedtuple("Move", ["risk", "x", "y", "last_dir", "moves_in_that_dir"])


def everybody_do_the_dijkstra(puzzle_input, max_moves=3, min_moves=0):
    grid = create_grid(puzzle_input, max_moves=max_moves)
    max_x = len(puzzle_input[0])
    max_y = len(puzzle_input)
    grid = {key: None for key in grid.keys()}
    grid[(0, 0, (0, 0), 0)] = 0  # x, y, last dir, num moves in that dir
    queue = [Move(0, 0, 0, None, 0)]
    while True:
        risk, x, y, last_dir, moves_in_that_dir = heapq.heappop(queue)
        for delta_x, delta_y in helpers.NEIGHBORS_ORTH:
            if (
                moves_in_that_dir == max_moves and (last_dir == (delta_x, delta_y))
            ) or (last_dir == (-1 * delta_x, -1 * delta_y)):
                continue
            if min_moves:
                if 1 <= moves_in_that_dir <= (min_moves - 1) and last_dir != (
                    delta_x,
                    delta_y,
                ):
                    continue
            new_x, new_y = x + delta_x, y + delta_y
            dir = (delta_x, delta_y)
            num_moves = moves_in_that_dir + 1 if (last_dir == dir) else 1
            if (
                0 <= new_x < max_x
                and 0 <= new_y < max_y
                and not grid[(new_x, new_y, dir, num_moves)]
            ):
                grid[(new_x, new_y, dir, num_moves)] = risk + int(
                    puzzle_input[new_y][new_x]
                )
                if ((new_x, new_y) == (max_x - 1, max_y - 1)) and (
                    not min_moves or (min_moves <= num_moves <= max_moves)
                ):
                    return risk + int(puzzle_input[new_y][new_x])
                heapq.heappush(
                    queue,
                    Move(
                        grid[(new_x, new_y, dir, num_moves)],
                        new_x,
                        new_y,
                        dir,
                        num_moves,
                    ),
                )


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    return everybody_do_the_dijkstra(puzzle_input, max_moves=3, min_moves=0)


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    return everybody_do_the_dijkstra(puzzle_input, max_moves=10, min_moves=4)


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
