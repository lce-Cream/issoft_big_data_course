import sys
import argparse
from itertools import groupby
from typing import TextIO, List, Tuple

def parse_cli():
    """
    Returns dictionary like object with parsed arguments from terminal.
    """
    parser = argparse.ArgumentParser(description='reduces to n values')

    parser.add_argument('-n', '--number', help='number of values to reduce',
                        metavar='<int>', type=int)

    return parser.parse_args()

def shuffle(data: TextIO, num_reducers: int=1) -> List[Tuple[str, List[str]]]:
    '''Returns list of tuples (key: [value1, value2, ...]).'''
    result = []
    splitted_data = [line.strip().split('\t') for line in sys.stdin]
    grouped_data = groupby(splitted_data, lambda pair: pair[0])
    shuffled_items = [(key, [x for _, x in group]) for key, group in grouped_data]

    def per_reducer(items: list, reducers: int) -> int:
        '''
        Returns optimal number of items which
        should be processed by one reducer.
        '''
        num_items_per_reducer = len(items) // reducers
        if len(items) / reducers != num_items_per_reducer:
            num_items_per_reducer += 1
        return num_items_per_reducer
    
    items_per_reducer = per_reducer(shuffled_items, num_reducers)

    for i in range(num_reducers):
        start = items_per_reducer*i
        finish = items_per_reducer*(i+1)
        result.append(shuffled_items[start:finish])

    return result

def reduce(key: str, values: List[Tuple[str, str]], number: int) -> Tuple[str, List[Tuple[str, str]]]:
    '''Reduces values to given number.'''
    return key, values[:number]

if __name__ == '__main__':
    data = sys.stdin
    args = parse_cli()

    for group in shuffle(data):
        for key, values in group:
            result_key, result_value = reduce(key, values, args.number)
            print(f"{result_key}\t{result_value}")
