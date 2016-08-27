from z3 import *
import pypatt
import tainter as T

@pypatt.transform
def translate_op(x, y, ops):
    with match(ops):
        with "&":
            return x & y
        with "^":
            return x ^ y
        with "|":
            return x | y
        with "~":
            return ~y
        with "<<":
            return y << x
        with ">>":
            return y >> x
        with "shr":
            return LShR(y, x)
        with "*":
            return x * y
        with "div":
            return y / x
        with "+":
            return x + y
        with "-":
            return y - x
        with "mov":
            return x
        with "movsbl":
            if x.size() == 8:
                return Concat(BitVecVal(0xffffff, 24), x)
            else:
                return x
        with "movzbl":
            if x.size() == 8:
                return Concat(BitVecVal(0, 24), x)
            else:
                return x


def op_isassign(ops):
    return ops.startswith("mov")


def op_isarith(ops):
    return ops in ['+', '-', 'div', '*', 'shr', 'shl', '<<', ">>", '~', "|", "^", "&"]


def process_long(o, dst, src, ops):
    if dst in o.reg_32_map and dst not in ['t1', 't0']:
        process(o, dst, src, ops)

    elif dst[0] == '-' and dst[1:].isdigit() and isinstance(int(dst), (int, long)) and src in o.ctx:
        if op_isassign(ops):
            T.remove_taint_reg(dst, o)
        else:
            return

    elif dst.isdigit() and isinstance(int(dst), (int, long)) and src in o.ctx:
        if op_isassign(ops):
            T.remove_taint_reg(dst, o)
        else:
            return

    elif dst in o.ctx and (src in o.ctx or src in o.reg_32_map or src in o.reg_small_map):
        if op_isarith(ops):
            if T.check_reg_taint(src, o):
                return
            else:
                T.spread_reg_taint(dst, src, o)
        else:
            T.spread_reg_taint(src, dst, o)
    else:
        print o, src, dst
        raise Exception('This instruction of is not handled.')


def process(o, dst, src, ops):
    print "----------------"
    print dst, src, ops
    print "----------------"

    if (dst in ['t0', 't1'] and src in o.ctx) or (dst in o.ctx and dst not in ['t0', 't1']):
        process_long(o, dst, src, ops)

    elif dst.isdigit() and src in o.ctx:
        process_long(o, dst, src, ops)

    elif dst in o.reg_32_map and (src in o.ctx or src in o.reg_32_map):
        if op_isarith(ops):
            if T.check_reg_taint(src, o):
                return
            else:
                T.spread_reg_taint(dst, src, o)
        else:
            T.spread_reg_taint(src, dst, o)

    elif dst in o.reg_32_map and src in o.reg_small_map:
        if op_isarith(ops):
            if T.check_reg_taint(src, o):
                return
            else:
                T.spread_reg_taint(dst, src, o)
        else:
            T.spread_reg_taint(src, dst, o)


    elif src in o.reg_32_map and dst in o.reg_small_map:
        if op_isarith(ops):
            if T.check_reg_taint(src, o):
                return
            else:
                T.spread_reg_taint(dst, src, o)
        else:
            T.spread_reg_taint(src, dst, o)


    elif dst.isdigit() and isinstance(int(dst), (int, long)) and src in o.reg_32_map:
        if op_isassign(ops):
            T.remove_taint_reg(dst, o)
        else:
            return

    elif dst.isdigit() and isinstance(int(dst), (int, long)) and src in o.reg_small_map:
        if op_isassign(ops):
            T.remove_taint_reg(dst, o)
        else:
            return

    elif src in o.reg_small_map and dst in o.reg_small_map:
        if op_isarith(ops):
            if T.check_reg_taint(src, o):
                return
            else:
                T.spread_reg_taint(dst, src, o)
        else:
            T.spread_reg_taint(src, dst, o)
    else:
        print o, src, dst
        raise Exception('This instruction is not handled.')


def process_4_process(o, dst, src, src_2, ops):
    raise Exception("undefined process 4")
    if dst in o.ctx and src in o.ctx and src_2.isdigit():
        o.set_reg_with_equation(dst, translate_op(int(src_2), o.get_reg_equation(src), ops))
    elif dst in o.ctx and src in o.ctx and src_2 in o.ctx:
        o.set_reg_with_equation(dst, translate_op(o.get_reg_equation(src_2), o.get_reg_equation(src), ops))
    elif dst in o.ctx and src in o.reg_32_map and src_2.isdigit():
        ((s1,e1), r1) = o.reg_32_map[src]
        src_s = Extract(s1, e1, o.get_reg_equation(r1))

        o.set_reg_with_equation(dst, Concat(BitVec(0,32),translate_op(int(src_2), src_s, ops)))
    elif dst in o.ctx and src in o.ctx and src_2 in o.reg_32_map:
        ((s1,e1), r1) = o.reg_32_map[src_2]
        src_s = Concat(BitVec(0,32), Extract(s1, e1, o.get_reg_equation(r1)))

        o.set_reg_with_equation(dst, translate_op(src_s, o.get_reg_equation(src), ops))
    else:
        raise Exception('This instruction is not handled.')


def process_3_process(o, dst, src, ops):
    raise Exception("undefined process 3")
    if dst in o.ctx and src in o.ctx:
        de = o.get_reg_equation(dst)
        re = o.get_reg_equation(src)

        o.set_reg_with_equation(dst, translate_op(re, de, ops))
    elif dst in o.ctx and src.isdigit() and isinstance(int(src), (int, long)):
        de = o.get_reg_equation(dst)

        o.set_reg_with_equation(dst, translate_op(int(src), de, ops))
    else:
        raise Exception('This instruction is not handled.')


def process_8(o, dst, src, ops):
    raise Exception("undefined process 8")
    if src.isdigit() and src in ["t0", 't1']:
        dst = o.get_reg_equation(src)
        dst_s = Extract(7, 0, dst)

        src_s = BitVec(int(src), 8)
        dst_s = translate_op(src_s, dst_s, ops)
        dst_s = Extract(7, 0, dst)

        o.set_reg_with_equation(dst, dst_s)
    else:
        process(o, dst, src, ops)


@pypatt.transform
def calculate_by_op(o, op, a, b):
    with match(op):
        with "+":
            return a + b
        with "-":
            return a - b
        with "*":
            return a * b
        with _:
            raise Exception("undefined behavior")
