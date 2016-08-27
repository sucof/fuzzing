import os, sys, re, os.path

fn = sys.argv[1]
bn = os.path.basename(fn)


blacklist = ['__libc_csu_init', '__libc_csu_fini', '__i686.get_pc_thunk.bx', '__do_global_ctors_aux', '_start', '__do_global_dtors_aux', 'frame_dummy']
addrs = []
addrs_2 = []
regex1 = re.compile(r'<(.*)>:',re.I)

os.system('objdump -Dr -j .text '+fn+" > dump.s")

lines = []
with open("dump.s") as f:
    lines = f.readlines()


fd = {}
fnl = ""


for i in range(len(lines)):
    l = lines[i]

    if ">:" in l:
        lp = lines[i-2]
        fn = regex1.search(l).groups()[0]
        fnsa = int("0x" + l.split()[0], 16)

        fd[fn] = (fnsa, 0)

        if ".text" in lp:
            # first function
            fnl = fn
        else:
            fnea = int("0x" + lp.split()[0][:-1], 16)
            t = fd[fnl]
            fd[fnl] = (t[0], fnea)
            fnl = fn

fnea = int("0x" + lines[-1].split()[0][:-1], 16)
t = fd[fnl]
fd[fnl] = (t[0], fnea)

lines1 = []

for k, v in fd.items():
    lines1.append(k + " : " + hex(v[0]) + " : " + hex(v[1]) + "\n")


with open(bn + "_info.txt", 'w') as f:
    f.writelines(lines1)

