from collections import defaultdict

source = "day9.txt"
#source = "sample.txt"

with open(source, 'r') as f:
    lines = f.read().split('\n')

coords = []

for line in lines:
    a, b = line.split(',')
    coords.append((int(a), int(b)))

max_area = 0

for i in range(len(coords) - 1):
    row_a, col_a = coords[i]
    for j in range(i + 1, len(coords)):
        row_b, col_b = coords[j]
        row_size = abs(row_a - row_b) + 1
        col_size = abs(col_a - col_b) + 1
        max_area = max(row_size * col_size, max_area)

print(f'Part 1: {max_area}')

# part 2
# maybe raycast sorta thing. Like if horizontal potential rectangle sides cross multiple vertical lines (that aren't adjacent),
# then the rectangle is invalid. if vertical potential sides cross multiple non-adjacent horizontal lines, invalid

# but that doesn't really work if one of the points of the rectangle is just a point inside the shape.
# maybe some sort of clockwise/counter clockwise winding type of thing. like if the points are all CCW, then anything
# to the left is always inside the shape. I can use that logic potentially to determine valid trials.

# I don't think it's possible to just keep a list of all points inside the shape; that's probably too much space and
# too much runtime.

# determine if we're always making a turn at a vertex
# A B
# C B
# C D
# E D
# E F
# . F

# then, use shoelace to determine if it's clockwise or counterclockwise
# If it's counter clockwise, any left turn means that backwards and left are the only valid directions inside the
# shape. If it's a right turn, then any direction is valid to remain inside the polygon.

# then, use the logic above with a set of horizontal points, a set of vertical points, and a set of vertices with their
# relevant "contained"-ness. (0, 1), (0, -1), (1, 0), (-1, 0). When checking if a horizontal point is valid inside
# a candidate rectangle, if it crosses over a point in the vertical set, the candidate is invalid, unless the
# point immediately after is also in the vertical set TODO: is this actually possible/will it show up ever??
# same thing for checking the vertical components of a candidate rectantle
# if the candidate side crosses over a vertex, just make sure the current direction of travel is a valid
# "to the middle" direction for that particular vertex. For example, if I'm checking if I can go from point B up
# to point A in a candidate rectangle and I pass across point C halfway there. if (-1, 0) is a valid "inward" direction
# from point C, then continue checking. Otherwise, discard the candidate rectangle.

# only try to go between points when the candidate vertices have valid inward directionality that align with the
# sides of the candidate rectangle. For example, for a left turn with right (0, 1) and down (1, 0) directionality,
# don't try to create a candidate rectangle if the other potential vertex is either further up (-1, 0) or further left
# (0, -1) from it.

inward_dirs = defaultdict(set)
horizontal = set()
vertical = set()

# determine if clockwise or counter
# if total left turns is more, counter, else clockwise
lefts, rights = 0, 0

def normalize(pair):
    first, second = pair
    if first >= 1:
        first = 1
    elif first <= -1:
        first = -1
    if second >= 1:
        second = 1
    elif second <= -1:
        second = -1

    return first, second

def add_horizontal(start, end, l_r):
    if l_r == (0, -1):
        begin = start[1] - 1
    else:
        begin = start[1] + 1

    for column in range(begin, end[1], l_r[1]):
        horizontal.add((start[0], column))

def add_vertical(start, end, u_d):
    if u_d == (1, 0):
        begin = start[0] + 1
    else:
        begin = start[0] - 1

    for row in range(begin, end[0], u_d[0]):
        vertical.add((row, start[1]))

# right, up, left, down
dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]
horizontal_dirs = {(0, 1), (0, -1)}
vertical_dirs = {(1, 0), (-1, 0)}

a, b = coords[0], coords[1]

dif = (b[0] - a[0], b[1] - a[1])
curr_dir = normalize(dif)
if curr_dir in horizontal_dirs:
    add_horizontal(a, b, curr_dir)
else:
    add_vertical(a, b, curr_dir)

start_dir = curr_dir

