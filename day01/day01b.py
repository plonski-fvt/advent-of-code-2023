import re

regex_string = r"0|1|2|3|4|5|6|7|8|9|zero|one|two|three|four|five|six|seven|eight|nine"
digit_to_int = {"zero": 0,
                "one" : 1,
                "two" : 2,
                "three" : 3,
                "four" : 4,
                "five": 5, 
                "six": 6,
                "seven": 7,
                "eight": 8,
                "nine": 9}

f = open("day01-input.txt", "r")

running_sum = 0

for line in f:
    first_digit_match = re.search(regex_string, line)
    assert first_digit_match is not None
    first_digit = first_digit_match.group()
    try:
        first_digit_as_int = int(first_digit)
    except:
        first_digit_as_int = digit_to_int[first_digit]

    last_digit_match = re.search(regex_string[::-1], line[::-1])
    assert last_digit_match is not None
    last_digit = last_digit_match.group()[::-1]
    try:
        last_digit_as_int = int(last_digit)
    except:
        last_digit_as_int = digit_to_int[last_digit]

    combined = 10 * first_digit_as_int + last_digit_as_int
    # print(line)
    # print(combined)
    running_sum += combined

print(running_sum)
        