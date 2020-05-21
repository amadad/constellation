### Keyword Frequency Script
import os, io
import argparse
import collections
import pandas as pd
import json
import spacy

BRAND = "secondipity"
min_value = 50
pos_tag = ['PROPN', 'NOUN', 'ADJ', 'VERB']
stop_words = [BRAND]

csv_keywords = {}
csv_keywords["keyword"] = []
csv_keywords["frequency"] = []
json_keywords = []

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, default="-", help="did not specify file")
args = parser.parse_args()

if args.file != "-":
    raw = io.open(args.file, 'r',encoding='utf-8')
    path = os.path.dirname(args.file) + "/"
    txt = raw.read().lower()

    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 6709324
    doc = nlp(txt)
    words = [token.text for token in doc if ((not token.is_punct) and (not token.is_stop) and (token.pos_ in pos_tag) and (token.shape_ != "x") and (token.shape_ != "xx") and (token.shape_ != "xxx") and (not token.like_num) and (not token.is_space) and (token.text not in stop_words) and (not token.text.startswith('@')) and (token.text.isalnum()))]
    counter = collections.Counter(words)
    #print(counter.most_common(150))

    for k in counter.most_common():
        keyword = k[0]
        sents = []
        if k[1] > min_value:
            print("--")
            print("keyword: " + keyword)
            csv_keywords["keyword"].append( k[0] )
            csv_keywords["frequency"].append( k[1] )
            json_keywords.append( {"keyword": k[0], "frequency": k[1], "brand": BRAND } )

    df = pd.DataFrame(csv_keywords)
    df.to_excel(path + BRAND + '-keywords.xlsx', index=False, encoding='utf-8')

    with open(path + BRAND + "-keywords.json", 'w', encoding='utf-8') as fp:
        json.dump(json_keywords, fp, ensure_ascii=False)
else:
    print("did not specify file")
