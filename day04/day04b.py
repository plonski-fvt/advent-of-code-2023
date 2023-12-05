import re
from dataclasses import dataclass
from typing import List

@dataclass
class Card:
    id: int
    copied_ids: List[int]

f = open("day04-input.txt")

all_cards = []

for line in f:
    id = len(all_cards)
    numbers = re.findall(r"(\d+)", line)
    card_number = int(numbers[0])
    winning_numbers = [int(x) for x in numbers[1:11]]
    sample_numbers = [int(x) for x in numbers[11:]]
    # print(card_number, winning_numbers, sample_numbers)
    copied_ids = []
    for number in sample_numbers:
        if number in winning_numbers:
            copied_ids.append(id + 1 + len(copied_ids))
    all_cards.append(Card(id, copied_ids))

cards_to_score = all_cards.copy()

total_score = 0
while len(cards_to_score) > 0:
    card_to_score = cards_to_score.pop(-1)
    total_score += 1
    for copied_id in card_to_score.copied_ids:
        if copied_id < len(all_cards):
            cards_to_score.append(all_cards[copied_id])

print(total_score)