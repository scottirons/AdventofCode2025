# part 1

source = "day2.txt"
#source = "sample.txt"

with open(source, "r") as f:
    lines = f.read().split(',')

total = 0
# caching doesn't save time because math operations are O(1)
for line in lines:
    a, b = map(int, line.split("-"))
    for n in range(a, b + 1):
        num_len = len(str(n))
        if num_len % 2 != 0:
            continue
        div_factor = 10 ** (num_len // 2)
        first_half = n // div_factor
        if first_half * div_factor + first_half == n:
            total += n

print(f"Part 1: {total}")

# Part 2
# actually I'll just do string stuff this time...
total = 0
for line in lines:
    a, b = map(int, line.split("-"))
    for n in range(a, b + 1):
        string_n = str(n)
        len_n = len(string_n)
        for i in range(2, len_n + 1):
            if len_n % i == 0:
                size = len_n // i
                split_n = [string_n[j:j+size] for j in range(0, len_n, size)]
                if len(set(split_n)) == 1:
                    total += n
                    break

print(f"Part 2: {total}")