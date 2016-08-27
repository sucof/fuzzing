void restoreMemory(void)
{
    list<struct memoryInput>::iterator i;

    for(i = memInput.begin(); i != memInput.end(); ++i){
        *(reinterpret_cast<ADDRINT*>(i->address)) = i->value;
    }
    memInput.clear();
}

bool checkPtrValid(ADDRINT ptr)
{
    if (ptr >= 0x7f0000000000)
        return true;
    else
    {
        return false;
    }
}

VOID WriteMemAll(ADDRINT insAddr, std::string insDis, ADDRINT memOp)
{
    struct memoryInput elem;
    if (checkPtrValid(memOp)) {
        ADDRINT addr = memOp;

        if (_lock == LOCKED)
            return;

        elem.address = addr;
        elem.value = *(reinterpret_cast<ADDRINT*>(addr));

        memInput.push_back(elem);
    }
    else
        return;
}


ADDRINT memAddrForRead()
{
    return (ADDRINT)ptrHeap + 20;
}


ADDRINT memAddrForWrite()
{
    return (ADDRINT)ptrHeap + 20;
}


UINT32 valueForFP()
{
    return 0xa;
}

ADDRINT randMEM(int len, ADDRINT i)
{
    return (rand() % (len)) * 8;
}

void initMemoryRegion()
{
    ptrHeap = new ADDRINT[1073];

    cout << "============= ptrHeap " << hex << ptrHeap << " ==========" << endl;
    ADDRINT i = 0;

    for (i = 0; i < 1073 - 1; i++)
    {
        ADDRINT t = (ADDRINT)ptrHeap + (i + 1)*8;
        *(ptrHeap+i) = t;
    }

    *(ptrHeap+i) = (ADDRINT)ptrHeap;

}

void resetMemoryRegion()
{
  cout << "[RESET MEMORY]" << endl;
  srand(0x232323);

  ADDRINT i = 0;
  for (i = 0; i < 1073; i++)
    {
      ADDRINT t = (ADDRINT)ptrHeap +  randMEM(1073, i);
      *(ptrHeap+i) = t;

      *(ptrHeapWrite+i) = 0;
    }

  ptrHeapReadList.clear();

  cout << "[RESET MEMORY FINISHED]" << endl;
}

void initMemoryRegionRandom()
{
    ptrHeap = new ADDRINT[1073];

    cout << "============= ptrHeap " << hex << ptrHeap << " ==========" << endl;
    ADDRINT i = 0;

    srand(0x232323);

    for (i = 0; i < 1073; i++)
      {
        ADDRINT t = (ADDRINT)ptrHeap +  randMEM(1073, i);
        *(ptrHeap+i) = t;
      }


    ptrHeapWrite = new ADDRINT[1073]();
  
    cout << "============= ptrHeapWrite " << hex << ptrHeapWrite << " ==========" << endl;

    offsetHeap = (long int)ptrHeapWrite - (long int)ptrHeap;

    rewrite_reg[0] = PIN_ClaimToolRegister();
    rewrite_reg[1] = PIN_ClaimToolRegister();
    rewrite_reg[2] = PIN_ClaimToolRegister();
}


bool inPtrheapRegion(ADDRINT ea)
{
  static ADDRINT end1 = (ADDRINT)ptrHeap + 1073 * sizeof(ADDRINT);
  static ADDRINT end2 = (ADDRINT)ptrHeapWrite + 1073 * sizeof(ADDRINT);

  if (ea >= (ADDRINT)ptrHeap && ea < end1)
    return true;

  else if (ea >= (ADDRINT)ptrHeapWrite && ea < end2)
    return true;

  else
    return false;
}


VOID RecordMemRead(VOID * ip, VOID * addr, CONTEXT *ctx)
{
  ADDRINT rsp = PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSP) - 128;
  if ((ADDRINT)addr >= code_e && (ADDRINT)addr < rsp && !(inPtrheapRegion((ADDRINT)addr)))
    fprintf(trace,"real heap r: %lu\n", *(ADDRINT*)addr);

  if ((ADDRINT)addr >= rodata_b && (ADDRINT) addr < rodata_e)
    fprintf(trace,"rodata r: %lu\n", (ADDRINT)addr-(ADDRINT)rodata_b);

  else if ((ADDRINT)addr >= data_b && (ADDRINT) addr < data_e)
    fprintf(trace,"data r: %lu\n", (ADDRINT)addr-(ADDRINT)data_b);

  else if ((ADDRINT)addr >= bss_b && (ADDRINT) addr < bss_e)
    fprintf(trace,"bss r: %lu\n", (ADDRINT)addr-(ADDRINT)bss_b);

  else if ((ADDRINT)addr >= gotplt_b && (ADDRINT) addr < gotplt_e)
    fprintf(trace,"gotplt r: %lu\n", (ADDRINT)addr-(ADDRINT)gotplt_b);

  return;
}


