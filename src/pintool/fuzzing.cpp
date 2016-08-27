void finishFuzzing(CONTEXT *ctx)
{
    std::cout << "[IN-MEMORY FUZZING STOPPED]" << std::endl;
    fprintf(trace,"MEMORY TRACING FINISHED\n");

    fuzzProcess = false;

    Fini(0, 0);

    return PIN_RemoveInstrumentation();
}

void resumeFromStart(CONTEXT *ctx)
{
    _resume = true;
    std::cout << "[RESTART FUZZING, RESTORE CONTEXT]" << std::endl;

    instrTrace.clear();

    typedef std::map<ADDRINT, bool>::iterator it_type;
    for(it_type iterator = inputHasFixMap.begin(); iterator != inputHasFixMap.end(); iterator++) {
        ADDRINT k = iterator->first;
	inputHasFixMap[k] = false;
    }

    PIN_SaveContext(&lastFuzzingCTX, ctx);
    restoreMemory();

    resetMemoryRegion();
    PIN_ExecuteAt(ctx);
}


void startFuzzing(CONTEXT *ctx, ADDRINT nextInsAddr, ADDRINT callNext)
{
    std::cout << "[START FUZZING, SAVE CONTEXT]" << std::endl;

    PIN_SaveContext(ctx, &snapshot);
    mutate_ctx(ctx);
    
    dumpCurrentContext(ctx, CONTEXT_FLG, "START");

    PIN_SetContextReg(ctx, LEVEL_BASE::REG_RIP, KnobStart.Value());

    typedef std::map<ADDRINT, bool>::iterator it_type;
    for(it_type iterator = inputHasFixMap.begin(); iterator != inputHasFixMap.end(); iterator++) {
        ADDRINT k = iterator->first;
	inputHasFixMap[k] = false;
    }
    
    PIN_SaveContext(ctx, &lastFuzzingCTX);
    _lock = UNLOCKED;
    resetMemoryRegion();
    instrTrace.clear();
    PIN_ExecuteAt(ctx);
}


void stopFuzzing(CONTEXT *ctx)
{
    _lock = LOCKED;
    std::cout << "[STOP FUZZING, RESTORE CONTEXT]" << std::endl;
    
    DumpHeapMemory();
    dumpCurrentContext(ctx, CONTEXT_FLG, "END");
    PIN_SaveContext(&snapshot, ctx);
    restoreMemory();

    PIN_ExecuteAt(ctx);
}
