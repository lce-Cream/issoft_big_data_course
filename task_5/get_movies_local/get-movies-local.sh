#!/bin/sh
help(){
echo '''Usage: get-movies-local [OPTION]
Local MapReduce emulator orchestration script.

  -d, --data            path to data file
  -g, --genres          genres to filter for
  -r, --regex           regex to filter for
  -f, --year_from       command to run benchmark for
  -t, --year_to         display this help message
  -n, --number          number of values to reduce

Examples:
  get-movies-local -d small_movies.csv -r toy -t 2000 -n 1
'''
}

# default parameters
DATA="./data/small_movies_10.csv"
MAPPER_ARGS=""
REDUCER_ARGS=""

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -d|--data)
      DATA="$2 "
      shift 2
      ;;
    -g|--genres)
      MAPPER_ARGS+="-g $2 "
      shift 2
      ;;
    -r|--regex)
      MAPPER_ARGS+="-r $2 "
      shift 2
      ;;
    -f|--year_from)
      MAPPER_ARGS+="-f $2 "
      shift 2
      ;;
    -t|--year_to)
      MAPPER_ARGS+="-t $2 "
      shift 2
      ;;
    -n|--number)
      REDUCER_ARGS+="-n $2 "
      shift 2
      ;;
    -h|--help)
      help
	    exit
      ;;
  esac
done

echo "$(cat ${DATA} | python mapper.py ${MAPPER_ARGS} | sort | python reducer.py ${REDUCER_ARGS})"
