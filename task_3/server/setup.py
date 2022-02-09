import logging
import time
import yaml
import re
import os

import mysql.connector as connector
from mysql.connector import MySQLConnection

# setting up logger
handler = logging.StreamHandler()
formatter = logging.Formatter('SERVER::%(levelname)s:: %(message)s')
handler.setFormatter(formatter)

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(handler)
_LOGGER.setLevel(logging.INFO)


class Database:
    def __init__(self, config=None) -> None:
        '''Initialization of the Database class instance'''
        # setting up the config
        if not config:
            try:
                with open("./config.yaml") as config:
                    self.config = yaml.safe_load(config)

            except FileNotFoundError as ex:
                _LOGGER.error("config.yaml not found")
                raise SystemExit

            except yaml.scanner.ScannerError as ex:
                _LOGGER.error("incorrect yaml data:", ex.problem, ex.problem_mark)
                raise SystemExit

            except Exception as ex:
                _LOGGER.exception(ex)
                raise SystemExit
        else:
            self.config = config

        # making connection
        try:
            self.connection = MySQLConnection(**self.config['connection'])
        except connector.Error as ex:
            if ex.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                _LOGGER.error("wrong username or password")
            elif ex.errno == connector.errorcode.ER_BAD_DB_ERROR:
                _LOGGER.error(f"database {self.config['database']} does not exist")
            else:
                _LOGGER.error(ex)
            raise SystemExit
        else:
            _LOGGER.info(f"database {self.config['connection']['database']} connected successfully")
            # setting up the tables
            if self._create_tables():
                self._fill_tables()
                self._create_procedure()
            _LOGGER.info("everything is ready")
            

    def _create_tables(self) -> bool:
        '''
        Return True if tables are created successfully or already exist,
        False otherwise.
        '''
        def create_movies() -> None:
            '''Creates movies table from sql code in file.'''
            with open(self.config['paths']['table_movies']) as movies:
                movies_table = movies.read()
                base_name = self.config['connection']['database']
                movies_table = re.sub("{DATABASE_PLACEHOLDER}", base_name, movies_table)

            with self.connection.cursor() as cursor:
                # when executing many satements at once it is required to
                # iterate over result for every statement to be executed
                [_ for _ in cursor.execute(movies_table, multi=True)]

        def create_ratings() -> None:
            '''Creates ratings table from sql code in file.'''
            with open(self.config['paths']['table_ratings']) as ratings:
                ratings_table = ratings.read()
                base_name = self.config['connection']['database']
                ratings_table = re.sub("{DATABASE_PLACEHOLDER}", base_name, ratings_table)

            with self.connection.cursor() as cursor:
                [_ for _ in cursor.execute(ratings_table, multi=True)]

        def create_movies_ratings() -> None:
            '''Creates joined movies and ratings table from sql code in file.'''
            with open(self.config['paths']['table_movies_ratings']) as movies_ratings:
                movies_ratings_table = movies_ratings.read()
                base_name = self.config['connection']['database']
                movies_ratings_table = re.sub("{DATABASE_PLACEHOLDER}", base_name, movies_ratings_table)

            with self.connection.cursor() as cursor:
                [_ for _ in cursor.execute(movies_ratings_table, multi=True)]

        def is_created(table: str) -> bool:
            '''
            Returns True if all tables were created successfully, False otherwise.
            '''
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute('SHOW TABLES')
                    tables = [table[0] for table in cursor.fetchall()]
                    return table in tables
            except connector.Error as err:
                _LOGGER.exception(err)
                return False

        # ensuring tables are created
        try:
            if not is_created('movies'):
                create_movies()
                _LOGGER.info('creating table movies: OK')
            
            if not is_created('ratings'):
                create_ratings()
                _LOGGER.info('creating table ratings: OK')
            
            if not is_created('movies_ratings'):
                create_movies_ratings()
                _LOGGER.info('creating joined table movies_ratings: OK')

        # if something is wrong with sql or database
        except connector.Error as ex:
            self.connection.rollback()
            _LOGGER.exception(ex)
        # if something is wrong with the files
        except Exception as ex:
            _LOGGER.exception(ex)
        else:
            self.connection.commit()

        return is_created('movies') and is_created('ratings') and is_created('movies_ratings')
        return True


    def _fill_tables(self) -> bool:
        '''Returns True if tables are filled successfully, False otherwise.'''

        def fill_movies() -> None:
            '''Fills movies table from data in csv file.'''
            with open(self.config['paths']['insert_movies']) as insert:
                insert_statement = insert.read()

                path = os.path.abspath(self.config['paths']['csv_movies']).replace('\\', os.sep*4)
                base_name = self.config['connection']['database']
                
                insert_statement = re.sub("{PATH_PLACEHOLDER}", path, insert_statement)
                insert_statement = re.sub("{DATABASE_PLACEHOLDER}", base_name, insert_statement)

                with self.connection.cursor() as cursor:
                    [_ for _ in cursor.execute(insert_statement, multi=True)]

        def fill_ratings() -> None:
            '''Fills ratings table from data in csv file.'''
            with open(self.config['paths']['insert_ratings']) as insert:
                insert_statement = insert.read()

                path = os.path.abspath(self.config['paths']['csv_ratings']).replace('\\', os.sep*4)
                base_name = self.config['connection']['database']

                insert_statement = re.sub("{PATH_PLACEHOLDER}", path, insert_statement)
                insert_statement = re.sub("{DATABASE_PLACEHOLDER}", base_name, insert_statement)
                
                with self.connection.cursor() as cursor:
                    [_ for _ in cursor.execute(insert_statement, multi=True)]

        def fill_movies_ratings() -> None:
            '''Fills movies_ratings table from data in csv file.'''
            with open(self.config['paths']['insert_movies_ratings']) as insert:
                insert_statement = insert.read()
                base_name = self.config['connection']['database']
                insert_statement = re.sub("{DATABASE_PLACEHOLDER}", base_name, insert_statement)
            
            with self.connection.cursor() as cursor:
                [_ for _ in cursor.execute(insert_statement, multi=True)]

        def is_filled(table: str) -> bool:
            '''Returns True if tables exist and are filled in, False otherwise'''
            try:
                table_count = 0
                with self.connection.cursor() as cursor:
                    cursor.execute(f'SELECT COUNT(*) FROM {table};')
                    table_count = cursor.fetchone()
                return table_count[0]
            except connector.Error as err:
                _LOGGER.exception(err)
                return False

        try:
            if not is_filled('movies'):
                fill_movies()
                _LOGGER.info("filling table movies: OK")

            if not is_filled('ratings'):
                fill_ratings()
                _LOGGER.info("filling table ratings: OK")

            if not is_filled('movies_ratings'):
                fill_movies_ratings()
                _LOGGER.info("filling table movies_ratings: OK")

        except connector.Error as ex:
            self.connection.rollback()
            _LOGGER.exception(ex)
        except Exception as ex:
            _LOGGER.exception(ex)
        else:
            self.connection.commit()

        return is_filled('movies') and is_filled('ratings') and is_filled('movies_ratings')
        return True


    def _create_procedure(self) -> bool:
        '''
        Creates procedure in database from specified in config file and returns
        True if procedure created successful or already exists.
        '''
        def get_procedure_name() -> str:
            '''Returns procedure's name, assuming it matches it's file name.'''
            try:
                proc_name = '.'.join(self.config['paths']['procedure'].split('/')[-1].split('.')[:-1])
                return proc_name
            except Exception as ex:
                _LOGGER.exception(ex)

        def is_created(procedure_name: str) -> bool:
            '''Check if procedure with provided name exists in database.'''
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(f"SHOW PROCEDURE STATUS WHERE db='{self.config['connection']['database']}';")
                result = cursor.fetchone()
                return procedure_name == result['Name'] if result else False

        try:
            self.procedure_name = get_procedure_name()
            if not is_created(self.procedure_name):
                with open(self.config['paths']['procedure']) as procedure_file:
                    procedure = procedure_file.read()
                    base_name = self.config['connection']['database']
                    procedure = re.sub("{DATABASE_PLACEHOLDER}", base_name, procedure)

                    with self.connection.cursor() as cursor:
                        [_ for _ in cursor.execute(procedure, multi=True)]
                _LOGGER.info('create procedure: OK')
            else:
                return True

        except connector.Error as ex:
            _LOGGER.exception(ex)
            self.connection.rollback()
        except Exception as ex:
            _LOGGER.exception(ex)


    def get_movies(self, number:      int=None,
                         genres:      str=None, 
                         year_from:   int=None,
                         year_to:     int=None,
                         title_regex: str=None) -> list:
        '''Returns filtered list of movies from database. Left here just in case'''
        row = (number, genres, year_from, year_to, title_regex)

        try:
            with self.connection.cursor() as cursor:
                cursor.callproc(self.procedure_name, args=row)
                result = [resp.fetchall() for resp in cursor.stored_results()][0]
            return result
        except Exception as ex:
                _LOGGER.exception(ex)


def test_request(db: Database) -> None:
    '''Makes test request to the database.'''
    def csv_like(movies: list) -> None:
        '''Print request result in a csv like format.'''
        result = 'genre,title,year,rating\n'
        for movie in movies:
            result += (','.join(map(str, movie)))+'\n'
        return result

    number, genres, year_from, year_to, title = 1, None, None, None, None
    
    start = time.time()
    response = db.get_movies(number, genres, year_from, year_to, title)
    end = time.time()
    _LOGGER.info(f"request took {round(end - start, 3)} seconds, containing {len(response)} records:")
    return csv_like(response)


if __name__ == '__main__':
    start = time.time()
    db = Database()
    end = time.time()
    _LOGGER.info(f"setup time: {round(end - start, 3)} seconds")

    # print(test_request(db))
