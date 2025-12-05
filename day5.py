source = "day5.txt"
#source = "sample.txt"

# part 1
total = 0
with open(source, "r") as f:
    a, b = f.read().split('\n\n')

ranges = list(map(lambda x: (int(x[0]), int(x[1])), (r.split('-') for r in a.split('\n'))))

ingredients = list(map(int, b.split('\n')))

for ingredient in ingredients:
    for interval in ranges:
        if interval[0] <= ingredient <= interval[1]:
            total += 1
            break

print(f"Part 1: {total}")

# part 2
ranges.sort()

# merge ranges where relevant
merged_ranges = []
i = 0
while i < len(ranges):
    a, b = ranges[i][0], ranges[i][1]
    j = i + 1
    while j < len(ranges):
        low, high = ranges[j][0], ranges[j][1]
        if a <= low <= b:
            b = max(b, high)
        else:
            break
        j += 1
    merged_ranges.append((a, b))
    i = j

total = sum(b - a + 1 for a, b in merged_ranges)
print(f"Part 2: {total}")