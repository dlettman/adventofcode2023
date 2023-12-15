from math import floor

import pyperclip

from helpers import helpers


def parse_cards(puzzle_input):
    cards = {}
    for line in puzzle_input:
        card_num, nums = line.split(": ")
        card_num = card_num.split()[1]
        winning_nums, your_nums = nums.split(" | ")
        cards[card_num] = {
            "winning_nums": set([int(num) for num in winning_nums.strip().split()]),
            "your_nums": set([int(num) for num in your_nums.strip().split()]),
        }
    return cards


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    score = 0
    cards = parse_cards(puzzle_input)
    for card in cards:
        card_score = 0.5
        for _ in cards[card]["winning_nums"].intersection(cards[card]["your_nums"]):
            card_score *= 2
        score += floor(card_score)
    return score


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    cards = parse_cards(puzzle_input)
    card_count = {str(n + 1): 1 for n in range(len(puzzle_input))}
    for card in cards:
        card_multiplier = card_count[card]
        card_score = len(
            cards[card]["winning_nums"].intersection(cards[card]["your_nums"])
        )
        next_card = int(card) + 1
        for n in range(card_score):
            card_count[str(next_card)] += card_multiplier
            next_card += 1
    return sum(card_count.values())


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
