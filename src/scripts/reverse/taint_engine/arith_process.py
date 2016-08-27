from z3 import *

import utility as U

def shll_process(o, dst, src):
    U.process_long(o, dst, src, "<<")

def shl_process(o, dst, src):
    U.process(o, dst, src, "<<")

def shrl_process(o, dst, src):
    U.process_long(o, dst, src, "shr")

def shr_process(o, dst, src):
    U.process(o, dst, src, "shr")

def sarl_process(o, dst, src):
    U.process_long(o, dst, src, ">>")

def sar_process(o, dst, src):
    U.process(o, dst, src, ">>")


def mul_4_process(o, dst, src, src_2):
    U.process_4_process(o, dst, src, src_2, "*")

def mul_3_process(o, dst, src):
    U.process(o, dst, src, "*")


def mul_2_process(o, dst):

    if dst in o.ctx:
        return
    if dst in o.reg_32_map:
        ((s1,e1), r1) = o.reg_32_map[dst]
        ((s2,e2), r2) = o.reg_32_map['%eax']
        ((s3,e3), r3) = o.reg_32_map['%edx']

        e_eax = Extract(s2, e2, o.get_reg_equation(r2))
        e_r = Extract(s1, e1, o.get_reg_equation(r1))

        v = e_eax * e_r

        v = simplify(v)

        o.set_reg_with_equation('%rdx', BitVec(0, 64))
        o.set_reg_with_equation('%rax', Concat(BitVec(0, 32), Extract(31,0,v)))

    else:
        raise Exception('This encoding of "mul" is not handled.')

def div_2_process(o, dst):
    return

def div_3_process(o, dst, src):
    return

def add_4_process(o, dst, src, src_2):
    U.process_4_process(o, dst, src, src_2, "+")

def addl_process(o, dst, src):
    U.process_long(o, dst, src, "+")

def add_process(o, dst, src):
    U.process(o, dst, src, "+")

def subl_process(o, dst, src):
    U.process_long(o, dst, src, "-")

def sub_4_process(o, dst, src, src_2):
    U.process_4_process(o, dst, src, src_2, "-")

def sub_process(o, dst, src):
    U.process(o, dst, src, "-")
