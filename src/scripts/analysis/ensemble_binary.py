
import random, sys
import ensemble as EN
import voting_svm as VS
import verify_model as VM


import numpy as np
from sklearn.cross_validation import KFold

group_num = 10
def generate_subsets(data):
    def aux_expand(bl):
        # expend the binlist
        fnl = ["gccO0vsgccO3", "gccO2vsgccO3", "iccO0vsiccO3", "iccO2vsiccO3", "llvmO0vsllvmO3", "llvmO2vsllvmO3"]
        dl = []
        b1 = [bl + "." + fn for fn in fnl]
        dl.extend(b1)

        return dl

    ss = []
    
    for d in data:
        b1 = aux_expand(d)
        ss.extend(b1)

    return ss

import os
def prepare_data_train(bn):
    fbn = "new.fv.txt." + bn
    lines = []

    if not os.path.isfile("./" + fbn):
        print "cannot find file", fbn
        return ([], [])

    with open(fbn) as f:
        lines = f.readlines()

    r = []
    for l in lines:
        items = l.split(",")
        items = map(lambda i: float(i), items)
        r.append(items)

    #
    data = []
    label = []
    for l in r:
        
        data.append(l[:-1])
        label.append(l[-1])

    label = map(int, label)
    return (data, label)



def prepare_data_test(bn):
    fbn1 = "fv.txt." + bn + ".test"
    fbn2 = "fv.txt." + bn + ".train"
    lines = []

    with open(fbn1) as f:
        lines = f.readlines()

    with open(fbn2) as f:
        lines.extend(f.readlines())

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


def get_bindata_train(binlist):
    data = []
    label = []
    for b in binlist:
        (d, l) = prepare_data_train(b)
        data.extend(d)
        label.extend(l)

    return (data, label)


def get_bindata_test(binlist):
    data = []
    label = []
    for b in binlist:
        (d, l) = prepare_data_test(b)
        data.extend(d)
        label.extend(l)

    return (data, label)


from sklearn import metrics
def verify_model(m, x, y):
    print len(x), len(y)
    # m.fit(x, y)
    yp = m.predict(x)
    yp1 = filter(lambda i: i == 1, yp)
    print len(yp1)
    yp1 = filter(lambda i: i == 1, y)
    print len(yp1)
    p = metrics.precision_score(y, yp)
    c = metrics.recall_score(y, yp)
    f = metrics.f1_score(y, yp)

    # print (p, c, f)
    return (p, c, f)


def print_out(al):
    # fnl = ["gccO0vsgccO3", "gccO2vsgccO3", "iccO0vsiccO3", "iccO2vsiccO3", "llvmO0vsllvmO3", "llvmO2vsllvmO3"]
    # fnl = ["gccO0vsiccO3", "gccO0vsllvmO3", "iccO0vsllvmO3", "iccO0vsgccO3", "llvmO0vsiccO3", "llvmO0vsgccO3"]
    fnl = ["gccO0vsgccO3"]
    # fnl = ["gccO0vsiccO3"]
    # fnl = ["gccO0vsllvmO3"]
    # fnl = ["iccO0vsllvmO3"]
    # fnl = ["llvmO0vsgccO3", "llvmO0vsiccO3"]
    # fnl = ["iccO0vsgccO3"]
    # fnl = ["iccO0vsllvmO3bcf", "iccO0vsllvmO3fla"]
    # fnl = ["gccO0vsllvmO3fla"]
    # fnl = ["gccO0vsllvmO3bcf"]
    # fnl = ["llvmO0vsllvmO3bcf"]
    # fnl = ["llvmO0vsllvmO3fla"]
    # fnl = ["llvmO0vsllvmO3sub"]
    # fnl = ["llvmO2vsllvmO3sub", "llvmO2vsllvmO3fla", "llvmO2vsllvmO3bcf"]
    # fnl = ["llvmO0vsllvmO3sub", "llvmO0vsllvmO3fla", "llvmO0vsllvmO3bcf"]
    # fnl = ["llvmO0vsllvmO3sub", "llvmO0vsllvmO3fla", "llvmO0vsllvmO3bcf"]
    # fnl = ["llvmO0vsllvmO3sub", "llvmO0vsllvmO3fla", "llvmO0vsllvmO3bcf", "llvmO2vsllvmO3sub", "llvmO2vsllvmO3fla", "llvmO2vsllvmO3bcf", "llvmO3vsllvmO3sub", "llvmO3vsllvmO3fla", "llvmO3vsllvmO3bcf"]
    # fnl = ["llvmO3vsllvmO3fla", "llvmO3vsllvmO3bcf"]
    # fnl = ["gccO0vsllvmO3sub", "gccO0vsllvmO3fla", "gccO0vsllvmO3bcf", "iccO0vsllvmO3sub", "iccO0vsllvmO3fla", "iccO0vsllvmO3bcf"]
    # fnl = ["llvmO0vsllvmO3sub", "llvmO0vsllvmO3fla", "llvmO0vsllvmO3bcf", "llvmO2vsllvmO3sub", "llvmO2vsllvmO3fla", "llvmO2vsllvmO3bcf", "llvmO3vsllvmO3sub", "llvmO3vsllvmO3fla", "llvmO3vsllvmO3bcf"]
    # fnl = ["llvmO0vsllvmO3sub", "llvmO0vsllvmO3fla", "llvmO0vsllvmO3bcf", "llvmO3vsllvmO3sub", "llvmO3vsllvmO3fla", "llvmO3vsllvmO3bcf"]
    # fnl = ["llvmO0vsllvmO3sub"]
    # fnl = ["gccO0vsiccO3"]
    fnl = ["llvmO0vsllvmO3sub", "llvmO0vsllvmO3fla", "llvmO0vsllvmO3bcf"]
    for fn in fnl:
        print "-------------", fn, "------------------"
        av1 = []
        av2 = []
        av3 = []
        for a in al:
            if fn in a[0]:
                if a[1] == -1:
                    print "failed to verify", a[0]
		else:
                    # print "|", a[0], "|", a[1][0], "|", a[1][1], "|", a[1][2]
                    if a[1][0] > 0:
                        av1.append(a[1][0])
                    if a[1][1] > 0:
                        av2.append(a[1][1])
                    if a[1][2] > 0:
                        av3.append(a[1][2])
                    else:
                        raise Exception("undefined behavior")

        print sum(av1) / float(len(av1))
        print sum(av2) / float(len(av2))
        print sum(av3) / float(len(av2))
        print "---------------------------------------"


