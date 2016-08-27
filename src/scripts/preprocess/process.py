from __future__ import print_function

import os, sys, re, os.path
import dis as D
import lcs as LCS
import fuzzing as F
import selectFunc as SF


class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def check_exe():
    lines = []
    with open("elf.info") as f:
        lines = f.readlines()
    if "LSB shared object" in lines[0]:
        return False
    else:
        return True


def check_64():
    lines = []
    with open("elf.info") as f:
        lines = f.readlines()
    if "64-bit" in lines[0]:
        return True
    else:
        return False


def check_unstrip():
    lines = []
    with open("elf.info") as f:
        lines = f.readlines()
    if "not stripped" in lines[0]:
        return True
    else:
        return False


def dump(fn):
    os.system('file ' + fn + ' > elf.info')

    if check_exe() and check_unstrip() and check_64():
        os.system("python func_info.py " + fn)


def warning(*objs):
    print(*objs, file=sys.stderr)


def process(fn1, fn2, targetf):
    dump(fn1)
    dump(fn2)

    fmap1, cb1, cr1 = SF.process(fn1)
    fmap2, cb2, cr2 = SF.process(fn2)


    res = SF.select(fmap1, fmap2)

    binname1 = ""
    binname2 = ""
    if len(fmap1) >= len(fmap2):
        binname1 = fn2
        binname2 = fn1
    else:
        binname1 = fn1
        binname2 = fn2

    SF.data_range_info_new(binname1, "1")
    SF.data_range_info_new(binname2, "2")

    for r in res:
        if target_func == "":
            warning("start fuzzing ", binname1, r[0])
            os.system("cp data_section1.info /data/pin_sets/temp1/pin-3.0-76991-gcc-linux/source/tools/inMemFuzzing/data_section.info")
            F.fuzzing_new(binname1, r[0], r[1][0], r[1][1], cb1, cr1)

            warning("start fuzzing ", binname2, r[0])
            os.system("cp data_section2.info /data/pin_sets/temp1/pin-3.0-76991-gcc-linux/source/tools/inMemFuzzing/data_section.info")
            F.fuzzing_new(binname2, r[0], r[2][0], r[2][1], cb2, cr2)
	elif r[0].strip() == target_func:
            warning("start fuzzing ", binname1, r[0])
            os.system("cp data_section1.info /data/pin_sets/temp1/pin-3.0-76991-gcc-linux/source/tools/inMemFuzzing/data_section.info")
            F.fuzzing_new(binname1, r[0], r[1][0], r[1][1], cb1, cr1)
	
            warning("start fuzzing ", binname2, r[0])
            os.system("cp data_section2.info /data/pin_sets/temp1/pin-3.0-76991-gcc-linux/source/tools/inMemFuzzing/data_section.info")
            F.fuzzing_new(binname2, r[0], r[2][0], r[2][1], cb2, cr2)


import pickle

def write_to_file(res, fn):
    output = open(fn, 'wb')

    pickle.dump(res, output)
    output.close()


def read_from_file(fn):
    pkl_file = open(fn, 'rb')

    res = pickle.load(pkl_file)
    pkl_file.close()

    return res


if __name__ == '__main__':
    fn1 = sys.argv[1]
    fn2 = sys.argv[2]
    target_func = sys.argv[3]


    failed_list = process(fn1, fn2, target_func)


    fn = 'similarity_dic.pkl'
    write_to_file(F.res, fn)
    write_to_file(failed_list, "fail_list.pkl")

    
    res = read_from_file('similarity_dic.pkl')
    print ("read res finished")
    failed_list = []
    LCS.process(fn1, fn2, res, failed_list)


if __name__ == '__main__1':
    fn1 = sys.argv[1]
    fn2 = sys.argv[2]

    res = read_from_file('similarity_dic.pkl')
    print ("read res finished")
    fail_list = []
    LCS.process(fn1, fn2, res, fail_list)
