#!/bin/env python3
import os
#dirpath="/eos/user/f/fsalerno/Data/PF/prova"
dirpath="/eos/user/f/fsalerno/Data/PF/topevaluate/to_hadd"
outputdir = "/eos/user/f/fsalerno/Data/PF/topevaluate"
#component="TTZprimetoTT_M_3000_W_4_MC2022"
#component="WtoLNu_4Jets_MC2022"
component="TT_semilep_MC2022"
files = []
for i,file in enumerate(os.listdir(dirpath)):
    if not file.startswith("./") and i<200:#and i<400 and os.path.isfile(os.path.join(dirpath, file))
        print(file)
        files.append(f"{dirpath}/{file}")
files_str = " ".join(files)
#print(files_str)
#Syntax: haddnano.py out.root input1.root input2.root ..."
os.system(f"python3 haddnano.py {outputdir}/nano_mcRun3_{component}_evaluate_presel.root {files_str}")
#os.system(f"rm {files_str}")
