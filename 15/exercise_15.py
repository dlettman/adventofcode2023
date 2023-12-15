import sys

from helpers import helpers
import pyperclip
import time
import re


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    score = 0
    seqs = input[0].split(",")
    for seq in seqs:
        score += get_hash(seq)
    return score


def get_hash(string):
    score = 0
    for char in string:
        ascii_val = ord(char)
        score += ascii_val
        score *= 17
        score = score % 256
    return score


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    score = 0
    seqs = input[0].split(",")
    boxes = {n: {} for n in range(256)}
    for seq in seqs:
        letters = re.search("[a-z]+", seq).group(0)
        operation = re.search("[=-]", seq).group(0)
        if operation == "=":
            numbers = re.search("[0-9]", seq).group(0)
        box = get_hash(letters)
        if operation == "-":
            if letters in boxes[box]:
                del boxes[box][letters]
        elif operation == "=":
            boxes[box][letters] = numbers
    for box in boxes:
        for idx, label in enumerate(boxes[box]):
            score += (1 + int(box)) * (1 + idx) * int(boxes[box][label])
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
