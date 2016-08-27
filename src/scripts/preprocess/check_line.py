import sys

lines = []
fn = sys.argv[1]

with open(fn) as f:
    lines = f.readlines()

index_list = []
for i in range(len(lines)):
   l = lines[i]
   l = str.strip(l)
   if l[-1] == '1':
       index_list.append(i)

for i in range(len(index_list)-1):
    a = index_list[i]
    b = index_list[i+1]

    print b - a
    
