from collections import deque, defaultdict
from heapq import heappush, heappop

source = "day7.txt"
#source = "sample.txt"

# part 1
with open(source, 'r') as f:
    data = f.read().split('\n')

a_splits = set()
visited = set()
queue = deque()

start_col = data[0].index('S')

queue.append((0, start_col))
visited.add((0, start_col))

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

# part 2
# memo should be a dict instead of a set where I keep track of the running total of paths that led to the point.
# so if coords in memo, increment amount. then carry on that amount to the next split and increment/set the memos of the
# L/R points to the carried on value
heap = [(0, start_col)]
visited_count = defaultdict(int, {(0, start_col): 1})
b_result = 0

while heap:
    row, col = heappop(heap)
    curr_count = visited_count[(row, col)]
    next_row = row + 1
    while next_row < len(data):
        if data[next_row][col] == '^':
            heappush(heap, (next_row, col - 1)) if (next_row, col - 1) not in visited_count else None
            heappush(heap, (next_row, col + 1)) if (next_row, col + 1) not in visited_count else None
            visited_count[(next_row, col - 1)] += curr_count
            visited_count[(next_row, col + 1)] += curr_count
            break
        next_row += 1
    if next_row == len(data):
        b_result += curr_count

print(f"Part 2: {b_result}")