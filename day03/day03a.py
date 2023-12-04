from dataclasses import dataclass
from typing import List
import re

@dataclass
class NumberWithPosition:
    number: int
    row: int
    col: int
    num_digits: int

@dataclass
class SymbolWithPosition:
    row: int
    col: int

f = open("day03-input.txt")

symbols_regex = r"([^\w.\n])"
numbers_regex = r"(\d+)"

numbers_by_row: List[List[NumberWithPosition]] = []
symbols_by_row: List[List[SymbolWithPosition]] = []

for line in f:
    row = len(symbols_by_row)
    symbols_in_row = []
    for symbol_match in re.finditer(symbols_regex, line):
        #print(symbol_match.groups()[0])
        symbols_in_row.append(SymbolWithPosition(row, symbol_match.start()))
    symbols_by_row.append(symbols_in_row)

    numbers_in_row = []
    for number_match in re.finditer(numbers_regex, line):
        col = number_match.start()
        number_as_string = number_match.groups()[0]
        num_digits = len(number_as_string)
        number = int(number_as_string)
        numbers_in_row.append(NumberWithPosition(number, row, col, num_digits))

    numbers_by_row.append(numbers_in_row)

summed_numbers = 0

for numbers_in_row in numbers_by_row:
    for number in numbers_in_row:
        min_col = number.col - 1
        max_col = number.col + number.num_digits
        found_symbol = False
        for row_to_test in range(number.row - 1, number.row + 2):
            if row_to_test < 0:
                continue
            if row_to_test >= len(symbols_by_row):
                continue
            for symbol in symbols_by_row[row_to_test]:
                if (symbol.col >= min_col) and (symbol.col <= max_col):
                    found_symbol = True
                    break
            if found_symbol:
                break
        print(number.number, found_symbol)
        if found_symbol:
            summed_numbers += number.number

print(summed_numbers)
