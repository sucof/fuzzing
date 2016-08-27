VOID displayCurrentContext(CONTEXT *ctx, UINT32 flag);

INT32 Usage();

void initExecutionFlow(CONTEXT *ctx);

VOID checkRet(UINT64 insAddr, std::string insDis, CONTEXT *ctx);

VOID checkJump(UINT64 insAddr, ADDRINT dst, CONTEXT *ctx);

VOID checkRecursive(ADDRINT dst, ADDRINT insAddr, CONTEXT *ctx);

ADDRINT getNextAddr(std::string insDis);

std::string exec(const char* cmd);

VOID dump_crash_point(CONTEXT *ctx, FILE *t, LEVEL_BASE::REG r);

std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems);

ADDRINT hexstr_to_int(string s);

LEVEL_BASE::REG get_reg_from_str(string s);

std::string first_line_file(char const * fn);

VOID dumpCTXTrace(CONTEXT *ctx, FILE *t);
