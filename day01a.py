f = open("day01-input.txt", "r")

running_sum = 0
for line in f:
    # find all digits
    digits = [x for x in line if x in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}]
    first_digit = digits[0]
    last_digit = digits[-1]
    both_digits = first_digit + last_digit
    running_sum += int(both_digits)

print("total: ", running_sum)