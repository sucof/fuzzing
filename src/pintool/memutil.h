VOID restoreMemory(void);
VOID WriteMemAll(ADDRINT insAddr, std::string insDis, ADDRINT memOp);
ADDRINT memAddrForRead();
ADDRINT memAddrForWrite();
void initMemoryRegion();
void initMemoryRegionRandom();
void traceMemory(ADDRINT addr);
UINT32 valueForFP();
