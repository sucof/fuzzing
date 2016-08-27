import pypatt
from z3 import *

def check_reg_taint(r, sym):
    return r in sym.regs_tainted


def remove_mem_tainted(addr, sym):
    del sym.addr_tainted[addr]
    print (">>>>>>>", addr, " is now freed")


def add_mem_tainted(addr, sym):
    sym.addr_tainted[addr] = sym.get_cur_addr()
    print (">>>>>>>>", addr, " is now tainted")

def taint_reg(reg, sym):
    addr = sym.get_cur_addr()
    return taint_reg_true(reg, addr, sym)


@pypatt.transform
def taint_reg_true(reg, addr, sym):

    with match(reg):
        with "rax":
            sym.regs_tainted["rax"] = addr
            sym.regs_tainted["eax"] = addr
            sym.regs_tainted["ax"] = addr
            sym.regs_tainted["ah"] = addr
            sym.regs_tainted["al"] = addr
        with "eax":
            sym.regs_tainted["eax"] = addr
            sym.regs_tainted["ax"] = addr
            sym.regs_tainted["ah"] = addr
            sym.regs_tainted["al"] = addr
        with "ax":
            sym.regs_tainted["ax"] = addr
            sym.regs_tainted["ah"] = addr
            sym.regs_tainted["al"] = addr
        with "ah":
            sym.regs_tainted["ah"] = addr
        with "al":
            sym.regs_tainted["al"] = addr

        with "rbx":
            sym.regs_tainted["rbx"] = addr
            sym.regs_tainted["ebx"] = addr
            sym.regs_tainted["bx"] = addr
            sym.regs_tainted["bh"] = addr
            sym.regs_tainted["bl"] = addr
        with "ebx":
            sym.regs_tainted["ebx"] = addr
            sym.regs_tainted["bx"] = addr
            sym.regs_tainted["bh"] = addr
            sym.regs_tainted["bl"] = addr
        with "bx":
            sym.regs_tainted["bx"] = addr
            sym.regs_tainted["bh"] = addr
            sym.regs_tainted["bl"] = addr
        with "bh":
            sym.regs_tainted["bh"] = addr
        with "bl":
            sym.regs_tainted["bl"] = addr

        with "rcx":
            sym.regs_tainted["rcx"] = addr
            sym.regs_tainted["ecx"] = addr
            sym.regs_tainted["cx"] = addr
            sym.regs_tainted["ch"] = addr
            sym.regs_tainted["cl"] = addr
        with "ecx":
            sym.regs_tainted["ecx"] = addr
            sym.regs_tainted["cx"] = addr
            sym.regs_tainted["ch"] = addr
            sym.regs_tainted["cl"] = addr
        with "cx":
            sym.regs_tainted["cx"] = addr
            sym.regs_tainted["ch"] = addr
            sym.regs_tainted["cl"] = addr
        with "ch":
            sym.regs_tainted["ch"] = addr
        with "cl":
            sym.regs_tainted["cl"] = addr

        with "rdx":
            sym.regs_tainted["rdx"] = addr
            sym.regs_tainted["edx"] = addr
            sym.regs_tainted["dx"] = addr
            sym.regs_tainted["dh"] = addr
            sym.regs_tainted["dl"] = addr
        with "edx":
            sym.regs_tainted["edx"] = addr
            sym.regs_tainted["dx"] = addr
            sym.regs_tainted["dh"] = addr
            sym.regs_tainted["dl"] = addr
        with "dx":
            sym.regs_tainted["dx"] = addr
            sym.regs_tainted["dh"] = addr
            sym.regs_tainted["dl"] = addr
        with "dh":
            sym.regs_tainted["dh"] = addr
        with "dl":
            sym.regs_tainted["dl"] = addr

        with "r8":
            sym.regs_tainted["r8"] = addr
            sym.regs_tainted["r8d"] = addr
            sym.regs_tainted["r8w"] = addr
            sym.regs_tainted["r8b"] = addr
        with "r8d":
            sym.regs_tainted["r8d"] = addr
            sym.regs_tainted["r8w"] = addr
            sym.regs_tainted["r8b"] = addr
        with "r8w":
            sym.regs_tainted["r8w"] = addr
            sym.regs_tainted["r8b"] = addr
        with "r8b":
            sym.regs_tainted["r8b"] = addr

        with "r9":
            sym.regs_tainted["r9"] = addr
            sym.regs_tainted["r9d"] = addr
            sym.regs_tainted["r9w"] = addr
            sym.regs_tainted["r9b"] = addr
        with "r9d":
            sym.regs_tainted["r9d"] = addr
            sym.regs_tainted["r9w"] = addr
            sym.regs_tainted["r9b"] = addr
        with "r9w":
            sym.regs_tainted["r9w"] = addr
            sym.regs_tainted["r9b"] = addr
        with "r9b":
            sym.regs_tainted["r9b"] = addr

        with "r10":
            sym.regs_tainted["r10"] = addr
            sym.regs_tainted["r10d"] = addr
            sym.regs_tainted["r10w"] = addr
            sym.regs_tainted["r10b"] = addr
        with "r10d":
            sym.regs_tainted["r10d"] = addr
            sym.regs_tainted["r10w"] = addr
            sym.regs_tainted["r10b"] = addr
        with "r10w":
            sym.regs_tainted["r10w"] = addr
            sym.regs_tainted["r10b"] = addr
        with "r10b":
            sym.regs_tainted["r10b"] = addr

        with "r11":
            sym.regs_tainted["r11"] = addr
            sym.regs_tainted["r11d"] = addr
            sym.regs_tainted["r11w"] = addr
            sym.regs_tainted["r11b"] = addr
        with "r11d":
            sym.regs_tainted["r11d"] = addr
            sym.regs_tainted["r11w"] = addr
            sym.regs_tainted["r11b"] = addr
        with "r11w":
            sym.regs_tainted["r11w"] = addr
            sym.regs_tainted["r11b"] = addr
        with "r11b":
            sym.regs_tainted["r11b"] = addr

        with "r12":
            sym.regs_tainted["r12"] = addr
            sym.regs_tainted["r12d"] = addr
            sym.regs_tainted["r12w"] = addr
            sym.regs_tainted["r12b"] = addr
        with "r12d":
            sym.regs_tainted["r12d"] = addr
            sym.regs_tainted["r12w"] = addr
            sym.regs_tainted["r12b"] = addr
        with "r12w":
            sym.regs_tainted["r12w"] = addr
            sym.regs_tainted["r12b"] = addr
        with "r12b":
            sym.regs_tainted["r12b"] = addr

        with "r13":
            sym.regs_tainted["r13"] = addr
            sym.regs_tainted["r13d"] = addr
            sym.regs_tainted["r13w"] = addr
            sym.regs_tainted["r13b"] = addr
        with "r13d":
            sym.regs_tainted["r13d"] = addr
            sym.regs_tainted["r13w"] = addr
            sym.regs_tainted["r13b"] = addr
        with "r13w":
            sym.regs_tainted["r13w"] = addr
            sym.regs_tainted["r13b"] = addr
        with "r13b":
            sym.regs_tainted["r13b"] = addr

        with "r14":
            sym.regs_tainted["r14"] = addr
            sym.regs_tainted["r14d"] = addr
            sym.regs_tainted["r14w"] = addr
            sym.regs_tainted["r14b"] = addr
        with "r14d":
            sym.regs_tainted["r14d"] = addr
            sym.regs_tainted["r14w"] = addr
            sym.regs_tainted["r14b"] = addr
        with "r14w":
            sym.regs_tainted["r14w"] = addr
            sym.regs_tainted["r14b"] = addr
        with "r14b":
            sym.regs_tainted["r14b"] = addr

        with "r15":
            sym.regs_tainted["r15"] = addr
            sym.regs_tainted["r15d"] = addr
            sym.regs_tainted["r15w"] = addr
            sym.regs_tainted["r15b"] = addr
        with "r15d":
            sym.regs_tainted["r15d"] = addr
            sym.regs_tainted["r15w"] = addr
            sym.regs_tainted["r15b"] = addr
        with "r15w":
            sym.regs_tainted["r15w"] = addr
            sym.regs_tainted["r15b"] = addr
        with "r15b":
            sym.regs_tainted["r15b"] = addr

        with "rdi":
            sym.regs_tainted["rdi"] = addr
            sym.regs_tainted["edi"] = addr
            sym.regs_tainted["di"] = addr
            sym.regs_tainted["dil"] = addr
        with "edi":
            sym.regs_tainted["edi"] = addr
            sym.regs_tainted["di"] = addr
            sym.regs_tainted["dil"] = addr
        with "di":
            sym.regs_tainted["di"] = addr
            sym.regs_tainted["dil"] = addr
        with "dil":
            sym.regs_tainted["dil"] = addr

        with "rsi":
            sym.regs_tainted["rsi"] = addr
            sym.regs_tainted["esi"] = addr
            sym.regs_tainted["si"] = addr
            sym.regs_tainted["sil"] = addr
        with "esi":
            sym.regs_tainted["esi"] = addr
            sym.regs_tainted["si"] = addr
            sym.regs_tainted["sil"] = addr
        with "si":
            sym.regs_tainted["si"] = addr
            sym.regs_tainted["sil"] = addr
        with "sil":
            sym.regs_tainted["sil"] = addr

        with "t0":
            sym.regs_tainted["t0"] = addr
        with "t1":
            sym.regs_tainted["t1"] = addr

        with "rbp":
            sym.regs_tainted["rbp"] = addr
            sym.regs_tainted["ebp"] = addr
        with "ebp":
            sym.regs_tainted["ebp"] = addr

        with _:
            print (">>>>>>", reg, " can't be tainted")
            return False

    print ">>>>>> " + reg + " is tainted now"
    return True


