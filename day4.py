source = "day4.txt"
#source = "sample.txt"

dirs = ((0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1))

# part 1
total = 0
with open(source, "r") as f:
    lines = f.read().split("\n")

lines = [list(line) for line in lines]

def no_tp(row, column):
    if row < 0 or column < 0 or row >= len(lines) or column >= len(lines[0]) or lines[row][column] == '.':
        return False
    return True

for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] == '@' and sum(no_tp(r + a, c + b) for a, b in dirs) < 4:
            total += 1

print(f"Part 1: {total}")

# part 2
total = 0
removed = 0
while True:
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if lines[r][c] == '@' and sum(no_tp(r + a, c + b) for a, b in dirs) < 4:
                lines[r][c] = '.'
                removed += 1
    total += removed
    if not removed:
        break
    removed = 0

print(f"Part 2: {total}")