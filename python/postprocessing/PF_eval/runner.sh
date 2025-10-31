#!/usr/bin/bash 
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/PF_eval
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 PF_eval.py -dat $1 -final_name $2 -outname $3 -label $4
echo $3 ->files_names.txt 