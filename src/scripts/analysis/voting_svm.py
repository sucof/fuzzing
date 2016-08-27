import os, random
from sklearn import ensemble
from sklearn.externals.six import StringIO
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier

from time import time
from operator import itemgetter
from scipy.stats import randint as sp_randint

import numpy as np

from sklearn.ensemble import RandomForestClassifier


import resampling as RS
from numpy import array


def process(r):
    #print r
    data = []
    label = []
    for i in r:
        #print i
        data.append(i[:-1])
        label.append(i[-1])

    label = map(int, label)
    # print label
    return (data, label)


def model(data, label):
    print "begin train"
    datan = array(data)
    labeln = array(label)
    
    (usx, usy) = RS.undersampling(datan, labeln)

    return train(usx, usy)


def train_ee(x_train, y_train):
    print "training model"
    clf = svm.LinearSVC(C=2^4).fit(x_train, y_train)
    return ("ee", clf)


def test_ee(clf, x, y):
    a = cross_val_score(clf, x, y, cv=5, scoring='accuracy')
    p = cross_val_score(clf, x, y, cv=5, scoring='precision')
    r = cross_val_score(clf, x, y, cv=5, scoring='recall')
    f1 = cross_val_score(clf, x, y, cv=5, scoring='f1')
    aa = float(sum(a))/len(a)
    pa = float(sum(p))/len(p)
    ra = float(sum(r))/len(r)
    fa = float(sum(f1))/len(f1)

    print aa, pa, ra, fa


from sklearn.ensemble import ExtraTreesClassifier




def train(x_train, y_train):
    print "training size ", len(y_train)

    clf = ExtraTreesClassifier(n_estimators=100, n_jobs=24).fit(x_train, y_train)
    return clf


def num_of_positive_samples(label):
    c = 0
    for l in label:
        if l == 1:
            c += 1

    return c


def sample_from_list(l, K):
    indices = random.sample(range(len(l)), K)
    sample_set = [l[i] for i in indices]

    unsample_set = []
    for i in range(len(l)):
        if not(i in indices):
            unsample_set.append(l[i])

    return (sample_set, unsample_set, indices)


def get_positive_sample(data, label):

    pd = []
    for i in range(len(data)):
        if label[i] == 1:
            pd.append(data[i])

    return pd


# Utility function to report best scores
def report(grid_scores, n_top=1):
    top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
    for i, score in enumerate(top_scores):
        print("Model with rank: {0}".format(i + 1))
        print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
              score.mean_validation_score,
              np.std(score.cv_validation_scores)))
        print("Parameters: {0}".format(score.parameters))
        print("")


def get_negative_sample(data, label):
    nd = []
    for i in range(len(data)):
        if label[i] == 0:
            nd.append(data[i])

    return nd


if __name__ == '__main__':
    lines = []
    with open("fv.csv") as f:
        lines = f.readlines()

    r = []
    for l in lines:
        items = l.split(",")
        items = map(lambda i: float(i), items)
        r.append(items)

    (d, l) = process(r)

    np = num_of_positive_samples(l)

    (dp) = get_positive_sample(d, l)
    (dn) = get_negative_sample(d, l)
    (lp) = get_positive_sample(l, l)
    (ln) = get_negative_sample(l, l)
    print len(dn), np

    dn1 = sample_from_list(dn, np)[0]
    ln1 = sample_from_list(ln, np)[0]

    dp.extend(dn1)
    lp.extend(ln1)
    

