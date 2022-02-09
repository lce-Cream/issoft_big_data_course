#!/usr/bin/env python
import sys
from itertools import groupby

def shuffle(data) -> list:
    '''Returns list of tuples (key: [value1, value2, ...]).'''
    splitted_data = [line.strip().split('\t') for line in data]
    grouped_data = groupby(splitted_data, lambda pair: pair[0])
    return [(key, [x for _, x in group]) for key, group in grouped_data]

def reduce(word, values) -> tuple:
    '''Reduces values by making sum.'''
    return word, sum(map(int, values))

if __name__ == "__main__":
    data = sys.stdin
    for key, values in shuffle(data):
        result_key, result_value = reduce(key, values)
        print(f"{result_key}\t{result_value}")
