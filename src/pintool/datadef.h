
#define LOCKED        1
#define UNLOCKED      !LOCKED

#define CONTEXT_FLG   0
#define SIGSEGV_FLG   1

struct memoryInput
{
  ADDRINT address;
  UINT64  value;
};

struct regRef
{
  std::string       name;
  LEVEL_BASE::REG   ref;
};

static UINT32                   _lock = LOCKED;
static bool                     _first = true;
std::list<struct memoryInput>   memInput;
CONTEXT                         snapshot;
CONTEXT                         lastFuzzingCTX;
static UINT32                   InCur;
static bool                     analyzed = false;
static bool                     _resume = false;

static KNOB<ADDRINT> KnobStart(KNOB_MODE_WRITEONCE, "pintool", "start", "0", "The start address of the fuzzing area");
static KNOB<ADDRINT> KnobEnd(KNOB_MODE_WRITEONCE, "pintool", "end", "0", "The end address of the fuzzing area");

static KNOB<ADDRINT> KnobCodeStart(KNOB_MODE_WRITEONCE, "pintool", "codeStart", "0", "The start address of the code section");
static KNOB<ADDRINT> KnobCodeRange(KNOB_MODE_WRITEONCE, "pintool", "codeRange", "0", "The size of code section");
static KNOB<ADDRINT> KnobStartValue(KNOB_MODE_WRITEONCE, "pintool", "startValue", "0", "The start value");
static KNOB<UINT32> KnobFuzzCount(KNOB_MODE_WRITEONCE, "pintool", "fuzzingCount", "20", "The number of fuzzing iterations for each register");
static KNOB<ADDRINT> KnobRegNum(KNOB_MODE_WRITEONCE, "pintool", "regNum", "0x6", "how many input registers will be fuzzed");
static KNOB<string>  KnobFuzzType(KNOB_MODE_WRITEONCE, "pintool", "fuzzingType", "none", "Type of fuzzing: incremental, random or step");

static UINT64 fuzzValue;
static UINT32 fuzzCount;

static bool fuzzProcess = true;

enum FPOp
{
    FPInvalid,
    FPplus,
    FPminus
};

struct fpRecord
{
    LEVEL_BASE::REG   regFP;
    FPOp              op;
    INT64             offset;
};

struct instrRecord
{
    std::string        insDis;
    LEVEL_BASE::REG    regRead;
    LEVEL_BASE::REG    regWrite;
    fpRecord           fpr;
    LEVEL_BASE::OPCODE op;
    ADDRINT            addrNext;
};

struct instrRecord mri;
static ADDRINT mra;
static std::map<ADDRINT, INS> instrMap;
static std::map<ADDRINT, struct instrRecord> instrMapNew;

static std::map<ADDRINT, LEVEL_BASE::REG> inputMap;

static std::map<ADDRINT, bool> inputHasFixMap;

static UINT32 parList[] = {4, 5, 3, 2, 22, 23};
static UINT32 parIndex = 0;
static struct regRef regsRef[] =
{
  {"rax", LEVEL_BASE::REG_RAX},
  {"rbx", LEVEL_BASE::REG_RBX},
  {"rcx", LEVEL_BASE::REG_RCX}, // <--- arg4
  {"rdx", LEVEL_BASE::REG_RDX}, // <--- arg3
  {"rdi", LEVEL_BASE::REG_RDI}, // <--- arg1
  {"rsi", LEVEL_BASE::REG_RSI}, // <--- arg2
  {"eax", LEVEL_BASE::REG_EAX},
  {"ebx", LEVEL_BASE::REG_EBX},
  {"ecx", LEVEL_BASE::REG_ECX},
  {"edx", LEVEL_BASE::REG_EDX},
  {"edi", LEVEL_BASE::REG_EDI},
  {"esi", LEVEL_BASE::REG_ESI},
  {"ah",  LEVEL_BASE::REG_AH},
  {"bh",  LEVEL_BASE::REG_BH},
  {"ch",  LEVEL_BASE::REG_CH},
  {"dh",  LEVEL_BASE::REG_DH},
  {"al",  LEVEL_BASE::REG_AL},
  {"bl",  LEVEL_BASE::REG_BL},
  {"cl",  LEVEL_BASE::REG_CL},
  {"dl",  LEVEL_BASE::REG_DL},
  {"dil", LEVEL_BASE::REG_DIL},
  {"sil", LEVEL_BASE::REG_SIL},
  //  8 additional registers
  {"r8", LEVEL_BASE::REG_R8}, // <--- arg5
  {"r9", LEVEL_BASE::REG_R9}, // <--- arg6
  {"r10", LEVEL_BASE::REG_R10},
  {"r11", LEVEL_BASE::REG_R11},
  {"r12", LEVEL_BASE::REG_R12},
  {"r13", LEVEL_BASE::REG_R13},
  {"r14", LEVEL_BASE::REG_R14},
  {"r15", LEVEL_BASE::REG_R15},
  {"",    REG_INVALID()}
};


