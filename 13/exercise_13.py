import sys
import time

sys.path.append("..")
from helpers import helpers
import pyperclip

DEBUG = True


def get_maps(input):
    maps = []
    cur_map = []
    for line in input:
        if not line:
            maps.append(cur_map.copy())
            cur_map = []
        else:
            cur_map.append(line)
    maps.append(cur_map)
    return maps


def find_horizontal_reflection(map):
    for reflection_point in range(len(map[0])):
        left = [row[reflection_point - 1 :: -1] for row in map]
        right = [row[reflection_point:] for row in map]
        num_to_compare = min(len(left[0]), len(right[0]))
        left = [item[:num_to_compare] for item in left]
        right = [item[:num_to_compare] for item in right]
        if left == right:
            if DEBUG:
                print(f"found it, column {reflection_point}")
            return reflection_point
    return 0


def find_vertical_reflection(map):
    rotated = []
    for n in range(len(map[0])):
        rotated.append("".join([line[n] for line in map]))
    for reflection_point in range(len(rotated[0])):
        if reflection_point in [0]:
            continue
        left = [row[reflection_point - 1 :: -1] for row in rotated]
        right = [row[reflection_point:] for row in rotated]
        num_to_compare = min(len(left[0]), len(right[0]))
        left = [item[:num_to_compare] for item in left]
        right = [item[:num_to_compare] for item in right]
        if left == right:
            if DEBUG:
                print(f"found it, row {reflection_point}")
            return reflection_point
    return 0


def find_horizontal_smudge(map):
    for reflection_point in range(len(map[0])):
        left = [row[reflection_point - 1 :: -1] for row in map]
        right = [row[reflection_point:] for row in map]
        num_to_compare = min(len(left[0]), len(right[0]))
        left = [item[:num_to_compare] for item in left]
        right = [item[:num_to_compare] for item in right]
        smudge = None
        try:
            for row_idx, row in enumerate(left):
                for idx, char in enumerate(row):
                    if right[row_idx][idx] != char:
                        if smudge is None:
                            smudge = reflection_point
                        else:
                            raise KeyError
        except KeyError:
            continue
        if smudge:
            return smudge


def find_vertical_smudge(map):
    rotated = []
    for n in range(len(map[0])):
        rotated.append("".join([line[n] for line in map]))
    for reflection_point in range(len(rotated[0])):
        # print(f"reflection point = {reflection_point}")
        # if DEBUG:
        #     print(reflection_point)
        if reflection_point in [0]:
            continue
        left = [row[reflection_point - 1 :: -1] for row in rotated]
        right = [row[reflection_point:] for row in rotated]
        num_to_compare = min(len(left[0]), len(right[0]))
        left = [item[:num_to_compare] for item in left]
        right = [item[:num_to_compare] for item in right]
        smudge = None
        try:
            for row_idx, row in enumerate(left):
                for idx, char in enumerate(row):
                    if right[row_idx][idx] != char:
                        if smudge is None:
                            smudge = reflection_point
                        else:
                            raise KeyError
        except KeyError:
            continue
        if smudge:
            return smudge


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    maps = get_maps(input)
    print(maps)
    score = 0
    for idx, map in enumerate(maps):
        print(f"MAP {idx}")
        if DEBUG:
            for line in map:
                print(line)
        horiz = find_horizontal_reflection(map)
        if horiz:
            print(f"Horizontal reflection at {horiz}")
            score += horiz
        vert = find_vertical_reflection(map)
        if vert:
            print(f"Verical reflection at {vert}")
            score += 100 * vert
        if not horiz and not vert:
            print(f"No reflection in map {[str(line) for line in map]}")
    # do stuff here
    return score


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    maps = get_maps(input)
    print(maps)
    score = 0
    for idx, map in enumerate(maps):
        print(f"MAP {idx}")
        if DEBUG:
            for line in map:
                print(line)
        horiz = find_horizontal_smudge(map)
        if horiz:
            print(f"vert reflection at {horiz}")
            score += horiz
        vert = find_vertical_smudge(map)
        if vert:
            print(f"horiz reflection at {vert}")
            score += 100 * vert
        if not horiz and not vert:
            print(f"No reflection in map {[str(line) for line in map]}")
    # do stuff here
    return score


if __name__ == "__main__":
    # print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    # onestart = time.time()
    # p1result = part_one("input.txt")
    # oneend = time.time()
    # print(f"REAL RESULT = {p1result}")
    # print(f"Time = {oneend - onestart}")
    # print("\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    twostart = time.time()
    p2result = part_two("input.txt")
    twoend = time.time()
    print(f"REAL RESULT = {p2result}")
    print(f"Time = {twoend - twostart}")
    # if p1result:
    #     pyperclip.copy(p1result)
    # elif p2result:
    #     pyperclip.copy(p2result)
