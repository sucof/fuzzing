//
//  BEGIN_LEGAL
//  Intel Open Source License
//
//  Copyright (c) 2002-2013 Intel Corporation. All rights reserved.
//
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//
//  Redistributions of source code must retain the above copyright notice,
//  this list of conditions and the following disclaimer.  Redistributions
//  in binary form must reproduce the above copyright notice, this list of
//  conditions and the following disclaimer in the documentation and/or
//  other materials provided with the distribution.  Neither the name of
//  the Intel Corporation nor the names of its contributors may be used to
//  endorse or promote products derived from this software without
//  specific prior written permission.
//
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
//  ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
//  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
//  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE INTEL OR
//  ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
//  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
//  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
//  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
//  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
//  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
//  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//  END_LEGAL
//
//  ------------------------------------------------------------------------
//
//

#include "pin.H"
#include <asm/unistd.h>
#include <csignal>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <list>
#include <unistd.h>
#include <map>
#include <boost/algorithm/string.hpp>

#include "mutation.h"
#include "instrutil.h"
#include "memutil.h"
#include "signal.h"
#include "utility.h"
#include "fuzzing.h"
#include "instrument.h"
#include "recorder.h"
#include "datadef.h"

VOID Fini(INT32 code, VOID *v)
{

    fprintf(trace, "#eof\n");
    fclose(trace);

    delete[] ptrHeap;


    cout << "[CRASH]" << endl;
    ADDRINT* dumpPtr = 0x0;
    *dumpPtr = 10;
}


int main(int argc, char *argv[])
{
    if(PIN_Init(argc, argv)){
        return Usage();
    }

    if (!KnobStart.Value() || !KnobEnd.Value())
      return Usage();



    fuzzValue = KnobStartValue.Value() - 1;

    initMemoryRegionRandom();

    PIN_SetSyntaxIntel();
    PIN_InterceptSignal(SIGSEGV, catchSignalSEGV, 0);
    PIN_InterceptSignal(SIGFPE, catchSignalFP, 0);
    INS_AddInstrumentFunction(Instruction, 0);

    PIN_AddFiniFunction(Fini, 0);
    PIN_StartProgram();

    return 0;
}
