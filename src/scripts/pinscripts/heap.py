import sys, os

def get_proc_id(fn):
    os.system("ps -ef | grep " + fn + " > proc.info")

    lines = []

    with open("proc.info") as f:
        lines = f.readlines()

    for l in lines:
        if fn in l and not ("grep" in l):
            items = l.split()
            return items[1]


def get_heap_range(id):
    
    os.system("cat /proc/" + id + "/maps > segment.info")

    lines = []
    with open("segment.info") as f:
        lines = f.readlines()

    for l in lines:
        if "[heap]" in l:
            r = l.split()[0]
            items = r.split("-")[0]

            print items

    print "none"


def process(id):

    return get_heap_range(id)


if __name__ == '__main__':
    process(sys.argv[1])


