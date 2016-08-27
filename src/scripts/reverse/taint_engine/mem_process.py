from z3 import *
from utility import *
import tainter as T


def load_process(o, dst, src, op, src2):
    print dst, src, op, src2

    inext = o.get_next_instruction()
    if inext[0] == "lea":
        T.spread_reg_taint(src, dst, o)
    else:
        if dst in o.ctx and src in o.ctx and src2.isdigit() and op in o.opl:
            s = calculate_by_op(o, op, o.get_reg_equation(src), int(src2))
            ss = simplify(s)

            T.read_mem(dst, str(ss), o)

        elif src in o.reg_32_map and dst in o.ctx and src2.isdigit() and op in o.opl:
            ((s1,e1), r1) = o.reg_32_map[src]
            src_s = Extract(s1, e1, o.get_reg_equation(r1))
            s = calculate_by_op(o, op, o.get_reg_equation(src_s), int(src2))
            ss = simplify(s)

            T.read_mem(dst, str(ss), o)
        else:
            raise Exception('This encoding of "load" is not handled.')


def loadl_process(o, dst, src, src2):
    load_process(o, dst, src, src2)


def load_long_process(o, dst, src1, op1, src2, op2, src3, op3, src4):
    inext = o.get_next_instruction()
    if inext[0] == "lea":
        T.spread_reg_taint(src1, dst, o)
    else:
        if dst in o.ctx and src1 in o.ctx and src2 in o.ctx and src3.isdigit() and src4.isdigit():
            s2 = calculate_by_op(o, op2, o.get_reg_equation(src2), int(src3))
            s1 = calculate_by_op(o, op1, o.get_reg_equation(src1), s2)
            s3 = calculate_by_op(o, op3, s2, int(src4))
            ss = simplify(s3)

            T.read_mem(dst, str(ss), o)
        else:
            raise Exception('This encoding of "load long" is not handled.')


def store_long_process(o, dst1, op1, dst2, op2, dst3, op3, dst4, src):
    iprevious = o.get_previous_instruction()
    if iprevious[0] == "lea":
        T.spread_reg_taint(src, dst1, o)
    else:
        if src in o.ctx and dst1 in o.ctx and dst2 in o.ctx and dst3.isdigit() and dst4.isdigit():
            s2 = calculate_by_op(o, op2, o.get_reg_equation(dst2), int(dst3))
            s1 = calculate_by_op(o, op1, o.get_reg_equation(dst1), s2)
            s3 = calculate_by_op(o, op3, s2, int(dst4))
            ss = simplify(s3)

            T.write_mem(src, str(ss), o)
        else:
            raise Exception('This encoding of "store long" is not handled.')


def store_process(o, dst, op, dst2, src):
    iprevious = o.get_previous_instruction()
    if iprevious[0] == "lea":
        T.spread_reg_taint(src, dst, o)
    else:
        if dst in o.ctx and dst2.isdigit() and src in o.ctx and op in o.opl:
            s = calculate_by_op(o, op, o.get_reg_equation(dst), int(dst2))
            ss = simplify(s)

            T.write_mem(src, str(ss), o)
        elif src in o.ctx and dst in o.reg_32_map and dst2.isdigit():
            ((s1,e1), r1) = o.reg_32_map[dst]
            dst_s = Extract(s1, e1, o.get_reg_equation(r1))
            s = calculate_by_op(o, dst_s, op, int(dst2))
            ss = simplify(s)

            T.write_mem(src, str(ss), o)
        else:
            raise Exception('This encoding of "store" is not handled.')


def storel_process(o, dst, src, src2):
    store_process(o, dst, src, src2)
