sym_list = ['stdin', 'stdout', 'stderr', '__progname', '__progname_full']

def preprocess(s):
    if '(' in s:
        return s
    else:
        if "_next" in s and "$" not in s:
            d = int(s.split('_')[1], 16) + 5
            return str(d)
        elif "_next" in s:
            d = int(s.split('_')[1][1:], 16) + 5
            return str(d)
        elif s.startswith('S_0x'):
            d = int(s[2:], 16)
            return "(" + str(d) + ")"
        elif s.startswith('$S_0x'):
            d = int(s[3:], 16)
            return str(d)
        elif '%gs:0x' in s:
            s = '(' + s + ')'
            return s
        elif s in sym_list:
            return '(' + str(999) + ')'
        else:
            return s


def preprocess_op(p):
    if len(p) == 5 and p.endswith('ss'):
        t = p[:-2]
        print 'change ' + p + ' to ' + t
        return t
    if len(p) == 4 and p.startswith('i'):
        t = p[1:]
        print 'change ' + p + ' to ' + t
        return t
    if len(p) == 3 and p.startswith('or'):
        t = p[:-1]
        print 'change ' + p + ' to ' + t
        return t
    else:
        return p


class EquationId(object):
    def __init__(self, id_):
        self.id = id_

    def __repr__(self):
        return 'EID:%d' % self.id



def prove(f):
    s = Solver()
    s.add(Not(f))
    if s.check() == unsat:
        return True
    return False


class Disassembler(object):



    def __init__(self, instrl, last_addr):
        self.instrlist = []
        self.blist = ['nop', 'int', 'hlt', 'repz', 'cvtsi2sd', 'cvtsi2ss',
                      'ucomiss','cvttss2si']

        self.clist = ['shrl', 'shr', 'shl']

        self.alist = ['div', 'mul', 'sar']

        self.wlist = ['not', 'sbb', 'bsr']

        self.llist = {'ror': 'shr', 'rol' : 'shl'}


        self.cond_list = {
            'cmove'  : 'mov',
            'cmovne' : 'mov',
            'cmovae' : 'mov',
            'cmovbe' : 'mov',
            'cmovb'  : 'mov',
            'cmova'  : 'mov',
            'movabs' : 'mov',
            'movaps' : 'mov',
            'movapd' : 'mov',
            'movsd'  : 'mov',
            'movzx'  : 'mov',
            'addsd'  : 'add',
            'movsd'  : 'mov',
            'movss'  : 'mov',
            'movsxd' : 'mov',
            'movlps' : 'mov',
            'movhps' : 'mov',
            'addss'  : 'add',
            'subss'  : 'sub',
            'divss'  : 'div',
            'mulss'  : 'mul',
            'divsd'  : 'div',
            'mulsd'  : 'mul',
            'movw'   : 'mov',
            'xorps'  : 'xor',
        }


        self.q_list = {
            'movq' : "movl",
            'subq' : "subl",
            'addq' : "addl",
            'movslq' : "mov",
            'movzwl' : "mov",
            'orq' : "or",
        }


        self.reg_8_list = [
            '%al',
            '%bl',
            '%cl',
            '%dl'
        ]
        self.instrlist = instrl
        self.addrlist = [last_addr]
        self.addrlist = map(lambda l: l[0], self.instrlist)


    def change(self, items):
        items = [items[0], '1', items[1]]
        return items


    def get_next_instruction(self):
        for l in self.instrlist:
            print "************ ", l , " ********************"
            addr = l[0]
            items = []
            items.append(l[1])
            if l[2]:
                items.extend(l[2])

            if items[0] in self.blist:
                print "don't handle:", l
                yield ["nop"]
            elif (len(items[0]) == 3 or len(items[0]) == 4) and items[0][0] == 'j':
                print "don't handle jump instruction", l
                yield ["nop"]
            elif len(items) == 3 and items[0] in self.q_list:
                items[0] = self.q_list[items[0]]
                items[1] = preprocess(items[1])
                items[2] = preprocess(items[2])
                yield items
            elif len(items) == 3 and items[0] == 'mov' and items[1] in self.reg_8_list:
                items[0] = 'movb'
                items[1] = preprocess(items[1])
                items[2] = preprocess(items[2])
                yield items
            elif len(items) == 3 and items[0] in self.llist:
                items[0] = self.llist[items[0]]
                items[1] = preprocess(items[1])
                items[2] = preprocess(items[2])
                yield items
            elif len(items) == 3 and items[0] in self.cond_list:
                items[0] = self.cond_list[items[0]]
                items[1] = preprocess(items[1])
                items[2] = preprocess(items[2])
                yield items
            elif len(items) == 2 and items[0] in self.clist:
                items = self.change(items)
                items[1] = preprocess(items[1])
                yield items
            elif len(items) == 2 and items[0] in self.wlist:
                yield items
            elif len(items) == 3 and items[0] in self.wlist:
                yield items
            elif len(items) == 2 and items[0] in self.alist:
                yield items
            elif len(items) == 3:
                items[0] = preprocess_op(items[0])
                items[1] = preprocess(items[1])
                items[2] = preprocess(items[2])
                yield items
            elif items[0] in ('mov', 'sub', 'mul', 'add', 'load', 'store'):
                yield items
            else:
                yield ["nop"]


    def get_instrs(self):
        il = []
        for i in self.get_next_instruction():
            il.append(i)

        return il
