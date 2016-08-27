
import os

blacklist = ['__libc_csu_init', '__libc_csu_fini', '__i686.get_pc_thunk.bx', '__do_global_ctors_aux', '_start', '__do_global_dtors_aux', 'frame_dummy']

def process(fn):
    ce, cr = code_range_info(fn)
    fn = os.path.basename(fn)

    with open(fn + "_info.txt") as f:
        lines = f.readlines()

    funcmap = {}
    for l in lines:
        (funcname, ba, ea) = l.split(":")
        ba = str.strip(ba)
        ea = str.strip(ea)

        funcmap[funcname] = (ba, ea)

    
    return (funcmap, ce, cr)


def select_topn(fmap1, fmap2):
    count = 1

    res = []
    for k, v in fmap1.items():

        if count == 100000:
            break
        else:
            if k in fmap2:
                count += 1
                res.append((k, fmap1[k], fmap2[k]))

    return res


def code_range_info(fn):
    os.system("readelf -SW " + fn + " > section.info")

    lines = []
    with open("section.info") as f:
        lines = f.readlines()

    ce = 0
    cr = 0
    for l in lines:
        items = l.split()
        if len(items) > 10:
            if ".text" == items[1] or ".text" == items[2]:
                ce = int(items[3], 16)
                cr = int(items[4], 16)
                break

    return (ce, cr)



def data_range_info(fn):
    lines = []
    with open("section.info") as f:
        lines = f.readlines()

    db = 0
    de = 0
    for l in lines:
        items = l.split()
        if len(items) > 10:
            if ".rodata" == items[1]:
                db = int(items[3], 16)
            elif ".bss" == items[1]:
                t1 = int(items[3], 16)
                t2 = int(items[4], 16)
                de = t1 + t2
                break

    return (db, de)


def data_range_info_new(fn, tag):
    os.system("readelf -SW " + fn + " > section.info")
    with open("section.info") as f:
        lines = f.readlines()

    t = []
    for l in lines:
        items = l.split()
        if len(items) > 10:
            if ".rodata" == items[1]:
                db = int(items[3], 16)
                dr = int(items[5], 16)
                de = db + dr
                t = str(db) + "," + str(de) + ","
            elif ".data" == items[1]:
                db = int(items[3], 16)
                dr = int(items[5], 16)
                de = db + dr
                t = t + str(db) + "," + str(de) + ","
            elif ".got.plt" == items[1]:
                db = int(items[3], 16)
                dr = int(items[5], 16)
                de = db + dr
                t = t + str(db) + "," + str(de) + ","
            elif ".bss" == items[1]:
                db = int(items[3], 16)
                dr = int(items[5], 16)
                de = db + dr
                t = t + str(db) + "," + str(de) + "\n"
                break

    with open("data_section" + tag + ".info", 'w') as f:
        f.writelines(t)


def select(fmap1, fmap2):
    if len(fmap1) >= len(fmap2):
        return select_topn(fmap2, fmap1)
    else:
        return select_topn(fmap1, fmap2)
