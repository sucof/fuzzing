
import sys, os
import lib as LIB

res = []


def check_mem(mem):
    mems = set(mem)
    r = {}


    print r




def appendix():
    
    lines = []

    with open("pinatrace.out") as f:
        lines = f.readlines()

    if len(lines) < 14 or not ("END" in lines[-14]):
        
        os.system("python analysis/compl.py")



memt = []

def collect():
    find_start = False
    find_end = False

    lines = []

    with open("pinatrace.out") as f:
        lines = f.readlines()


    t = []
    hr = []
    hw = []

    rhr = []
    rhw = []

    gr = []
    gw = []

    gotpltr = []
    gotpltw = []
    rodatar = []
    rodataw = []
    datar = []
    dataw = []
    bssr = []
    bssw = []

    mem = []
    scl = []

    for i in range(len(lines)):
        l = lines[i]

        if 'START' in l:
            
            find_start = True
            find_end = False

        if find_start == True:
            if "RDI" in l or "RSI" in l or "RDX" in l or "RCX" in l or "R8" in l or "R9" in l:
                v = int(l.split("=")[1])

            if ": W" in l or ": R" in l:
                addr = l.split()[-1]
                addr = int(addr, 16)
                if addr >= 0x700000000000 and addr < 0x7ffffff00000:
                    mem.append(addr)

        if "real" in l:
            items = l.split()
            if items[2] == "w:":
                # memory write
                value = items[3]
                rhw.append(int(value))
            if items[2] == "r:":
                # memory read
                value = items[3]
                rhr.append(int(value))

        if "heap" in l and not ("real" in l):
            items = l.split()
            if items[1] == "w:":
                # memory write
                offset = items[2]
                hw.append(int(offset))
            if items[1] == "r:":
                # memory read
                offset = items[2]
                hr.append(int(offset))

        if "gotplt" in l:
            items = l.split()
            if items[1] == "w:":
                
                offset = items[2]
                gotpltw.append(int(offset))
            if items[1] == "r:":
               
                offset = items[2]
                gotpltr.append(int(offset))

        if "rodata" in l:
            items = l.split()
            if items[1] == "w:":
                # memory write
                offset = items[2]
                rodataw.append(int(offset))
            if items[1] == "r:":
                # memory read
                offset = items[2]
                rodatar.append(int(offset))

        if "data" in l and not ("ro" in l):
            items = l.split()
            if items[1] == "w:":
                # memory write
                offset = items[2]
                dataw.append(int(offset))
            if items[1] == "r:":
                # memory read
                offset = items[2]
                datar.append(int(offset))

        if "bss" in l:
            items = l.split()
            if items[1] == "w:":
                # memory write
                offset = items[2]
                bssw.append(int(offset))
            if items[1] == "r:":
                # memory read
                offset = items[2]
                bssr.append(int(offset))

        if "END" in l:
            find_start = False
            find_end = True

        if "call" in l:
            d = l.split(":")[1]
            fn = LIB.trans(int(d, 16))
            scl.append(fn)

        if find_end == True:
            if "RAX" in l:
                
                v = int(l.split("=")[1])
                t.append(v)

                t.append(hr)
                t.append(hw)
                t.append(gotpltr)
                t.append(gotpltw)
                t.append(rodatar)
                t.append(rodataw)
                t.append(datar)
                t.append(dataw)
                t.append(bssr)
                t.append(bssw)
                t.append(rhr)
                t.append(rhw)
                if len(scl) == 0:
                    scl = []
                    t.append(scl)
                else:
                    t.append(sorted(set(scl)))

                res.append(t)
                #check_mem(mem)
                mem = []
                t = []


appendix()

fp = sys.argv[1]
fn = os.path.basename(fp)
bp = os.path.dirname(fp)

LIB.preprocess(fn, bp)

collect()

for r in res:
    print r[0], ";", r[1], ";", r[2], ";", r[3], ";", r[4], ";", r[5], ";", r[6], ";", r[7], ";", r[8], ";", r[9], ';', r[10], ';', r[11], ';', r[12], ';', r[13]
