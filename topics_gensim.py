### LDA Topic Modeling - Gensim Implementation
import os, io, json
import pandas as pd
import argparse
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import spacy
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words = []

csv_lda_topics = {}
json_lda_topics = []

BRAND = "all"
corpus = []
a = []

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, default="-", help="did not specify file")
args = parser.parse_args()

if args.file != "-":
    path = os.path.dirname(args.file) + "/"
    if args.file.endswith('.csv'):
        raw = io.open(args.file, 'r',encoding='utf-8')
        path = os.path.dirname(args.file) + "/"
        posts = pd.read_csv(args.file)
        print("Number of social posts:",len(posts['posts']))
    elif args.file.endswith('.txt'):
        raw = io.open(args.file, 'r',encoding='utf-8')
        txt = raw.read().lower().split('\n')

for i in range(len(posts['posts'])):
    a=posts['posts'][i]
    corpus.append(a)

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

data_words = list(sent_to_words(corpus))

# Build the bigram and trigram models
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if (word not in stop_words) and (word.isalpha())] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

# Remove Stop Words
data_words_nostops = remove_stopwords(data_words)
print("here - nostops")
# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)
print("here - bigrams")

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
nlp.max_length = 4551473
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
print("here - lemma")

id2word = corpora.Dictionary(data_lemmatized) # Create Dictionary
texts = data_lemmatized # Create Corpus
corpus = [id2word.doc2bow(text) for text in texts] # Term Document Frequency

print("here - mallet") # Mallet LDA model
num_topics = [10,15,20]
mallet_path = 'mallet-2.0.8/bin/mallet'
count = 0
while count < 3:
    ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics[count], id2word=id2word)
    topics_mallet = ldamallet.show_topics(num_words=10, formatted=False, num_topics=num_topics[count])

    for topic in topics_mallet:
        top_words = []
        json_top_words = []
        #json_weights = []
        for word in topic[1]:
            top_words.append(word[0])
            top_words.append(round(word[1],3))
            json_top_words.append(word[0])
            #json_weights.append(round(word[1],3))
        #csv_lda_topics[topic[0]] = top_words
        #, "weights": json_weights
        json_lda_topics.append( {"topic": topic[0], "cluster": json_top_words})

    # df = pd.DataFrame(csv_lda_topics)
    # df.to_excel(path + '-topics-' + str(num_topics) + '.xlsx', index=False, encoding='utf-8')

    with open(path + "topics-" + str(num_topics) + ".json", 'w') as fp:
        json.dump(json_lda_topics, fp)
    count += 1

coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence_ldamallet = coherence_model_ldamallet.get_coherence()
print('\nCoherence Score: ', coherence_ldamallet) # Compute Coherence Score




####################################################################################################################################################################################

#print([[(id2word[id], freq) for id, freq in cp] for cp in corpus[:1]])

# Regular LDA model
# lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
#                                            id2word=id2word,
#                                            num_topics=20,
#                                            random_state=100,
#                                            update_every=1,
#                                            chunksize=100,
#                                            passes=30,
#                                            alpha='auto',
#                                            per_word_topics=True)
# print(lda_model.print_topics())
# print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.
#
# coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
# coherence_lda = coherence_model_lda.get_coherence()
# print('\nCoherence Score: ', coherence_lda)
