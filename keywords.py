### Keyword Frequency Script
import os, io
import argparse
import collections
import pandas as pd
from nltk.util import ngrams
import json
import spacy
statement = ""

pos_verb = ['VERB']
pos_noun = ['PROPN','NOUN']
stop_words = []

csv_keywords = {}
json_keywords = {}

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, default="-", help="did not specify file")
args = parser.parse_args()

def remove_dup(bigrams):
    for gram in bigrams:
        if gram[0][0] == gram[0][1]:
            bigrams.remove(gram)
        if gram[0][0] == '️' or gram[0][1] == '️':
            bigrams.remove(gram)
    return bigrams

if args.file != "-":
    path = os.path.dirname(args.file) + "/"
    if args.file.endswith('.csv'):
        responses = pd.read_csv(args.file)
        for i in range(len(responses['posts'])):
            statement += str(responses['posts'][i].lower()) + str(". ")
    elif args.file.endswith('.txt'):
        raw = io.open(args.file, 'r',encoding='utf-8')
        txt = raw.read().lower()

    nlp = spacy.load("en_core_web_sm")
    # nlp.max_length = 13618515
    doc = nlp(statement)
    # unigrams
    nouns = [token.lemma_ for token in doc if ((not token.is_punct) and (not token.is_stop) and (token.pos_ in pos_noun) and (token.shape_ != "x") and (token.shape_ != "xx") and (token.shape_ != "xxx") and (not token.like_num) and (not token.is_space) and (token.lemma_ not in stop_words) )]
    verbs = [token.lemma_ for token in doc if ((not token.is_punct) and (not token.is_stop) and (token.pos_ in pos_verb) and (token.shape_ != "x") and (token.shape_ != "xx") and (token.shape_ != "xxx") and (not token.like_num) and (not token.is_space) and (token.lemma_ not in stop_words) )]
    unigrams_n = collections.Counter(nouns)
    unigrams_v = collections.Counter(verbs)
    # bigrams
    n_gram = 2
    bigrams_n = collections.Counter(ngrams(nouns, n_gram))

    unigrams_n = list(filter(lambda x: (x[1] > 10), unigrams_n.most_common()[:50]))
    unigrams_v = list(filter(lambda x: (x[1] > 10), unigrams_v.most_common()[:50]))
    bigrams_n = list(filter(lambda x: (x[1] > 5), bigrams_n.most_common()[:50]))
    bigrams_n = remove_dup(bigrams_n)

    #unigrams_n = [[k[0],k[1]] for k in unigrams_n]
    #unigrams_v = [[k[0],k[1]] for k in unigrams_v]
    bigrams_n = [(str(k[0][0]) + " " + str(k[0][1]), k[1]) for k in bigrams_n]

    df = pd.DataFrame({'unigrams(NOUN)': pd.Series(unigrams_n), 'unigrams(VERB)': pd.Series(unigrams_v), 'bigrams(NOUN)': pd.Series(bigrams_n) })
    df.to_excel(path + 'keywords.xlsx', index=False, encoding='utf-8')

    json_keywords['unigrams_n'] = unigrams_n
    json_keywords['unigrams_v'] = unigrams_v
    json_keywords['bigrams_n'] = bigrams_n

    with open(path + "keywords.json", 'w', encoding='utf-8') as fp:
        json.dump(json_keywords, fp, ensure_ascii=False)
else:
    print("did not specify file")
