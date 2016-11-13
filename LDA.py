import sklearn.decomposition
from sklearn.feature_extraction.text import CountVectorizer
import scipy.sparse
import os
import numpy as np
import string

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print('Topic #%d:' % topic_idx)
        print(' '.join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

#stopwordsList = stopwords.words('english')
translator = str.maketrans({key: None for key in string.punctuation})

def preprocess(text, vectorizer=None):
    text.translate(translator)
    tf_vectorizer = None
    if vectorizer:
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features = 20000, vocabulary=vectorizer.vocabulary_)
    else:
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features = 20000, stop_words='english')

    splitText = text.split('\n')
    tf_vectorizer.fit(splitText)
    tf = tf_vectorizer.transform(splitText)
    return (tf, tf_vectorizer)


def getLDAModel():
    lda = sklearn.decomposition.LatentDirichletAllocation(n_topics=10, max_iter = 30)
    with open('news.tsv') as f:
        news = f.read()
        (tf, tf_vectorizer) = preprocess(news)
        tf_feature_names = tf_vectorizer.get_feature_names()
        lda.fit(tf)
        transformed = lda.transform(tf)
        print_top_words(lda, tf_feature_names, 20)
    return (lda, tf_vectorizer, transformed)









'''
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

data = []
indices = []
indptr = []
word2id = {}
id2word = {}
counter = 0
indptr.append(0)
numLines = -1
lines = []

with open('news.tsv') as f:
    news = f.read()
    news.translate(translator)
    lines = news.split('\n')
    numLines = len(lines)
    for line in lines:
        tokens = line.split(' ')
        lineTokens = []
        for token in tokens:
            if token in stopwordsList:
                continue
            if token not in word2id:
                word2id[token] = counter
                id2word[counter] = token
                lineTokens.append(counter)
                counter += 1
            else:
                lineTokens.append(word2id[token])
        lineTokens.sort()
        lineTokens = f7(lineTokens)
        indptr.append(indptr[-1] + len(lineTokens))
        indices = indices + lineTokens

data = [1] * len(indices)

X = scipy.sparse.csr_matrix((data, indices, indptr), shape=(numLines, len(word2id)))
model = sklearn.decomposition.LatentDirichletAllocation()
transformed = model.fit_transform(X=X)
maxIndices = np.argpartition(transformed[:,5], -10)[-10:]
for ind in maxIndices:
    print(lines[ind])
    print('-----------------------------')
'''
