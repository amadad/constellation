### LDA Topic Modeling - Sklearn Implementation
import os, io
import pandas as pd
import numpy as np
import argparse
import json, csv
import tempfile
from collections import OrderedDict
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction import text

csv_lda_topics = {}
json_lda_topics = []
corpus = []
a = []

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, default="-", help="did not specify file")
args = parser.parse_args()

if args.file != "-":
    raw = io.open(args.file, 'r',encoding='utf-8')
    txt = raw.read().lower()
    path = os.path.dirname(args.file) + "/"
    tweets = pd.read_csv(args.file)
    print("Number of tweets:",len(tweets['scrape']))

for i in range(len(tweets['scrape'])):
        a=tweets['scrape'][i]
        corpus.append(a)
TEMP_FOLDER = tempfile.gettempdir()
print('Folder "{}" will be used to save temporary dictionary and corpus.'.format(TEMP_FOLDER))

no_features = 500
my_additional_stop_words = []
stop_words = text.ENGLISH_STOP_WORDS.union(my_additional_stop_words)

# NMF uses tf-idf
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words=stop_words)
tfidf = tfidf_vectorizer.fit_transform(corpus)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

# LDA uses raw term counts because it is a probabilistic graphical model
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words=stop_words)
tf = tf_vectorizer.fit_transform(corpus)
tf_feature_names = tf_vectorizer.get_feature_names()

no_topics = 20

# Run NMF
nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)

# Run LDA
lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        top_words = []
        for i in topic.argsort()[:-no_top_words - 1:-1]:
            top_words.append(feature_names[i])
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))
        json_lda_topics.append( {"topic": topic_idx, "top_words": top_words} )
        csv_lda_topics[topic_idx] = top_words

no_top_words = 10
#display_topics(nmf, tfidf_feature_names, no_top_words)
display_topics(lda, tf_feature_names, no_top_words)

keys = sorted(csv_lda_topics.keys())
with open(path + "topics(sklearn).csv", "w") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(keys)
   writer.writerows(zip(*[csv_lda_topics[key] for key in keys]))

with open(path + "topics(sklearn).json", 'w') as fp:
    json.dump(json_lda_topics, fp)
