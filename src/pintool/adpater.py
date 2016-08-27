import sys, os


class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


c = sys.argv[1]

def process(c):
    if c == '1':
        with cd("~/work/project/fuzzing/src/scripts/reverse/"):
            os.system("python process.py")

        os.system("cp ~/work/project/fuzzing/src/scripts/reverse/reverse.output .")


process(c)
