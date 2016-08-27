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


def get_code_range(id):
    
    os.system("cat /proc/" + id + "/maps > segment.info")

    lines = []
    with open("segment.info") as f:
        lines = f.readlines()

    
    l = lines[2]
    l1 = l.split()[0]
    items = l1.split("-")
    a = int(items[0], 16)
    b = int(items[1], 16)
    print str(a) + "-" + str(b)


def process(id):
    
    get_code_range(id)


if __name__ == '__main__':
    process(sys.argv[1])
