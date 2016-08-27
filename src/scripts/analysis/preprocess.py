import os

def check_threshold(items):
    items = map(float, items)
    s = sum(items)
    s1 = len(items) - 2.0
    if s > 1 * s1:
        return True
    else:
        return False

def adjust(i):
    lines = []
    with open(i) as f:
        lines = f.readlines()

    nlines = []
    for l in lines:
        l1 = l.strip()
        items = l1.split(",")
        t = len(items)
        k = filter(lambda x: x == '1', items)
        print items, t, k, len(k)
        if len(k) == t-2 or check_threshold(items[:-1]):
            l1 = l1[:-1] + "1"


        l1 = l1 + "\n"
        nlines.append(l1)

    with open("new." + i, 'w') as f:
        f.writelines(nlines)


for i in os.listdir(os.getcwd()):
    if i.startswith("fv.txt.") and "new" not in i:
        adjust(i)
    else:
        continue
