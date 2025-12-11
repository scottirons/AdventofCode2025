from collections import defaultdict
from functools import cache

source = "day11.txt"
#source = "sample.txt"

with open(source, 'r') as f:
    data = f.read().split('\n')

connections = {}
reverse_connections = {}

for line in data:
    source, destinations = line.split(": ")
    connections[source] = list(destinations.split(' '))

reaches_end = set()
paths = defaultdict(int)

@cache
def dfs(curr_loc, start, target):

    if curr_loc == target:
        return 1
    elif curr_loc not in connections:
        return 0
    return sum(dfs(loc, start, target) for loc in connections[curr_loc])

num_paths = dfs('you', 'you', 'out')

print(f'Part 1: {num_paths}')

# find all paths from svr to fft, fft to dac, dac to out, svr to dac, dac to fft, fft to out
svr_dac_fft_out = dfs('svr', 'svr', 'fft') * dfs('fft', 'fft', 'dac') * dfs('dac', 'dac', 'out')
svr_fft_dac_out = dfs('svr', 'svr', 'dac') * dfs('dac', 'dac', 'fft') * dfs('fft', 'fft', 'out')

print("Part 2:", svr_dac_fft_out + svr_fft_dac_out)