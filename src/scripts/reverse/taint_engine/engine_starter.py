import threading, os, sys, os.path


class bb_engine(threading.Thread):

    def __init__(self, thread_id, begin_index, end_index):
        threading.Thread.__init__(self)
        self.ti = thread_id
        self.bi = begin_index
        self.ei = end_index



    def run(self):

        print 'thread ' + str(self.ti) + " with range " + str(self.bi) + " to " + str(self.ei)

        log_fn = "log_" + str(self.ti) + ".log"

        os.system('rm ' + log_fn)

        for i in range(self.bi, self.ei):
            bn = 'BB_' + str(i)
	    if os.path.isfile("instr_list_" + bn + ".txt"):
                os.system("python plugins/symbolic_engine/engine_64/engine.py " + bn + " >> " + log_fn)



def single(n):
    for i in range(int(n)):
        bn = 'BB_' + str(i)
        os.system("cp ../../../instr_list_" + bn + ".txt .")
        if os.path.isfile("instr_list_" + bn + ".txt"):
            os.system("python engine.py " + bn)



def main(bnum):

    threads = []

    bnum = int(bnum)
    b_range = bnum / 6
    try:
        for i in range(1,6):
            b = (i-1) * b_range
            e = (i) * b_range
            t = bb_engine(i, b, e)
            t.start()

            threads.append(t)


        b = 5 * b_range
        e = bnum
        t = bb_engine(6, b, e+1)
        t.start()
        threads.append(t)


        for t in threads:
            t.join()


    except:
        print "Error: unable to start thread"


if __name__ == '__main__':
    bnum = sys.argv[1]
    single(bnum)
