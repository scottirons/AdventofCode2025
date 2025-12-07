from collections import deque

source = "day7.txt"
#source = "sample.txt"

# part a
with open(source, 'r') as f:
    data = f.read().split('\n')

a_splits = set()
visited = set()
queue = deque()

queue.append((0, data[0].index('S')))
visited.add((0, data[0].index('S')))

while queue:
    row, col = queue.popleft()
    next_row = row + 1
    while next_row < len(data) and (next_row, col) not in visited:
        visited.add((next_row, col))
        if data[next_row][col] == '^':
            a_splits.add((next_row, col))
            queue.append((next_row, col - 1)) if (next_row, col - 1) not in visited else None
            queue.append((next_row, col + 1)) if (next_row, col + 1) not in visited else None
            break
        next_row += 1

print(f"Part 1: {len(a_splits)}")
