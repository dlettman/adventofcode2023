import sys

sys.path.append("..")
from helpers import helpers
import pyperclip
from collections import Counter

RANKS = list("AKQJT98765432")

RANKS2 = list("AKQT98765432J")


def sort_tier(tier):
    return sorted(tier, key=lambda x: [RANKS.index(c) for c in x[0]])


def sort_tier2(tier):
    return sorted(tier, key=lambda x: [RANKS2.index(c) for c in x[0]])


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    ranked = []
    tiers = {"5": [], "4": [], "FH": [], "3": [], "2P": [], "1P": [], "HC": []}
    for line in input:
        hand = line.split()[0]
        card_count = Counter(line.split()[0])
        bid = int(line.split()[1])
        card = sorted(card_count, key=lambda x: card_count[x], reverse=True)[0]
        if card_count[card] == 5:
            tiers["5"].append((hand, int(bid)))
        elif card_count[card] == 4:
            tiers["4"].append((hand, int(bid)))
        elif card_count[card] == 3:
            fh = False
            for card2 in card_count:
                if card_count[card2] == 2:
                    tiers["FH"].append((hand, int(bid)))
                    fh = True
            if not fh:
                tiers["3"].append((hand, int(bid)))
        elif card_count[card] == 2:
            TP = False
            card2 = sorted(card_count, key=lambda x: card_count[x], reverse=True)[1]
            if card_count[card2] == 2:
                tiers["2P"].append((hand, int(bid)))
            else:
                tiers["1P"].append((hand, int(bid)))
        else:
            tiers["HC"].append((hand, int(bid)))
    for tier in ["5", "4", "FH", "3", "2P", "1P", "HC"]:
        ranked += sort_tier(tiers[tier])
    ranked.reverse()
    score = 0
    for idx, hand in enumerate(ranked):
        score += (idx + 1) * hand[1]
    return score


def part_two(input_filename):
    input = helpers.parse_input(input_filename)
    ranked = []
    tiers = {"5": [], "4": [], "FH": [], "3": [], "2P": [], "1P": [], "HC": []}
    for line in input:
        hand = line.split()[0]
        card_count = Counter(line.split()[0])
        bid = int(line.split()[1])
        sorted_cards = sorted(card_count, key=lambda x: card_count[x], reverse=True)
        # sorted_cards = sorted(sorted_cards, key=lambda x: x == 'J')
        card = sorted_cards[0]
        if "J" in card_count:
            if card != "J":
                card_count[card] += card_count["J"]
            else:  # card == J
                try:
                    card = sorted_cards[1]
                    card_count[card] += card_count["J"]
                    card_count["J"] = 0
                except IndexError:  #
                    pass
        if card_count[card] == 5:
            tiers["5"].append((hand, int(bid)))
        elif card_count[card] == 4:
            tiers["4"].append((hand, int(bid)))
        elif card_count[card] == 3:
            fh = False
            for card2 in card_count:
                if card_count[card2] == 2:
                    tiers["FH"].append((hand, int(bid)))
                    fh = True
            if not fh:
                tiers["3"].append((hand, int(bid)))
        elif card_count[card] == 2:
            card2 = sorted(card_count, key=lambda x: card_count[x], reverse=True)[1]
            if card_count[card2] == 2:
                tiers["2P"].append((hand, int(bid)))
            else:
                tiers["1P"].append((hand, int(bid)))
        else:
            tiers["HC"].append((hand, int(bid)))
    for tier in ["5", "4", "FH", "3", "2P", "1P", "HC"]:
        tiers[tier] = sort_tier2(tiers[tier])
        ranked += sort_tier2(tiers[tier])
    ranked.reverse()
    score = sum([(idx + 1) * hand[1] for idx, hand in enumerate(ranked)])
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
