import sys

sys.path.append("..")
from helpers import helpers
import pyperclip
import curses
from time import sleep

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
    scr = helpers.init_curses()
    for line in input:
        first, last, f_index, l_index, f_ischar, l_ischar = (
            None,
            None,
            None,
            None,
            False,
            False,
        )
        for idx, char in enumerate(line):
            scr.addch(0, idx, char, curses.color_pair(1))
        for idx, char in enumerate(line):
            num, num_ischar = None, False
            if char.isnumeric():
                num = int(char)
            else:
                for dig_idx, digit in enumerate(DIGITS):
                    try:
                        if line[idx : idx + len(digit)] == digit:
                            num = dig_idx + 1
                            num_ischar = True
                    except IndexError:
                        pass
            if num:
                last, l_index, l_ischar = (num, idx, num_ischar)
                (first, f_index, f_ischar) = (
                    (num, idx, num_ischar)
                    if first is None
                    else (first, f_index, f_ischar)
                )
            scr.refresh()
            for new_idx, char in enumerate(line[0 : idx + 1]):
                scr.addch(0, new_idx, char, curses.color_pair(1))
                if first:
                    if f_ischar:
                        if f_index + len(DIGITS[first - 1]) <= new_idx:
                            for d_idx, char in enumerate(DIGITS[first - 1]):
                                scr.addch(
                                    0, f_index + d_idx, char, curses.color_pair(2)
                                )
                    else:
                        scr.addch(0, f_index, str(first), curses.color_pair(2))
                if last:
                    if l_ischar:
                        for d_idx, char in enumerate(DIGITS[last - 1]):
                            scr.addch(0, l_index + d_idx, char, curses.color_pair(3))
                    else:
                        scr.addch(0, l_index, str(first), curses.color_pair(3))
                sleep(0.1)
        scr.clear()
    return counter


if __name__ == "__main__":
    p1result = None
    # print("*** PART ONE ***\n")
    # print(f"Test result = {part_one('inputtest.txt')}\n")
    # p1result = part_one('input.txt')
    # print(f"REAL RESULT = {p1result}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    p2result = part_two("input.txt")
    print(f"REAL RESULT = {p2result}")
    if p1result:
        pyperclip.copy(p1result)
    elif p2result:
        pyperclip.copy(p2result)
