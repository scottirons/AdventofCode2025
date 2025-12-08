import math
from collections import defaultdict

source = "day8.txt"
#source = "sample.txt"

def calc_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)

with open(source, 'r') as f:
    data = f.read().split('\n')

shortest_connections = []
tuple_data = []

for line in data:
    split_line = line.split(',')
    a, b, c = map(int, split_line)
    tuple_data.append((a, b, c))

for i in range(len(tuple_data) - 1):
    for j in range(i + 1, len(tuple_data)):
        a, b = tuple_data[i], tuple_data[j]
        dist = calc_distance(a, b)
        shortest_connections.append((dist, a, b))

shortest_connections.sort(reverse=True)

current_group = 1
circuit_location = defaultdict(int)
circuits = [set()] # Python-esque ha ha
# circuit_groups = defaultdict(set) # 1 connects to 2 so 1: {}; 2 connects to 5 so 2: {5}

num_conns = 0
part_1_conn = 1000 if source == "day8.txt" else 10

while True:

    if num_conns == part_1_conn:
        sizes = [len(circuit) for circuit in circuits]
        sizes.sort(reverse=True)
        print(f"Part 1: {sizes[0] * sizes[1] * sizes[2]}")

    _, a, b = shortest_connections.pop()

    a_group = circuit_location[a]
    b_group = circuit_location[b]

    # only one of the circuits is in a group so far, or they're in different groups
    if a_group != b_group:
        # one of them isn't in a group yet
        if a_group == 0:
            circuits[b_group].add(a)
            circuit_location[a] = b_group

        elif b_group == 0:
            circuits[a_group].add(b)
            circuit_location[b] = a_group

        # they're both in separate groups. check if the groups are already linked together. if not, link them (just move all from b to a I guess lol)...
        else:
            min_g = min(a_group, b_group)
            max_g = max(a_group, b_group)
            circuits[min_g] = circuits[min_g].union(circuits[max_g])
            for box in circuits[max_g]:
                circuit_location[box] = min_g
            circuits[max_g] = set()


    elif a_group == b_group:
        # both are 0; add them to a new circuit group in the list.
        if a_group == 0:
            circuits.append(set())
            circuits[-1].add(a)
            circuits[-1].add(b)
            circuit_location[a] = current_group
            circuit_location[b] = current_group
            current_group += 1
    num_conns += 1
    if len(circuits[1]) == len(tuple_data):
        print(f"Part B: {a[0] * b[0]}")
        break

        # otherwise, they're in the same group already, so nothing to do here. don't really need this, but it's here
        # for completeness and debugging lol
        # wait did I misread this?

# for i in range(1, current_group):
#     if i in visited_groups:
#         continue
#     curr_size = 0
#     curr_set = i
#     combined_set = {i}
#     while curr_set not in visited_groups:
#         curr_size += len(circuits[curr_group])
#         groups = sorted(list(circuit_groups[curr_group]), reverse=True)
#         for group in groups:
#             if group != i and group not in visited_groups:
#                 link_sets.append(group)
#                 visited_groups.add(group)
#     sizes.append(curr_size)


