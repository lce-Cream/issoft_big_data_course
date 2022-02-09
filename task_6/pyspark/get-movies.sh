#!/bin/bash

help(){
echo '''Usage: get-movies [OPTION]
Spark job orchestration script for movie retrieval.

  -g, --genres          genres to filter by
  -r, --regex           regex to filter by
  -f, --year_from       year to filter movies from
  -t, --year_to         year to filter movies to
  -n, --number          number of movies in each genre
  -u, --user            username to execute program from
  -m, --movies          movies csv file
  -a, --ratings         ratings csv file
  -h, --help            print this help message

Examples:
$ ./get-movies.sh -m small_movies.csv -a small_ratings.csv -r toy -t 2000 -n 1
'''
}

# default parameters
MOVIES="small_movies.csv"
RATINGS="small_ratings.csv"
USER=$USER
FILTER_ARGS=""

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -g|--genres)
      FILTER_ARGS+="-g \"$2\" "
      shift 2
      ;;
    -r|--regex)
      FILTER_ARGS+="-r $2 "
      shift 2
      ;;
    -f|--year_from)
      FILTER_ARGS+="-f $2 "
      shift 2
      ;;
    -t|--year_to)
      FILTER_ARGS+="-t $2 "
      shift 2
      ;;
    -n|--number)
      FILTER_ARGS+="-n $2 "
      shift 2
      ;;
    -u|--user)
      USER="$2"
      shift 2
      ;;
    -m|--movies)
      MOVIES="$2"
      shift 2
      ;;
    -a|--ratings)
      RATINGS="$2"
      shift 2
      ;;
    -h|--help)
      help
	    exit
      ;;
  esac
done

hadoop fs -rm /user/$USER/output/* &> /dev/null
hadoop fs -rmdir /user/$USER/output/ &> /dev/null
hadoop fs -put $MOVIES /user/$USER/  &> /dev/null
hadoop fs -put $RATINGS /user/$USER/ &> /dev/null
spark-submit get-movies.py $FILTER_ARGS -u $USER -m $MOVIES -a $RATINGS &> /dev/null
hadoop fs -cat /user/$USER/output/*
