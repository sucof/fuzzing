void audit(ADDRINT insAddr, std::string insDis, CONTEXT *ctx)
{
      if (inputMap.find(insAddr) != inputMap.end() && inputHasFixMap[insAddr] == false)
        {
            cout << "[FOUND AUDIT TARGET]" << endl;
            LEVEL_BASE::REG cr = inputMap[insAddr];
            PIN_SetContextReg(ctx, cr, memAddrForRead());

	    inputHasFixMap[insAddr] = true;
            cout << "[FIX MEMORY ERROR] : " << hex << insAddr << " : " << insDis << endl;
            _resume = false;
            PIN_ExecuteAt(ctx);
        }
}

VOID resumeExecute(ADDRINT insAddr, std::string insDis, CONTEXT *ctx, ADDRINT nextInsAddr)
{
    if (_start_resume == true)
    {
        cout << "[RESUME EXECUTION] : " << hex << insAddr << insDis << endl;
        _start_resume = false;
        resumeFromStart(ctx);
    }
    else
        return;
}


VOID insCallBack(bool check, ADDRINT insAddr, std::string insDis, CONTEXT *ctx, ADDRINT nextInsAddr)
{
    resumeExecute(insAddr, insDis, ctx, nextInsAddr);

    if (_first == true)
    {
        _first = false;
        cout << "[INIT FUZZING ENV]" << endl;

        initExecutionFlow(ctx);
        return;
    }

    ADDRINT callNext = nextInsAddr;
    if (analyzed == false)
    {
        
        if (InCur == 0)
        {
            if (_resume == false)
            {
                
                if (insAddr == KnobStart.Value())
                {
                    if (parIndex >= sizeof(parList)/sizeof(UINT32))
                        
                        finishFuzzing(ctx);
                    else
                    {
                       
                        analyzed = true;
                        startFuzzing(ctx, nextInsAddr, callNext);
                    }
                }
            }
        }
    }
    else
        analyzed = false;


    if (_lock == LOCKED)
        return;

    
    audit(insAddr, insDis, ctx);

    std::cout << "+--> " << std::hex << insAddr << ": " << insDis << std::endl;
   

    std::stringstream out;
    out << insAddr;
    instrTrace.push_back(out.str() + ": " + insDis);
    ctxTrace.push_back(*ctx);

    if (insAddr >= KnobStart.Value() && insAddr <= KnobEnd.Value())
        mra = callNext;
}


VOID Instruction(INS ins, VOID *v)
{
    PIN_LockClient();
    IMG img = IMG_FindByAddress(INS_Address(ins));
    PIN_UnlockClient();

    bool check = INS_HasFallThrough(ins);
    if (IMG_Valid(img) && IMG_IsMainExecutable(img)){
        
        traceMemory(ins);

        recordInstrOperand(INS_Address(ins), ins);

        INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)insCallBack,
                       IARG_BOOL, check,
                       IARG_ADDRINT, INS_Address(ins),
                       IARG_PTR, new string(INS_Disassemble(ins)),
                       IARG_CONTEXT,
                       IARG_ADDRINT, INS_NextAddress(ins),
                       IARG_END);


           if (INS_MemoryOperandIsWritten(ins, 0)){
               INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)WriteMemAll,
                              IARG_ADDRINT, INS_Address(ins),
                              IARG_PTR, new string(INS_Disassemble(ins)),
                              IARG_MEMORYOP_EA, 0,
                              IARG_END);
           }


        if (INS_IsRet(ins)){
            INS_InsertCall(
                ins, IPOINT_BEFORE, (AFUNPTR)checkRet,
                IARG_ADDRINT, INS_Address(ins),
                IARG_PTR, new string(INS_Disassemble(ins)),
                IARG_CONTEXT,
                IARG_END);
        }

        if (INS_IsDirectBranchOrCall(ins) || INS_IsIndirectBranchOrCall(ins)){
            if(INS_IsCall(ins))
            {
                INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR) checkRecursive,
                               IARG_ADDRINT, INS_Address(ins),
                               IARG_BRANCH_TARGET_ADDR,
                               IARG_CONTEXT,
                               IARG_END);

                INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR) recordCall,
                               IARG_ADDRINT, INS_Address(ins),
                               IARG_BRANCH_TARGET_ADDR,
                               IARG_END);
            }
            else
            {
                INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR) checkJump,
                               IARG_ADDRINT, INS_Address(ins),
                               IARG_BRANCH_TARGET_ADDR,
                               IARG_CONTEXT,
                               IARG_END);
            }
        }

    }

    return;
}
