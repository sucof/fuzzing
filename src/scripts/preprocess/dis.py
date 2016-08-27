from __future__ import print_function
import distance, os, sys
from tabulate import tabulate

def warning(*objs):
    print(*objs, file=sys.stderr)

def hamming(v1, v2):
    return distance.hamming(v1, v2)

def jaccard(v1, v2):
    return distance.jaccard(v1, v2)

def similarity_func(v1, v2):

    return jaccard(v1, v2)


def similairity_func_iter(ref, vl):

    return sorted(distance.ifast_comp(ref, vl))[0]



def similarity_func_iter(fn1, fn2):
    return

def similairity_bin(fn1, fn2):
    return


def aux(v):
    
    if str.strip(v).isdigit() == True:
        return int(v)
    elif str.strip(v).startswith("['") == True:
        
        v = str.strip(v)
        v = v[1:-1]
       
        return v
    else:
        return v


def filter_by_index(v):
    l = len(v)
    v1 = range(l)
    vv = zip(v1, v)
    vv = filter(lambda vi: not (vi[0] % 4 == 0), vv)

    return map(lambda v: v[1], vv)


def compare_iter_mul(fn1, fn2, fl1, fl2, res):
    fn1 = os.path.basename(fn1)
    fn2 = os.path.basename(fn2)

    # print res

    rr = []

    for k, v in res.items():
        items = k.split("_")
        opt1 = items[3]
        func1 = "_".join(items[5:])

        for k1, v1 in res.items():
            items = k1.split("_")
            opt2 = items[3]
            func2 = "_".join(items[5:])

            if not (opt1 == opt2):
                
                v1 = res[k]
                v2 = res[k1]
                v1 = v1.split(",")
                v2 = v2.split(",")
               
                v1 = map(aux, v1)
                v2 = map(aux, v2)

              

                v1 = filter_by_index(v1)
                v2 = filter_by_index(v2)

                print (v1)
                print (v2)

                warning(opt1, ": ", func1, ' ----> ', opt2, ": ", func2, similarity_func(v1, v2))
                print (opt1, ": ", func1, ' ----> ', opt2, ": ", func2, similarity_func(v1, v2))



def compare_iter(fn1, fn2, fl1, fl2, res):
    fn1 = os.path.basename(fn1)
    fn2 = os.path.basename(fn2)

    rr = ["function name", "level1", "level3", "distance"]
    for fl in fl1:
        fnn1 = fn1 + "_" + fl + " "
        fnn2 = fn2 + "_" + fl + " "

        if fnn1 in res and fnn2 in res:
            
            v1 = res[fnn1]
            v2 = res[fnn2]
            v1 = v1.split(",")
            v2 = v2.split(",")
           
          
            v1 = map(aux, v1)
            v2 = map(aux, v2)

         
        
       
            rr.append([fl, "op0 ", "op3", similarity_func(v1, v2)])
        elif fnn1 not in res and fnn2 not in res:
      
            pass
        else:

            raise Exception("undefined behavior")


def process(fn1, fn2, res):

    lines = []

    
    fn1 = os.path.basename(fn1)
    fn2 = os.path.basename(fn2)

    print (res)

    with open(fn1 + "_info.txt") as f:
        lines = f.readlines()

    fnl1 = []
    for l in lines:
        fnl1.append(l.split(":")[0])

    fnl1 = map(lambda f : str.strip(f), fnl1)

    
    with open(fn2 + "_info.txt") as f:
        lines = f.readlines()

    fnl2 = []
    for l in lines:
        fnl2.append(l.split(":")[0])

    fnl2 = map(lambda f : str.strip(f), fnl2)


    if len(fnl1) <= len(fnl2):
        compare_iter_mul(fn1, fn2, fnl1, fnl2, res)
    else:
        compare_iter_mul(fn2, fn1, fnl2, fnl1, res)
