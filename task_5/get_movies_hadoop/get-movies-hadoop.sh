#!/bin/bash

# base command
# hadoop fs -rm /user/aleksandr_zhukov8/output/*; \
# hadoop fs -rmdir /user/aleksandr_zhukov8/output/; \
# yarn jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
# -input /user/aleksandr_zhukov8/small_movies_10.csv \
# -output /user/aleksandr_zhukov8/output \
# -file ~/tasks/task_5/get_movies_hadoop/mapper.py \
# -file ~/tasks/task_5/get_movies_hadoop/reducer.py \
# -mapper "$PYSPARK_PYTHON mapper.py" \
# -reducer "$PYSPARK_PYTHON reducer.py"

help(){
echo '''Usage: get-movies-hadoop [OPTION]
Hadoop MapReduce orchestration script.

  -d, --data            path to data file
  -g, --genres          genres to filter for
  -e, --regex           regex to filter for
  -f, --year_from       command to run benchmark for
  -t, --year_to         display this help message
  -n, --number          number of values to reduce
  -s, --streaming       path to hadoop-streaming.jar file
  -m, --mapper          path to mapper file
  -r, --reducer         path to reducer file
  -h, --help            print this help message

Examples:
$ ./get-movies-hadoop.sh -d small_movies.csv -e toy -t 2000 -n 1 -m mapper.py -r reducer.py
'''
}

# default parameters
STREAMING_JAR="/usr/lib/hadoop-mapreduce/hadoop-streaming.jar"
DATA="small_movies_10.csv"
INPUT="/user/$USER/$DATA"
OUTPUT="/user/$USER/output"
MAPPER_ARGS=""
REDUCER_ARGS=""
MAPPER_PATH=""
MAPPER_NAME=""
REDUCER_PATH=""
REDUCER_NAME=""

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -d|--data)
      DATA="$2 "
      shift 2
      ;;
    -g|--genres)
      MAPPER_ARGS+=" -g \"$2\""
      shift 2
      ;;
    -e|--regex)
      MAPPER_ARGS+=" -r $2"
      shift 2
      ;;
    -f|--year_from)
      MAPPER_ARGS+=" -f $2"
      shift 2
      ;;
    -t|--year_to)
      MAPPER_ARGS+=" -t $2"
      shift 2
      ;;
    -n|--number)
      REDUCER_ARGS+=" -n $2"
      shift 2
      ;;
    -s|--streaming)
      STREAMING_JAR="$2"
      shift 2
      ;;
    -m|--mapper)
      MAPPER_PATH="./$2"
      MAPPER_NAME="$PYSPARK_PYTHON $(basename $2)"
      shift 2
      ;;
    -r|--reducer)
      REDUCER_PATH="./$2"
      REDUCER_NAME="$PYSPARK_PYTHON $(basename $2)"
      shift 2
      ;;
    -h|--help)
      help
	    exit
      ;;
  esac
done

# For some reason hadoop streaming refuses to consume arguments not printed in terminal directly
# so I have to just print it from script, copy and execute. Script here works like command constructor.

# echo "$(yarn jar ${STREAMING_JAR} -input ${INPUT} -output ${OUTPUT}\
#  -file ${MAPPER_PATH} -file ${REDUCER_PATH} -mapper \"${MAPPER_NAME}${MAPPER_ARGS}\"\
#  -reducer \"${REDUCER_NAME}${REDUCER_ARGS}\")"

echo "$(hadoop fs -rm /user/$USER/output/*; hadoop fs -rmdir /user/$USER/output/)"

echo "yarn jar ${STREAMING_JAR} -input ${INPUT} -output ${OUTPUT}\
 -file ${MAPPER_PATH} -file ${REDUCER_PATH} -mapper \"${MAPPER_NAME}${MAPPER_ARGS}\"\
 -reducer \"${REDUCER_NAME}${REDUCER_ARGS}\""
