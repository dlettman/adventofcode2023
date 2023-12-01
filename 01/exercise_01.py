import sys
sys.path.append("..")
from helpers import helpers

DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    counter = 0
    for line in input:
        first, last = None, None
        for char in line:
            if char.isnumeric():
                last = char
                first = char if first is None else first
        counter += int(first + last)
    return counter


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    counter = 0
    for line in input:
        first, last = None, None
        for idx, char in enumerate(line):
            num = None
            if char.isnumeric():
                num = int(char)
            else:
                for dig_idx, digit in enumerate(DIGITS):
                    try:
                        if line[idx:idx+len(digit)] == digit:
                            num = dig_idx + 1
                    except IndexError:
                        pass
            if num:
                last = num
                first = num if first is None else first
        counter += int(str(first) + str(last))
    return counter


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_one('input.txt')}\n\n")
    print("*** PART TWO ***\n")
    # print(f"Test result = {part_two('inputtest.txt')}\n")
    print(f"REAL RESULT = {part_two('input.txt')}")
