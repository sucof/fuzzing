
def aux(i):
    if i[2] == None:
        return i
    elif len(i[2]) == 2:
        t = i[2][0]
        i[2][0] = i[2][1]
        i[2][1] = t
        return i
    else:
        return i

def aux(s):
    if s.startswith("0x"):
        return str(int(s, 16))
    else:
        return s


def lex(s):
    items = s.split()
    addr = items[0][:-1]

    op = items[1]

    if "," in s:
        s1 = " ".join(items[2:])
        if s1.count(',') == 1:
            opn1 = str.strip(s1.split(",")[0])
            opn2 = str.strip(s1.split(",")[1])
            opn1 = aux(opn1)
            opn2 = aux(opn2)
            return [addr, op, [opn1, opn2]]
        else:
            raise Exception("undefined behavior in lex1: " + s)
    else:
        if len(items) == 2:
            return [addr, op, None]
        elif len(items) == 3:
            items[2] = aux(items[2])
            return [addr, op, [items[2]]]
        elif len(items) == 5:
            return [addr, op, [" ".join(items[2:])]]
        else:
            raise Exception("undefined behavior in lex2: " + s)
