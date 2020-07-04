### Word Count Script
import pandas as pd
import argparse

word_count = 0

parser = argparse.ArgumentParser()
parser.add_argument("-file", "--file", type=str, default="-", help="did not specify file")
args = parser.parse_args()

a = []
corpus = []

if args.file != "-":
    if args.file.endswith('.txt'):
        with open(args.file, 'r') as file:
            for line in file:
                word_count += len(line.split())
    elif args.file.endswith('.csv'):
        responses = pd.read_csv(args.file)
        for i in range(len(responses['posts'])):
            a=responses['posts'][i]
            corpus.append(a)
        for sentence in corpus:
            print(sentence)
            print(sentence.split())
            print(len(sentence.split()))
            word_count += len(sentence.split())

print("number of words: ", word_count)
