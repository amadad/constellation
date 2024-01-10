### Rake Script
from rake_nltk import Rake
import pandas as pd
import argparse
import os

BRAND = "schwab"
min_value = 10

rake_csv = {}
rake_csv["phrase"] = []
rake_csv["score"] = []

r = Rake(min_length=2, max_length=4) # Uses stopwords for english from NLTK, and all puntuation characters.

parser = argparse.ArgumentParser()
parser.add_argument("-file", "--file", type=str, default="-", help="did not specify file")
args = parser.parse_args()

if args.file != "-":
    raw = open(args.file, 'r')
    path = os.path.dirname(args.file) + "/"

text = raw.read().lower()
a = r.extract_keywords_from_text(text)
b = r.get_ranked_phrases()
sentences = r.get_ranked_phrases_with_scores()

for sentence in sentences:
    if sentence[0] > min_value:
        rake_csv["phrase"].append( sentence[1] )
        rake_csv["score"].append( round(sentence[0], 2) )

df = pd.DataFrame(rake_csv)
df.to_excel(path + BRAND + '-rake-phrases.xlsx')
