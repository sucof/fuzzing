VOID displayCurrentContext_Full(CONTEXT *ctx, UINT32 flag)
{
  std::cout << "[" << (flag == CONTEXT_FLG ? "CONTEXT" : "SIGSGV")
    << "]=----------------------------------------------------------" << std::endl;
  std::cout << std::hex << std::internal << std::setfill('0')
    << "RAX = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RAX) << " "
    << "RBX = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RBX) << " "
    << "RCX = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RCX) << std::endl
    << "RDX = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RDX) << " "
    << "RDI = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RDI) << " "
    << "RSI = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSI) << std::endl
    << "RBP = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RBP) << " "
    << "RSP = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSP) << " "
    << "R8 = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_R8) << std::endl
    << "R9 = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_R9) << " "
    << "R10 = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_R10) << " "
    << "R11 = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_R11) << std::endl
    << "R12 = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_R12) << " "
    << "R13 = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_R13) << " "
    << "R14 = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_R14) << std::endl
    << "R15 = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_R15) << " "
    << "RIP = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RIP) << std::endl;
  std::cout << "+-------------------------------------------------------------------" << std::endl;
}


VOID displayCurrentContext(CONTEXT *ctx, UINT32 flag)
{
    std::cout << "[" << (flag == CONTEXT_FLG ? "CONTEXT" : "SIGSGV")
    << "]=----------------------------------------------------------" << std::endl;
    std::cout << std::hex << std::internal << std::setfill('0')
    << "RAX = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RAX) << " "
    << "RBX = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RBX) << " "
    << "RCX = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RCX) << std::endl
    << "RDX = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RDX) << " "
    << "RDI = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RDI) << " "
    << "RSI = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSI) << std::endl
    << "RBP = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RBP) << " "
    << "RSP = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSP) << " "
    << "RIP = " << std::setw(16) << PIN_GetContextReg(ctx, LEVEL_BASE::REG_RIP) << std::endl;
  std::cout << "+-------------------------------------------------------------------" << std::endl;
}