def read_mem(r, mem_addr, sym):
    ins_addr = sym.get_cur_addr()

    if mem_addr in sym.addr_tainted:
        print ("[READ in ", mem_addr, "]\t", ins_addr)

        taint_reg(r, sym)
        remove_mem_tainted(mem_addr, sym)
        return

    if check_reg_taint(r, sym):
        print ("[READ in ", mem_addr, "]\t", ins_addr)

        remove_taint_reg(r, sym)



def write_mem(r, mem_addr, sym):
    ins_addr = sym.get_cur_addr()

    if mem_addr in sym.addr_tainted:
        print ("[WRITE in ", mem_addr, "]\t", ins_addr)

        if check_reg_taint(r, sym):
            remove_mem_tainted(mem_addr, sym)

    if check_reg_taint(r, sym):
        print ("[WRITE in ", mem_addr, "]\t", ins_addr)

        add_mem_tainted(mem_addr, sym)

        remove_taint_reg(r, sym)


def spread_reg_taint(reg_r, reg_w, sym):
    ins_addr = sym.get_cur_addr()

    if check_reg_taint(reg_w, sym) and not (check_reg_taint(reg_r, sym)):
        print ("[SPREAD]", ins_addr)
        print (">>>>>>>> output: ", reg_w, " | input : ", reg_r)

        taint_reg(reg_w, sym)


    elif (not check_reg_taint(reg_w, sym)) and check_reg_taint(reg_r, sym):
        print ("[SPREAD]", ins_addr)
        print (">>>>>>>> output: ", reg_w, " | input : ", reg_r)

        taint_reg(reg_w, sym)
        remove_taint_reg(reg_r, sym)


