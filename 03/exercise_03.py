import sys

sys.path.append("..")
from helpers import helpers
import pyperclip
import numpy

NEIGHBORS = helpers.NEIGHBORS


def is_symbol(char):
    return (not char.isdigit()) and char != "."


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    score = 0
    for y, line in enumerate(input):
        number = ""
        found_neighbor_symbol = False
        for x, char in enumerate(line):
            if char.isnumeric():
                number += char
                if not found_neighbor_symbol:
                    for neighbor in NEIGHBORS:
                        neighbor_coord = numpy.add((x, y), neighbor)
                        if neighbor_coord[0] >= 0 and neighbor_coord[1] >= 0:
                            try:
                                if is_symbol(
                                    input[neighbor_coord[1]][neighbor_coord[0]]
                                ):
                                    found_neighbor_symbol = True
                            except IndexError:
                                pass
            else:
                if number:  # score it
                    if found_neighbor_symbol:
                        score += int(number)
                    number = ""
                    found_neighbor_symbol = False
        if number:  # score it
            if found_neighbor_symbol:
                score += int(number)
            number = ""
            found_neighbor_symbol = False
    return score


def find_neighbor_numbers(coord, input):
    seen = set()
    numbers = []
    for neighbor in NEIGHBORS:
        test_coord = numpy.add(coord, neighbor)
        if tuple(test_coord) in seen:
            continue
        seen.add(tuple(test_coord))
        if input[test_coord[1]][test_coord[0]].isdigit():
            num = input[test_coord[1]][test_coord[0]]
            current_coord = test_coord
            stop_looking_here = False
            # fan left
            while True:
                current_coord = numpy.add(current_coord, (-1, 0))
                if (
                    current_coord[0] < 0
                    or current_coord[1] < 0
                    or current_coord[0] > (len(input[0]) - 1)
                    or current_coord[1] > (len(input) - 1)
                ):
                    break
                if input[current_coord[1]][current_coord[0]].isdigit():
                    if tuple(current_coord) in seen:
                        stop_looking_here = True
                        break
                    seen.add(tuple(current_coord))
                    num = input[current_coord[1]][current_coord[0]] + num
                else:
                    break
            if stop_looking_here:
                continue
            # fan right
            current_coord = test_coord
            while True:
                current_coord = numpy.add(current_coord, (1, 0))
                if (
                    current_coord[0] < 0
                    or current_coord[1] < 0
                    or current_coord[0] > (len(input[0]) - 1)
                    or current_coord[1] > (len(input) - 1)
                ):
                    break
                if input[current_coord[1]][current_coord[0]].isdigit():
                    if tuple(current_coord) in seen:
                        stop_looking_here = True
                        break
                    seen.add(tuple(current_coord))
                    num = num + input[current_coord[1]][current_coord[0]]
                else:
                    break
            if not stop_looking_here:
                numbers.append(num)
    return numbers


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    score = 0
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if char == "*":
                neighbor_numbers = find_neighbor_numbers((x, y), input)
                if len(neighbor_numbers) == 2:
                    score += int(neighbor_numbers[0]) * int(neighbor_numbers[1])
    return score


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    p1result = part_one("input.txt")
    print(f"REAL RESULT = {p1result}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    p2result = part_two("input.txt")
    print(f"REAL RESULT = {p2result}")
    if p2result:
        pyperclip.copy(p2result)
    elif p1result:
        pyperclip.copy(p1result)
