#!/usr/bin/env python3
import os

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

# this takes care of converting the input files from CRAB
#from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.Mtt_cut_gen_lvl import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.deltaR_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MET_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection_PF import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2_PF_partonFlavour import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2_PF import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.score_selection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.test_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.Idx_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.histos_eval_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_pre_presel_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_post_presel_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_5_per_100_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_1_per_100_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.event_counter_1_per_1000_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_hadronicTop import*
from PhysicsTools.NanoAODTools.postprocessing.modules.common.pt_cut_top_gen_lvl import*
from PhysicsTools.NanoAODTools.postprocessing.modules.common.truth_comparer import*
from PhysicsTools.NanoAODTools.postprocessing.modules.common.Mtt_branch import *
'''
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
'''


from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-dat",            dest="dat",         default="/path/to/default/data", required=False, type=str, help="path to input data")
parser.add_argument("-final_name",     dest="final_name",  default="final_output",          required=False, type=str, help="final name for processing")
parser.add_argument("-outname",        dest="outname",     default="output_file.root",      required=False, type=str, help="name of the output file")
parser.add_argument("-label",          dest="label",       default="default_label",         required=False, type=str, help="label for plots or outputs")

options = parser.parse_args()

### ARGS ###
dat         = options.dat
final_name  = options.final_name
outname     = options.outname
label       = options.label
#filepath=[f"{dirpath}/nano_mcRun3_{component}.root"]
#filepath=["/eos/user/f/fsalerno/Data/PF/topevaluate/nano_mcRun3_WtoLNu_4Jets_MC2022_topeval_PF_presel_16000000.root"]
filepath=[dat]
histo_dir = "n_events"
dirpath = "/eos/user/f/fsalerno/Data/PF/topevaluate/to_hadd"
#####FULL PIPELINE######
p=PostProcessor(dirpath, inputFiles=filepath, modules=[event_counter_pre(),preselection(),GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),GenPart_hadronicTop(), Idx_PF(), deltaR_PF(),collectionMerger(input=["PFCands"], output="PFCands", sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None), nanoprepro(isMC=1),nanoTopcand(isMC=1),nanoTopevaluate_MultiScore()], friend=False, postfix="", provenance=True, fwkJobReport=True, outputbranchsel='keep_and_drop.txt') # histFileName=histo_name, histDirName=histo_dir maxEntries=10000
p.run()
print('DONE')