static REG intputRegsRef[] =
{
    LEVEL_BASE::REG_RDI, // <--- arg1
    LEVEL_BASE::REG_RSI, // <--- arg2
    LEVEL_BASE::REG_RDX, // <--- arg3
    LEVEL_BASE::REG_RCX, // <--- arg4
    LEVEL_BASE::REG_R8, // <--- arg5
    LEVEL_BASE::REG_R9, // <--- arg6
};

static UINT64* fuzzing_context[60] =
  {
    (UINT64 []){0xb120, 0xb130, 0xb1a0, 0xb1b0, 0xb3ba, 0xa3aa},
    (UINT64 []){0xa3ba, 0xa32a, 0xa33a, 0xa130, 0xb120, 0xb920},
    (UINT64 []){0xb9b0, 0xb9a0, 0xbbaa, 0xabba, 0xa3ba, 0xbfba},
    (UINT64 []){0xbfaa, 0xbda0, 0xadb0, 0xa5b0, 0xb9b0, 0xb930},
    (UINT64 []){0xbb3a, 0xab2a, 0xa32a, 0xbf2a, 0xbfaa, 0x373b},
    (UINT64 []){0x272b, 0x2f2b, 0x332b, 0x33ab, 0xbb3a, 0xb746},
    (UINT64 []){0xbf46, 0xa346, 0xa3c6, 0x2b57, 0x272b, 0x266b},
    (UINT64 []){0x3a6b, 0x3aeb, 0xb27a, 0xbe06, 0xbf46, 0xbf56},
    (UINT64 []){0xbfd6, 0x3747, 0x3b3b, 0x3a7b, 0x3a6b, 0xfa6b},
    (UINT64 []){0x72fa, 0x7e86, 0x7fc6, 0x7fd6, 0xbfd6, 0x5cc6},
    (UINT64 []){0x50ba, 0x51fa, 0x51ea, 0x91ea, 0x72fa, 0x76fa},
    (UINT64 []){0x77ba, 0x77aa, 0xb7aa, 0x54ba, 0x50ba, 0x57fa},
    (UINT64 []){0x57ea, 0x97ea, 0x74fa, 0x70fa, 0x77ba, 0xb3ba},
    (UINT64 []){0x73ba, 0x90aa, 0x94aa, 0x93ea, 0x57ea, 0xd7aa},
    (UINT64 []){0x34ba, 0x30ba, 0x37fa, 0xf3fa, 0x73ba, 0x3bba},
    (UINT64 []){0x3fba, 0x38fa, 0xfcfa, 0x7cba, 0x34ba, 0x113e},
    (UINT64 []){0x167e, 0xd27e, 0x523e, 0x1a3e, 0x3fba, 0x3fba},
    (UINT64 []){0xfbba, 0x7bfa, 0x33fa, 0x167e, 0x167e, 0x323e},
    (UINT64 []){0xb27e, 0xfa7e, 0xdffa, 0xdffa, 0xfbba, 0xebb8},
    (UINT64 []){0xa3b8, 0x863c, 0x863c, 0xa27c, 0xb27e, 0xf47c},
    (UINT64 []){0xd1f8, 0xd1f8, 0xf5b8, 0xe5ba, 0xa3b8, 0xe698},
    (UINT64 []){0xe698, 0xc2d8, 0xd2da, 0x94d8, 0xd1f8, 0xd3b8},
    (UINT64 []){0xf7f8, 0xe7fa, 0xa1f8, 0xe4d8, 0xe698, 0xe688},
    (UINT64 []){0xf68a, 0xb088, 0xf5a8, 0xf7e8, 0xf7f8, 0xf7f8},
    (UINT64 []){0xb1fa, 0xf4da, 0xf69a, 0xf68a, 0xf68a, 0xfe86},
    (UINT64 []){0xbba6, 0xb9e6, 0xb9f6, 0xb9f6, 0xb1fa, 0xb1e8},
    (UINT64 []){0xb3a8, 0xb3b8, 0xb3b8, 0xbbb4, 0xbba6, 0xef26},
    (UINT64 []){0xef36, 0xef36, 0xe73a, 0xe728, 0xb3a8, 0xb7a0},
    (UINT64 []){0xb7a0, 0xbfac, 0xbfbe, 0xeb3e, 0xef36, 0xef3e},
    (UINT64 []){0xe732, 0xe720, 0xb3a0, 0xb7a8, 0xb7a0, 0xb7b0},
    (UINT64 []){0xb7a2, 0xe322, 0xe72a, 0xe722, 0xe732, 0xe752},
    (UINT64 []){0xb3d2, 0xb7da, 0xb7d2, 0xb7c2, 0xb7a2, 0xb5b2},
    (UINT64 []){0xb1ba, 0xb1b2, 0xb1a2, 0xb1c2, 0xb3d2, 0xbb74},
    (UINT64 []){0xbb7c, 0xbb6c, 0xbb0c, 0xb91c, 0xb1ba, 0xb9fa},
    (UINT64 []){0xb9ea, 0xb98a, 0xbb9a, 0xb33c, 0xbb7c, 0xbb6c},
    (UINT64 []){0xbb0c, 0xb91c, 0xb1ba, 0xb9fa, 0xb9ea, 0xbae2},
    (UINT64 []){0xb8f2, 0xb054, 0xb814, 0xb804, 0xbb0c, 0x3b5c},
    (UINT64 []){0x33fa, 0x3bba, 0x3baa, 0x38a2, 0xb8f2, 0xbcf2},
    (UINT64 []){0xb4b2, 0xb4a2, 0xb7aa, 0x37fa, 0x33fa, 0x93aa},
    (UINT64 []){0x93ba, 0x90b2, 0x10e2, 0x14e2, 0xb4b2, 0xb432},
    (UINT64 []){0xb73a, 0x376a, 0x336a, 0x933a, 0x93ba, 0x51b2},
    (UINT64 []){0xd1e2, 0xd5e2, 0x75b2, 0x7532, 0xb73a, 0xf33b},
    (UINT64 []){0xf73b, 0x576b, 0x57eb, 0x95e3, 0xd1e2, 0xf1c2},
    (UINT64 []){0x5192, 0x5112, 0x931a, 0xd71b, 0xf73b, 0xf633},
    (UINT64 []){0xf6b3, 0x34bb, 0x70ba, 0x509a, 0x5192, 0x089a},
    (UINT64 []){0xca92, 0x8e93, 0xaeb3, 0xafbb, 0xf6b3, 0xd6b7},
    (UINT64 []){0x92b6, 0xb296, 0xb39e, 0xea96, 0xca92, 0x2a92},
    (UINT64 []){0x0ab2, 0x0bba, 0x52b2, 0x72b6, 0x92b6, 0x9a96},
    (UINT64 []){0x9b9e, 0xc296, 0xe292, 0x0292, 0x0ab2, 0x5ab2},
    (UINT64 []){0x03ba, 0x23be, 0xc3be, 0xcb9e, 0x9b9e, 0x998e},
    (UINT64 []){0xb98a, 0x598a, 0x51aa, 0x01aa, 0x03ba, 0x0bb2},
    (UINT64 []){0xebb2, 0xe392, 0xb392, 0xb182, 0xb98a, 0xba8b},
    (UINT64 []){0xb2ab, 0xe2ab, 0xe0bb, 0xe8b3, 0xebb2, 0x0bb2},
    (UINT64 []){0x5bb2, 0x59a2, 0x51aa, 0x52ab, 0xb2ab, 0x5a32},
    (UINT64 []){0x5822, 0x502a, 0x532b, 0xb32b, 0x5bb2, 0x5da2},
    (UINT64 []){0x55aa, 0x56ab, 0xb6ab, 0x5e32, 0x5822, 0x5827},
    (UINT64 []){0x5b26, 0xbb26, 0x53bf, 0x55af, 0x55aa, 0x25ba},
    (UINT64 []){0xc5ba, 0x2d23, 0x2b33, 0x2b36, 0x5b26, 0x5b27},
    (UINT64 []){0xb3be, 0xb5ae, 0xb5ab, 0xc5bb, 0xc5ba, 0x452a},
    (UINT64 []){0x433a, 0x433f, 0x332f, 0x332e, 0xb3be, 0x33ae}
  };

static FILE * trace;

static ADDRINT* ptrHeap;

static ADDRINT* ptrHeapWrite;

std::list<ADDRINT>  ptrHeapReadList;

REG rewrite_reg[3];

static long int offsetHeap;
static ADDRINT current_write_ptr = 0;
static ADDRINT current_read_ptr = 0;
std::list<std::string>  instrTrace;
std::list<CONTEXT>  ctxTrace;

static ADDRINT fix_addr;

static LEVEL_BASE::REG fix_r;

static bool _start_resume = false;

static ADDRINT rodata_b = 0;
static ADDRINT rodata_e = 0;
static ADDRINT gotplt_b = 0;
static ADDRINT gotplt_e = 0;
static ADDRINT data_b = 0;
static ADDRINT data_e = 0;
static ADDRINT bss_b = 0;
static ADDRINT bss_e = 0;

static ADDRINT code_b = 0;
static ADDRINT code_e = 0;
