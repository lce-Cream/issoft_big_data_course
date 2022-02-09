usage: converter.py [-h] [-c <csv file> <parquet file> | -p <parquet file> <csv file> | -s <parquet file>]

csv parquet converter

optional arguments:
  -h, --help            show this help message and exit
  -c <csv file> <parquet file>, --csv2parquet <csv file> <parquet file>
                        convert csv to parquet
  -p <parquet file> <csv file>, --parquet2csv <parquet file> <csv file>
                        convert parquet to csv
  -s <parquet file>, --get-schema <parquet file>
                        get parquet file schema

usage examples:
py .\converter.py -c .\files\data.csv data.parquet
py .\converter.py -p .\files\data.parquet data.csv
py .\converter.py -s .\files\data.parquet
py .\converter.py -h
