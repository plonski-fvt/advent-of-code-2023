from dataclasses import dataclass
import re

@dataclass
class Sample:
    num_red: int = 0
    num_green: int = 0
    num_blue: int = 0
    def populate_a_count(self, count: int, color: str):
        if color == "red":
            self.num_red = count
        if color == "green":
            self.num_green = count
        if color == "blue":
            self.num_blue = count

regex_for_game = r"Game (\d+):"
regex_for_squares = r"(\d+) (red|blue|green)([,;\n])"

f = open("day02-input.txt")

sample_to_test = Sample(12, 13, 14)

accumulated_good_games = 0

for line in f:
    game_match = re.search(regex_for_game, line)
    assert game_match is not None
    str_for_game_number = game_match.groups()[0]
    game_number = int(str_for_game_number)

    matches_for_squares = re.findall(regex_for_squares, line)

    samples_in_game = []
    active_sample = Sample(0, 0, 0)    
    for match in matches_for_squares:
        active_sample.populate_a_count(int(match[0]), match[1])
        if match[2] == ";":
            samples_in_game.append(active_sample)
            active_sample = Sample(0, 0, 0)
        if match[2] == "\n":
            samples_in_game.append(active_sample)
    
    print(samples_in_game)

    bad_sample = False
    for sample in samples_in_game:
        if (sample.num_red > sample_to_test.num_red) or (sample.num_green > sample_to_test.num_green) or (sample.num_blue > sample_to_test.num_blue):
            bad_sample = True
            break

    print("game number: {}, bad_sample: {}".format(game_number, bad_sample))

    if not bad_sample:
        accumulated_good_games += game_number

print(accumulated_good_games)






