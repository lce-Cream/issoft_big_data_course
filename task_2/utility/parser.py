import argparse

class cli_parser:
    def parse():
        """
        Returns dictionary like object with parsed arguments from terminal.
        """
        parser = argparse.ArgumentParser(description='allows to perform queries to csv movies file')

        parser.add_argument('-n', '--number', help='number of movies',
                            metavar='<int>', type=int)

        parser.add_argument('-g', '--genres', help='genres to search for',
                            metavar='<str>')

        parser.add_argument('-f', '--year_from', help='get movies from this year',
                            metavar='<int>', type=int)

        parser.add_argument('-t', '--year_to', help='get movies to this year',
                            metavar='<int>', type=int)

        parser.add_argument('-r', '--regexp', help='get movies by title regexp',
                            metavar='<regexp>')

        return parser.parse_args()