for i in range(2, len(coords)):
    c = coords[i]
    next_dif = (c[0] - b[0], c[1] - b[1])
    next_dir = normalize(next_dif)
    dir_i_next = dirs.index(next_dir)
    dir_i_curr = dirs.index(curr_dir)
    if dir_i_next - dir_i_curr in {1, -3}:
        inward_dirs[b].add(dirs[(dir_i_curr + 2) % 4])
        inward_dirs[b].add(next_dir)
    else:
        for direction in dirs:
            inward_dirs[b].add(direction)
    curr_dir = next_dir
    a, b = b, c
    if curr_dir in horizontal_dirs:
        add_horizontal(a, b, curr_dir)
    else:
        add_vertical(a, b, curr_dir)

# looping back to start
c = coords[0]
next_dif = (c[0] - b[0], c[1] - b[1])
next_dir = normalize(next_dif)
dir_i_next = dirs.index(next_dir)
dir_i_curr = dirs.index(curr_dir)
if dir_i_next - dir_i_curr in {1, -3}:
    inward_dirs[b].add((dir_i_curr + 2) % 4)
    inward_dirs[b].add(next_dir)
else:
    for direction in dirs:
        inward_dirs[b].add(direction)
curr_dir = next_dir
a, b = b, c
if curr_dir in horizontal_dirs:
    add_horizontal(a, b, curr_dir)
else:
    add_vertical(a, b, curr_dir)

start_dir_i = dirs.index(start_dir)
curr_dir_i = dirs.index(curr_dir)

if start_dir_i - curr_dir_i in {1, -3}:
    inward_dirs[b].add((curr_dir_i + 2) % 4)
    inward_dirs[b].add(start_dir)
else:
    for direction in dirs:
        inward_dirs[b].add(direction)

max_area_b = 0

valid_moves_in_dir = {}

for key, directions in inward_dirs.items():
    valid_moves_in_dir[key] = {}
    for direction in directions:
        valid_moves_in_dir[key][direction] = 0


