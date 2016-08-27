from z3 import *

import utility as U



def lea_process(o, dst, src):
    U.process(o, dst, src, "mov")
