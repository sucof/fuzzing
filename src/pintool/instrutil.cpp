bool isMemReadReg(INS ins)
{
    
    return (INS_OperandCount(ins) > 1 && INS_MemoryOperandIsRead(ins, 1) && INS_OperandIsReg(ins, 1));
}


bool isMemWriteReg(INS ins)
{
    return (INS_OperandCount(ins) > 1 && INS_MemoryOperandIsWritten(ins, 0) && INS_OperandIsReg(ins, 0));
}


REG getMemReadReg(INS ins)
{
    return INS_OperandReg(ins, 1);
}


REG getMemWriteReg(INS ins)
{
    return INS_OperandReg(ins, 0);
}



fpRecord aux(REG r, FPOp op, INT64 addr)
{
    fpRecord f = {r, op, addr};

    return f;
}

LEVEL_BASE::OPCODE getOP(INS ins)
{
    return INS_Opcode(ins);
}

bool isControlOP(LEVEL_BASE::OPCODE op)
{
    return op == XED_ICLASS_JMP || op == XED_ICLASS_CALL_NEAR || op == XED_ICLASS_JMP_FAR || op == XED_ICLASS_CALL_FAR;
}

fpRecord regInFP(INS ins)
{
    if (INS_OperandCount(ins) == 4)
    {
        if (INS_OperandIsReg(ins, 0))
        {
            REG r = INS_OperandReg(ins, 0);
            return aux(r, FPInvalid, 0);
        }
        else if (INS_OperandIsMemory(ins, 0))
        {
            REG r = INS_OperandMemoryBaseReg(ins, 0);
            INT64 d = INS_OperandMemoryDisplacement(ins, 0);
            return aux(r, FPInvalid, d);
        }
        else
            return aux(REG_INVALID_, FPInvalid, 0);
    }
    else
    {
        return aux(REG_INVALID_, FPInvalid, 0);
    }
}


REG regInMemoryRead(INS ins)
{
    if (INS_OperandCount(ins) == 1)
    {
        cout << "unhanded 1 " << INS_Disassemble(ins) << endl;
        return REG_INVALID_;
    }
    else if (INS_OperandCount(ins) == 2)
    {
        if (INS_OperandIsReg(ins, 1))
            return REG_INVALID_;

        else if (INS_OperandIsImmediate(ins, 1))
            return REG_INVALID_;

        else if (INS_OperandIsMemory(ins, 1))
            return INS_OperandMemoryBaseReg(ins, 1);

        else if (INS_OperandIsImplicit(ins, 1))
        {
            cout << " is implicit" << endl;
            return REG_INVALID_;
        }
        else if (INS_OperandIsFixedMemop(ins, 1))
        {
            cout << " is fixed mem op" << endl;
            return REG_INVALID_;
        }
        else if (INS_OperandIsBranchDisplacement(ins, 1))
        {
            cout << " is branch displacement" << endl;
            return REG_INVALID_;
        }

        else {
            cout << "unhanded 2 " << INS_Disassemble(ins) << endl;
            return REG_INVALID_;
        }
    }
    else if (INS_OperandCount(ins) == 3) {
        if (REG_StringShort(INS_OperandReg(ins, 2)) == "rflags")
        {
            if (INS_OperandIsReg(ins, 1))
                return REG_INVALID_;

            else if (INS_OperandIsImmediate(ins, 1))
                return REG_INVALID_;

            else if (INS_OperandIsMemory(ins, 1))
                return INS_OperandMemoryBaseReg(ins, 1);

            else if (INS_OperandIsImplicit(ins, 1))
            {
                cout << " is implicit" << endl;
                return REG_INVALID_;
            }
            else if (INS_OperandIsFixedMemop(ins, 1))
            {
                cout << " is fixed mem op" << endl;
                return REG_INVALID_;
            }
        else if (INS_OperandIsBranchDisplacement(ins, 1))
        {
            cout << " is branch displacement" << endl;
            return REG_INVALID_;
        }

            else {
                cout << "unhanded 3 " << INS_Disassemble(ins) << endl;
                return REG_INVALID_;
            }
        }
        else{
            cout << "unhanded 4 " << INS_Disassemble(ins) << endl;
            return REG_INVALID_;
        }
    }
    else
    {
        /*
        */
        cout << "unhanded 5 " << INS_Disassemble(ins) << endl;
        return REG_INVALID_;
    }
}


