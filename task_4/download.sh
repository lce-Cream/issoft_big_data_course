#!/bin/sh

help(){
echo '''Usage: download [OPTION]
Download specified dataset and unarchive it.

  -s, --size            dataset size, must be in small|medium|huge
  -d, --destination     directory path to save to
  -h, --help            display this help message

Examples:
  download -s small -d ./small_dataset/
  download --destination ../huge_dataset/ --size huge
'''
}

# default value
DESTINATION="./"

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -s|--size)
      SIZE="$2"
      shift 2
      ;;
    -d|--destination)
      DESTINATION="$2/"
      shift 2
      ;;
    -h|--help)
      help
	  exit
      ;;
  esac
done

case $SIZE in
  small)
    LINK="https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    ;;
  medium)
    LINK="https://files.grouplens.org/datasets/movielens/ml-latest.zip"
    ;;
  huge)
    LINK="https://files.grouplens.org/datasets/movielens/ml-20mx16x32.tar"
    ;;
  *)
    echo "${SIZE}, only small|medium|huge size is valid, use --help for more"
    exit
    ;;
esac

echo "$(curl -o ${DESTINATION}dataset.zip ${LINK})"
echo "$(unzip -j ${DESTINATION}dataset.zip -d ${DESTINATION})"
echo "$(rm ${DESTINATION}dataset.zip)"
