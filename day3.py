source = "day3.txt"
#source = "sample.txt"

with open(source, "r") as f:
    lines = f.read().split()

# part 1
total = 0
for line in lines:
    a, b = '0', '0'
    for i, jolt in enumerate(line):
        if jolt > a and i != len(line) - 1:
            a = jolt
            b = '0'
        elif jolt > b:
            b = jolt
    total += int(a) * 10 + int(b)

print(f"Part 1: {total}")

# part 2
total = 0
for line in lines:
    curr_num = list(line[-12:])
    for i in range(-13, -len(line) - 1, -1):
        curr_char = line[i]
        j = 0
        while j < 12 and curr_char >= curr_num[j]:
            curr_char, curr_num[j] = curr_num[j], curr_char
            j += 1

    total += int(''.join(curr_num))

print(f"Part 2: {total}")