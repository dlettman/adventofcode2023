import pyperclip

from helpers import helpers

DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    counter = 0
    for line in puzzle_input:
        first, last = None, None
        for char in line:
            if char.isnumeric():
                last = char
                first = char if first is None else first
        if first:
            counter += int(first + last)
    return counter


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    counter = 0
    for line in puzzle_input:
        first, last = None, None
        for idx, char in enumerate(line):
            num = None
            if char.isnumeric():
                num = int(char)
            else:
                for dig_idx, digit in enumerate(DIGITS):
                    try:
                        if line[idx : idx + len(digit)] == digit:
                            num = dig_idx + 1
                    except IndexError:
                        pass
            if num:
                last = num
                first = num if first is None else first
        counter += int(str(first) + str(last))
    return counter


if __name__ == "__main__":
    helpers.display_outupt(
        part1_func=part_one,
        part1_test=True,
        part1=True,
        part2_func=part_two,
        part2_test=True,
        part2=True,
    )
