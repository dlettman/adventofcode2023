import time

import pyperclip

from helpers import helpers

import heapq

from collections import namedtuple


def create_grid(input_data, scale_factor):
    rows = []
    coord_risk_dict = {}
    for y_iter in range(scale_factor):
        for row in input_data:
            new_row = []
            for x_iter in range(scale_factor):
                new_row += [int(item) + x_iter + y_iter for item in row]
            for idx, num in enumerate(new_row):
                if num > 9:
                    new_row[idx] = num - 9
            rows.append(new_row)
    for y, row in enumerate(rows):
        for x, value in enumerate(row):
            coord_risk_dict[(x, y)] = value
    return coord_risk_dict


Move = namedtuple("Move", ["risk", "x", "y", "last_moves"])


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    grid = create_grid(puzzle_input, 1)
    scale_mod = 1
    max_x = len(puzzle_input[0] * scale_mod)
    max_y = len(puzzle_input * scale_mod)
    total_risks = {key: None for key in grid.keys()}
    total_risks[(0, 0)] = 0
    queue = [Move(0, 0, 0, [])]
    while not total_risks[(max_x - 1), (max_y - 1)]:
        risk, x, y, last_moves = heapq.heappop(queue)
        for delta_x, delta_y in helpers.NEIGHBORS_ORTH:
            if len(last_moves) == 3 and last_moves[-1] == (
                delta_x,
                delta_y,
            ):  # disqualify triple moves
                continue
            new_x, new_y = x + delta_x, y + delta_y
            if (
                0 <= new_x < max_x
                and 0 <= new_y < max_y
                and not total_risks[(new_x, new_y)]
            ):
                total_risks[(new_x, new_y)] = risk + grid[(new_x, new_y)]
                recent_moves = last_moves.copy()
                if recent_moves:
                    if recent_moves[-1] == (delta_x, delta_y):
                        recent_moves.append((delta_x, delta_y))
                    else:
                        recent_moves = [(delta_x, delta_y)]
                else:
                    recent_moves = [(delta_x, delta_y)]
                heapq.heappush(
                    queue, (total_risks[(new_x, new_y)], new_x, new_y, recent_moves)
                )
    return total_risks[(max_x - 1, max_y - 1)]


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    # do stuff here
    output = None
    return output


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
