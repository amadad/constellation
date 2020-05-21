### Word Count Script 
import pandas as pd
import argparse

word_count = 0

parser = argparse.ArgumentParser()
parser.add_argument("-file", "--file", type=str, default="-", help="did not specify file")
args = parser.parse_args()

if args.file != "-":
    with open(args.file, 'r') as file:
        for line in file:
            word_count += len(line.split())

print("number of words: ", word_count)
