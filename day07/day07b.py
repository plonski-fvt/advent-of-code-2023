from functools import total_ordering
from typing import List, Tuple
from collections import Counter
import re

character_to_value = {
    "J" : 1,
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "T" : 10,
    "Q" : 12,
    "K" : 13,
    "A" : 14
}

class Card:
    value: int
    def __init__(self, character: str):
        self.value = character_to_value[character]
    
@total_ordering
class Hand:
    cards: List[Card]

    def get_type_value(self):
        card_values_without_j = [card.value for card in self.cards if card.value != 1]

        if len(card_values_without_j) == 0:
            # if they're all js
            return 6

        counter = Counter(card_values_without_j)
        common_card_counts = counter.most_common()
        card_counts = [x[1] for x in common_card_counts]

        num_js = 5 - len(card_values_without_j)
        card_counts[0] += num_js

        if card_counts[0] == 5:
            return 6 # five of a kind
        if card_counts[0] == 4:
            return 5 # four of a kind
        if card_counts[0] == 3:
            if card_counts[1] == 2:
                return 4 # full house
            return 3 # three of a kind
        if card_counts[0] == 2:
            if card_counts[1] == 2:
                return 2 # two pair
            return 1 # one pair
        return 0
    
    def get_cards_value(self):
        multipliers = [0xFFFFFFFF, 0xFFFFFF, 0xFFFF, 0xFF, 1]
        card_values = [card.value for card in self.cards]
        return sum([a * b for a, b in zip(multipliers, card_values)])

    def __init__(self, hand_string: str):
        assert len(hand_string) == 5
        self.cards = []
        for char in hand_string:
            self.cards.append(Card(char))

    def __eq__(self, other):
        if not isinstance(other, Hand):
            return NotImplemented
        return self.cards == other.cards
    
    def __lt__(self, other):
        if not isinstance(other, Hand):
            return NotImplemented
        our_type = self.get_type_value()
        other_type = other.get_type_value()
        print(f"our type {our_type} other type {other_type}")
        if our_type != other_type:
            return our_type < other_type
        return self.get_cards_value() < other.get_cards_value()

hands_and_bids: List[Tuple[Hand, int]] = []
f = open("day07-input.txt")
for line in f:
    match = re.match(r"(\w+) (\d+)", line)
    assert match is not None
    groups = match.groups()
    hand = Hand(groups[0])
    bid = int(groups[1])
    hands_and_bids.append((hand, bid))

# print(hands_and_bids)
hands_and_bids.sort(key=lambda x: x[0])
print([[card.value for card in x[0].cards] for x in hands_and_bids])

answer = 0
for hand_and_bid, rank in zip(hands_and_bids, range(1, len(hands_and_bids) + 1)):
    answer += hand_and_bid[1] * rank

print(answer)