import distance, os, sys
from tabulate import tabulate

from ctypes import cdll
import ctypes
lib = cdll.LoadLibrary('./liblcs.so')


def lcs_length(a, b):
    table = [[0] * (len(b) + 1) for _ in xrange(len(a) + 1)]
    for i, ca in enumerate(a, 1):
        for j, cb in enumerate(b, 1):
            table[i][j] = (
                table[i - 1][j - 1] + 1 if ca == cb else
                max(table[i][j - 1], table[i - 1][j]))
    return table[-1][-1]


def lcs(a, b):
    
    max_lcs = 0
   
  
 

    ml = max(len(a), len(b))

    if all(i == '' for i in a):
        a = ['']
    if all(i == '' for i in b):
        b = ['']

    if ml == 0:
        return 1
    elif (a == [''] and b == ['']):
        return 1
    elif a == [''] or b == ['']:
	return 0
    else:
        ac = a[0]
        a[0], b[0]
        
       
      
        if isinstance(a[0], (int, long)) and isinstance(b[0], (int, long)):
            
            la = len(a)
            lb = len(b)
           
            maxJ = min(la, lb) / float(max(la, lb))
            if maxJ < max_lcs:
                return max_lcs
            else:
                an = (ctypes.c_ulong * la)()
                bn = (ctypes.c_ulong * lb)()
	        print ("length ", la, lb)
                for i in range(la):
                    an[i] = a[i]
                for i in range(lb):
                    bn[i] = b[i]
                lcsl = lib._Z9LCSLengthPmS_mm(an, bn, la, lb) / float(ml)
                return lcsl / float(la + lb - lcsl)
        else:

            la = len(a)
            lb = len(b)
            maxJ = min(la, lb) / float(max(la, lb))
            if maxJ < max_lcs:
                return max_lcs
            else:
                print "python lcs"
                lcsl = lcs_length(a, b) / float(ml)
                
                return lcsl / float(la + lb - lcsl)



def translate(a):
    l1 = []

    l2 = []
    l3 = []
    l4 = []
    l5 = []
    l6 = []
    l7 = []
    l8 = []
    l9 = []
    l10 = []
    l11 = []
    l12 = []
    l13 = []

    l14 = []


    for i in a:
        
        l1.append(i[0])

       
        l2.extend(i[1])
      
        l3.extend(i[2])
        
        l4.extend(i[3])
       
        l5.extend(i[4])
      
        l6.extend(i[5])
        l7.extend(i[6])
        l8.extend(i[7])
        l9.extend(i[8])
        l10.extend(i[9])
        l11.extend(i[10])
        l12.extend(i[11])
        l13.extend(i[10])
        l14.extend(i[11])

    return (l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14)


def process(fn1, fn2, res, failed_list):
    lines = []

    fn1 = os.path.basename(fn1)
    fn2 = os.path.basename(fn2)

    

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
        compare_iter_mul_threads(fn1, fn2, fnl1, fnl2, res)
        
    else:
        compare_iter_mul_threads(fn2, fn1, fnl2, fnl1, res)
       


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

            (rvs1, mrs1, mws1, lib1) = translate(v1)
            (rvs2, mrs2, mws2, lib2) = translate(v2)

            s1 = lcs(rvs1, rvs2)
            s2 = lcs(mrs1, mrs2)
            s3 = lcs(mws1, mws2)
            s4 = lcs(lib1, lib2)




            sa = sum([s1, s2, s3, s4]) / 4.0

            rr.append([fl, "op0 ", "op3", sa])
        elif fnn1 not in res and fnn2 not in res:

            pass
        else:


            raise Exception("undefined behavior")




def process_single_comp(k, v, k1, v1):
    if len(v1) == 0:
        print "failed in ", k
 	raise Exception("failed")
        return None

    items = k1.split("_")
    opt2 = items[3]
    func2 = "_".join(items[5:])

    items = k.split("_")
    opt1 = items[3]
    func1 = "_".join(items[5:])

    if not (opt1 == opt2) and (opt1 < opt2):
        v2 = v1
        v1 = v

        (rvs1, mrs1, mws1, gotpltr1, gotpltw1, rodr1, rodw1, dr1, dw1, bssr1, bssw1, rhw1, rhr1, lib1) = translate(v1)
        (rvs2, mrs2, mws2, gotpltr2, gotpltw2, rodr2, rodw2, dr2, dw2, bssr2, bssw2, rhw2, rhr2, lib2) = translate(v2)

        sl = []
        sl.append(lcs(rvs1, rvs2))
        sl.append(lcs(mrs1, mrs2))
        sl.append(lcs(mws1, mws2))
        sl.append(lcs(gotpltr1, gotpltr2))
        sl.append(lcs(gotpltw1, gotpltw2))
        sl.append(lcs(rodr1, rodr2))
        sl.append(lcs(rodw1, rodw2))
        sl.append(lcs(dr1, dr2))
        sl.append(lcs(dw1, dw2))
        sl.append(lcs(bssr1, bssr2))
        sl.append(lcs(bssw1, bssw2))
        sl.append(lcs(rhw1, rhw2))
        sl.append(lcs(rhr1, rhr2))
        sl.append(lcs(lib1, lib2))

        dump_fv_into_file(func1, func2, sl)
    else:
        return None

