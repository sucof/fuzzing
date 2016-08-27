
import random, sys
import voting_svm as VS


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


def indice_from_list(l, indices):
    return [l[i] for i in indices]


def get_positive_sample(data, label):
    pd = []
    for i in range(len(data)):
        if label[i] == 1:
            pd.append(data[i])

    return pd


def get_negative_sample(data, label):
    nd = []
    for i in range(len(data)):
        if label[i] == 0:
            nd.append(data[i])

    return nd


group_num = 10

from sklearn import metrics
def verify_model(m, x, y):
    print len(x), len(y)
    # m.fit(x, y)
    yp = m.predict(x)
    p = metrics.precision_score(y, yp)
    c = metrics.recall_score(y, yp)
    f = metrics.f1_score(y, yp)

    # print (p, c, f)
    return (p, c, f)

import numpy as np
from sklearn.cross_validation import KFold

def generate_subsets(data):
    data = np.array(data)
    kf = KFold(len(data), n_folds=group_num)
    ss = []
    for train, test in kf:
        strain = data[train]
        stest = data[test]
        ss.append((list(stest), list(strain), test))

    return ss


def divide(data, label):
    np = num_of_positive_samples(label)
    pd = get_positive_sample(data, label)
    nd = get_negative_sample(data, label)
    # sub_n = np / group_num

    spd = generate_subsets(pd)
    # snd = generate_subsets(nd)

    tp = []
    tc = []
    tf = []
    for i in range(group_num):
        (pd_test, pd_train, indice_t1) = spd[i]
        (nd_test, nd_train, indice_t2) = sample_from_list(nd, len(indice_t1))

        pd_train.extend(nd_train)
        data_train = pd_train
        pd_test.extend(nd_test)
        data_test = pd_test
        label_train = [1] * (np - len(indice_t1))
        label_train.extend([0] * (len(label) - np - len(indice_t2)))
        label_test = [1] * len(indice_t1)
        label_test.extend([0] * len(indice_t2))

        m = VS.model(data_train, label_train)

        (p, c, f) = verify_model(m, data_test, label_test)
        tp.append(p)
        tc.append(c)
        tf.append(f)


    ap = sum(tp)/len(tp)
    ac = sum(tc)/len(tc)
    af = sum(tf)/len(tf)
    print ap, ac, af


def model_gen(d, l):
    np = num_of_positive_samples(label)
    pd = get_positive_sample(data, label)
    nd = get_negative_sample(data, label)
    # sub_n = np / group_num

    spd = generate_subsets(pd)
    # snd = generate_subsets(nd)

    tp = []
    tc = []
    tf = []
    for i in range(group_num):
        (pd_test, pd_train, indice_t1) = spd[i]
        
        (nd_test, nd_train, indice_t2) = sample_from_list(nd, len(indice_t1))

        pd_train.extend(nd_train)
        data_train = pd_train
        pd_test.extend(nd_test)
        data_test = pd_test
        label_train = [1] * (np - len(indice_t1))
        label_train.extend([0] * (len(label) - np - len(indice_t2)))
        label_test = [1] * len(indice_t1)
        label_test.extend([0] * len(indice_t2))

        m = VS.model(data_train, label_train)




def preprocess():
    fn = sys.argv[1]
    lines = []

    with open(fn) as f:
        lines = f.readlines()

    r = []
    for l in lines:
        items = l.split(",")
        items = map(lambda i: float(i), items)
        r.append(items)

    #print r
    data = []
    label = []
    for l in r:
        #print i
        data.append(l[:-1])
        label.append(l[-1])

    label = map(int, label)
    return (data, label)


def model(d, l):
    return model_gen(d, l)


if __name__ == '__main__':
    (d, l) = preprocess()
    divide(d, l)
