source = 'day12.txt'
#source = 'sample.txt'

with open(source) as f:
    data = f.read().rstrip()
    groups = data.split('\n\n')

dimensions = []
target_counts = []
shape_sizes = []

targets = groups.pop().split('\n')

for target in targets:
    dims, counts = target.split(': ')
    dimensions.append(list(map(int, dims.split('x'))))
    target_counts.append(list(map(int, counts.split(' '))))

for shape in groups:
    shape_sizes.append(shape.count('#'))

# part 1
total_a_maybe = 0
total_a_def = 0
for i in range(len(dimensions)):
    a, b = dimensions[i][0], dimensions[i][1]
    total_size = a * b
    total_presents = sum(target_counts[i])
    if total_presents <= (a // 3) * (b // 3):
        total_a_def += 1
    for j, target_count in enumerate(target_counts[i]):
        total_size -= shape_sizes[j] * target_count
    if total_size >= 0:
        total_a_maybe += 1

print(f'Part 1: {total_a_maybe} maybes. {total_a_def} definitely.')