#!/bin/sh
help(){
echo '''Usage: benchmark [OPTION]
Benchmark specified application.

  -i, --iteration          number of iterations to test
  -l, --logfile            path to log file
  -p, --plotfile           path to plot
  -c, --command            command to run benchmark for
  -h, --help               display this help message

Examples:
  benchmark -i 10 -l statistics.log -p plot.png -c "py get-movies.py -r shrek -t 2008"
'''
}

# default parameters
ITERATIONS=5
LOGFILE="./bench/stats.log"
PLOTFILE="./bench/plot.png"
# COMMAND="py get-movies.py -r shrek -t 2008"

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -i|--iterations)
      ITERATIONS="$2"
      shift 2
      ;;
    -l|--log)
      LOGFILE="$2"
      shift 2
      ;;
    -p|--plot)
      PLOTFILE="$2"
      shift 2
      ;;
    -c|--command)
      COMMAND="$2"
      shift 2
      ;;
    -h|--help)
      help
	    exit
      ;;
  esac
done

echo "$(mkdir -p bench)"
echo "$(cmdbench -i ${ITERATIONS} -p ${PLOTFILE} -s ${COMMAND} | head -n -3 | grep "Process" -A 100)" >> $LOGFILE
