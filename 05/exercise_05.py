import sys

sys.path.append("..")
from helpers import helpers
import pyperclip
from itertools import count


def parse_range(line, part2=False):
    dest_start, source_start, range_length = [int(item) for item in line.split()]
    if part2:
        mod = source_start - dest_start
        return (dest_start, (dest_start + range_length - 1), mod)
    else:
        mod = dest_start - source_start
        return (source_start, (source_start + range_length - 1), mod)


def get_location_from_map(seed, big_map):
    cur_num = seed
    for item in [
        "seed",
        "soil",
        "fertilizer",
        "water",
        "light",
        "temperature",
        "humidity",
    ]:
        try:
            for (source_start, source_stop), mod in big_map[item].items():
                if source_start <= cur_num <= source_stop:
                    cur_num += mod
                    break
        except KeyError:
            continue
    return cur_num


def part_one(input_filename):
    input = helpers.parse_input(input_filename)
    seeds = [int(item) for item in input[0].split(": ")[1].split()]
    source = ""
    big_map = {}
    for line in input[1:]:
        if not line:
            continue
        elif "map" in line:
            source, destination = line.split()[0].split("-to-")
            big_map[source] = {}
        else:
            source_start, source_stop, mod = parse_range(line)
            big_map[source][(source_start, source_stop)] = mod
    return min([get_location_from_map(seed, big_map) for seed in seeds])


def parse_seeds(seed_line):
    seeds = []
    seed_line = seed_line.split()
    for n in range(len(seed_line)):
        if n % 2:
            continue
        bottom, top = seed_line[n], seed_line[n + 1]
        seeds.append((int(bottom), int(bottom) + int(top) - 1))
    return seeds


def build_mapping_list(input):
    mappings_list = []
    current_map = {}
    for line in input:
        if not line:
            continue
        elif "map" in line:
            if current_map:
                mappings_list.append(current_map)
                current_map = {}
        else:
            dest_start, dest_stop, mod = parse_range(line, part2=True)
            current_map[(dest_start, dest_stop)] = mod
    mappings_list.append(current_map)
    return mappings_list


def part_two(input_filename):
    # playtime's over. time to strategically apply brute force
    input = helpers.parse_input(input_filename)
    seeds = parse_seeds(input[0].split(": ")[1])
    mappings_list = build_mapping_list(input[2:])
    mappings_list.reverse()
    for n in count():
        if not n % 100000:  # little heartbeat so I know it's doing something
            print(n)
        cur_num = n
        for mapping in mappings_list:
            for dest_start, dest_stop in mapping:
                if cur_num in range(dest_start, dest_stop + 1):
                    cur_num += mapping[(dest_start, dest_stop)]
                    break
        for seed_pair in seeds:
            if seed_pair[0] <= cur_num <= seed_pair[1]:
                return n


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
