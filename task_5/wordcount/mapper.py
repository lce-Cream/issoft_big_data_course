#!/usr/bin/env python
import sys 

def map(line): 
    for word in line.split():
        yield word.lower(), 1

for line in sys.stdin:
    for key, value in map(line):
        print(f"{key}\t{value}")
