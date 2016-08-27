import re, os


def lea_process(i):
    op = i[1]
    if op == "lea":
        op2 = i[2][1]
        if "ptr [" in op2:
            i[2][1] = op2[5:]
            return i
        else:
            raise Exception("undefined lea process")
    else:
        return i


def lea_process_reverse(i):
    op = i[1]
    print i
    if op == "lea":
        op1 = i[2][0]
        if "ptr [" in op1:
            i[2][0] = op1[4:]
            return i
        else:
            raise Exception("undefined lea process")
    else:
        return i


def call_ret_process(i):
    if "call" in i[1] or "ret" in i[1]:
        i1 = [i[0], "push", [i[2][0]]]
        i2 = [i[0], "jmp", i[2]]
        return [i1, i2]
    elif "ret" in i[1]:
        i1 = [i[0], "pop", ["rcx"]]
        i2 = [i[0], "jmp", ["ptr [rcx]"]]
        return [i1, i2]
    else:
        return [i]


def stack_process(i):
    if "push" in i[1]:
        i1 = [i[0], "mov", [i[2][0], "qword ptr [rsp]"]]
        i2 = [i[0], "sub", ["4", "rsp"]]
        return [i1, i2]
    elif "pop" in i[1]:
        i1 = [i[0], "mov", [i[2][0], "qword ptr [rsp]"]]
        i2 = [i[0], "add", ["4", "rsp"]]
        return [i1, i2]
    elif "leave" in i[1]:
        i1 = [i[0], "mov", ["rbp", "rsp"]]
        i2 = [i[0], "mov", ["qword ptr [rsp]", "rbp"]]
        i3 = [i[0], "add", ["4", "rsp"]]
        return [i1, i2, i3]
    else:
        return [i]


def parse_opend(op1):
    regex1 = re.compile(r'\[(.*)\]',re.I)
    op11 = regex1.search(op1).groups()[0]
    if "+" in op11:
        if op11.count("+") == 2:
            items = op11.split("+")
            if "*" in items[1]:
                items1 = items[1].split("*")
                return [items[0], "+", items1[0], "*", items1[1], "+", str(int(items[2],16))]
            else:
                raise Exception("undefined behavior in parse opend" + op1)
        elif op11.count("+") == 1 and "*" in op11:
            items = op11.split("+")
            items1 = items[1].split("*")
            return [items[0], "+", items1[0], "*", items1[1], "+", "0"]
        elif op11.count("+") == 1:
            items = op11.split("+")
            items[1] = str(int(items[1], 16))
            return [items[0], "+", items[1]]
    elif "-" in op11:
        items = op11.split("-")
        items[1] = str(int(items[1], 16))
        return [items[0], "-", items[1]]
    elif "*" in op11:
        items = op11.split("*")
        items[1] = str(int(items[1], 16))
        return [items[0], "*", items[1]]
    elif len(op11) == 3 or len(op11) == 2:
        return [op11, "+", "0"]
    else:
        raise Exception("undefined behavior in parse operand" + op1)


def mem_process(i):
    print i
    def aux(s):
        if s.startswith("0x"):
            return str(int(s, 16))
        else:
            return s

    if len(i[2]) == 2:
        op1 = i[2][0]
        op2 = i[2][1]

        if "[" in op1 and not ("[" in op2):
            ret = parse_opend(op1)
            ret1 = ["t0"]
            ret1.extend(ret)
            ret.append("t0")
            i1 = [i[0], "load", ret1]
            i[2][1] = aux(i[2][1])
            i2 = [i[0], i[1], ["t0", i[2][1]]]
            i3 = [i[0], "store", ret]
            return [i1, i2, i3]
        elif "[" in op2 and not ("[" in op1):
            ret = parse_opend(op2)
            ret1 = ["t0"]
            ret1.extend(ret)
            i1 = [i[0], "load", ret1]
            i[2][0] = aux(i[2][0])
            i2 = [i[0], i[1], [i[2][0], "t0"]]
            return [i1, i2]
        elif "[" in op2 and "[" in op1:
            ret = parse_opend(op2)
            ret1 = ["t0"]
            ret1.extend(ret)
            i1 = [i[0], "load", ret1]

            ret = parse_opend(op1)
            ret1 = ["t1"]
            ret1.extend(ret)
            ret.append("t1")
            i3 = [i[0], "load", ret1]
            i4 = [i[0], i[1], ["t1", "t0"]]
            i5 = [i[0], "store", ret]

            return [i1, i3, i4, i5]
        else:
            return [i]
    elif len(i[2]) == 1:
        op = i[2]
        if "[" in op and i[1][0] == 'j':
            ret = parse_opend(i[2])
            ret1 = ["t0"]
            ret1.extend(ret)
            i1 = [i[0], "load", ret1]
            i[2][0] = aux(i[2][0])
            i2 = [i[0], i[1], [i[2][0], "t0"]]
            return [i1, i2]
        elif "[" in op:
            raise Exception("undefined behavior in mem process 2")
        else:
            return [i]
    else:
        return [i]


def pre_process(i):
    if "cm" in i[1]:
        return [i[0], 'nop', None]
    elif "test" in i[1]:
        return [i[0], 'nop', None]
    else:
        return i

def parse(i):
    i = pre_process(i)

    operlist = i[2]
    if operlist == None:
        return [i]
    else:
        i = lea_process_reverse(i)
        il = call_ret_process(i)
        il1 = []
        for i in il:
            il1.extend(stack_process(i))
        il2 = []
        for i in il1:
            il2.extend(mem_process(i))

        return il2
