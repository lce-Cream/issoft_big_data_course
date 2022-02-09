import argparse
import pandas as pd
import pyarrow.parquet as pq

class CSV:

    def read_csv(path: str) -> pd.DataFrame:
        '''Read a csv file, returning pandas dataframe'''
        try:
            data = pd.read_csv(path)
        except Exception as error:
            print(error)
        else:
            return data

    def write_csv(data: pd.DataFrame, dest: str) -> bool:
        '''Write a csv file, return True for success or False for failure'''
        try:
            data.to_csv(dest, index=False)
            return True
        except Exception as error:
            print(error)
            return False

class Parquet:

    def read_parquet(path: str) -> pd.DataFrame:
        '''Read a parquet file, returning pandas dataframe'''
        try:
            data = pd.read_parquet(path)
        except Exception as error:
            print(error)
        else:
            return data

    def write_parquet(data: pd.DataFrame, dest: str) -> bool:
        '''Write a parquet file, return True for success or False for failure'''
        try:
            data.to_parquet(dest)
            return True
        except Exception as error:
            print(error)
            return False

    def get_schema(path: str):
        '''Return parquet file schema'''
        try:
            return pq.read_schema(path).remove_metadata()
        except Exception as error:
            print(error)


class Parser:
    def parse():
        """
        Returns dictionary like object with parsed arguments from terminal
        """
        parser = argparse.ArgumentParser(description='csv parquet converter')
        group = parser.add_mutually_exclusive_group()

        group.add_argument('-c', '--csv2parquet', help='convert csv to parquet',
                            nargs=2, metavar=('<csv file>', '<parquet file>'))

        group.add_argument('-p', '--parquet2csv', help='convert parquet to csv',
                            nargs=2, metavar=('<parquet file>','<csv file>'))

        group.add_argument('-s', '--get-schema', help='get parquet file schema',
                            metavar='<parquet file>')

        return parser.parse_args()


if __name__ == '__main__':
    args = Parser.parse()
    c2p, p2c, schema = args.csv2parquet, args.parquet2csv, args.get_schema
    
    if c2p:
        print('converting csv to parquet...', end=' ')
        csv_file = c2p[0]
        prq_file = c2p[1]
        data = CSV.read_csv(csv_file)
        print('success') if Parquet.write_parquet(data, prq_file) else print('failure')

    elif p2c:
        print('converting parquet to csv...', end=' ')
        prq_file = p2c[0]
        csv_file = p2c[1]
        data = Parquet.read_parquet(prq_file)
        print('success') if CSV.write_csv(data, csv_file) else print('failure')

    elif schema:
        print('getting schema...')
        print(Parquet.get_schema(schema))
