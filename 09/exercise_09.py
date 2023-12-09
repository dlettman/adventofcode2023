import sys

sys.path.append("..")
from helpers import helpers
import pyperclip


def build_me_a_pyramid(line):
    nums = [int(item) for item in line.split()]
    pyramid = [nums.copy()]
    while True:  # push rows onto the pyramid
        new_row = []
        for n in range(len(nums) - 1):
            new_row.append(nums[n + 1] - nums[n])
        if all([num == 0 for num in new_row]):
            break
        else:
            nums = new_row
            pyramid.append(new_row.copy())
    return pyramid


def find_the_mummys_gold(pyramid, side="right"):
    new_num = 0
    while pyramid:  # pop rows off and fill
        row = pyramid.pop()
        if side == "right":
            new_num = row[-1] + new_num
        elif side == "left":
            new_num = row[0] - new_num
    return new_num


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    extrapolated = []
    for line in input:
        pyramid = build_me_a_pyramid(line)
        extrapolated.append(find_the_mummys_gold(pyramid))
    return sum(extrapolated)


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    extrapolated = []
    for line in input:
        pyramid = build_me_a_pyramid(line)
        extrapolated.append(find_the_mummys_gold(pyramid, side="left"))
    return sum(extrapolated)


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
