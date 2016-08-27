import os

for i in os.listdir("."):
    if i.startswith("fv"):
	if os.stat(i).st_size == 0:
            pass
	else:
	    os.system("cat " + i + " >> fv.txt")
