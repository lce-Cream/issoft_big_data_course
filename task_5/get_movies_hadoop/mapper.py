#!/usr/bin/env python
import argparse
import sys
import csv
import re
from typing import Iterator, NamedTuple, Tuple, Union

def parse_cli():
    '''
    Returns dictionary like object with parsed arguments from terminal.
    '''
    parser = argparse.ArgumentParser(description='filter movies by title and year')

    parser.add_argument('-g', '--genres', help='genres to filter for',
                        metavar='<str>', type=str)

    parser.add_argument('-r', '--regex', help='regex to filter for',
                        metavar='<regex>', type=str)

    parser.add_argument('-f', '--year_from', help='year to filter from',
                        metavar='<int>', type=int)

    parser.add_argument('-t', '--year_to', help='year to filter to',
                        metavar='<int>', type=int)

    return parser.parse_args()

def map(line: str) -> Iterator[Union[Tuple[str, Tuple[str, str]], None]]:
    '''
    Yields (genre, (title, year)) pairs or None if movie does not suit
    or line is corrupted.
    '''
    try:
        reader = csv.reader([line])
        _, title, genres = next(reader)
    except:
        return None

    search_result = re.match(r'(.*)[ ]\((\d{4})\)$', title)
    title = search_result.group(1) if search_result else ''
    year = int(search_result.group(2)) if search_result else 0

    for genre in genres.split('|'):
        yield (genre, (title, year))

def movie_filter(key: str, value: Tuple[str, str], filter_rules: NamedTuple) -> bool:
    '''
    Recieves movie and filter rules, returns True if passed movie
    meets these rules and false otherwise.
    '''
    def year_filter(year_from: int, year_to: int, year: int) -> bool:
        '''
        Returns True if passed movie's release year matches given interval,
        False otherwise.
        '''
        if year_from and year_to:
            return year_from <= year <= year_to

        elif year_from and not year_to:
            return year >= year_from

        elif not year_from and year_to:
            return year <= year_to
        else:
            return True

    def regex_filter(regexp: str, title: str) -> bool:
        '''
        Returns True if passed movie's title matches regular expression,
        False otherwise.
        '''
        if regexp:
            return True if re.search(regexp, title, re.IGNORECASE) else False
        else:
            return True

    def genre_filter(request_genres: str, genre: str) -> bool:
        '''Returns True if requested genre expression matches film's genre, False otherwise.'''
        if not request_genres:
            return True

        request_genres = request_genres.lower().split('|')
        genre = genre.lower()
        return genre in request_genres

    genre = key
    title = value[0]
    year = value[1]

    match_genre = genre_filter(filter_rules.genres, genre)
    match_year = year_filter(filter_rules.year_from, filter_rules.year_to, year)
    match_regexp = regex_filter(filter_rules.regex, title)

    return True if match_genre and match_year and match_regexp else False

def is_header(first_line: str) -> bool:
    '''Detects csv file header.'''
    search_result = re.match(r'[a-z]+,[a-z]+,[a-z]+', first_line, re.I)
    return bool(search_result)

if __name__ == '__main__':
    filter_args = parse_cli()
    data = sys.stdin

    first_line = data.readline()
    if not is_header(first_line):
        for key, value in map(first_line):
            if movie_filter(key, value, filter_args):
                print(f"{key}\t{value}")

    for line in data:
        for key, value in map(line):
            if movie_filter(key, value, filter_args):
                print(f"{key}\t{value}")
