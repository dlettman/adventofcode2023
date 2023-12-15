import sys

sys.path.append("..")
from helpers import helpers
import time
import functools
import pyperclip

from typing import List

CHAR_BIN_MAPPING = {".": "0", "#": "1"}


def parse_line(line):
    slots, groups = line.split()
    slots = list(slots)
    groups = groups.split(",")
    return slots, groups


def get_combo_count_for_line(slots, groups):
    slot_length = len(slots)
    successful_combos = 0
    comb_attempt = 0
    while True:
        binary = str(bin(comb_attempt))[2:]
        if len(binary) > slot_length:
            return successful_combos
        slotted = binary.zfill(len(slots))
        if verify_combo(slotted, groups, slots):
            successful_combos += 1
        comb_attempt += 1


CHAR_BIN_MAPPING = {".": "0", "#": "1"}


def verify_combo(
    combo: str, groupings: List, slots: str
):  # combo is binary, slots is a list of ints, slots is the og string
    groupings = iter(groupings)
    cur_len = 0
    for idx in range(len(combo)):
        if (
            slots[idx] in CHAR_BIN_MAPPING
            and CHAR_BIN_MAPPING[slots[idx]] != combo[idx]
        ):
            return False
        if combo[idx] == "0":
            if cur_len:
                try:
                    ng = int(next(groupings))
                    if ng != cur_len:
                        return False
                    cur_len = 0
                except StopIteration:
                    return False
        elif combo[idx] == "1":
            cur_len += 1
    if cur_len:
        try:
            ng = int(next(groupings))
            if ng != cur_len:
                return False
        except StopIteration:
            return False
    try:
        _ = next(groupings)
        return False
    except StopIteration:
        return True


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    score = 0
    for line in input:
        slots, groups = parse_line(line)
        print(slots)
        print(groups)
        score += get_combo_count_for_line(slots, groups)
    return score


@functools.cache  # cache is doing a lot of heavy lifting here
def get_solution_count(springs: tuple, contigs: tuple, current_run=0) -> int:
    if not springs:  # base case
        if contigs:
            if len(contigs) == 1 and current_run == contigs[0]:
                return 1
            else:
                return 0
        else:
            if not current_run:
                return 1
            else:
                return 0
    elif springs[0] == "#":  # recursive cases
        return get_solution_count(springs[1:], contigs, current_run=(current_run + 1))
    elif springs[0] == ".":
        if current_run:
            try:
                this_group = contigs[0]
            except IndexError:
                return 0
            if this_group == current_run:
                return get_solution_count(springs[1:], contigs[1:], current_run=0)
            else:
                return 0
        else:
            return get_solution_count(springs[1:], contigs, current_run=0)
    elif springs[0] == "?":
        broke_copy = list(springs)
        broke_copy[0] = "#"
        broke_copy = tuple(broke_copy)
        broke_score = get_solution_count(broke_copy, contigs, current_run)
        fixed_copy = list(springs)
        fixed_copy[0] = "."
        fixed_copy = tuple(fixed_copy)
        fixed_score = get_solution_count(fixed_copy, contigs, current_run)
        return fixed_score + broke_score
    else:  # oh crap everything is broken case
        raise Exception("WTF is this")


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    score = 0
    for line in input:
        springs, groups = parse_line(line)
        springs = (list(springs + ["?"]) * 5)[:-1]
        groups = [int(item) for item in groups]
        groups = groups * 5
        springs, groups = tuple(springs), tuple(groups)
        line_score = get_solution_count(springs, groups)
        score += line_score
    return score


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
