from sklearn import metrics

def get_range_info(lines):
    index_list = []
    for i in range(len(lines)):
       l = lines[i]
       
       if l == 1:
           index_list.append(i)
    
    print index_list

    range_index = []
    for i in range(len(index_list)-1):
        a = index_list[i]
        b = index_list[i+1]
        range_index.append(b - a)

    print range_index
    if (len(set(range_index)) > 1):
        return -1

    return range_index[0]


import os

def get_bindata(bn):
    fbn = "fv.txt." + bn
    lines = []

    if not os.path.isfile("./" + fbn):
        print "cannot find file", fbn
        return ([], [], [])

    with open(fbn) as f:
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

    return (data, label, [])


def process(m, bn):
    (d, l, fn) = get_bindata(bn)
    if d == []:
        return -1
    return process_bin(m, d, l, fn, bn)


def process_bin(m, x, y, fnl, bn):
    r = get_range_info(y)
    if r == -1:
        print "failed"
        return 0.0


    n = len(x) / (r-1)
    res = []
    # print y

    fn = ""
    for i in range(n):
        a = i*(r-1)
        b = (i+1)*(r-1)

        xt = x[a:b]
        yt = y[a:b]

        res.append((verify_model(m, xt, yt, i)))

    print res

    c1 = 0
    c2 = 0
    c3 = 0
    for i in res:
        if i[0] == 1:
            c1 += 1
        if i[1] == 1:
            c2 += 1
        if i[2] == 1:
            c3 += 1

    c1 = c1/float(n)
    c2 = c2/float(n)
    c3 = c3/float(n)


    return (c1, c2, c3)


check_rank = 5

def verify_model(m, xt, yt, iiii):
    global check_rank
    ypp = m.predict_proba(xt)

    ypn = zip(range(0, len(ypp)), ypp)

    ypn.sort(key=lambda x: x[1][1])

    ypp1 = map(lambda x: x[1], ypp)
    
    ypns = sorted(ypp1)
    max_plist = []
    ypns.reverse()

    res = []
    check_rank = 1
    max_plist = ypns[0:check_rank]

    typn = []
    for yx in ypn:
        if any([abs(x - yx[1][1]) < 0.00001 for x in max_plist]):
            typn.append(yx[0])

    if iiii in typn:
        res.append(1)
    else:
        res.append(0)

    check_rank = 3
    max_plist = ypns[0:check_rank]

    typn = []
    for yx in ypn:
        if any([abs(x - yx[1][1]) < 0.00001 for x in max_plist]):
            typn.append(yx[0])

    if iiii in typn:
        res.append(1)
    else:
        res.append(0)

    check_rank = 5
    max_plist = ypns[0:check_rank]

    typn = []
    for yx in ypn:
        if any([abs(x - yx[1][1]) < 0.00001 for x in max_plist]):
            typn.append(yx[0])

    if iiii in typn:
        res.append(1)
    else:
        res.append(0)

    return res


rrr = []


def verify_model_update(m, xt, yt, iiii):
    ypp = m.predict_proba(xt)
    

    ypn = zip(range(0, len(ypp)), ypp)

    ypn.sort(key=lambda x: x[1][1])

    ypp1 = map(lambda x: x[1], ypp)
    ypns = sorted(list(set(ypp1)))
    max_plist = []
    ypns.reverse()
    max_plist = ypns[0:check_rank]

   
    typn = []
    for yx in ypn:
        if any([abs(x - yx[1][1]) < 0.0001 for x in max_plist]):
            typn.append(yx[0])


    
    tl = len(xt)
    r = [0] * tl
    for kk in typn:
        r[kk] = 1


    res = []
    for i in range(len(xt)):
        xt[i].append(yt[i])
        xt[i].append(r[i])
        res.append(xt[i])

    global rrr
    rrr.extend(res)

    return 0



if __name__ == '__main__':
    binl = []
    with open("binlist") as f:
        binl = f.readlines()

    binl = map(lambda n:str.strip(n), binl)

    divide(binl)