# now check coordinate
for i in range(len(coords) - 1):
    cand_a = coords[i]
    print(f"Checking index {i}")
    for j in range(i + 1, len(coords)):
        cand_b = coords[j]
        if cand_a == (9, 7) and cand_b == (2, 5):
            pass
        # determine bounds of candidate rectangle
        top, bottom = min(cand_a[0], cand_b[0]), max(cand_a[0], cand_b[0])
        left, right = min(cand_a[1], cand_b[1]), max(cand_a[1], cand_b[1])

        # let's just ignore horizontal and vertical now. No way they're going to be the largest. Right??
        if top == bottom or left == right:
            continue

        valid_candidate = True
        width = right - left + 1
        height = bottom - top + 1
        if width * height < max_area_b:
            continue

        # determine if we have an TL-BR or BL-TR situation
        # doesn't matter which of the candidates it is.
        if (top, left) in {cand_a, cand_b}:

            # try from top, left to top, right
            # dir == (0, 1)
            # I believe in the something somethingness but I can just check not all the way to the edge
            # because if the second to last point is an invalid corner, then we're cooked
            if (0, 1) in inward_dirs[(top, left)]:
                start, end = left, right
                start = start + valid_moves_in_dir[(top, left)][(0, 1)]
                for k in range(start, end):
                    if (top, k) in inward_dirs and (0, 1) not in inward_dirs[(top, k)]:
                        valid_candidate = False
                        break
                    elif (top, k) in vertical:
                        valid_candidate = False
                        break
                    valid_moves_in_dir[(top, left)][(0, 1)] += 1
            else:
                continue

            # don't need to keep checking if we're already at an invalid candidate
            if not valid_candidate:
                continue

            # now going from top left to bottom left
            if (1, 0) in inward_dirs[(top, left)]:
                start, end = top, bottom
                start = start + valid_moves_in_dir[(top, left)][(1, 0)]
                for k in range(start, end):
                    if (k, left) in inward_dirs and (1, 0) not in inward_dirs[(k, left)]:
                        valid_candidate = False
                        break
                    elif (k, left) in horizontal:
                        valid_candidate = False
                        break
                    valid_moves_in_dir[(top, left)][(1, 0)] += 1
            else:
                continue

            if not valid_candidate:
                continue

            # now going from bottom right to bottom left
            if (0, -1) in inward_dirs[(bottom, right)]:
                start, end = right, left
                start = start - valid_moves_in_dir[(bottom, right)][(0, -1)]
                for k in range(start, end, -1):
                    if (bottom, k) in inward_dirs and (0, -1) not in inward_dirs[(bottom, k)]:
                        valid_candidate = False
                        break
                    elif (bottom, k) in vertical:
                        valid_candidate = False
                        break
                    valid_moves_in_dir[(bottom, right)][(0, -1)] += 1
            else:
                continue

            if not valid_candidate:
                continue

            # bottom right to top right
            if (-1, 0) in inward_dirs[(bottom, right)]:
                start, end = bottom, top
                start = start - valid_moves_in_dir[(bottom, right)][(-1, 0)]
                for k in range(start, end, -1):
                    if (k, right) in inward_dirs and (-1, 0) not in inward_dirs[(k, right)]:
                        valid_candidate = False
                        break
                    elif (k, right) in horizontal:
                        valid_candidate = False
                        break
                    valid_moves_in_dir[(bottom, right)][(-1, 0)] += 1
            else:
                continue

        # otherwise, we're in a BL-TR situation
        else:

            # try from bottom left to bottom right
            if (0, 1) in inward_dirs[(bottom, left)]:
                start, end = left, right
                start = start + valid_moves_in_dir[(bottom, left)][(0, 1)]
                for k in range(start, end):
                    if (bottom, k) in inward_dirs and (0, 1) not in inward_dirs[(bottom, k)]:
                        valid_candidate = False
                        break
                    elif (bottom, k) in vertical:
                        valid_candidate = False
                        break
                    valid_moves_in_dir[(bottom, left)][(0, 1)] += 1
            else:
                continue

            # bottom left to top left
            if (-1, 0) in inward_dirs[(bottom, left)]:
                start, end = bottom, top
                start = start - valid_moves_in_dir[(bottom, left)][(-1, 0)]
                for k in range(start, end, -1):
                    if (k, left) in inward_dirs and (-1, 0) not in inward_dirs[(k, left)]:
                        valid_candidate = False
                        break
                    elif (k, left) in horizontal:
                        valid_candidate = False
                        break
                    valid_moves_in_dir[(bottom, left)][(-1, 0)] += 1
            else:
                continue

            # now top right to top left
            if (0, -1) in inward_dirs[(top, right)]:
                start, end = right, left
                start = start - valid_moves_in_dir[(top, right)][(0, -1)]
                for k in range(start, end, -1):
                    if (top, k) in inward_dirs and (0, -1) not in inward_dirs[(top, k)]:
                        valid_candidate = False
                        break
                    elif (top, k) in vertical:
                        valid_candidate = False
                        break
                    valid_moves_in_dir[(top, right)][(0, -1)] += 1
            else:
                continue

            # top right to bottom right
            if (1, 0) in inward_dirs[(top, right)]:
                start, end = top, bottom
                start = start + valid_moves_in_dir[(top, right)][(1, 0)]
                for k in range(start, end):
                    if (k, right) in inward_dirs and (1, 0) not in inward_dirs[(k, right)]:
                        valid_candidate = False
                        break
                    elif (k, right) in horizontal:
                        valid_candidate = False
                    valid_moves_in_dir[(top, right)][(1, 0)] += 1
            else:
                continue

        if valid_candidate:
            #print(cand_a, cand_b, f'area = {width * height}')
            max_area_b = max(max_area_b, width * height)

print(f"Part 2: {max_area_b}")


# ok it's clockwise lol lefts are greater than rights
#print(f"Total lefts: {lefts}, total rights: {rights}")
