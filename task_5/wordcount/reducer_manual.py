#!/usr/bin/env python
import sys 

def reduce(word, values):
    '''Reduces values by making sum.'''
    return word, sum(values) 

if __name__ == "__main__":
    prev_key = None 
    values = [] 

    for line in sys.stdin: 
        key, value = line.split("\t")

        if key != prev_key and prev_key:
            result_key, result_value = reduce(prev_key, values)
            values = []
            print(f"{result_key}\t{result_value}")

        prev_key = key 
        values.append(int(value)) 
    
    if prev_key: 
        result_key, result_value = reduce(prev_key, values) 
        print(f"{result_key}\t{result_value}") 
