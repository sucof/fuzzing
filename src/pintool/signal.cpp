bool fixMemoryAccessError(ADDRINT exptaddr, FAULTY_ACCESS_TYPE ty, ADDRINT faddr, CONTEXT *ctx)
{
    instrRecord ir = getInstrByAddrOperand(exptaddr);

    if (ir.insDis == "dummy")
    {

        PIN_SetContextReg(ctx, LEVEL_BASE::REG_RIP, mra);

        return false;
    }
    else
    {
        LEVEL_BASE::OPCODE op = ir.op;

        if (isControlOP(op) == true)
        {
            PIN_SetContextReg(ctx, LEVEL_BASE::REG_RIP, ir.addrNext);

            return false;
        }
        else
        {
            bool mr = fixMemReadNew(ir.regRead, faddr, ctx);
            bool mw = fixMemWriteNew(ir.regWrite, faddr, ctx);

            if (mr == true && mw == false)
                return false;
            else if (mr == false && mw == true)
                return false;
            else if (mr == true && mw == true)
                return false;
            else
                return true;
        }
    }
}


bool analysisExcept(const EXCEPTION_INFO *pExceptInfo, CONTEXT *ctx)
{
    cout << "AnalysisHandler: Caught exception. " << PIN_ExceptionToString(pExceptInfo) << endl;

    if (PIN_GetExceptionCode(pExceptInfo) == EXCEPTCODE_ACCESS_INVALID_ADDRESS)
    {
        ADDRINT exptAddr = PIN_GetExceptionAddress(pExceptInfo);

        ADDRINT *faddr = new ADDRINT;
        PIN_GetFaultyAccessAddress(pExceptInfo, faddr);
        FAULTY_ACCESS_TYPE ty = PIN_GetFaultyAccessType(pExceptInfo);

        if (exptAddr != 0)
        {
            bool res = fixMemoryAccessError(exptAddr, ty, *faddr, ctx);
            delete faddr;
            return res;
        }
        else
        {
            delete faddr;
            return true;
        }
    }
    else if (PIN_GetExceptionCode(pExceptInfo) == EXCEPTCODE_PRIVILEGED_INS)
    {
        ADDRINT exptAddr = PIN_GetExceptionAddress(pExceptInfo);
        instrRecord ir = getInstrByAddrOperand(exptAddr);
        if (ir.insDis == "dummy")
        {
            PIN_SetContextReg(ctx, LEVEL_BASE::REG_RIP, mra);
            return false;
        }
        else
        {
            LEVEL_BASE::OPCODE op = ir.op;
            if (isControlOP(op) == true)
            {
                PIN_SetContextReg(ctx, LEVEL_BASE::REG_RIP, ir.addrNext);
                return false;
            }
            else
            {
                PIN_SetContextReg(ctx, LEVEL_BASE::REG_RIP, ir.addrNext);
                return false;
            }
        }
    }
    else
    {
        ADDRINT exptAddr = PIN_GetExceptionAddress(pExceptInfo);
        instrRecord ir = getInstrByAddrOperand(exptAddr);
        PIN_SetContextReg(ctx, LEVEL_BASE::REG_RIP, ir.addrNext);
        return false;
    }
}


BOOL catchSignalSEGV(THREADID tid, INT32 sig, CONTEXT *ctx, BOOL hasHandler, const EXCEPTION_INFO *pExceptInfo, VOID *v)
{
    if (fuzzProcess == true) {
        std::cout << std::endl << std::endl << "/!\\ SIGSEGV received /!\\" << std::endl;
        displayCurrentContext_Full(ctx, CONTEXT_FLG);

        return analysisExcept(pExceptInfo, ctx);
    }
    else {
        return true;
    }

}


bool fixFPError(ADDRINT exptaddr, CONTEXT *ctx)
{
    instrRecord ir = getInstrByAddrOperand(exptaddr);
    bool fp = fixFPInstr(ir.fpr, ctx);

    if (fp == true)
        return false;
    else
        return true;
}


bool analysisExceptFP(const EXCEPTION_INFO *pExceptInfo, CONTEXT *ctx)
{
    cout << "AnalysisHandlerFP: Caught exception. " << PIN_ExceptionToString(pExceptInfo) << endl;

    if (PIN_GetExceptionCode(pExceptInfo) == EXCEPTCODE_INT_DIVIDE_BY_ZERO)
    {
        ADDRINT exptAddr = PIN_GetExceptionAddress(pExceptInfo);

        if (exptAddr != 0)
        {
            bool res = fixFPError(exptAddr, ctx);
            return res;
        }
        else
        {
            cout << "undefined exception" << endl;
            return true;
        }
    }
    else
    {
        cout << "undefined exception" << endl;
        return true;
    }
}


BOOL catchSignalFP(THREADID tid, INT32 sig, CONTEXT *ctx, BOOL hasHandler, const EXCEPTION_INFO *pExceptInfo, VOID *v)
{
    if (fuzzProcess == true) {
        std::cout << std::endl << std::endl << "/!\\ SIGSEGV received /!\\" << std::endl;

        return analysisExceptFP(pExceptInfo, ctx);
    }
    else {
        return true;
    }
}
