import argparse
import logging
import time
import yaml

from mysql import connector
from mysql.connector import MySQLConnection

# вопросы:
# использовать ли трединг при инсертах в базу?

handler = logging.FileHandler('client.log', 'a', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s::CLIENT::%(levelname)s:: %(message)s')
handler.setFormatter(formatter)

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(handler)
_LOGGER.setLevel(logging.INFO)

class Connection:
    '''MySQL connection class.'''
    def __init__(self, config: dict=None) -> None:
        '''Initializes connection class by establishing a connection.'''
        if not config:
            try:
                with open("./config.yaml") as config:
                    self.config = yaml.safe_load(config)
                    self.procedure_name = self.config['variables']['procedure_name']

            except FileNotFoundError as ex:
                _LOGGER.error("config.yaml not found")
                raise SystemExit
            except yaml.scanner.ScannerError as ex:
                _LOGGER.error("incorrect yaml data:", ex.problem, ex.problem_mark)
                raise SystemExit
            except Exception as ex:
                _LOGGER.error(ex)
                raise SystemExit

        # making connection
        try:
            self.connection = MySQLConnection(**self.config['connection'])

        except connector.Error as ex:
            if ex.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                _LOGGER.error("wrong username or password")
            elif ex.errno == connector.errorcode.ER_BAD_DB_ERROR:
                _LOGGER.error(f"database {config['database']} does not exist")
            else:
                _LOGGER.error(ex)
                raise SystemExit
        else:
            _LOGGER.info(f"database {self.config['connection']['database']} connected successfully")


    def get_movies(self,
                   number:         int=None,
                   genres:         str=None,
                   year_from:      int=None,
                   year_to:        int=None,
                   title_regex:    str=None
                   ) -> list:
        '''Returns filtered list of movies from database.'''
        row = (number, genres, year_from, year_to, title_regex)

        try:
            with self.connection.cursor() as cursor:
                cursor.callproc(self.procedure_name, args=row)
                result = [resp.fetchall() for resp in cursor.stored_results()][0]
                return result
        except Exception as ex:
            _LOGGER.error(ex)


def main(write_logs: bool=False) -> None:
    def csv_like(movies: list) -> None:
        '''Print request result in a csv like format.'''
        result = 'genre,title,year,rating\n'
        for movie in movies:
            result += (','.join(map(str, movie)))+'\n'
        return result

    def parse():
        """
        Returns dictionary like object with parsed arguments from terminal.
        """
        parser = argparse.ArgumentParser(description='allows to perform queries to database')

        parser.add_argument('-n', '--number', help='number of movies to retrieve',
                            metavar='<int>', type=int)

        parser.add_argument('-g', '--genres', help='get movies by genres in x|y|z format',
                            metavar='<str>')

        parser.add_argument('-f', '--year_from', help='get movies from this year',
                            metavar='<int>', type=int)

        parser.add_argument('-t', '--year_to', help='get movies to this year',
                            metavar='<int>', type=int)

        parser.add_argument('-r', '--title_regex', help='get movies by title regexp',
                            metavar='<regexp>')

        return parser.parse_args()

    args = parse()
    connection = Connection()

    start = time.time()
    try:
        response = connection.get_movies(args.number,
                                        args.genres,
                                        args.year_from,
                                        args.year_to,
                                        args.title_regex
                                        )
    except Exception as ex:
        print(ex, 'Did you run setup.py first?')
    end = time.time()

    print(csv_like(response))

    if write_logs:
        message = "request with parameters "\
                f"{args.number, args.genres, args.year_from, args.year_to, args.title_regex} "\
                f"took {round(end - start, 3)} seconds, containing {len(response)} records: "\
                +'\n'+csv_like(response)
        _LOGGER.info(message)
    
if __name__ == '__main__':
    main(True)
