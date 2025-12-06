source = "day6.txt"
#source = "sample.txt"

with open(source, "r") as f:
    data = f.read().split('\n')

numbers = []
string_nums = []

for i in range(0, len(data) - 1):
    curr_line = data[i]
    numbers.append(list(map(int, curr_line.split())))
    string_nums.append(curr_line)

symbols = list(data[-1].split())

result = 0

for col in range(len(numbers[0])):
    total = 0 if symbols[col] == '+' else 1
    for row in range(len(numbers)):
        if symbols[col] == '+':
            total += numbers[row][col]
        else:
            total *= numbers[row][col]
    result += total

print(f"Part 1: {result}")

# part 2
result = 0
symbol_index = 0
curr_symbol = symbols[symbol_index]
curr_num = 0
curr_total = 1 if curr_symbol == '*' else 0
for col in range(len(string_nums[0])):
    for row in range(len(string_nums)):
        curr_digit = string_nums[row][col]
        if curr_digit != ' ':
            curr_num = curr_num * 10 + int(curr_digit)
    if curr_num == 0:
        result += curr_total
        symbol_index += 1
        curr_symbol = symbols[symbol_index]
        curr_total = 1 if curr_symbol == '*' else 0
    elif curr_symbol == '*':
        curr_total *= curr_num
    else:
        curr_total += curr_num
    curr_num = 0
    if col == len(string_nums[0]) - 1:
        result += curr_total
        break



print(f"Part B: {result}")
