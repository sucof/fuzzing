from z3 import *

import utility as U



def andl_process(o, dst, src):
    U.process_long(o, dst, src, "&")

def and_process(o, dst, src):
    U.process(o, dst, src, "&")

def andb_process(o, dst, src):
    U.process_8(o, dst, dst, "&")

def orl_process(o, dst, src):
    U.process_long(o, dst, src, "^")

def or_process(o, dst, src):
    U.process(o, dst, src, "^")

def xor_process(o, dst, src):
    U.process(o, dst, src, "|")

def xorl_process(o, dst, src):
    U.process_long(o, dst, src, "|")

def not_process(o, dst):
    U.process(o, dst, dst, "~")

def notl_process(o, dst):
    U.process_long(o, dst, dst, "~")