REG regInMemoryWrite(INS ins)
{
    if (INS_OperandCount(ins) == 1)
    {
        cout << "unhanded 1 " << INS_Disassemble(ins) << endl;
        return REG_INVALID_;
    }
    else if (INS_OperandCount(ins) == 2)
    {
        if (INS_OperandIsReg(ins, 0))
            return REG_INVALID_;

        else if (INS_OperandIsImmediate(ins, 0))
            return REG_INVALID_;

        else if (INS_OperandIsMemory(ins, 0))
            return INS_OperandMemoryBaseReg(ins, 0);

        else
        {
            cout << "unhanded 2 " << INS_Disassemble(ins) << endl;
            return REG_INVALID_;
        }
    }
    else if (INS_OperandCount(ins) == 3) {
        if (REG_StringShort(INS_OperandReg(ins, 2)) == "rflags")
        {
            if (INS_OperandIsReg(ins, 0))
                return REG_INVALID_;

            else if (INS_OperandIsImmediate(ins, 0))
                return REG_INVALID_;

            else if (INS_OperandIsMemory(ins, 0))
                return INS_OperandMemoryBaseReg(ins, 0);

            else {
                cout << "unhanded 3 " << INS_Disassemble(ins) << endl;
                return REG_INVALID_;
            }
        }
        else{
            cout << "unhanded 4 " << INS_Disassemble(ins) << endl;
            return REG_INVALID_;
        }
    }
    else
    {
        cout << "unhanded 5 " << INS_Disassemble(ins) << endl;
        return REG_INVALID_;
    }
}

bool fixMemRead(INS ins, ADDRINT faddr, CONTEXT *ctx)
{
    REG r = regInMemoryRead(ins);

    if (r == REG_INVALID_)
        return false;
    else
    {

        cout << "fix mem read function" << endl;

        fixErrorByReverseTaintAnalysis(ctx, r);
        return true;
    }
}

bool fixMemWrite(INS ins, ADDRINT faddr, CONTEXT *ctx)
{
    cout << "reg in memory write " << INS_Disassemble(ins) << hex << INS_Address(ins) << endl;
    REG r = regInMemoryWrite(ins);

    if (r == REG_INVALID_)
        return false;
    else
    {
        fixErrorByReverseTaintAnalysis(ctx, r);

        return true;
    }
}


bool fixMemReadNew(REG r, ADDRINT faddr, CONTEXT *ctx)
{
    if (r == REG_INVALID_)
    {
        return false;
    }
    else
    {
        cout << "fix mem read on " << REG_StringShort(r) << endl;

        fixErrorByReverseTaintAnalysis(ctx, r);
        return true;
    }
}

bool fixMemWriteNew(REG r, ADDRINT faddr, CONTEXT *ctx)
{
    if (r == REG_INVALID_)
        return false;
    else
    {
        cout << "fix mem write on " << REG_StringShort(r) << endl;

        fixErrorByReverseTaintAnalysis(ctx, r);
        return true;
    }
}

bool fixFPInstr(fpRecord fpr, CONTEXT *ctx)
{
    if (fpr.regFP == REG_INVALID_)
        return false;
    else
    {
        if (fpr.regFP == LEVEL_BASE::REG_RBP)
        {
            ADDRINT rv = PIN_GetContextReg(ctx, LEVEL_BASE::REG_RBP);
            ADDRINT des = rv + fpr.offset;
            *(reinterpret_cast<ADDRINT*>(des)) = valueForFP();

            return true;
        }
        else
        {
            PIN_SetContextReg(ctx, fpr.regFP, valueForFP());

            return true;
        }

    }
}



bool fixErrorByReverseTaintAnalysis(CONTEXT *ctx, LEVEL_BASE::REG r)
{

    cout << "fix error by reverse taint analysis" << endl;
    exec("rm ctx.info pin.trace");

    FILE * t = fopen("pin.trace", "w");
    list<std::string>::iterator i;

    for(i = instrTrace.begin(); i != instrTrace.end(); ++i)
        fprintf(t, "%s\n", (*i).c_str());

    fprintf(t, "#eof\n");
    fclose(t);


    t = fopen("ctx.trace", "w");
    list<CONTEXT>::iterator j;
    for(j = ctxTrace.begin(); j != ctxTrace.end(); ++j)
        dumpCTXTrace(&(*j), t);

    fprintf(t, "#eof\n");
    fclose(t);

    instrTrace.clear();
    ctxTrace.clear();


    t = fopen("ctx.info", "w");
    dump_crash_point(ctx, t, r);
    fprintf(t, "#eof\n");
    fclose(t);

    exec("cp ctx.info ~/work/project/fuzzing_1/src/scripts/reverse/");
    exec("cp ctx.trace ~/work/project/fuzzing_1/src/scripts/reverse/");
    exec("cp pin.trace ~/work/project/fuzzing_1/src/scripts/reverse/");

    exec("python adpater.py 1");

    char const * fn = "reverse.output";
    string sss = first_line_file(fn);
    cout << "[ROOT CAUSE] " << sss << endl;
    std::vector<std::string> elems;
    elems = split(sss, ':', elems);

    fix_addr = hexstr_to_int(elems[1]);
    fix_r = get_reg_from_str(elems[0]);

    inputMap[fix_addr] = fix_r;
    inputHasFixMap[fix_addr] = false;
    _resume = true;

    _start_resume = true;

    return false;
}
