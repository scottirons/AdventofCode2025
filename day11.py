source = "day11.txt"
source = "sample.txt"

with open(source, 'r') as f:
    data = f.read().split('\n')

connections = {}
reverse_connections = {}

for line in data:
    source, destinations = line.split(": ")
    connections[source] = list(destinations.split(' '))

for start, dests in connections.items():
    for dest in dests:
        if dest in reverse_connections:
            reverse_connections[dest].append(start)
        else:
            reverse_connections[dest] = [start]

# something something actual backtracking this time.
# ok but could I start from outs and just go backwards until I either reach a cycle, reach the end of nothing, or
# reach a 'you'? Yes this is definitely better because it's tracing a single path and not checking options.
# ok in that case I need to still need to backtrack, so wait does this save me any time at all? there's no guarantee
# that a particular path leads from out to start. I'll do both and see what's faster :P

# It probably just makes more sense to do normal backtracking, then... No guarantees there will even be a path to each
# potential out, at least that seems to be the case in the sample input (they do sometimes converge on aaa, though. hmm)