fv = []


def dump_fv_into_file(fn1, fn2, sl):
    print "dump_fv_into_file"
    global fv

    if fn1 == fn2:
        
        sl.append(1)
        fv.append(sl)
    else:
        sl.append(0)
        fv.append(sl)

    print "dump_fv_into_file finished"


import itertools

def compare_iter_mul_threads(fn1, fn2, fl1, fl2, res):
   fn1 = os.path.basename(fn1)
   fn2 = os.path.basename(fn2)
   start_threads(res)

   global total_res
   tt = similarity_sort(total_res)

   ttt = tabulate(tt, headers=['op1', 'func1', 'op2', 'func2', 'similarity'], tablefmt='orgtbl')
   print ttt
   with open("sim_output.txt", 'w') as f:
	f.writelines(ttt)


def compare_iter_mul(fn1, fn2, fl1, fl2, res):
   fn1 = os.path.basename(fn1)
   fn2 = os.path.basename(fn2)

   tt = []

   for k, v in res.iteritems():
       if len(v) == 0:
           print "failed in ", k, v
	   raise Exception("sdasd")
           continue

       items = k.split("_")
       opt1 = items[3]
       func1 = "_".join(items[5:])

       ttt  = []
       for k1, v1 in res.iteritems():
           items = k1.split("_")
           opt2 = items[3]
           func2 = "_".join(items[5:])

           print k1, k
           if not ("dir_put_indicator" in k1) or not ("O0" in k):
               continue

           print "process ", k, k1
           
           sa = process_single_comp(k, v, k1, v1)
           if sa:
               ttt.append((opt1, func1, opt2, func2, sa))

       if ttt:
           tt.append(ttt)

   print tabulate(tt, headers=['op1', 'func1', 'op2', 'func2', 'similarity'], tablefmt='orgtbl')
   print ""
   tt = similarity_sort(tt)
   print tabulate(tt, headers=['op1', 'func1', 'op2', 'func2', 'similarity'], tablefmt='orgtbl')


def similarity_sort(res):
    new_res = []
    for r in res:
        rs = sorted(r,key=lambda x: x[4])
        max_similarity = rs[-1][4]

        max_t = []
        
        target = None
        target_in_max = False
        for rr in rs:
            if max_similarity == rr[4]:
                max_t.append(rr)
                if rr[1] == rr[3]:
                    target_in_max = True
            if rr[1] == rr[3]:
                target = rr

        if not target:
            op1 = rs[0][0]
            op2 = rs[0][2]
            func1 = rs[0][1]
            target = (op1, func1, op2, func1, "failed")

        if target_in_max == True:
            new_res.extend(max_t)
        else:
            max_t.append(target)
            new_res.extend(max_t)

    return new_res




import threading, os, sys, os.path


total_res = []

class lcs_engine(threading.Thread):

    def __init__(self, thread_id, l, res):
        threading.Thread.__init__(self)
	print "create ", thread_id
        self.ti = thread_id
        
        self.l = l
       
        self.res = res

    def run(self):
        global total_res

        for (k, v) in self.l:
            if len(v) == 0:
                print "failed in ", k, v
                raise Exception("cannot handle zero list")
                continue

            items = k.split("_")
            opt1 = items[3]
            func1 = "_".join(items[5:])

            ttt  = []
            
            for k1, v1 in sorted(self.res.iteritems()):

                items = k1.split("_")
                opt2 = items[3]
                func2 = "_".join(items[5:])

                print len(v)
                print len(v1)

                process_single_comp(k, v, k1, v1)


def start_threads(res):
    global fv
    threads = []

    resnum = len(res)
    
    r_range = resnum / 1

    tt = []
    ttt = []
    r_count = 0
    for k, v in sorted(res.iteritems()):
        print k
        r_count += 1
        if r_count == r_range:
	    ttt.append((k, v))
            tt.append(ttt)
            ttt = []
            r_count = 0

        else:
	    ttt.append((k, v))

    ll = len(tt)

    print ll
    try:
        for i in range(0, ll):
            t = lcs_engine(i, tt[i], res)
            t.start()

            threads.append(t)

        for t in threads:
            t.join()

    except:
        print "Error: unable to start thread"

    print "finish lcs computation"

    res = []
    for fv1 in fv:
	t = map(str, fv1)
        res.append(",".join(t) + "\n")

    with open("fv.txt", 'w') as f:
        f.writelines(res)
