import time
from collections import Counter

import pyperclip

from helpers import helpers

RANKS = "AKQJT98765432"
RANK_DICT = {char: idx for idx, char in enumerate(RANKS)}

RANKS2 = "AKQT98765432J"
RANK2_DICT = {char: idx for idx, char in enumerate(RANKS2)}


def parse_hand(line):
    hand, bid = line.split()
    bid = int(bid)
    card_count = Counter(hand)
    sorted_cards = sorted(card_count, key=lambda x: card_count[x], reverse=True)
    return hand, bid, card_count, sorted_cards


def make_tiers(lines, part_2=False):
    tiers = {"5": [], "4": [], "FH": [], "3": [], "2P": [], "1P": [], "HC": []}
    for line in lines:
        hand, bid, card_count, sorted_cards = parse_hand(line)
        card = sorted_cards[0]
        if part_2:
            if "J" in card_count:
                if card != "J":
                    card_count[card] += card_count["J"]
                else:  # card == J
                    try:
                        card = sorted_cards[1]
                        card_count[card] += card_count["J"]
                        card_count["J"] = 0
                    except IndexError:  # All Js, baby!
                        pass
        if card_count[card] == 5:
            tiers["5"].append((hand, int(bid)))
        elif card_count[card] == 4:
            tiers["4"].append((hand, int(bid)))
        elif card_count[card] == 3:
            card2 = sorted_cards[1]
            if card_count[card2] == 2:
                tiers["FH"].append((hand, int(bid)))
            else:
                tiers["3"].append((hand, int(bid)))
        elif card_count[card] == 2:
            card2 = sorted(card_count, key=lambda x: card_count[x], reverse=True)[1]
            if card_count[card2] == 2:
                tiers["2P"].append((hand, int(bid)))
            else:
                tiers["1P"].append((hand, int(bid)))
        else:
            tiers["HC"].append((hand, int(bid)))
    return tiers


def sort_tier(tier, part_2=False):
    key_dict = RANK2_DICT if part_2 else RANK_DICT
    return sorted(tier, key=lambda x: [key_dict[c] for c in x[0]])


def make_ranking(tiers, part_2=False):
    ranked = []
    for tier in ["5", "4", "FH", "3", "2P", "1P", "HC"]:
        ranked += sort_tier(tiers[tier], part_2=part_2)
    ranked.reverse()
    return ranked


def do_it(input_filename, part_2=False):
    puzzle_input = helpers.parse_input(input_filename)
    tiers = make_tiers(puzzle_input, part_2=part_2)
    ranked = make_ranking(tiers, part_2=part_2)
    score = sum([(idx + 1) * hand[1] for idx, hand in enumerate(ranked)])
    return score


def part_one(input_filename):
    return do_it(input_filename)


def part_two(input_filename):
    return do_it(input_filename, part_2=True)


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    p1result = part_one("input.txt")
    print(f"REAL RESULT = {p1result}\n\n")
    print("*** PART TWO ***\n")
    print(f"Test result = {part_two('inputtest.txt')}\n")
    start = time.time()
    p2result = part_two("input.txt")
    end = time.time()
    print(f"Time = {end - start}")
    print(f"REAL RESULT = {p2result}")
    if p2result:
        pyperclip.copy(p2result)
    elif p1result:
        pyperclip.copy(p1result)
