import pyperclip

from helpers import helpers


def part_one(input_filename):
    maxes = {"red": 12, "green": 13, "blue": 14}
    puzzle_input = helpers.parse_input(input_filename)
    games = {}
    score = 0
    for idx, line in enumerate(puzzle_input):
        game_num = line.split(":")[0].split(" ")[1]
        rounds = []
        for segment in line.split(":")[1].split(";"):
            rounds.append([seg.strip(",") for seg in segment.strip().split(" ")])
        games[game_num] = rounds
    for game, rounds in games.items():
        game_broken = False
        for round in rounds:
            broke_limit = False
            counter = None
            for element in round:
                if counter is None:
                    counter = int(element)
                else:
                    color = element.strip(",")
                    if maxes[color] < counter:
                        broke_limit = True
                        break
                    else:
                        counter = None
            if broke_limit:
                game_broken = True
                break
        if not game_broken:
            score += int(game)
    return score


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    games = {}
    score = 0
    for idx, line in enumerate(puzzle_input):
        game_num = line.split(":")[0].split(" ")[1]
        rounds = []
        for segment in line.split(":")[1].split(";"):
            rounds.append([seg.strip(",") for seg in segment.strip().split(" ")])
        games[game_num] = rounds
    for game, rounds in games.items():
        maxes = {"red": 0, "green": 0, "blue": 0}
        for round in rounds:
            counter = None
            for element in round:
                if counter is None:
                    counter = int(element)
                else:
                    color = element.strip(",")
                    maxes[color] = max(maxes[color], counter)
                    counter = None
        score += maxes["red"] * maxes["green"] * maxes["blue"]
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
