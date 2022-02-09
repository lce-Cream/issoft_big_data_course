#!/usr/bin/env python
import re
import csv
import argparse

from collections import namedtuple
from pyspark import SparkContext, rdd
from typing import List, NamedTuple, Tuple, Union

def parse_cli() -> NamedTuple:
    '''
    Returns dictionary like object with parsed arguments from terminal.
    '''
    parser = argparse.ArgumentParser(description='filter movies by title, year or regexp')

    parser.add_argument('-g', '--genres', help='genres to filter for',
                        metavar='<str>', type=str)

    parser.add_argument('-r', '--regex', help='regex to filter for',
                        metavar='<regex>', type=str)

    parser.add_argument('-f', '--year_from', help='year to filter from',
                        metavar='<int>', type=int)

    parser.add_argument('-t', '--year_to', help='year to filter to',
                        metavar='<int>', type=int)

    parser.add_argument('-n', '--number', help='number of movies in each genre',
                        metavar='<int>', type=int)

    parser.add_argument('-u', '--user', help='username for program execution',
                        metavar='<str>', type=str)

    parser.add_argument('-m', '--movies', help='movies csv file',
                        metavar='<str>', type=str)

    parser.add_argument('-a', '--ratings', help='ratings csv file',
                        metavar='<str>', type=str)

    return parser.parse_args()

def read_data(path: str) -> rdd:
    '''Read csv file into rdd and skip it's header.'''
    try:
        raw_data = sc.textFile(path)
        header = raw_data.first()
        rdd_data = raw_data.filter((lambda row: row!=header))
    except Exception as e:
        print(e)
        raise SystemExit
    return rdd_data

def normalize_movie(line) -> Union[List[Tuple[int, Tuple[str, int, str]]], None]:
    '''Split line and return this line for every genre movie has.'''
    try:
        reader = csv.reader([line])
        id, title, genres = next(reader)
    except:
        return None

    search_result = re.match(r'(.*)[ ]\((\d{4})\)$', title)

    genres = genres.split('|')
    title = search_result.group(1) if search_result else ''
    year = int(search_result.group(2)) if search_result else 0

    return [(int(id), (title, year, genre)) for genre in genres]

def normalize_rating(line) -> Union[Tuple[int, Tuple[float, int]], None]:
    '''Split line and use only movie id and rating.'''
    try:
        reader = csv.reader([line])
        _, movie_id, rating, _ = next(reader)
    except:
        return None

    return int(movie_id), [float(rating), 1]

def movie_filter(line: Tuple[int, Tuple[str, int, str]], filter_rules: NamedTuple) -> bool:
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

    # (1, ('Toy Story', 1995, 'Adventure'))
    title = line[1][0]
    year =  line[1][1]
    genre = line[1][2]

    match_genre = genre_filter(filter_rules.genres, genre)
    match_year = year_filter(filter_rules.year_from, filter_rules.year_to, year)
    match_regexp = regex_filter(filter_rules.regex, title)

    return True if match_genre and match_year and match_regexp else False

def to_csv(rdd) -> rdd:
    '''Convert rdd for csv like output ready format.'''
    def flatten(movie):
        '''Reorganize movie line.'''
        _, (title, year, genre, rating) = movie
        return genre, title, year, round(rating, 1)

    rdd = rdd \
            .map(flatten) \
            .sortBy(lambda line: (line[0], -line[2], -line[3]), ascending=True) \
            .map(lambda line: ','.join(map(str, line)))

    rdd_header = sc.parallelize(["genre,title,year,rating"])
    return rdd_header.union(rdd)

def get_movies(cli_args: NamedTuple) -> rdd:
    '''Returns rdd with requested movies.'''

    def reduce(rdd_movies_ratings, N: int=None):
        '''Reduce number of movies in each genre to this number.'''
        return rdd_movies_ratings \
                .sortBy(lambda line: (line[1][2], line[1][1], line[1][3]), ascending=False) \
                .groupBy(lambda line: line[1][2]) \
                .flatMap(lambda line: list(line[1])[:N])

    Rule = namedtuple('Rule', ['regex', 'genres', 'year_from', 'year_to'])
    rules = Rule(cli_args.regex, cli_args.genres, cli_args.year_from, cli_args.year_to)

    rdd_movies  = read_data(f"/user/{cli_args.user}/{cli_args.movies}")
    rdd_ratings = read_data(f"/user/{cli_args.user}/{cli_args.ratings}")

    rdd_normalized_and_filtered_movies = \
    rdd_movies \
        .flatMap(normalize_movie) \
        .filter(lambda movie: movie_filter(movie, rules))

    # sum ratings and counts accordingly
    # divide sum of ratings on their count
    rdd_average_ratings = \
    rdd_ratings \
        .map(normalize_rating) \
        .reduceByKey(lambda a, b: [a[0]+b[0], a[1]+b[1]]) \
        .mapValues(lambda value: value[0]/value[1])

    rdd_movies_ratings = \
    rdd_normalized_and_filtered_movies \
        .join(rdd_average_ratings) \
        .mapValues(lambda values: (values[0][0], values[0][1], values[0][2], values[1]))

    return reduce(rdd_movies_ratings, cli_args.number)

if __name__ == "__main__":
    sc = SparkContext("local[*]", "get_movies")
    cli_args = parse_cli()

    rdd_result = get_movies(cli_args)
    to_csv(rdd_result).saveAsTextFile("output")