VOID dumpCurrentContext(CONTEXT *ctx, UINT32 flag, string prefix)
{
    fprintf(trace, "========================%s=====================\n", prefix.c_str());
    fprintf(trace, "RAX = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RAX));
    fprintf(trace, "RBX = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RBX));
    fprintf(trace, "RDI = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RDI));
    fprintf(trace, "RSI = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSI));
    fprintf(trace, "RDX = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RDX));
    fprintf(trace, "RCX = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RCX));
    fprintf(trace, "RBP = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RBP));
    fprintf(trace, "RSP = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSP));
    fprintf(trace, "R8 = %lu\n",  PIN_GetContextReg(ctx, LEVEL_BASE::REG_R8));
    fprintf(trace, "R9 = %lu\n",  PIN_GetContextReg(ctx, LEVEL_BASE::REG_R9));
    fprintf(trace, "======================================================\n");
}


VOID dumpCTXTrace(CONTEXT *ctx, FILE *t)
{
    fprintf(t, "========================START:%lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RIP));
    fprintf(t, "RAX = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RAX));
    fprintf(t, "RBX = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RBX));
    fprintf(t, "RDI = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RDI));
    fprintf(t, "RSI = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSI));
    fprintf(t, "RDX = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RDX));
    fprintf(t, "RCX = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RCX));
    fprintf(t, "RBP = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RBP));
    fprintf(t, "RSP = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSP));
    fprintf(t, "R8 = %lu\n",  PIN_GetContextReg(ctx, LEVEL_BASE::REG_R8));
    fprintf(t, "R9 = %lu\n",  PIN_GetContextReg(ctx, LEVEL_BASE::REG_R9));
    fprintf(t, "========================END============================\n");
}


VOID dump_crash_point(CONTEXT *ctx, FILE *t, LEVEL_BASE::REG r)
{
    fprintf(t, "========================START=====================\n");
    fprintf(t, "RAX = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RAX));
    fprintf(t, "RBX = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RBX));
    fprintf(t, "RDI = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RDI));
    fprintf(t, "RSI = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSI));
    fprintf(t, "RDX = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RDX));
    fprintf(t, "RCX = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RCX));
    fprintf(t, "RBP = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RBP));
    fprintf(t, "RSP = %lu\n", PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSP));
    fprintf(t, "R8 = %lu\n",  PIN_GetContextReg(ctx, LEVEL_BASE::REG_R8));
    fprintf(t, "R9 = %lu\n",  PIN_GetContextReg(ctx, LEVEL_BASE::REG_R9));
    fprintf(t, "taint=%s\n", REG_StringShort(r).c_str());
    fprintf(t, "========================END============================\n");
}


INT32 Usage()
{
    std::cerr << "In-Memory Fuzzing tool to capture input-output relation" << std::endl;
    cerr << endl << KNOB_BASE::StringKnobSummary() << endl;
    return -1;
}


std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}


std::string first_line_file(char const * fn)
{
    string sLine;
    ifstream infile(fn);

    if (infile.good())
        getline(infile, sLine);

    infile.close();
    return sLine;
}


ADDRINT hexstr_to_int(string s)
{
    ADDRINT x;
    std::stringstream ss;
    ss << s;
    ss >> x;

    return x;
}


LEVEL_BASE::REG get_reg_from_str(string s)
{
    if (strcmp(s.c_str(), "rdi") == 0)
        return LEVEL_BASE::REG_RDI;
    else if (strcmp(s.c_str(), "rsi") == 0)
        return LEVEL_BASE::REG_RSI;
    else if (strcmp(s.c_str(), "rdx") == 0)
        return LEVEL_BASE::REG_RDX;
    else if (strcmp(s.c_str(), "rcx") == 0)
        return LEVEL_BASE::REG_RCX;
    else if (strcmp(s.c_str(), "r8") == 0)
        return LEVEL_BASE::REG_R8;
    else if (strcmp(s.c_str(), "r9") == 0)
        return LEVEL_BASE::REG_R9;
    else
        return LEVEL_BASE::REG_INVALID_;

}


void initRegBeforeFuzzing(CONTEXT *ctx)
{
  	PIN_SetContextReg(ctx, LEVEL_BASE::REG_RIP, KnobStart.Value());

  	PIN_SetContextReg(ctx, LEVEL_BASE::REG_RDI, 0);
  	PIN_SetContextReg(ctx, LEVEL_BASE::REG_RSI, 0);
  	PIN_SetContextReg(ctx, LEVEL_BASE::REG_RDX, 0);
  	PIN_SetContextReg(ctx, LEVEL_BASE::REG_RCX, 0);
  	PIN_SetContextReg(ctx, LEVEL_BASE::REG_R8, 0);
  	PIN_SetContextReg(ctx, LEVEL_BASE::REG_R9, 0);

  	PIN_SetContextReg(ctx, LEVEL_BASE::REG_RAX, 0);

}


std::string exec(const char* cmd)
{
    FILE* pipe = popen(cmd, "r");
    if (!pipe) return "ERROR";
    char buffer[128];
    std::string result = "";
    while (!feof(pipe)) {
        if (fgets(buffer, 128, pipe) != NULL)
            result += buffer;
    }
    pclose(pipe);
    return result;
}


void dataRange()
{
  char const * fn = "data_section.info";
  string sss = first_line_file(fn);
  std::vector<std::string> elems;
  elems = split(sss, ',', elems);

  rodata_b = hexstr_to_int(elems[0]);
  rodata_e = hexstr_to_int(elems[1]);

  gotplt_b = hexstr_to_int(elems[2]);
  gotplt_e = hexstr_to_int(elems[3]);

  data_b = hexstr_to_int(elems[4]);
  data_e = hexstr_to_int(elems[5]);

  bss_b = hexstr_to_int(elems[6]);
  bss_e = hexstr_to_int(elems[7]);

  return;
}


void codeRange()
{
  string a = "python analysis/codesection.py ";
  char* x = new char[a.length() + 4];

  sprintf(x, "%s %d", a.c_str(), PIN_GetPid());
  string rr = exec(x);


  std::vector<std::string> elems;
  elems = split(rr, '-', elems);
  code_b = hexstr_to_int(elems[0]);
  code_e = hexstr_to_int(elems[1]);

  return;
}


void initExecutionFlow(CONTEXT *ctx)
{
    restoreMemory();
    
    initRegBeforeFuzzing(ctx);
    initRecorder();
    dataRange();

    codeRange();

    
    trace = fopen("pinatrace.out", "w");

   
    PIN_ExecuteAt(ctx);
    return;
}


void startOneExecution(CONTEXT *ctx)
{
    if (parIndex >= KnobRegNum.Value())
    {
        cout << "[Finish Execution in Exception Handling]" << endl;
        
        return;
    }
    else
    {
        std::cout << "[Restore Context in Exception Handling]" << std::endl;
        displayCurrentContext(ctx, CONTEXT_FLG);
        PIN_SaveContext(&snapshot, ctx);
        restoreMemory();

        parIndex++;
        
        PIN_SetContextReg(ctx, LEVEL_BASE::REG_RIP, 0);
        PIN_ExecuteAt(ctx);

        return;
    }
}


VOID checkRet(UINT64 insAddr, std::string insDis, CONTEXT *ctx)
{
    if (insAddr >= KnobStart.Value() && insAddr <= KnobEnd.Value())
    {
        if(InCur == 0)
        {
            stopFuzzing(ctx);
        }
        else
        {
            InCur--;
        }
    }
}


VOID checkJump(UINT64 insAddr, ADDRINT dst, CONTEXT *ctx)
{

    if (insAddr >= KnobStart.Value() && insAddr <= KnobEnd.Value())
    {
        if (dst < KnobStart.Value() || dst > KnobEnd.Value())
        {
          if (dst >= KnobCodeStart.Value() && dst <= (KnobCodeRange.Value() + KnobCodeStart.Value()))
            stopFuzzing(ctx);
        }
    }
}


VOID checkRecursive(ADDRINT dst, ADDRINT insAddr, CONTEXT *ctx)
{

    ADDRINT funcBegin = KnobStart.Value();
    ADDRINT funcEnd = KnobEnd.Value();

    if (dst >= funcBegin && dst <= funcEnd && insAddr >= funcBegin && insAddr <= funcEnd)
    {
        
        InCur++;
    }
}


ADDRINT getNextAddr(std::string insDis)
{
    ADDRINT nextInsAddr = 0;

    if (insDis.find("call") != std::string::npos)
    {
       
        std::vector<std::string> strs;
        boost::split(strs, insDis, boost::is_any_of("\t "));
        std::stringstream ss;
        ss << std::hex << strs[1];
        ss >> nextInsAddr;
    }
    else if (insDis.find("jmp") != std::string::npos)
    {
        
        std::vector<std::string> strs;
        boost::split(strs, insDis, boost::is_any_of("\t "));
        std::stringstream ss;
        ss << std::hex << strs[1];
        ss >> nextInsAddr;
    }
    else
    {
        nextInsAddr = -1;
    }

    return nextInsAddr;
}