void UpdateMemRead(void * ip, void *addr)
{
  if (current_read_ptr != 0)
    {
      ADDRINT offset = (ADDRINT)current_read_ptr - (ADDRINT)ptrHeap;
      ptrHeapReadList.push_back(offset);

      current_read_ptr = 0;
    }
}


VOID RecordMemWrite(VOID * ip, VOID * addr, CONTEXT *ctx)
{

  if ((ADDRINT)addr >= rodata_b && (ADDRINT) addr < rodata_e)
    fprintf(trace,"rodata w: %lu\n", (ADDRINT)addr-(ADDRINT)rodata_b);

  else if ((ADDRINT)addr >= data_b && (ADDRINT) addr < data_e)
    fprintf(trace,"data w: %lu\n", (ADDRINT)addr-(ADDRINT)data_b);

  else if ((ADDRINT)addr >= bss_b && (ADDRINT) addr < bss_e)
    fprintf(trace,"bss w: %lu\n", (ADDRINT)addr-(ADDRINT)bss_b);

  else if ((ADDRINT)addr >= gotplt_b && (ADDRINT) addr < gotplt_e)
    fprintf(trace,"gotplt w: %lu\n", (ADDRINT)addr-(ADDRINT)gotplt_b);

  return;
}


void TranslateMemRead(ADDRINT ea)
{
  static ADDRINT end = (ADDRINT)ptrHeap + 1073 * sizeof(ADDRINT);
  if (ea >= (ADDRINT)ptrHeap && ea < end)
      current_read_ptr = ea;
}


static ADDRINT TranslateMemRef(ADDRINT ea)
{
  static ADDRINT end = (ADDRINT)ptrHeap + 1073 * sizeof(ADDRINT);
  if (ea >= (ADDRINT)ptrHeap && ea < end)
    {
      current_write_ptr = ea;

      return ea + offsetHeap;
    }
  else
    return ea;
}

void DumpHeapMemory()
{
  static int i;
  for (i = 0; i < 1073; i++)
    {
      if(*(ptrHeapWrite+i) != 0)
        {
          fprintf(trace,"heap w: %d %lu\n", i, *(ptrHeapWrite+i));
        }
    }

  list<ADDRINT>::iterator j;

  for(j = ptrHeapReadList.begin(); j != ptrHeapReadList.end(); ++j)
    {
      fprintf(trace,"heap r: %lu\n", *(j));
    }
}


VOID UpdateMem(VOID * ip, VOID * addr, CONTEXT *ctx)
{
  if (current_write_ptr != 0)
    {
      ADDRINT n = current_write_ptr + offsetHeap;
      memcpy((ADDRINT*)n, (ADDRINT*)current_write_ptr, sizeof(ADDRINT));

      current_write_ptr = 0;
    }

  ADDRINT rsp = PIN_GetContextReg(ctx, LEVEL_BASE::REG_RSP) - 128;
  if ((ADDRINT)addr >= code_e && (ADDRINT)addr < rsp && !(inPtrheapRegion((ADDRINT)addr)))
    fprintf(trace,"real heap w: %lu\n", *(ADDRINT*)addr);
}


void traceMemory(INS ins)
{
    UINT32 memOperands = INS_MemoryOperandCount(ins);
    ASSERTX(memOperands <= 3);

    for (UINT32 memOp = 0; memOp < memOperands; memOp++)
    {

        if (INS_MemoryOperandIsRead(ins, memOp))
        {
            INS_InsertPredicatedCall(
                ins, IPOINT_BEFORE, (AFUNPTR)RecordMemRead,
                IARG_INST_PTR,
                IARG_MEMORYOP_EA, memOp,
                IARG_CONTEXT,
                IARG_END);

            INS_InsertPredicatedCall(
                                     ins, IPOINT_BEFORE, (AFUNPTR)TranslateMemRead,
                                     IARG_MEMORYOP_EA, (ADDRINT)memOp,
                                     IARG_END);


            if (INS_HasFallThrough(ins))
              {
                INS_InsertPredicatedCall(
                                         ins, IPOINT_AFTER, (AFUNPTR)UpdateMemRead,
                                         IARG_INST_PTR,
                                         IARG_END);
              }
        }

        if (INS_MemoryOperandIsWritten(ins, memOp))
        {
          INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)TranslateMemRef,
                         IARG_MEMORYOP_EA, (ADDRINT)memOp,
                         IARG_RETURN_REGS, rewrite_reg[memOp],
                         IARG_END);

          INS_InsertPredicatedCall(ins, IPOINT_BEFORE, (AFUNPTR)RecordMemWrite,
                                   IARG_INST_PTR,
                                   IARG_MEMORYOP_EA, memOp,
                                   IARG_CONTEXT,
                                   IARG_END);

          if (INS_HasFallThrough(ins))
            {
              INS_InsertPredicatedCall(ins, IPOINT_AFTER, (AFUNPTR)UpdateMem,
                                       IARG_INST_PTR,
                                       IARG_MEMORYOP_EA, memOp,
                                       IARG_CONTEXT,
                                       IARG_END);
            }
        }
    }

    return;
}
