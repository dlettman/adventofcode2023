import sys
import math
import time

sys.path.append("..")
from helpers import helpers
import pyperclip


def parse_lines(input):
    times, distances = [
        [int(item) for item in input[n].split(": ")[1].strip().split()]
        for n in range(2)
    ]
    return times, distances


def part_one(input_filename):
    scores = []
    input = helpers.parse_input(input_filename)
    times, distances = parse_lines(input)
    for time, distance in zip(times, distances):
        scores.append(sum([1 for n in range(time) if (((time - n) * n) > distance)]))
    return math.prod(scores)


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    time, distance = [
        int("".join(input[n].split(": ")[1].strip().split())) for n in range(2)
    ]
    score = sum([1 for n in range(time) if (((time - n) * n) > distance)])
    return score


def get_distance(charge_time, total_time):
    return charge_time * (total_time - charge_time)


def part2():
    SAMPLE_TIME = 71530
    SAMPLE_DISTANCE = 940200
    INPUT_TIME = 58819676
    INPUT_DISTANCE = 434104122191218
    time = SAMPLE_TIME
    distance = SAMPLE_DISTANCE
    time = INPUT_TIME
    distance = INPUT_DISTANCE
    # brute force?
    winner_count = 0
    for charge_time in range(time + 1):
        if get_distance(charge_time, time) > distance:
            winner_count += 1
    # brute force! Ran in like 10sec ¯\_(ツ)_/¯
    return winner_count


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    p1result = part_one("input.txt")
    print(f"REAL RESULT = {p1result}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    start = time.time()
    p2result = part_two("input.txt")
    end = time.time()
    start = time.time()
    p2result = part2()
    end = time.time()
    print(f"Time = {end - start}")
    print(f"REAL RESULT = {p2result}")
    if p2result:
        pyperclip.copy(p2result)
    elif p1result:
        pyperclip.copy(p1result)
