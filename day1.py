source = "day1.txt"

# part 1
with open(source, "r") as f:
    lines = f.read().splitlines()

n = 50
count = 0

for line in lines:
    if line[0] == 'L':
        n = (n - int(line[1:])) % 100
    else:
        n = (n + int(line[1:])) % 100
    if n == 0:
        count += 1

print(f"Part 1: {count}")

# part 2
count = 0
n = 50
for line in lines:
    direction, steps = line[0], int(line[1:])
    # print(f"n = {n}, d = {direction}, steps = {steps}, count = {count}")
    if direction == 'L':
        if steps >= n:
            if n != 0:
                count += 1
            count += (steps - n) // 100
        n = (n - steps) % 100
    else:
        if n + steps >= 100:
            count += 1
            count += (steps - (100 - n)) // 100
        n = (n + steps) % 100

print(f"Part 2: {count}")