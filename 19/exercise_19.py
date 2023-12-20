import re
import time
from collections import namedtuple
from copy import deepcopy
from math import prod

import pyperclip

from helpers import helpers

Rule = namedtuple("Rule", ["attribute", "comparator", "value", "destination"])

Workflow = namedtuple("Workflow", ["name", "rules"])


def parse_part(part):
    x, m, a, s = [int(subpart.split("=")[1]) for subpart in part[1:-1].split(",")]
    return {"x": x, "m": m, "a": a, "s": s}


def parse_workflow(workflow):
    name, rules = workflow.split("{")
    rules = rules.split(",")
    parsed_rules = []
    for rule in rules:
        rule = rule.strip("}")
        if ">" in rule or "<" in rule:
            attribute = rule.split(">")[0] if ">" in rule else rule.split("<")[0]
            comparator = ">" if ">" in rule else "<"
            value = int(re.search("[0-9]+", rule)[0])
            destination = rule.split(":")[1]
            parsed_rules.append(Rule(attribute, comparator, value, destination))
        else:
            parsed_rules.append(Rule(None, None, None, rule))
    return name, parsed_rules


def process_workflows(part, workflows, workflow="in"):
    rules = workflows[workflow]
    while True:
        for rule in rules:
            if rule.comparator:
                if rule.comparator == ">":
                    if part[rule.attribute] > rule.value:
                        if rule.destination in "AR":
                            return rule.destination
                        else:
                            return process_workflows(
                                part, workflows, workflow=rule.destination
                            )
                elif rule.comparator == "<":
                    if part[rule.attribute] < rule.value:
                        if rule.destination in "AR":
                            return rule.destination
                        else:
                            return process_workflows(
                                part, workflows, workflow=rule.destination
                            )
            else:
                if rule.destination in "AR":
                    return rule.destination
                else:
                    return process_workflows(part, workflows, workflow=rule.destination)


def part_one(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    parts = []
    workflows = {}
    score = 0
    for line in puzzle_input:
        if not line:
            break
        else:
            name, rules = parse_workflow(line)
            workflows[name] = rules
    for line in puzzle_input:
        if line.startswith("{"):
            parts.append(parse_part(line))
    for part in parts:
        if process_workflows(part, workflows) == "A":
            score += sum(part.values())
    return score


def get_big_range():
    return {attribute: {"min": 1, "max": 4000} for attribute in "xmas"}


def is_valid_range(rng):
    return all([rng[attribute]["min"] <= rng[attribute]["max"] for attribute in rng])


def get_value(rng):
    return prod(
        [(rng[attribute]["max"] - rng[attribute]["min"]) + 1 for attribute in "xmas"]
    )


def process_workflows_too(rng, workflows, workflow="in"):
    rules = workflows[workflow]
    for rule in rules:
        if not is_valid_range(rng):
            return 0

        if rule.comparator:
            if rule.comparator == ">":
                if (
                    rng[rule.attribute]["min"] < rule.value < rng[rule.attribute]["max"]
                ):  # value falls in the middle, need to split the range
                    # positive case
                    pos_rule = deepcopy(rng)
                    pos_rule[rule.attribute]["min"] = rule.value + 1

                    # negative case
                    neg_rule = deepcopy(rng)
                    neg_rule[rule.attribute]["max"] = rule.value

                    return sum(
                        [
                            process_workflows_too(
                                case_rng, workflows, workflow=workflow
                            )
                            for case_rng in [pos_rule, neg_rule]
                        ]
                    )

                elif rng[rule.attribute]["max"] <= rule.value:  # fully negative
                    continue  # process next rule

                elif rng[rule.attribute]["min"] > rule.value:  # fully positive
                    if rule.destination == "A":
                        return get_value(rng)
                    elif rule.destination == "R":
                        return 0
                    else:
                        return process_workflows_too(
                            rng, workflows, workflow=rule.destination
                        )
                raise Exception("WTF, mate?")

            if rule.comparator == "<":
                if (
                    rng[rule.attribute]["min"] < rule.value < rng[rule.attribute]["max"]
                ):  # value falls in the middle, need to split the range
                    # positive case
                    pos_rule = deepcopy(rng)
                    pos_rule[rule.attribute]["max"] = rule.value - 1

                    # negative case
                    neg_rule = deepcopy(rng)
                    neg_rule[rule.attribute]["min"] = rule.value

                    return sum(
                        [
                            process_workflows_too(
                                case_rng, workflows, workflow=workflow
                            )
                            for case_rng in [pos_rule, neg_rule]
                        ]
                    )

                elif rng[rule.attribute]["min"] >= rule.value:  # fully negative
                    continue  # process next rule
                elif rng[rule.attribute]["max"] < rule.value:  # fully positive
                    if rule.destination == "A":
                        return get_value(rng)
                    elif rule.destination == "R":
                        return 0
                    else:
                        return process_workflows_too(
                            rng, workflows, workflow=rule.destination
                        )
                raise Exception("WTF, mate?")

        else:
            if rule.destination == "A":
                return get_value(rng)
            elif rule.destination == "R":
                return 0
            else:
                return process_workflows_too(rng, workflows, workflow=rule.destination)


def part_two(input_filename):
    puzzle_input = helpers.parse_input(input_filename)
    bigrange = get_big_range()
    workflows = {}
    for line in puzzle_input:
        if not line:
            break
        else:
            name, rules = parse_workflow(line)
            workflows[name] = rules
    score = process_workflows_too(bigrange, workflows, workflow="in")
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
