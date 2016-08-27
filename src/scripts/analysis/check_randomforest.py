from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris



def preprocess(fn):
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


if __name__ == '__main__':
    data = load_iris()

    dt = data.data[0:120]
    lt = data.target[0:120]

    dte = data.data[120:150]
    lte = data.target[120:150]

    clf = RandomForestClassifier(n_estimators=10)
    clf = clf.fit(dt, lt)

    pl = clf.predict_proba(dte)

    for i in range(len(pl)):
        print lte[i], '--->', pl[i]


