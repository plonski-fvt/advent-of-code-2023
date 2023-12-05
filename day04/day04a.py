import re

f = open("day04-input.txt")

num_points_sum = 0

for line in f:
    numbers = re.findall(r"(\d+)", line)
    card_number = int(numbers[0])
    winning_numbers = [int(x) for x in numbers[1:11]]
    sample_numbers = [int(x) for x in numbers[11:]]
    # print(card_number, winning_numbers, sample_numbers)
    num_matches = 0
    for number in sample_numbers:
        if number in winning_numbers:
            num_matches += 1
    if num_matches == 0:
        continue
    num_points = 2 ** (num_matches - 1)
    num_points_sum += num_points

print(num_points_sum)