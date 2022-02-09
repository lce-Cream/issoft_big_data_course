# python 3.8.2
import yaml
import csv
import re

from utility.decorators import request_time_used
from utility.parser import cli_parser
from utility.cache import make_cache

# вопросы:
# использовать import typing или достаточно таких вот примитивных аннотаций как в коде?
# стоит ли разбивать на классы дальше или такое количество методов в одном классе здесь терпимо?

_DEBUG = True

class Movie:
    '''
    Allows to make requests for movies csv file, request run time is faster
    if rules are specified more detailed. Memory efficiency does not depend from
    request detailization.
    '''
    def __init__(self) -> None:
        '''Set up Movie class instance with paths to csv files.'''
        self.config = {
            'sort_rules': 'rating desc',
            'title_regexp': r'(.*)[ ]\((\d{4})\)$',
            'movies_path': 'movies.csv',
            'ratings_path': 'ratings.csv',
            'cache_path': 'cache.csv'
            }

        try:
            with open('config.yaml', 'r') as config:
                json_config = yaml.safe_load(config)
                self.config.update(json_config)
        except FileNotFoundError as ex:
            print('config.yaml not found, using defaults')
        except yaml.scanner.ScannerError as ex:
            print('incorrect yaml data:', ex.problem, ex.problem_mark)

        try:
            with open(self.config['movies_path'], 'r') as movies:
                # movieId, title, genres
                self.movie_header = movies.readline().strip().split(',')
            with open(self.config['ratings_path'], 'r') as ratings:
                # userId, movieId, rating, timestamp
                self.rating_header = ratings.readline().strip().split(',')
        except Exception as ex:
            print(ex)

        try:
            open(self.config['cache_path'])
        except FileNotFoundError:
            start_cache = input('cash file not found, start caching now? (y/n)')
            if start_cache in ('y', 'yes', 1):
                print('caching may require up to couple of minutes...')
                make_cache(self.config)
                raise SystemExit('the script is ready now')
            else:
                raise SystemExit('work without cache is not supported yet')


    def _append_movie_rating(self, movies: list) -> list:
        '''Append to every movie in the passed list it's rating.'''
        self.movie_header.append('rating')
        movie_id_index = self.movie_header.index('movieId')

        def calculate_rating(movie: list) -> float:
            '''Returns calculated movie rating.'''
            with open(self.config['cache_path'], 'r') as ratings:
                ratings_reader = csv.reader(ratings)
                next(ratings_reader)

                for rating_movie_id, rating in ratings_reader:
                    if rating_movie_id == str(movie[movie_id_index]):
                        return float(rating)
                return 0

        for movie in movies:
            movie.append(calculate_rating(movie))
        return movies


    def _get_movie_year(self, movie: list) -> int:
        '''
        Parse movie's title and return it's release year as int or 0
        if parsing has failed.
        '''
        movie_title = movie[self.movie_header.index('title')]
        search_result = re.match(self.config['title_regexp'], movie_title)
        return int(search_result.group(2)) if search_result else 0


    def _get_movie_title(self, movie: list) -> str:
        '''
        Returns movie's title or empty string if there was parsing error.
        '''
        movie_title = movie[self.movie_header.index('title')]
        search_result = re.match(self.config['title_regexp'], movie_title)
        return search_result.group(1) if search_result else 0


    def _genre_filter(self, movie: list, request_genres: str) -> bool:
        '''Returns True if requested genre expression matches film's genre, False otherwise.'''
        if not request_genres:
            return True

        request_genres = request_genres.lower()
        genre_index = self.movie_header.index('genres')
        movie_genres = movie[genre_index].lower().split('|')

        if '|' in request_genres:
            request_genres = request_genres.split('|')

            for genre in request_genres:
                if genre in movie_genres:
                    return True
            return False
        else:
            return True if request_genres in movie_genres else False


    def _year_filter(self, movie: list, year_from: int, year_to: int) -> bool:
        '''
        Returns True if passed movie's release year matches given interval,
        False otherwise.
        '''
        movie_year = self._get_movie_year(movie)

        if year_from and year_to:
            return year_from <= movie_year <= year_to

        elif year_from and not year_to:
            return movie_year >= year_from

        elif not year_from and year_to:
            return movie_year <= year_to
        else:
            return True


    def _regex_filter(self, movie: list, regexp: str) -> bool:
        '''
        Returns True if passed movie's title matches regular expression,
        False otherwise.
        '''
        title_index = self.movie_header.index('title')
        movie_title = movie[title_index]

        if regexp:
            return True if re.search(regexp, movie_title, re.IGNORECASE) else False
        else:
            return True


    def movie_filter(self, movie: list, genre: str, year_from: int,
                     year_to: int, regexp: str) -> bool:
        '''
        Recieves movie and filter rules, returns True if passed movie
        meets these rules and false otherwise.
        '''
        match_genre = self._genre_filter(movie, genre)
        match_year = self._year_filter(movie, year_from, year_to)
        match_regexp = self._regex_filter(movie, regexp)

        return True if match_genre and match_year and match_regexp else False

    
    def _sort(self, movie_list: list) -> list:
        '''
        Sorts list of movies according to specified in config file rules.
        '''
        rules = list(map(str.strip, self.config['sort_rules'].split(',')))

        def key_function(movie):
            movie_rating = movie[self.movie_header.index('rating')]
            movie_genres = movie[self.movie_header.index('genres')]
            movie_year = self._get_movie_year(movie)
            
            movie_title = movie[self.movie_header.index('title')]
            search_result = re.match(self.config['title_regexp'], movie_title)
            movie_title = search_result.group(1) if search_result else ''

            rule_to_value = {
                'rating' : movie_rating,
                'year': movie_year,
                'genres': movie_genres,
                'title': movie_title
            }

            return [rule_to_value[rule] for rule in rules]
        return sorted(movie_list, key=key_function, reverse=True)


    @request_time_used(_DEBUG)
    def request(self, n: int=None, genres: str=None, year_from: int=None,
                year_to: int=None, regexp: str=None) -> list:
        '''Returns list of movies which matches filter parameters'''
        if not genres:
            genres = self.config['all_genres']
        
        def filter_and_sort_movies(genres: str, year_from: int,
                                   year_to: int, regexp: str) -> list:
            '''
            Returns filterd sorted list of movies from csv file.
            '''
            movie_list = []
            with open(self.config['movies_path'], 'r', encoding='utf-8') as movies_file:
                movies_reader = csv.reader(movies_file)
                next(movies_reader) # skip csv file header

                for movie in movies_reader:
                    if self.movie_filter(movie, genres, year_from, year_to, regexp):
                        movie_list.append(movie)

                return self._append_movie_rating(movie_list)

        def divide_genres(movies: list, genres: str, n: int=None) -> str:
            '''
            Splits movie's genre and heads first n values.
            '''
            genres = list(map(str.lower, genres.split('|')))
            divided_movies = {genre: [] for genre in genres}
            result = 'genre,title,year,rating\n'

            for genre in genres:
                for movie in movies:
                    if n:
                        if genre in movie[2].lower() and len(divided_movies[genre]) < n if n else True:
                            divided_movies[genre].append(movie)
                    else:
                        if genre in movie[2].lower():
                            divided_movies[genre].append(movie)

            for key in divided_movies.keys():
                for movie in divided_movies[key]:
                    genre = key.capitalize()
                    title = self._get_movie_title(movie)
                    year = self._get_movie_year(movie)
                    rating = movie[-1]
                    row = map(str, [genre, title, year, rating])
                    result += ','.join(row)+'\n'
            return result

        movie_list = filter_and_sort_movies(genres, year_from, year_to, regexp)
        return divide_genres(self._sort(movie_list), genres, n)


if __name__ == '__main__':
    movie = Movie()
    args = cli_parser.parse()

    number, genres, year_from, year_to, regexp = \
        args.number, args.genres, args.year_from, args.year_to, args.regexp

    print(movie.request(number, genres, year_from, year_to, regexp))
