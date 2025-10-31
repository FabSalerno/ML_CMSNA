#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/for_git/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/crab/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 crab_script_PF.py -dirpath /eos/user/f/fsalerno/Data/PF -component TT_semilep_MC2022
