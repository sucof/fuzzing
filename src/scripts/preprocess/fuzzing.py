from __future__ import print_function
import sys
import os
from functools import wraps
import errno
import signal


fuzzingcount = 10


class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def connect_list():
    lines = []
    with open("temp_func.info") as f:
        lines = f.readlines()

    if len(lines) < 1:
        return []


    res = []

    for l in lines:
        items = l.split(";")
        r = int(items[0])
        
        items1 = items[1][2:-2].split(',')
        if not (items1 == ['']):
            items1 = map(lambda x : int(long(x)), items1)
       
        items2 = items[2][2:-2].split(',')
        if not (items2 == ['']):
            items2 = map(lambda x : int(long(x)), items2)
      
        items3 = items[3][2:-2].split(',')
        if not (items3 == ['']):
            items3 = map(lambda x : int(long(x)), items3)
     
        items4 = items[4][2:-2].split(',')
        if not (items4 == ['']):
            items4 = map(lambda x : int(long(x)), items4)
    
        items5 = items[5][2:-2].split(',')
        if not (items5 == ['']):
            items5 = map(lambda x : int(long(x)), items5)
   
        items6 = items[6][2:-2].split(',')
        if not (items6 == ['']):
            items6 = map(lambda x : int(long(x)), items6)
  
        items7 = items[7][2:-2].split(',')
        if not (items7 == ['']):
            items7 = map(lambda x : int(long(x)), items7)
        
        items8 = items[8][2:-2].split(',')
        if not (items8 == ['']):
            items8 = map(lambda x : int(long(x)), items8)
       
        items9 = items[9][2:-2].split(',')
        if not (items9 == ['']):
            items9 = map(lambda x : int(long(x)), items9)
      
        items10 = items[10][2:-2].split(',')
        if not (items10 == ['']):
            items10 = map(lambda x : int(long(x)), items10)

     
        items11 = items[11][2:-2].split(',')
        if not (items11 == ['']):
            items11 = map(lambda x : int(long(x)), items11)
    
        items12 = items[12][2:-2].split(',')
        if not (items12 == ['']):
            items12 = map(lambda x : int(long(x)), items12)

        items13 = items[13][2:-2].split(',')

        res.append((int(r), items1, items2, items3, items4, items5, items6, items7, items8, items9, items10, items11, items12, items13))

    return res


res = {}
def warning(*objs):
    print("FUZZING: ", *objs, file=sys.stderr)


gfname = ""
error_func = []

from os import kill
from signal import alarm, signal, SIGALRM, SIGKILL
from subprocess import PIPE, Popen

def run(args, cwd = None, shell = False, kill_tree = True, timeout = -1, env = None):
    '''
    '''
    class Alarm(Exception):
        pass
    def alarm_handler(signum, frame):
        raise Alarm
    p = Popen(args, shell = shell, cwd = cwd, stdout = PIPE, stderr = PIPE, env = env)
    if timeout != -1:
        signal(SIGALRM, alarm_handler)
        alarm(timeout)
    try:
        stdout, stderr = p.communicate()
        if timeout != -1:
            alarm(0)
    except Alarm:
        pids = [p.pid]
        if kill_tree:
            pids.extend(get_process_children(p.pid))
        for pid in pids:
            
           
            try: 
                kill(pid, SIGKILL)
                global error_func
                global gfname
                error_func.append(gfname)
                
                os.system("python analysis/compl.py")
               
            except OSError:
                pass
        return -9, '', ''
    return p.returncode, stdout, stderr


def get_process_children(pid):
    p = Popen('ps --no-headers -o pid --ppid %d' % pid, shell = True,
              stdout = PIPE, stderr = PIPE)
    stdout, stderr = p.communicate()
    return [int(p) for p in stdout.split()]


def process(cmd, fn, funcname):
    global gfname
    bp = os.getcwd()
    with cd("/data/pin_sets/temp1/pin-3.0-76991-gcc-linux/source/tools/inMemFuzzing"):
        lines = []
        warning(cmd)

        os.system("rm pinatrace.out")

        gfname = fn + ":" + funcname
        
        run(cmd, shell=True, timeout = 20)

        if os.path.isfile("pinatrace.out"):
            
            os.system("python analysis/collect.py " + fn + " > " + bp + "/temp_func.info")
        else:
            raise Exception("undefined behavior")


    t = connect_list()
    fn1 = os.path.basename(fn)
    res[fn1 + "_" + funcname] = t


def new_cmd(fn, baddr, eaddr, ce, cr):
    runcmd = "../../../pin -t ./obj-intel64/process.so -start {0} -end {1} -codeStart {2} -codeRange {3} -fuzzingCount {4} -fuzzingType step -startValue 0x1 -- {5} > temp.out"

    return runcmd.format(*(baddr, eaddr, ce, cr, fuzzingcount, fn))


def fuzzing_old(fn):
    lines = []
    fn1 = os.path.basename(fn)

    with open(fn + "_info.txt") as f:
        lines = f.readlines()

    count = 1
    for l in lines:
        if count == 10:
            break
        else:
            count += 1
            (funcname, ba, ea) = l.split(":")
            ba = str.strip(ba)
            ea = str.strip(ea)

            c = new_cmd(fn, ba, ea)
            process(c, fn1, funcname)


def fuzzing_new(fn, funcname, ba, ea, ce, cr):
    global error_func
    c = new_cmd(fn, ba, ea, ce, cr)
    process(c, fn, funcname)

    return error_func
