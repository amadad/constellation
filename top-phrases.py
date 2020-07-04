import os, io
import re
import json, csv
import argparse
import collections
from nltk.util import ngrams
from gensim.summarization.summarizer import summarize
import spacy
import pandas as pd
import xlsxwriter

pos_tag = ['NOUN','ADJ', 'VERB']
pos_noun = ['PROPN','NOUN']
stop_words = []
sentences = []
a = []
max_value = 3

def remove_dup(bigrams,trigrams):
    for gram in bigrams:
        if gram[0][0] == gram[0][1]:
            bigrams.remove(gram)
        if gram[0][0] == '️' or gram[0][1] == '️':
            bigrams.remove(gram)
    for gram in trigrams:
        if gram[0][0] == gram[0][1] or gram[0][1] == gram[0][2]:
            trigrams.remove(gram)
    return bigrams, trigrams

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, default="-", help="did not specify file")
parser.add_argument("-t", "--topics", type=str, default="-", help="did not specify file")
args = parser.parse_args()

if args.file != "-":
    ## raw file
    path = os.path.dirname(args.file) + "/"
    workbook = xlsxwriter.Workbook(path + 'topics+phrases.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'text_wrap': True, 'align': 'left', 'valign': 'top'})
    red = workbook.add_format({'color': 'red'})
    wrap_test = workbook.add_format({'text_wrap': True, 'align': 'left', 'valign': 'top'})

    if args.file.endswith('.csv'):
        responses = pd.read_csv(args.file)
        for i in range(len(responses['posts'])):
            a=responses['posts'][i]
            sentences.append(a.lower())
    elif args.file.endswith('.txt'):
        with open(args.file) as f_in:
            sentences = (line.rstrip() for line in f_in)
            sentences = list(line for line in sentences if line)
    ## topics file
    with open(args.topics) as json_file:
        topics = json.load(json_file)

# -----------------------> EXTRACTING TOP PHRASES

for topic in topics:
    cluster = topic["cluster"]
    top_phrases = []
    for sentence in sentences:
        count = 0
        top_words = []
        for word in cluster:
            if re.search(r'\b' + word + r'\b', sentence):
                top_words.append(word)
                count += 1
        if count >= max_value:
            top_phrases.append( {"phrase":sentence, "top_words": top_words, "score": str(len(top_words)) + str("/") + str(len(cluster)) } )
    top_phrases = sorted(top_phrases, key=lambda k: len(k["top_words"]),reverse=True)
    topic["top_phrases"] = top_phrases

# -----------------------> EXTRACTING KEYWORDS FROM TOP PHRASES

for topic in topics:
    cluster = topic["cluster"]
    statement = ""
    keys = []
    for p in topic["top_phrases"]:
        statement += str(p["phrase"]) + str(". ")

    gen = summarize(statement,word_count=20)
    keys.append( {"gensim": gen} )

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(statement)
    #words = [token.text for token in doc if ((not token.is_punct) and (not token.is_stop) and (token.pos_ in pos_tag) and (token.shape_ != "x") and (token.shape_ != "xx") and (token.shape_ != "xxx") and (not token.like_num) and (not token.is_space) and (token.lemma_ not in stop_words))]
    nouns = [token.lemma_ for token in doc if ((not token.is_punct) and (not token.is_stop) and (token.pos_ in pos_noun) and (token.shape_ != "x") and (token.shape_ != "xx") and (token.shape_ != "xxx") and (not token.like_num) and (not token.is_space) and (token.lemma_ not in stop_words) )]
    bigrams_n = collections.Counter(ngrams(nouns, 2))
    trigrams_n = collections.Counter(ngrams(nouns, 3))
    unigrams_n = collections.Counter(nouns)

    unigrams_n = list(filter(lambda x: (x[1] > 10), unigrams_n.most_common()[:10]))
    bigrams_n = list(filter(lambda x: (x[1] > 1), bigrams_n.most_common()[:10]))
    trigrams_n = list(filter(lambda x: (x[1] > 1), trigrams_n.most_common()[:10]))
    bigrams_n, trigrams_n = remove_dup(bigrams_n, trigrams_n)

    for k in unigrams_n:
        keys.append( {"unigram":k[0], "score":k[1]} )
    for k in bigrams_n:
        keys.append( {"bigram": str(k[0][0]) + " " + str(k[0][1]), "score":k[1]} )
    for k in trigrams_n:
        keys.append( {"trigram": str(k[0][0]) + " " + str(k[0][1]) + " " + str(k[0][2]), "score":k[1]} )

    topic["keywords"] = keys


with open(path + "topics+phrases.json", 'w') as fp:
    json.dump(topics, fp)


# -----------------------> WRITING EXCEL SHEET

for topic in topics:
    y = 0
    cluster = topic["cluster"]
    worksheet.write(y, topic["topic"], topic["topic"], bold)
    y += 1
    for word in cluster:
        worksheet.write(y, topic["topic"], word)
        y += 1

saved_y_pos = y

for topic in topics:
    y = saved_y_pos
    k = topic["keywords"]
    flatten_trigrams = []
    flatten_bigrams = []
    flatten_unigrams = []
    flatten_gensim = []
    for key in k:
        if "trigram" in key:
            flatten_trigrams.append([key["trigram"], key["score"]])
        if "bigram" in key:
            flatten_bigrams.append([key["bigram"], key["score"]])
        if "unigram" in key:
            flatten_unigrams.append([key["unigram"], key["score"]])
        if "gensim" in key:
            flatten_gensim.append([key["gensim"]])

    worksheet.write(y, topic["topic"], "[GENSIM] " + str(flatten_gensim), wrap_test)
    y += 1
    worksheet.write(y, topic["topic"], "[TRIGRAMS] " + str(flatten_trigrams), wrap_test)
    y += 1
    worksheet.write(y, topic["topic"], "[BIGRAMS] " + str(flatten_bigrams), wrap_test)
    y += 1
    worksheet.write(y, topic["topic"], "[UNIGRAMS] " + str(flatten_unigrams), wrap_test)
    y += 1

saved_y_pos2 = y

for topic in topics:
    y = saved_y_pos2
    cluster = topic["cluster"]
    for p in topic["top_phrases"]:
        phrase = re.findall(r"[\w']+|[.,!?;:]|[\s]", p["phrase"])
        #phrase = list(chain(*zip(phrase.split(), cycle(' '))))[:-1]
        for word in cluster:
            if word in phrase:
                index = phrase.index(word)
                phrase.insert(index,red)

        phrase.insert(0,"[SCORE: ")
        phrase.insert(1,p["score"] + "] ")
        worksheet.write_rich_string(y, topic["topic"], *phrase, wrap_test)
        y += 1

workbook.close()













############################################################################################################################################################

# def getDuplicatesWithCount(listOfElems):
#     ''' Get frequency count of duplicate elements in the given list '''
#     dictOfElems = dict()
#     # Iterate over each element in list
#     for elem in listOfElems:
#         # If element exists in dict then increment its value else add it in dict
#         if elem in dictOfElems:
#             dictOfElems[elem] += 1
#         else:
#             dictOfElems[elem] = 1
#
#     return dictOfElems

# for topic in topics:
#     cluster = topic["cluster"]
#     phrases = []
#     topic["top_phrases"] = []
#     csv_phrases[topic["topic"]] = []
#     for sentence in sentences:
#         count = 0
#         for word in cluster:
#             if word in sentence:
#                 count += 1
#         if count >= max_value:
#             phrases.append(sentence)
#     dictOfElems = getDuplicatesWithCount(phrases)
#
#     for key, value in dictOfElems.items():
#         topic["top_phrases"].append( {"phrase":key, "co-occurences": value} )
#         cluster.append(key + "\n\n co-occurs: " + str(value))
#     csv_phrases[topic["topic"]] = cluster
