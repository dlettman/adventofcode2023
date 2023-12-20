import time
from collections import deque, namedtuple
from math import lcm

from helpers import helpers

Pulse = namedtuple("Pulse", ["destination_module", "sender", "value"])


class ConjunctionModule(object):
    def __init__(self, name, input_modules=[], output_modules=[], pulse_queue=None):
        self.name = name
        self.input_modules = {}
        self.output_modules = output_modules
        self.pulse_queue = pulse_queue

    def __repr__(self):
        return f"& - {self.name}. Inputs: {self.input_modules} - Outputs: {self.output_modules}"

    def receive_pulse(self, sender, pulse):
        self.input_modules[sender] = pulse
        self.send_pulse()

    def send_pulse(self):
        if 0 in self.input_modules.values():
            for module in self.output_modules:
                self.pulse_queue.append(Pulse(module, self.name, 1))
        else:
            for module in self.output_modules:
                self.pulse_queue.append(Pulse(module, self.name, 0))


class FlipFlopModule(object):
    def __init__(self, name, value=0, output_modules=[], pulse_queue=None):
        self.name = name
        self.value = value
        self.output_modules = output_modules
        self.pulse_queue = pulse_queue

    def __repr__(self):
        return f"% - {self.name}. Outputs: {self.output_modules}"

    def receive_pulse(self, sender, pulse):
        if pulse == 0:
            self.value = 1 if self.value == 0 else 0
            for module in self.output_modules:
                self.pulse_queue.append(Pulse(module, self.name, self.value))


class BroadcasterModule(object):
    def __init__(self, name="broadcaster", output_modules=[], pulse_queue=None):
        self.name = name
        self.output_modules = output_modules
        self.pulse_queue = pulse_queue

    def __repr__(self):
        return f"Broadcaster - {self.name}. Outputs: {self.output_modules}"

    def receive_pulse(self, sender, pulse):
        for module in self.output_modules:
            self.pulse_queue.append(Pulse(module, self.name, 0))


# class NullOpModule(object):
#     def __init(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return f"Nullop - {self.name}"
#
#     def receive_pulse(self, sender, pulse):
#         return


def parse_modules(puzzle_input, pulse_queue):
    modules = {}
    for line in puzzle_input:
        if line.startswith("%"):  # or
            name, _, *destinations = line[1:].split()
            modules[name] = FlipFlopModule(
                name,
                output_modules=[item.strip(",") for item in destinations],
                pulse_queue=pulse_queue,
            )
        elif line.startswith("&"):  # and
            name, _, *destinations = line[1:].split()
            modules[name] = ConjunctionModule(
                name,
                input_modules=[],
                output_modules=[item.strip(",") for item in destinations],
                pulse_queue=pulse_queue,
            )
        elif line.startswith("broadcaster"):
            name, _, *destinations = line.split()
            modules[name] = BroadcasterModule(
                name,
                output_modules=[item.strip(",") for item in destinations],
                pulse_queue=pulse_queue,
            )
    return modules


def link_up_conjunctions(modules):
    for module in modules.values():
        for output_module in module.output_modules:
            try:
                if hasattr(modules[output_module], "input_modules"):
                    modules[output_module].input_modules[module.name] = 0
            except KeyError:  # nullop?
                continue


def push_button(pulse_queue):
    pulse_queue.append(Pulse("broadcaster", None, 0))


def part_one(input_filename, button_presses=1000):
    puzzle_input = helpers.parse_input(input_filename)
    pulse_queue = deque()
    modules = parse_modules(puzzle_input, pulse_queue)
    link_up_conjunctions(modules)
    high_pulses, low_pulses = 0, 0
    for n in range(button_presses):
        push_button(pulse_queue)
        while pulse_queue:
            pulse = pulse_queue.popleft()
            if pulse.value == 0:
                low_pulses += 1
            elif pulse.value == 1:
                high_pulses += 1
            try:
                modules[pulse.destination_module].receive_pulse(
                    pulse.sender, pulse.value
                )
            except KeyError:  # nullop
                continue
    return high_pulses * low_pulses


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    pulse_queue = deque()
    modules = parse_modules(puzzle_input, pulse_queue)
    link_up_conjunctions(modules)
    qn_pulses = {module: [] for module in modules["qn"].input_modules}
    for n in range(1000000000000000000000000000):
        push_button(pulse_queue)
        while pulse_queue:
            pulse = pulse_queue.popleft()
            if (
                pulse.destination_module == "qn" and pulse.value == 1
            ):  # hard-coded & module that feeds rx
                if not len(qn_pulses[pulse.sender]) > 3:
                    qn_pulses[pulse.sender].append(n + 1)
                if all([len(v) > 3 for v in qn_pulses.values()]):
                    return lcm(*[v[-1] - v[-2] for v in qn_pulses.values()])
            try:
                modules[pulse.destination_module].receive_pulse(
                    pulse.sender, pulse.value
                )
            except KeyError:  # nullop
                continue


if __name__ == "__main__":
    print("*** PART ONE ***\n")
    print(f"Test result = {part_one('inputtest.txt')}\n")
    onestart = time.time()
    p1result = part_one("input.txt")
    oneend = time.time()
    print(f"REAL RESULT = {p1result}")
    print(f"Time = {oneend - onestart}")
    print("\n")
    # NO TEST FOR PART 2 WASTL YOU MONSTER
    twostart = time.time()
    p2result = part_two("input.txt")
    twoend = time.time()
    print(f"REAL RESULT = {p2result}")
    print(f"Time = {twoend - twostart}")
    if p1result:
        pyperclip.copy(p1result)
    elif p2result:
        pyperclip.copy(p2result)
