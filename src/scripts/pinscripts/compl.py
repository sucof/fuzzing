import os

lines = []
with open("pinatrace.out") as f:
    lines = f.readlines()

if len(lines) == 0:
    lines.append('''
    /n========================START=====================
    RAX = 666
    RBX = 0
    RDI = 0
    RSI = 0
    RDX = 0
    RCX = 0
    RBP = 0
    RSP = 0
    R8 = 0
    R9 = 0
    ======================================================
    /n========================END=====================
    RAX = 666
    RBX = 0
    RDI = 0
    RSI = 0
    RDX = 0
    RCX = 0
    RBP = 0
    RSP = 0
    R8 = 0
    R9 = 0
    ======================================================
    ''')
else:
    lines[-1] = ""
    
    lines.append('''
    /n========================END=====================
    RAX = 666
    RBX = 0
    RDI = 0
    RSI = 0
    RDX = 0
    RCX = 0
    RBP = 0
    RSP = 0
    R8 = 0
    R9 = 0
    ======================================================
    ''')
    

os.system("rm pinatrace.out")
with open("pinatrace.out", 'w') as f:
    f.writelines(lines)

