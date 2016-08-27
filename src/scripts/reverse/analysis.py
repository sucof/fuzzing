import os

def process(regs_tainted, addr_tainted):
    for k, v in regs_tainted.items():
        print k, "--->", v

    for k, v in addr_tainted.items():
        print k, "--->", v



def function_par(regs_tainted):

    if "edi" in regs_tainted:
        os.system('echo rdi:' + str(regs_tainted["edi"]) + " > reverse.output")
    elif "esi" in regs_tainted:
        os.system('echo rsi:' + str(regs_tainted["esi"]) + " > reverse.output")
    elif "edx" in regs_tainted:
        os.system('echo rdx:' + str(regs_tainted["edx"]) + " > reverse.output")
    elif "ecx" in regs_tainted:
        os.system('echo rcx:' + str(regs_tainted["ecx"]) + " > reverse.output")
    elif "r8" in regs_tainted:
        os.system('echo r8:' + str(regs_tainted["r8"]) + " > reverse.output")
    elif "r9" in regs_tainted:
        os.system('echo r9:' + str(regs_tainted["r9"]) + " > reverse.output")

    elif "rax" in regs_tainted:
        os.system('echo rax:' + str(regs_tainted["rax"]) + " > reverse.output")

    else:
        if len(regs_tainted) == 0:
            return;
        else:
            raise Exception("undefined register in taint analysis")




def mem_analysis(addr_tainted):
    for k, v in addr_tainted.items():
        os.system('echo addr:' + v + ":mem:" + k + " > reverse.mem.output" )


def regs_outputs(regs):
    for l in regs:
        print str.strip(l)
