from z3 import *

import utility as U


def movl_process(o, dst, src):
    U.process_long(o,dst, src, "mov")


def mov_process(o, dst, src):
    U.process(o, dst, src, "mov")


def movb_process(o, dst, src):
    U.process(o, dst, src, "mov")


def movsbl_process(o, dst, src):
    U.process(o, dst, src, "movsbl")


def movzbl_process(o, dst, src):
    
    U.process(o, dst, src, "movzbl")


def xchg_process(o, dst, src):
    if dst == src:
        return

    t = dst
    U.process(o, dst, src, "mov")
    U.process(o, src, t, "mov")
