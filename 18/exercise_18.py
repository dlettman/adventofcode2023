import sys
sys.path.append("..")
from helpers import helpers
import pyperclip

def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    # do stuff here
    output = None
    return output

def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    # do stuff here
    output = None
    return output

if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    p1result = part_one('input.txt')
    print(f"REAL RESULT = {p1result}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    p2result = part_two('input.txt')
    print(f"REAL RESULT = {p2result}")
    if p1result:
        pyperclip.copy(p1result)
    elif p2result:
        pyperclip.copy(p2result)
