import re
import time

import pyperclip

from helpers import helpers


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    score = 0
    seqs = puzzle_input[0].split(",")
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
    puzzle_input = helpers.parse_input(input_filename)
    score = 0
    seqs = puzzle_input[0].split(",")
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
    helpers.display_outupt(
        part1_func=part_one,
        part1_test=True,
        part1=True,
        part2_func=part_two,
        part2_test=True,
        part2=True,
    )
