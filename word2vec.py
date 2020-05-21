### Word2Vec Script
import random
import argparse
import io, os
import gensim
from gensim.models import Word2Vec,KeyedVectors
import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

all_keywords = []

### load Google model
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, default="-", help="did not specify file")
args = parser.parse_args()

if args.file != "-":
    path = os.path.dirname(args.file) + "/"
    ### load keywords data
    with open(args.file, 'r') as myfile:
        data = myfile.read()
obj = json.loads(data)

### reorganize json to include vector data
for o in obj:
    w = o["keyword"]
    tokens = w.split()
    #total = 0
    #vecs = []

    for token in tokens:
        if token in model:
            vec = model[token]
            #vecs.append(model[token])
    # if len(vecs) != 0:
    #     for vec in vecs:
    #         total = total + vec
    #     avg = total / len(vecs)
    BRAND = o["brand"]
    all_keywords.append( {"keyword": w, "vec": list(vec.tolist()), "frequency": o["frequency"], "brand": o["brand"]} )

### sizing down vector data
vector_list = list()
word_list = list()
sizedown_vector = list()

for object in all_keywords:
    vector_list.append(object["vec"])

for object in all_keywords:
    word_list.append(object["keyword"])

X = np.asarray(vector_list).astype('float64')
tsne_model = TSNE(n_components=2, perplexity=8, early_exaggeration=24.0, learning_rate=200.0, random_state=0)
np.set_printoptions(suppress=True)

sizedown_vector = tsne_model.fit_transform(X).tolist()

for i, object in enumerate(all_keywords):
    if object["keyword"] == word_list[i]:
        object["vec"] = sizedown_vector[i]

### output new file
with open(path + BRAND + "-vectors.json", 'w') as fp:
    json.dump(all_keywords, fp, indent=4)
