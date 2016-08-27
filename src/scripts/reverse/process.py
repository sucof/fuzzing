import os
import lex as L
import parse as P
from taint_engine.engine import *
import analysis as A

reverse_op = {
    "add"  : "sub",
    "sub"  : "add",
    "mul"  : "div",
    "div"  : "mul",
    "pop"  : "push",
    "push" : "pop",
    "shl"  : "shr",
    "shr" : "shl",
    }

def aux(i):

    if i[2] == None:
        return i

    if len(i[2]) == 2:
        t = i[2][0]
        i[2][0] = i[2][1]
        i[2][1] = t
        return i
    else:
        return i


def get_ctx():
    lines = []
    with open("ctx.info") as f:
        lines = f.readlines()

    ctx = {}
    taint_r = ""
    find_start = False
    for i in range(len(lines)):
        l = str.strip(lines[i])

        if "END" in l:
            break

        if find_start == True:
            if "taint" in l:
                taint_r = l.split("=")[1]
            elif "=" in l:
                v = int(l.split("=")[1])
                k = l.split("=")[0]
                ctx[k] = v

        if 'START' in l:
            find_start = True


    with open("ctx.trace") as f:
        lines = f.readlines()

    ctxl = {}
    find_start = False
    cur_addr = 0
    cctx = {}
    for i in range(len(lines)):
        l = str.strip(lines[i])

        if "END" in l:
            find_start = False
            ctxl[cur_addr] = cctx
            cctx = {}

        if find_start == True:
            if "=" in l:
                
                v = int(l.split("=")[1])
                k = str.strip(l.split("=")[0])
                cctx[k] = v

        if 'START' in l:
            find_start = True
            cur_addr = int(l.split(":")[1])


    lines = []

    with open("pin.trace") as f:
        lines = f.readlines()

    ol = map(lambda x:int(x[0:7], 10), lines[:-1])

    mol = {}
    for i in range(len(ol)):
	if i < len(ol)-1:
	    p1 = ol[i]
	    p2 = ol[i+1]
	    mol[p2] = p1

    first_addr = ol[0]
    ctxln = {}
    for k, v in ctxl.items():

	if not(k == first_addr):
	    k1 = mol[k]
	    ctxln[k1] = v
	 
    return (ctx, taint_r, ctxln)


def preprocess():
    lines = []

    with open("pin.trace") as f:
        lines = f.readlines()

    last_addr = int(lines[-2].split(":")[0])
    lines[-2] = "#" + lines[-2]
    lines = filter(lambda l : "#" not in l, lines)
    lines = map(lambda l: str.strip(l), lines)

    fctx, taint_r, ctxlist = get_ctx()

    linesb = lines
    lines.reverse()

    rl1 = []
    for l in lines:
        
        l1 = L.lex(l)
        l1 = aux(l1)
        rl1.extend(P.parse(l1))

    print 'Launching the 64-bit engine for taint analysis ...'

    te = TaintEngine("test", fctx, taint_r, rl1, last_addr, ctxlist)

    te.run()

    print 'execution finished..'
    os.system("rm reverse.output")
    os.system("rm reverse.mem.output")
    (ro, mo) = te.execution_outputs()
    (rt, mt) = te.taint_reults()
    print '-------------------'
    print rt
    print '-------------------'
    A.function_par(rt)
    A.mem_analysis(mt)
    A.regs_outputs(ro)
    return 1


if __name__ == '__main__':
    preprocess()
