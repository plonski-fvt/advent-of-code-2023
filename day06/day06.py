import math

def compute_num_ways_to_win(race_time, distance):
    # we want d > distance, where d = (race_time - charge_time) * charge_time
    # d = -charge_time^2 + race_time * charge_time
    # the roots occur where:
    # charge_time^2 - race_time * charge_time + distance = 0
    # so we use the quadratic formula

    first_root = 0.5 * (race_time - math.sqrt(race_time ** 2 - 4 * distance))
    second_root = 0.5 * (race_time + math.sqrt(race_time ** 2 - 4 * distance))

    print(first_root, second_root)

    first_winner = math.ceil(first_root)
    last_winner = math.floor(second_root)

    return 1 + last_winner - first_winner

first_answer = compute_num_ways_to_win(60, 475) * compute_num_ways_to_win(94, 2138) * compute_num_ways_to_win(78, 1015) * compute_num_ways_to_win(82, 1650)

print(first_answer)

second_answer = compute_num_ways_to_win(60947882, 475213810151650)

print(second_answer)