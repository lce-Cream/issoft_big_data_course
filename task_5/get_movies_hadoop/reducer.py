#!/usr/bin/env python
import sys
import argparse
from itertools import groupby

def parse_cli():
    """
    Returns dictionary like object with parsed arguments from terminal.
    """
    parser = argparse.ArgumentParser(description='reduces to n values')

    parser.add_argument('-n', '--number', help='number of values to reduce',
                        metavar='<int>', type=int)

    return parser.parse_args()

def shuffle(data) -> list:
    '''Returns list of tuples (key: [value1, value2, ...]).'''
    splitted_data = [line.strip().split('\t') for line in data]
    grouped_data = groupby(splitted_data, lambda pair: pair[0])
    return [(key, [x for _, x in group]) for key, group in grouped_data]

def reduce(key: str, values: list, number: int) -> tuple:
    '''Reduces values to given number.'''
    return key, values[:number]

if __name__ == '__main__':
    data = sys.stdin
    args = parse_cli()

    for key, values in shuffle(data):
        result_key, result_value = reduce(key, values, args.number)
        print(f"{result_key}\t{result_value}")
