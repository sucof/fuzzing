bool fixMemRead(INS ins, ADDRINT faddr, CONTEXT *ctx);
bool fixFPInstr(REG r, CONTEXT *ctx);
bool fixErrorByReverseTaintAnalysis(CONTEXT *ctx, LEVEL_BASE::REG r);
