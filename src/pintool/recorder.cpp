void loopInstrMap()
{
    cout << endl << endl;
    typedef std::map<ADDRINT, INS>::iterator it_type;

    for(it_type iterator = instrMap.begin(); iterator != instrMap.end(); ++iterator) {
        cout << "addr " << hex << iterator->first << " : "  << INS_Disassemble(iterator->second) << endl;
    }
    cout << endl << endl;
}

void recordInstr(ADDRINT insAddr, INS ins)
{
    loopInstrMap();

    if (instrMap.count(insAddr) > 0)
    {
        return;
    }

    instrMap[insAddr] = ins;
}


INS getInstrByAddr(ADDRINT insAddr)
{
    loopInstrMap();

    INS t = instrMap[insAddr];
    
    return t;
}


void recordInstrOperand(ADDRINT insAddr, INS ins)
{
    if (instrMapNew.count(insAddr) > 0)
    {
        return;
    }

    REG rr = regInMemoryRead(ins);
    REG rw = regInMemoryWrite(ins);
    
    fpRecord rfp = regInFP(ins);
   
    string rs = INS_Disassemble(ins);
    LEVEL_BASE::OPCODE opc = getOP(ins);

    struct instrRecord ir;
    ir.insDis = rs;
    ir.regRead = rr;
    ir.regWrite = rw;
    ir.fpr = rfp;
    ir.op = opc;
    ir.addrNext = INS_NextAddress(ins);

    instrMapNew[insAddr] = ir;

}

void initRecorder()
{
    
    struct instrRecord ir;
    ir.insDis = "dummy";
    ir.op = 0;
    ir.addrNext = 0;

    instrMapNew[1] = ir;
}

instrRecord getInstrByAddrOperand(ADDRINT insAddr)
{
    if (instrMapNew.count(insAddr) > 0)
    {
        instrRecord ir = instrMapNew[insAddr];
        
        return ir;
    }
    else
    {
       
        instrRecord dummy = instrMapNew[1];
        return dummy;
    }
}


VOID recordCall(ADDRINT insAddr, VOID* desAddr)
{
        fprintf(trace,"call:%p\n", desAddr);
}
