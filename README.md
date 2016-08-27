# IMF-sim: function-level similarity analysis on binary executables

## Introduction

IMF-sim is designed to identify similar functions among binary executables through
in-memory fuzzing. 

This repo contains the code we wrote in this research, including the
implementation of IMF-sim, as well as scripts for experiments. You can also find the 
program binaries used for our evaluation in the repo.

### src/pintool

Our fuzzer is built as a plugin (i.e., PinTool) of Pin, a widely-used dynamic
instrumentation tool. This folder contains the source code of the PinTool for
in-memory fuzzing and feature generation. Please put this folder in the
directory of Pin tools, e.g.,

    ~/pin-gcc-linux/source/tools/

To build the PinTool, use the "build" script in this folder.

    ./build

Please remember to configure the path to the taint engine (introduced later).
They are at line 20 and line 23 of the adpater.py script.

### src/scripts/pinscripts

Our PinTool employs scripts in this folder for multiple tasks (e.g., feature
collection).

Please create a subfolder named "analysis" under the PinTool folder, then put
all the Python scripts into this subfolder.

### src/scripts/preprocess

Scripts in this folder manage the whole procedure, e.g., fuzzer configuration,
binary disassembling and longest common subsequence (LCS) computation.

To launch the whole analysis, please run the following command:

    python iterate_bin.py 
    
Test targets (binaries) can be configured in this script. It should be very
understandable by reading the code there.

### src/scripts/reverse

Our backward taint analysis engine. The preprocess scripts (e.g., lexer; parser)
are in this folder. The taint analysis engine code is in the subfolder
reverse/engine.

You should not need to do any configuration for this engine, but please remember
to configure the "adapter.py" code in the PinTool folder with the path of this
engine.


### src/scripts/analysis

This folder contains code for training and testing. After running the
"iterate_bin.py" script, you should find multiple dumped feature sequences
(i.e., fv.txt.basename.gccO0vsgccO3) in the "preprocess" folder. Move all of
them into this folder.

You may also need to modify line 15, line 132, and line 199 of script
"ensemble_binary.py" with the comparison information (e.g., gccO0vsgccO3).
Please take a look at the code there, it is very understandable.

Run the following command to launch the training + testing:

    python ensemble_binary.py

The comparison results will be printed out then.

### data
   Binary executables used in our evaluation. As introduced in our paper, we select 95 programs without destructive semantics.
   The 95 programs are listed in data/binlist.

## Dependence

   1. Pin 3.0-76991-gcc: http://software.intel.com/sites/landingpage/pintool/downloads/pin-3.0-76991-gcc-linux.tar.gz
   2. Z3: https://github.com/Z3Prover/z3
   3. Sklearn: http://scikit-learn.org/

## misc.

Please find more details in our submitted paper: "From Testing to Comparison: In-Memory Fuzzing for Binary Code Similarity Analysis".

This report contains the code we implemented for our work. However, the
current research-prototype may not be very handy to use (you need to configure
multiple stuff and interfaces are not very flexible). We will provide a web service of
our tool with a trained model once this paper is officially published.