@pypatt.transform
def remove_taint_reg(reg, sym):
    if not (check_reg_taint(reg, sym)):
        print (reg, " is not tainted")
        return False

    with match(reg):
        with "rax":
            del sym.regs_tainted["rax"]
            del sym.regs_tainted["eax"]
            del sym.regs_tainted["ax"]
            del sym.regs_tainted["ah"]
            del sym.regs_tainted["al"]
        with "eax":
            del sym.regs_tainted["eax"]
            del sym.regs_tainted["ax"]
            del sym.regs_tainted["ah"]
            del sym.regs_tainted["al"]
        with "ax":
            del sym.regs_tainted["ax"]
            del sym.regs_tainted["ah"]
            del sym.regs_tainted["al"]
        with "ah":
            del sym.regs_tainted["ah"]
        with "al":
            del sym.regs_tainted["al"]

        with "rbx":
            del sym.regs_tainted["rbx"]
            del sym.regs_tainted["ebx"]
            del sym.regs_tainted["bx"]
            del sym.regs_tainted["bh"]
            del sym.regs_tainted["bl"]
        with "ebx":
            del sym.regs_tainted["ebx"]
            del sym.regs_tainted["bx"]
            del sym.regs_tainted["bh"]
            del sym.regs_tainted["bl"]
        with "bx":
            del sym.regs_tainted["bx"]
            del sym.regs_tainted["bh"]
            del sym.regs_tainted["bl"]
        with "bh":
            del sym.regs_tainted["bh"]
        with "bl":
            del sym.regs_tainted["bl"]

        with "rcx":
            del sym.regs_tainted["rcx"]
            del sym.regs_tainted["ecx"]
            del sym.regs_tainted["cx"]
            del sym.regs_tainted["ch"]
            del sym.regs_tainted["cl"]
        with "ecx":
            del sym.regs_tainted["ecx"]
            del sym.regs_tainted["cx"]
            del sym.regs_tainted["ch"]
            del sym.regs_tainted["cl"]
        with "cx":
            del sym.regs_tainted["cx"]
            del sym.regs_tainted["ch"]
            del sym.regs_tainted["cl"]
        with "ch":
            del sym.regs_tainted["ch"]
        with "cl":
            del sym.regs_tainted["cl"]

        with "rdx":
            del sym.regs_tainted["rdx"]
            del sym.regs_tainted["edx"]
            del sym.regs_tainted["dx"]
            del sym.regs_tainted["dh"]
            del sym.regs_tainted["dl"]
        with "edx":
            del sym.regs_tainted["edx"]
            del sym.regs_tainted["dx"]
            del sym.regs_tainted["dh"]
            del sym.regs_tainted["dl"]
        with "dx":
            del sym.regs_tainted["dx"]
            del sym.regs_tainted["dh"]
            del sym.regs_tainted["dl"]
        with "dh":
            del sym.regs_tainted["dh"]
        with "dl":
            del sym.regs_tainted["dl"]

        with "rdi":
            del sym.regs_tainted["rdi"]
            del sym.regs_tainted["edi"]
            del sym.regs_tainted["di"]
            del sym.regs_tainted["dil"]
        with "edi":
            del sym.regs_tainted["edi"]
            del sym.regs_tainted["di"]
            del sym.regs_tainted["dil"]
        with "di":
            del sym.regs_tainted["di"]
            del sym.regs_tainted["dil"]
        with "dil":
            del sym.regs_tainted["dil"]

        with "rsi":
            del sym.regs_tainted["rsi"]
            del sym.regs_tainted["esi"]
            del sym.regs_tainted["si"]
            del sym.regs_tainted["sil"]
        with "esi":
            del sym.regs_tainted["esi"]
            del sym.regs_tainted["si"]
            del sym.regs_tainted["sil"]
        with "si":
            del sym.regs_tainted["si"]
            del sym.regs_tainted["sil"]
        with "sil":
            del sym.regs_tainted["sil"]

        with "t0":
            del sym.regs_tainted["t0"]
        with "t1":
            del sym.regs_tainted["t1"]

        with "rbp":
            del sym.regs_tainted["rbp"]
            del sym.regs_tainted["ebp"]
        with "ebp":
            del sym.regs_tainted["ebp"]

        with "r8":
            del sym.regs_tainted["r8"]
            del sym.regs_tainted["r8d"]
            del sym.regs_tainted["r8w"]
            del sym.regs_tainted["r8b"]
        with "r8d":
            del sym.regs_tainted["r8d"]
            del sym.regs_tainted["r8w"]
            del sym.regs_tainted["r8b"]
        with "r8w":
            del sym.regs_tainted["r8w"]
            del sym.regs_tainted["r8b"]
        with "r8b":
            del sym.regs_tainted["r8b"]

        with "r9":
            del sym.regs_tainted["r9"]
            del sym.regs_tainted["r9d"]
            del sym.regs_tainted["r9w"]
            del sym.regs_tainted["r9b"]
        with "r9d":
            del sym.regs_tainted["r9d"]
            del sym.regs_tainted["r9w"]
            del sym.regs_tainted["r9b"]
        with "r9w":
            del sym.regs_tainted["r9w"]
            del sym.regs_tainted["r9b"]
        with "r9b":
            del sym.regs_tainted["r9b"]

        with "r10":
            del sym.regs_tainted["r10"]
            del sym.regs_tainted["r10d"]
            del sym.regs_tainted["r10w"]
            del sym.regs_tainted["r10b"]
        with "r10d":
            del sym.regs_tainted["r10d"]
            del sym.regs_tainted["r10w"]
            del sym.regs_tainted["r10b"]
        with "r10w":
            del sym.regs_tainted["r10w"]
            del sym.regs_tainted["r10b"]
        with "r10b":
            del sym.regs_tainted["r10b"]

        with "r11":
            del sym.regs_tainted["r11"]
            del sym.regs_tainted["r11d"]
            del sym.regs_tainted["r11w"]
            del sym.regs_tainted["r11b"]
        with "r11d":
            del sym.regs_tainted["r11d"]
            del sym.regs_tainted["r11w"]
            del sym.regs_tainted["r11b"]
        with "r11w":
            del sym.regs_tainted["r11w"]
            del sym.regs_tainted["r11b"]
        with "r11b":
            del sym.regs_tainted["r11b"]

        with "r12":
            del sym.regs_tainted["r12"]
            del sym.regs_tainted["r12d"]
            del sym.regs_tainted["r12w"]
            del sym.regs_tainted["r12b"]
        with "r12d":
            del sym.regs_tainted["r12d"]
            del sym.regs_tainted["r12w"]
            del sym.regs_tainted["r12b"]
        with "r12w":
            del sym.regs_tainted["r12w"]
            del sym.regs_tainted["r12b"]
        with "r12b":
            del sym.regs_tainted["r12b"]

        with "r13":
            del sym.regs_tainted["r13"]
            del sym.regs_tainted["r13d"]
            del sym.regs_tainted["r13w"]
            del sym.regs_tainted["r13b"]
        with "r13d":
            del sym.regs_tainted["r13d"]
            del sym.regs_tainted["r13w"]
            del sym.regs_tainted["r13b"]
        with "r13w":
            del sym.regs_tainted["r13w"]
            del sym.regs_tainted["r13b"]
        with "r13b":
            del sym.regs_tainted["r13b"]

        with "r14":
            del sym.regs_tainted["r14"]
            del sym.regs_tainted["r14d"]
            del sym.regs_tainted["r14w"]
            del sym.regs_tainted["r14b"]
        with "r14d":
            del sym.regs_tainted["r14d"]
            del sym.regs_tainted["r14w"]
            del sym.regs_tainted["r14b"]
        with "r14w":
            del sym.regs_tainted["r14w"]
            del sym.regs_tainted["r14b"]
        with "r14b":
            del sym.regs_tainted["r14b"]

        with "r15":
            del sym.regs_tainted["r15"]
            del sym.regs_tainted["r15d"]
            del sym.regs_tainted["r15w"]
            del sym.regs_tainted["r15b"]
        with "r15d":
            del sym.regs_tainted["r15d"]
            del sym.regs_tainted["r15w"]
            del sym.regs_tainted["r15b"]
        with "r15w":
            del sym.regs_tainted["r15w"]
            del sym.regs_tainted["r15b"]
        with "r15b":
            del sym.regs_tainted["r15b"]

        with _:
            print (reg, " can't remove taint")
            return False

    print ">>>>>> " + reg + " is free now"
    return True
