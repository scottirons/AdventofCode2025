
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