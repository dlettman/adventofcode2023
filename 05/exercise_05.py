from itertools import count

import pyperclip

from helpers import helpers


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
    puzzle_input = helpers.parse_input(input_filename)
    seeds = [int(item) for item in puzzle_input[0].split(": ")[1].split()]
    source = ""
    big_map = {}
    for line in puzzle_input[1:]:
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


def build_mapping_list(puzzle_input):
    mappings_list = []
    current_map = {}
    for line in puzzle_input:
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
    puzzle_input = helpers.parse_input(input_filename)
    seeds = parse_seeds(puzzle_input[0].split(": ")[1])
    mappings_list = build_mapping_list(puzzle_input[2:])
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
    helpers.display_outupt(
        part1_func=part_one,
        part1_test=True,
        part1=True,
        part2_func=part_two,
        part2_test=True,
        part2=True,
    )