def get_test_bin(binl):
    # fnl = "gccO0vsiccO3"
    # fnl = ["gccO0vsllvmO3"]
    # fnl = ["iccO0vsllvmO3"]
    # fnl = ["llvmO0vsgccO3", "llvmO0vsiccO3"]
    # fnl = ["iccO0vsgccO3"]
    # fnl = ["iccO0vsllvmO3bcf", "iccO0vsllvmO3fla"]
    # fnl = ["iccO0vsllvmO3sub"]
    # fnl = ["gccO0vsllvmO3sub"]
    # fnl = ["gccO0vsllvmO3fla"]
    # fnl = ["gccO0vsllvmO3bcf"]
    # fnl = ["gccO0vsiccO3", "gccO0vsllvmO3", "iccO0vsllvmO3", "iccO0vsgccO3", "llvmO0vsiccO3", "llvmO0vsgccO3"]
    # fnl = "llvmO0vsllvmO3bcf"
    # fnl = "llvmO0vsllvmO3fla"
    # fnl = "llvmO0vsllvmO3sub"
    # fnl = ["llvmO2vsllvmO3sub"]
    # fnl = ["llvmO2vsllvmO3sub", "llvmO2vsllvmO3fla", "llvmO2vsllvmO3bcf"]
    # fnl = ["llvmO0vsllvmO3sub", "llvmO0vsllvmO3fla", "llvmO0vsllvmO3bcf", "llvmO2vsllvmO3sub", "llvmO2vsllvmO3fla", "llvmO2vsllvmO3bcf", "llvmO3vsllvmO3sub", "llvmO3vsllvmO3fla", "llvmO3vsllvmO3bcf"]
    fnl = ["llvmO0vsllvmO3sub", "llvmO0vsllvmO3fla", "llvmO0vsllvmO3bcf"]
    # fnl = ["gccO0vsiccO3", "gccO0vsllvmO3", "iccO0vsllvmO3", "iccO0vsgccO3", "llvmO0vsiccO3", "llvmO0vsgccO3"]
    # fnl = ["gccO0vsgccO3"]
    # fnl = ["llvmO3vsllvmO3fla", "llvmO3vsllvmO3bcf"]
    # fnl = ["gccO0vsllvmO3sub", "gccO0vsllvmO3fla", "gccO0vsllvmO3bcf", "iccO0vsllvmO3sub", "iccO0vsllvmO3fla", "iccO0vsllvmO3bcf"]
    # fnl = ["llvmO0vsllvmO3sub"]
    # fnl = ["gccO0vsiccO3"]
    # fnl = ["gccO0vsllvmO3sub", "gccO0vsllvmO3fla", "gccO0vsllvmO3bcf", "iccO0vsllvmO3sub", "iccO0vsllvmO3fla", "iccO0vsllvmO3bcf"]
    dl = []
    for n in binl:
        for fn in fnl:
            dl.append(n + "." + fn)

    return dl


def divide(binl):
    # divide the binary list into test/train subsets.
    spd = generate_subsets(binl)
    testbin = get_test_bin(binl)

    tp = []
    tc = []
    tf = []
    bnl = []
    al = []
    trainbin = spd
    (data_train, label_train) = get_bindata_train(trainbin)

    # print testbin, trainbin
    m = VS.model(data_train, label_train)
    # return

    for tn in testbin:
        print 'check', tn
        a = VM.process(m, tn)
        al.append((tn, a))

    print_out(al)


if __name__ == '__main__':
    os.system("python preprocess.py > t")
    binl = []
    with open("binlist") as f:
        binl = f.readlines()

    binl = map(lambda n:str.strip(n), binl)

    divide(binl)
