import re, os

regex1 = re.compile(r'<(.*)@',re.I)
plts = {}


def function_simplify(fn):
    if fn.endswith("_chk"):
        fn = fn[:-4]

    if fn.startswith("__"):
        fn = fn[2:]

    return fn


def dump_pltinfo(bn, bp):
    global plts

    os.system("objdump -Dr -j .plt " + bp + "/" + bn + " > plt.info")

    lines = []
    with open("plt.info") as f:
        lines = f.readlines()

    for l in lines:
        if l.startswith("00"):
            a = int(l.split()[0], 16)
            fn = regex1.search(l).groups()[0]
            plts[a] = function_simplify(fn)



def preprocess(bn, bp):
    dump_pltinfo(bn, bp)


def trans(addr):
    if addr in plts:
        return plts[addr]
    else:
        return "undefined"



if __name__ == '__main__':
    bp = ""
    bn = ''
    process(bn, bp)
