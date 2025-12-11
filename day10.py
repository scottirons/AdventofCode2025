import math
from z3 import *

source = "day10.txt"
#source = "sample.txt"

with open(source, 'r') as f:
    data = f.read().split('\n')

# part 1
# recursive search should do the trick, and it's not going to be a huge sample size since we'll use each
# button at most once (if we press it twice, for example, it'll be the same as not pressing it at all).

targets: list[list[int]] = []
options = []
part_2_shenaniganery = []

for line in data:
    split_up = line.split(' ')
    target = split_up[0]
    something_mysterious = split_up[-1]
    curr_options = []

    for i in range(1, len(split_up) - 1):
        no_parentheses = split_up[i][1:-1]
        option = list(map(int, no_parentheses.split(',')))
        curr_options.append(option)
    options.append(curr_options)

    curr_target = []
    for i in range(1, len(target) - 1):
        if target[i] == '.':
            curr_target.append(False)
        else:
            curr_target.append(True)
    targets.append(curr_target)

    something_mysterious_but_without_curly_brackets = something_mysterious[1:-1]
    mysterious_numbers = list(map(int, something_mysterious_but_without_curly_brackets.split(',')))
    part_2_shenaniganery.append(mysterious_numbers)

def update_state(curr_state, curr_move):
    copied_state = curr_state.copy()
    for toggle in curr_move:
        copied_state[toggle] = not curr_state[toggle]
    return copied_state

def search(curr_state: list[bool], curr_size: int, curr_i: int, curr_target_i: int):
    if not curr_state:
        curr_state = [False for _ in targets[curr_target_i]]

    copied_state = curr_state.copy()

    if copied_state == targets[curr_target_i]:
        return curr_size

    if curr_i >= len(options[curr_target_i]):
        return math.inf

    updated_state = update_state(copied_state, options[curr_target_i][curr_i])

    return min(search(copied_state, curr_size, curr_i + 1, curr_target_i),
               search(updated_state, curr_size + 1, curr_i + 1, curr_target_i))

total = 0

for state_index, target_state in enumerate(targets):
    empty_state = [False for _ in target_state]
    include_first_state = update_state(empty_state, options[state_index][0])

    total += min(
        search(empty_state, 0, 1, state_index),
        search(include_first_state, 1, 1, state_index)
    )

print(f"Part 1: {total}")

# ok yea part 2 my intuition is correct that this is just a crazy critter thing to solve on my own. I'll use a
# Python library because so many people on Reddit who are better programmers than me are doing that lol.
# Go figure; this was the first time I've had to bend the rules all year.


def solve_line_with_z3(line_idx: int, opts: list[list[int]], rhs: list[int]):

    num_buttons = len(opts)
    num_rows = len(rhs)

    xs = [Int(f"x_{line_idx}_{j}") for j in range(num_buttons)]
    opt = Optimize()

    for x in xs:
        opt.add(x >= 0)

    for row in range(num_rows):
        terms = [xs[j] for j, rows in enumerate(opts) if row in rows]
        if terms:
            opt.add(Sum(terms) == rhs[row])
        else:
            opt.add(rhs[row] == 0)

    total_presses = Sum(xs)
    opt.minimize(total_presses)

    if opt.check() != sat:
        return None

    model = opt.model()
    presses = [model[x].as_long() for x in xs]
    min_total = model.eval(total_presses).as_long()
    return presses, min_total


all_min_totals = []
all_press_patterns = []

for i, (opts, rhs) in enumerate(zip(options, part_2_shenaniganery)):
    result = solve_line_with_z3(i, opts, rhs)
    if result is None:
        print(f"Line {i} has no solution")
        all_min_totals.append(None)
        all_press_patterns.append(None)
    else:
        presses, min_total = result
        all_min_totals.append(min_total)
        all_press_patterns.append(presses)
        print(f"Line {i}: min total presses = {min_total}, presses = {presses}")

part2_answer = sum(t for t in all_min_totals if t is not None)
print("Part 2 answer:", part2_answer)

