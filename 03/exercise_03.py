import numpy
import pyperclip

from helpers import helpers

NEIGHBORS = helpers.NEIGHBORS


def is_symbol(char):
    return (not char.isdigit()) and char != "."


def out_of_bounds(coord, grid):
    return any(
        [
            coord[0] < 0,
            coord[1] < 0,
            coord[0] > (len(grid[0]) - 1),
            coord[1] > (len(grid) - 1),
        ]
    )


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    score = 0
    for y, line in enumerate(puzzle_input):
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
                                    puzzle_input[neighbor_coord[1]][neighbor_coord[0]]
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


def find_neighbor_numbers(coord, puzzle_input):
    seen = set()
    numbers = []
    for neighbor in NEIGHBORS:
        test_coord = numpy.add(coord, neighbor)
        if tuple(test_coord) in seen:
            continue
        seen.add(tuple(test_coord))
        if puzzle_input[test_coord[1]][test_coord[0]].isdigit():
            num = puzzle_input[test_coord[1]][test_coord[0]]
            current_coord = test_coord
            stop_looking_here = False
            # fan left
            while True:
                current_coord = numpy.add(current_coord, (-1, 0))
                if out_of_bounds(current_coord, puzzle_input):
                    break
                if puzzle_input[current_coord[1]][current_coord[0]].isdigit():
                    if tuple(current_coord) in seen:
                        stop_looking_here = True
                        break
                    seen.add(tuple(current_coord))
                    num = puzzle_input[current_coord[1]][current_coord[0]] + num
                else:
                    break
            if stop_looking_here:
                continue
            # fan right
            current_coord = test_coord
            while True:
                current_coord = numpy.add(current_coord, (1, 0))
                if out_of_bounds(current_coord, puzzle_input):
                    break
                if puzzle_input[current_coord[1]][current_coord[0]].isdigit():
                    if tuple(current_coord) in seen:
                        stop_looking_here = True
                        break
                    seen.add(tuple(current_coord))
                    num = num + puzzle_input[current_coord[1]][current_coord[0]]
                else:
                    break
            if not stop_looking_here:
                numbers.append(num)
    return numbers


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    score = 0
    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            if char == "*":
                neighbor_numbers = find_neighbor_numbers((x, y), puzzle_input)
                if len(neighbor_numbers) == 2:
                    score += int(neighbor_numbers[0]) * int(neighbor_numbers[1])
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
