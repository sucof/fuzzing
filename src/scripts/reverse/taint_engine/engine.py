
import linecache
import sys
import traceback
from z3 import *

import assign_process as AP
import arith_process as ARP
import logic_process as LP
import mem_process as MP
import cmp_process as CP
import lea_process as LEAP
from disassembler import *
import tainter as T


def is_hex(s):
    try:
        int(s, 16)
    except :
        return False
    else:
        return True


class TaintEngine(object):

    def __init__(self, bn, init_ctx, taint_r, instrl, last_addr, ctxlist):

        self.addr_tainted = {}

        self.regs_tainted = {}

        self.cur_index = 0

        self.instr_list = 0

        self.opl = ["+", '-', '*']

        self.ctx = {
            'rax' : None,
            'rbx' : None,
            'rcx' : None,
            'rdx' : None,
            'rsi' : None,
            'rdi' : None,
            'rbp' : None,
            'rsp' : None,
            'rip' : None,
            'r8'  : None,
            'r9'  : None,
            'r10' : None,
            'r11' : None,
            'r12' : None,
            'r13' : None,
            'r14' : None,
            'r15' : None,
            't0'  : None,
            't1'  : None,
            'eiz' : None,
            'xmm0' : None,
            'xmm1' : None,
            'xmm2' : None,
            'xmm3' : None,
            'xmm4' : None,
            'xmm5' : None,
            'xmm6' : None,
            'xmm7' : None,
        }

        self.reg_32_map = {
            'eax' : ((31,0), 'rax'),
            'ebx' : ((31,0), 'rbx'),
            'ecx' : ((31,0), 'rcx'),
            'edx' : ((31,0), 'rdx'),
            'esi' : ((31,0), 'rsi'),
            'edi' : ((31,0), 'rdi'),
            'ebp' : ((31,0), 'rbp'),
            'esp' : ((31,0), 'rsp'),
            'r8d' : ((31,0), 'r8'),
            'r9d' : ((31,0), 'r9'),
            'r10d' : ((31,0), 'r10'),
            'r11d' : ((31,0), 'r11'),
            'r12d' : ((31,0), 'r12'),
            'r13d' : ((31,0), 'r13'),
            'r14d' : ((31,0), 'r14'),
            'r15d' : ((31,0), 'r15'),
            'eip' : ((31,0), 'rip'),
            't0' : ((31,0), 't0'),
            't1' : ((31,0), 't1'),
            }


        self.reg_small_map = {
            'ax' : ((15,0), 'rax'),
            'bx' : ((15,0), 'rbx'),
            'cx' : ((15,0), 'rcx'),
            'dx' : ((15,0), 'rdx'),
            'si' : ((15,0), 'rsi'),
            'di' : ((15,0), 'rdi'),
            'bp' : ((15,0), 'rbp'),
            'sp' : ((15,0), 'rsp'),
            'r8w' : ((15,0), 'r8'),
            'r9w' : ((15,0), 'r9'),
            'r10w' : ((15,0), 'r10'),
            'r11w' : ((15,0), 'r11'),
            'r12w' : ((15,0), 'r12'),
            'r13w' : ((15,0), 'r13'),
            'r14w' : ((15,0), 'r14'),
            'r15w' : ((15,0), 'r15'),
            'ah' : ((15,8), 'rax'),
            'al' : ((7,0),  'rax'),
            'bh' : ((15,8), 'rbx'),
            'bl' : ((7,0),  'rbx'),
            'ch' : ((15,8), 'rcx'),
            'cl' : ((7,0),  'rcx'),
            'dh' : ((15,8), 'rdx'),
            'dl' : ((7,0),  'rdx'),
            'sil' : ((7,0),  'rsi'),
            'dil' : ((7,0),  'rdi'),
            'bpl' : ((7,0),  'rbp'),
            'spl' : ((7,0),  'rsp'),
            'r8b' : ((7,0),  'r8'),
            'r9b' : ((7,0),  'r9'),
            'r10b' : ((7,0), 'r10'),
            'r11b' : ((7,0), 'r11'),
            'r12b' : ((7,0), 'r12'),
            'r13b' : ((7,0), 'r13'),
            'r14b' : ((7,0), 'r14'),
            'r15b' : ((7,0), 'r15'),
        }

        self.bn = bn

        self.disass = Disassembler(instrl, last_addr)

        self.mem = {}

        self.addr_list = self.disass.addrlist

        self.ctx_list = ctxlist
        self.idx = 0

        self.sym_variables = []

        self.equations = {}

        self.ninstrs = 0

        self.set_reg_with_equation('rax', BitVec('reg%d' % 1, 64))
        self.set_reg_with_equation('rbx', BitVec('reg%d' % 2, 64))
        self.set_reg_with_equation('rcx', BitVec('reg%d' % 3, 64))
        self.set_reg_with_equation('rdx', BitVec('reg%d' % 4, 64))
        self.set_reg_with_equation('rsi', BitVec('reg%d' % 5, 64))
        self.set_reg_with_equation('rdi', BitVec('reg%d' % 6, 64))
        self.set_reg_with_equation('rbp', BitVec('reg%d' % 7, 64))
        self.set_reg_with_equation('rsp', BitVec('reg%d' % 8, 64))
        self.set_reg_with_equation('rip', BitVec('reg%d' % 9, 64))
        self.set_reg_with_equation('r8',  BitVec('reg%d' % 10, 64))
        self.set_reg_with_equation('r9',  BitVec('reg%d' % 11, 64))
        self.set_reg_with_equation('r10', BitVec('reg%d' % 12, 64))
        self.set_reg_with_equation('r11', BitVec('reg%d' % 13, 64))
        self.set_reg_with_equation('r12', BitVec('reg%d' % 14, 64))
        self.set_reg_with_equation('r13', BitVec('reg%d' % 15, 64))
        self.set_reg_with_equation('r14', BitVec('reg%d' % 16, 64))
        self.set_reg_with_equation('r15', BitVec('reg%d' % 17, 64))
        self.set_reg_with_equation('eiz', BitVec('reg%d' % 18, 64))
        self.set_reg_with_equation('xmm1', BitVec('reg%d' % 19, 64))
        self.set_reg_with_equation('xmm2', BitVec('reg%d' % 20, 64))
        self.set_reg_with_equation('xmm3', BitVec('reg%d' % 21, 64))
        self.set_reg_with_equation('xmm4', BitVec('reg%d' % 22, 64))
        self.set_reg_with_equation('xmm5', BitVec('reg%d' % 23, 64))
        self.set_reg_with_equation('xmm6', BitVec('reg%d' % 24, 64))
        self.set_reg_with_equation('xmm7', BitVec('reg%d' % 25, 64))
        self.set_reg_with_equation('xmm0', BitVec('reg%d' % 26, 64))
        self.set_reg_with_equation('t0',  BitVec('t%d' % 0, 64))
        self.set_reg_with_equation('t1',  BitVec('t%d' % 1, 64))
        self.sym_variables.append(BitVec('reg%d' % 1, 64))
        self.sym_variables.append(BitVec('reg%d' % 2, 64))
        self.sym_variables.append(BitVec('reg%d' % 3, 64))
        self.sym_variables.append(BitVec('reg%d' % 4, 64))
        self.sym_variables.append(BitVec('reg%d' % 5, 64))
        self.sym_variables.append(BitVec('reg%d' % 6, 64))
        self.sym_variables.append(BitVec('reg%d' % 7, 64))
        self.sym_variables.append(BitVec('reg%d' % 8, 64))
        self.sym_variables.append(BitVec('reg%d' % 9, 64))
        self.sym_variables.append(BitVec('reg%d' % 10, 64))
        self.sym_variables.append(BitVec('reg%d' % 11, 64))
        self.sym_variables.append(BitVec('reg%d' % 12, 64))
        self.sym_variables.append(BitVec('reg%d' % 13, 64))
        self.sym_variables.append(BitVec('reg%d' % 14, 64))
        self.sym_variables.append(BitVec('reg%d' % 15, 64))
        self.sym_variables.append(BitVec('reg%d' % 16, 64))
        self.sym_variables.append(BitVec('reg%d' % 17, 64))
        self.sym_variables.append(BitVec('reg%d' % 18, 64))
        self.sym_variables.append(BitVec('reg%d' % 19, 64))
        self.sym_variables.append(BitVec('reg%d' % 20, 64))
        self.sym_variables.append(BitVec('reg%d' % 21, 64))
        self.sym_variables.append(BitVec('reg%d' % 22, 64))
        self.sym_variables.append(BitVec('reg%d' % 23, 64))
        self.sym_variables.append(BitVec('reg%d' % 24, 64))
        self.sym_variables.append(BitVec('reg%d' % 25, 64))
        self.sym_variables.append(BitVec('reg%d' % 26, 64))
        self.sym_variables.append(BitVec('t%d' % 0, 64))
        self.sym_variables.append(BitVec('t%d' % 1, 64))


        for k, v in init_ctx.items():
            x = BitVecVal(v, 64)
            k1 = str.lower(str.strip(k))
            self.set_reg_with_equation(k1, x)
            print ("init context ---> ", k1, " : ", x)

        T.taint_reg_true(taint_r, last_addr, self)


    def _check_if_reg64(self, r):
        '''XXX: make a decorator?'''
        return r.lower() in self.ctx

    def _push_equation(self, e):
        idx = EquationId(self.idx)
        self.equations[idx] = e
        self.idx += 1
        return idx


    def set_reg_with_equation(self, r, e):
        if self._check_if_reg64(r) == False:
            return

        self.ctx[r] = self._push_equation(e)


    def get_reg_equation(self, r):
        if self._check_if_reg64(r) == False:
            return None

        if isinstance(self.ctx[r], EquationId):
            return self.equations[self.ctx[r]]
        else:
            return self.ctx[r]


    def get_cur_addr(self):
        return self.addr_list[self.cur_index]


    def get_next_instruction(self):
        return self.instr_list[self.cur_index+1]


    def get_previous_instruction(self):
        return self.instr_list[self.cur_index-1]


    def update_ctx_info(self):
        caddr = int(self.get_cur_addr())
        c_ctx = self.ctx_list[caddr]

        for k, v in c_ctx.items():
            x = BitVecVal(v, 64)
            k1 = str.lower(str.strip(k))
            self.set_reg_with_equation(k1, x)



    def execute(self):
        il = self.disass.get_instrs()
        self.instr_list = il

        for ind in range(len(il)):
            self.cur_index = ind
            items = il[ind]
            print hex(int(self.get_cur_addr(),10)), items

            self.update_ctx_info()

            mnemonic = ""
            src = ""
            dst = ""
            src_2 = ""
            if len(items) == 1:
                mnemonic = items[0]
            elif len(items) == 2:
                mnemonic, dst = items
            elif len(items) == 3:
                mnemonic, dst, src = items
            elif len(items) == 4:
                mnemonic, src, src_2, dst = items
            elif len(items) == 5:
                mnemonic, dst, src, op, src_2 = items
            elif len(items) == 9 and items[0] == "load":
                mnemonic, dst, src1, op1, src2, op2, src3, op3, src4 = items
            elif len(items) == 9 and items[0] == "store":
                mnemonic, dst1, op1, dst2, op2, dst3, op3, dst4, src = items

            if (self.ninstrs % 5000) == 0 and self.ninstrs > 0:
                print '%d instructions, %d equations so far...' % (self.ninstrs, len(self.equations))

            if mnemonic == 'movl':
                AP.movl_process(self, dst, src)
            elif mnemonic == 'mov':
                AP.mov_process(self, dst, src)
            elif mnemonic == 'movb':
                AP.movb_process(self, dst, src)
            elif mnemonic == 'movzbl':
                AP.movzbl_process(self, dst, src)
            elif mnemonic == 'movsbl':
                AP.movsbl_process(self, dst, src)
            elif mnemonic == 'xchg':
                AP.xchg_process(self, dst, src)
            elif mnemonic == 'notl':
                LP.notl_process(self, dst)
            elif mnemonic == 'not':
                LP.not_process(self, dst)
            elif mnemonic == 'andl':
                LP.andl_process(self, dst, src)
            elif mnemonic == 'andb':
                LP.andb_process(self, dst, src)
            elif mnemonic == 'and':
                LP.and_process(self, dst, src)
            elif mnemonic == 'xorl':
                LP.xorl_process(self, dst, src)
            elif mnemonic == 'xor':
                LP.xor_process(self, dst, src)
            elif mnemonic == 'orl':
                LP.orl_process(self, dst, src)
            elif mnemonic == 'or':
                LP.or_process(self, dst, src)
            elif mnemonic == 'shr':
                ARP.shr_process(self, dst, src)
            elif mnemonic == 'adc':
                ARP.add_process(self, dst, src)
            elif mnemonic == 'sbb':
                ARP.sub_process(self, src, dst)
            elif mnemonic == 'shl':
                ARP.shl_process(self, dst, src)
            elif mnemonic == 'mul' and len(items) == 4:
                ARP.mul_4_process(self, dst, src, src_2)
            elif mnemonic == 'mul' and len(items) == 3:
                ARP.mul_3_process(self, dst, src)
            elif mnemonic == 'mul' and len(items) == 2:
                ARP.mul_2_process(self, dst)
            elif mnemonic == 'addl' and len(items) == 4:
                ARP.add_4_process(self, dst, src, src_2)
            elif mnemonic == 'addl' and len(items) == 3:
                ARP.addl_process(self, dst, src)
            elif mnemonic == 'subl' and len(items) == 4:
                ARP.subl_process(self, dst, src, src_2)
            elif mnemonic == 'subl' and len(items) == 3:
                ARP.subl_process(self, dst, src)
            elif mnemonic == 'add' and len(items) == 4:
                ARP.add_4_process(self, dst, src, src_2)
            elif mnemonic == 'add' and len(items) == 3:
                ARP.add_process(self, dst, src)
            elif mnemonic == 'sub' and len(items) == 4:
                ARP.sub_4_process(self, dst, src, src_2)
            elif mnemonic == 'sub' and len(items) == 3:
                ARP.sub_process(self, dst, src)
            elif mnemonic == 'div' and len(items) == 3:
                ARP.div_3_process(self, dst, src)
            elif mnemonic == 'div' and len(items) == 2:
                ARP.div_2_process(self, dst)
            elif mnemonic == 'sar' and len(items) == 2:
                ARP.sar_process(self, dst, '1')
            elif mnemonic == 'sar':
                ARP.sar_process(self, dst, src)
            elif mnemonic == 'load' and len(items) == 9:
                MP.load_long_process(self, dst, src1, op1, src2, op2, src3, op3, src4)
            elif mnemonic == 'load':
                MP.load_process(self, dst, src, op, src_2)
            elif mnemonic == 'loadl':
                MP.loadl_process(self, dst, src, op, src_2)
            elif mnemonic == 'store' and len(items) == 9:
                MP.store_long_process(self, dst1, op1, dst2, op2, dst3, op3, dst4, src)
            elif mnemonic == 'store':
                MP.store_process(self, dst, src, op, src_2)
            elif mnemonic == 'storel':
                MP.storel_process(self, dst, src, op, src_2)
            elif mnemonic == 'cmp':
                CP.cmp_process(self, dst, src)
            elif mnemonic == 'lea':
                LEAP.lea_process(self, dst, src)
            elif mnemonic == 'nop':
                continue
            else:
                print mnemonic, src, dst
                raise Exception('This instruction is not handled.' + mnemonic)

            self.ninstrs += 1


    def PrintException(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


    def run(self):
        try:
            self.execute()
        except:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            print "taint analysis of " + self.bn + " failed!"


    def _simplify_additions(self, eq):
        if prove(Sum(self.sym_variables) == eq):
            return Sum(self.sym_variables)

        return eq


    def get_reg_equation_simplified(self, reg):
        eq = self.get_reg_equation(reg)
        if isinstance(self.ctx[reg], EquationId):
            eq = simplify(eq)
        return eq


    def taint_reults(self):
        return (self.regs_tainted, self.addr_tainted)


    def execution_outputs(self):
        res = []

        for r in self.ctx:
            try:
                if self.ctx[r]:
                    if r != '%t1' and r != '%t0':
                        state = self.get_reg_equation_simplified(r)
                        res.append(r + " = " + str(state) + "\n")
                else:
                    res.append(r + ' = undefined\n')
            except:
                print "simplify failed: ", str(r), str(self.ctx[r])

        return (res, [])


def retrieving (sym, bn):
    res = []

    for r in sym.ctx:
        try:
            if sym.ctx[r]:
                if r != '%t1' and r != '%t0':
                    state = sym.get_reg_equation_simplified(r)
                    res.append(r + " = " + str(state) + "\n")
            else:
                res.append(r + ' = undefined\n')
        except:
            print "simplify failed: ", str(r), str(sym.ctx[r])


    res1 = MP.inspect_stack(sym)
    res = res + res1

    fn = 'symbolic_formula_' + bn
    with open (fn, 'w') as f:
        f.writelines(res)



def main(bn):
    print 'Launching the 64-bit engine for taint analysis ' + bn + ' ...'
    sym = TaintEngine("test", fctx, taint_r, rl1, last_addr, ctxlist)
    sym.run()
    print 'execution finished..'
    return 1


if __name__ == '__main__':
    bn = sys.argv[1]
    main(bn)
