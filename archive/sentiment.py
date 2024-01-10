### Sentiment Analysis Script
from textblob import TextBlob
import argparse
import pandas as pd

corpus = []
a = []
pos = []
neg = []
neu = []

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, default="-", help="did not specify file")
args = parser.parse_args()

if args.file != "-":
    tweets = pd.read_csv(args.file)

for i in range(len(tweets['posts'])):
        a=tweets['posts'][i]
        corpus.append(a)

for tweet in corpus:
    blob = TextBlob(tweet)
    if blob.sentiment.polarity > 0:
        pos.append(blob)
    if blob.sentiment.polarity < 0:
        neg.append(blob)
    if blob.sentiment.polarity == 0:
        neu.append(blob)

print("positives:")
print(round(len(pos) / total * 100, 2))
print("neutrals:")
print(round(len(neu) / total * 100, 2))
print("negatives:")
print(round(len(neg) / total * 100, 2))
