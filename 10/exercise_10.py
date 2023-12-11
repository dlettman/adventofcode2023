import sys

sys.path.append("..")
from helpers import helpers
import pyperclip
from numpy import add
import time
from collections import deque

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
# S = Special Case!

# def find_loop(pipes):
#     pipes_seen = set()
#     for y, line in enumerate(pipes):
#         for x, char in enumerate(line):
#             starting_coord = (x, y)
#             pipes_seen_this_round = set(starting_coord)
#             coord = starting_coord
#             print("STARTING AT", coord)
#             if pipes[coord[1]][coord[0]] == "." or coord in pipes_seen:
#                 pipes_seen.add(coord)
#                 continue
#             next_steps = [add(coord, mod) for mod in CONNECTIONS[char]]
#             found_opening = False
#             while next_steps:
#                 next_step = next_steps.pop()
#                 pipes_seen_this_round.add(tuple(next_step))
#                 print(f"next_step = {next_step}")
#                 next_coord = add(coord, next_step)
#                 pipes_seen_this_round.add(tuple(next_coord))
#                 if helpers.out_of_bounds(next_coord, pipes) or pipes[next_coord[1]][next_coord[0]] == ".":
#                     pipes_seen = pipes_seen_this_round.union(pipes_seen)
#                     found_opening = True
#                     break
#                 else:
#                     new_char = pipes[next_coord[1]][next_coord[0]]
#                     for new_coord in [add(next_coord, mod) for mod in CONNECTIONS[new_char]]:
#                         if tuple(new_coord) not in pipes_seen_this_round.union(pipes_seen):
#                             next_steps.append(new_coord)
#                 time.sleep(.5)
#             if not found_opening:
#                 return len(pipes_seen_this_round) / 2


def find_loop(pipes):
    for y, line in enumerate(pipes):
        for x, char in enumerate(line):
            if not char == "S":
                continue
            coord = (x, y)
            pipes_seen = set(coord)
            # print("STARTING AT", coord)
            next_steps = [([coord], add(coord, mod)) for mod in helpers.NEIGHBORS_ORTH]
            while next_steps:
                step = next_steps.pop()
                # print(f"NEXT STEP = {step}")
                # pipes_seen_this_round.add(tuple(next_step))
                coord = step[1]
                if (
                    helpers.out_of_bounds(coord, pipes)
                    or pipes[coord[1]][coord[0]] == "."
                ):
                    # print(f"path dies at {coord}")
                    continue  # path dies
                else:
                    # print(f"next_step = {step}")
                    new_char = pipes[coord[1]][coord[0]]
                    for new_coord in [add(coord, mod) for mod in CONNECTIONS[new_char]]:
                        if pipes[new_coord[1]][new_coord[0]] == "S" and (
                            len(step[0]) > 1
                        ):
                            print(step[0])
                            return step[0]
                        if tuple(new_coord) not in pipes_seen:
                            next_steps.append(
                                [step[0] + [tuple(coord)], tuple(new_coord)]
                            )
                            # print(f"appending {next_step[0] + [next_coord], new_coord}")

                pipes_seen.add(tuple(coord))


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    return (len(find_loop(input)) + 1) // 2


def part_two(input_filename):
    pipes = helpers.parse_input(input_filename)
    exterior = set(find_loop(pipes))
    print(exterior)
    score = 0
    for y, line in enumerate(pipes):
        for x, char in enumerate(line):
            coord = (x, y)
            if coord in exterior:
                continue
            else:
                found_edge = False
                for direction in helpers.NEIGHBORS_ORTH:
                    new_coord = coord
                    while not found_edge:
                        new_coord = tuple(add(new_coord, direction))
                        if new_coord in exterior:
                            break
                        elif helpers.out_of_bounds(new_coord, pipes):
                            found_edge = True
                            break
                    if found_edge:
                        break
                if not found_edge:
                    print(coord)
                    score += 1
    return score


if __name__ == "__main__":
    # print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    # p1result = part_one("input.txt")
    # print(f"REAL RESULT = {p1result}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    # p2result = part_two("input.txt")
    # print(f"REAL RESULT = {p2result}")
    # if p2result:
    #     pyperclip.copy(p2result)
    # elif p1result:
    #     pyperclip.copy(p1result)
