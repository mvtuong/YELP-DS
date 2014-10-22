from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np
from numpy.linalg import norm

import os
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from mpl_toolkits.mplot3d import Axes3D

filenames = ['Data/1star/1StarsSamples.json', 'Data/2star/2StarsSamples.json', 'Data/3star/3StarsSamples.json', 'Data/4star/4StarsSamples.json', 'Data/5star/5StarsSamples.json']

vectorizer = CountVectorizer(input='filename', ngram_range=(1,3), stop_words='english', strip_accents='unicode', token_pattern=ur'\b\w+\b')

dtm = vectorizer.fit_transform(filenames).toarray()

vocab = np.array(vectorizer.get_feature_names())

names = [os.path.basename(fn).replace('Samples.json', '') for fn in filenames]

dist = 1 - cosine_similarity(dtm)


_vectorizer = CountVectorizer(input='content', ngram_range=(1,3), stop_words='english', strip_accents='unicode', token_pattern=ur'\b\w+\b')
analyze = vectorizer.build_analyzer()
analyzed = analyze('Data/1star/1StarsSamples.json')
result = [0.0, 0.0, 0.0, 0.0, 0.0]
res = []
for item in analyzed:
    feature_index = vectorizer.vocabulary_.get(item)
    item_histogram = dtm[:, feature_index] #dtm[:, feature_index]*1.0/sum(dtm[:, feature_index])
    #result = np.dot(result, item_histogram)
    result = [x + y for x, y in zip(result, item_histogram)]
for item in result:
    item = item*1.0/sum(result)
    res.append(item)
print(res)

"""
#Visualization the data into 2D
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
pos = mds.fit_transform(dist)
xs, ys = pos[:, 0], pos[:, 1]
for x, y, name in zip(xs, ys, names):
    color = 'orange' if "Austen" in name else 'skyblue'
    plt.scatter(x, y, c=color)
    plt.text(x, y, name)
plt.show()
#Visualization the data into 3D
mds = MDS(n_components=3, dissimilarity="precomputed", random_state=1)
pos = mds.fit_transform(dist)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2])
for x, y, z, s in zip(pos[:, 0], pos[:, 1], pos[:, 2], names):
    ax.text(x, y, z, s)
plt.show()

"""
