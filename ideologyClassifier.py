import sklearn.decomposition
from sklearn.feature_extraction.text import CountVectorizer
import scipy.sparse
import os
import numpy as np
import string
import newspaper
from newspaper import Article
from sklearn.neighbors import KNeighborsClassifier

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
            if token not in word2id:
                word2id[token] = counter
                id2word[counter] = token
                lineTokens.append(counter)
                counter += 1
            else:
                lineTokens.append(word2id[token])
        lineTokens.sort()
        indptr.append(indptr[-1] + len(lineTokens))
        indices = indices + lineTokens
data = [1] * len(indices)

X = scipy.sparse.csr_matrix((data, indices, indptr), shape=(numLines, len(word2id)))

left = [1] * 317
right = [0] * 116
labels = np.concatenate((left, right), axis=0)

neigh = KNeighborsClassifier(n_neighbors=5)
neigh.fit(X, labels)

def classifyNewArticle(news):
    '''
    # get article text
    newsArticle = Article(url="http://nypost.com/2016/11/11/scenes-from-the-liberal-meltdown/")
    newsArticle.download()
    newsArticle.parse()
    news = newsArticle.text.replace('\n', ' ')
    '''

    # create feature vector
    data = []
    indices = []
    indptr = []
    counter = 0
    indptr.append(0)
    numLines = -1
    lines = []

    news.translate(translator)
    lines = news.split('\n')
    numLines = len(lines)
    for line in lines:
        tokens = line.split(' ')
        lineTokens = []
        for token in tokens:
            if token not in word2id:
                continue
            else:
                lineTokens.append(word2id[token])
        lineTokens.sort()
        indptr.append(indptr[-1] + len(lineTokens))
        indices = indices + lineTokens
    data = [1] * len(indices)

    test = scipy.sparse.csr_matrix((data, indices, indptr), shape=(numLines, len(word2id)))

    return neigh.predict(test)
