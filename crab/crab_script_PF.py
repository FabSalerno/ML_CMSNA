#!/usr/bin/env python3
import os

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

# this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.Mtt_cut_gen_lvl import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.deltaR_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MET_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection_PF import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp_PF import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2_PF_partonFlavour import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2_PF import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
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
parser                      = ArgumentParser()
parser.add_argument("-dirpath",                                 dest="dirpath",                                  default="/eos/user/f/fsalerno/Data/HOTVR/ttX_ntuplizer/tt_mtt-700to1000_MC2018_ntuplizer/",               required=False,         type=str,       help="path to file")
parser.add_argument("-component",                               dest="component",                                default="tt_mtt-700to1000_MC2018",                                                                        required=False,        type=str,       help="component considered")
parser.add_argument("-max_entries",                             dest="max_entries",                              default=100000,                                                                                             required=False,        type=int,       help="max entries")
options                     = parser.parse_args()

### ARGS ###
dirpath                        = options.dirpath
component                      = options.component
max_entries                    = options.max_entries


filepath=[f"{dirpath}/nano_mcRun3_{component}.root"]
### se voglio girare su files su tier (meglio getfiles_from_das)

#filepath=["root://cms-xrd-global.cern.ch//store/user/fsalerno/PFNano/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/TT_semilep_2022/250314_154005/0000/PFnano_mcRun3_TT_inclusive_1000_10.root"]
out_path = "/eos/user/f/fsalerno/Data/PF/prova/"
#histo_name = "histos_evaluation_PF_2022_1_jets_20_"+component+".root"
histo_dir = "histograms"

#### PER TOPEVAL###
p=PostProcessor(out_path, inputFiles=filepath, modules=[event_counter_pre(),preselection(),event_counter_post(),GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),GenPart_hadronicTop(), Idx_PF(), deltaR_PF(),collectionMerger(input=["PFCands"], output="PFCands", sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None), nanoprepro(isMC=1),nanoprepro_partonFlavour(isMC=1),nanoTopcand(isMC=1),nanoTopevaluate_MultiScore(),event_counter_5_100(),event_counter_1_100(),event_counter_1_1000()], friend=False, postfix=f"_topeval_PF_presel_{max_entries}", provenance=True, fwkJobReport=True, maxEntries=max_entries) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000

#####PER TOPEVAL FAST######preselection(),
#p=PostProcessor(out_path, inputFiles=filepath, modules=[nanoTopevaluate_MultiScore()], friend=False,postfix=f"_topcand_PF_{max_entries}", provenance=True, fwkJobReport=True, maxEntries=max_entries) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000


#####FULL PIPELINE######
#p=PostProcessor(out_path, inputFiles=filepath, modules=[event_counter_pre(),GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), GenPart_hadronicTop(), Idx_PF(), deltaR_PF(), collectionMerger(input=["PFCands"], output="PFCands", sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None), nanoprepro(isMC=1),nanoprepro_partonFlavour(isMC=1),nanoTopcand(isMC=1),nanoTopevaluate_MultiScore()], friend=False, postfix=f"_topeval_PF_presel_{component}_{max_entries}", provenance=True, fwkJobReport=True) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000

#####PER TOPCAND##########
#p=PostProcessor(out_path, inputFiles=filepath, modules=[GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),GenPart_hadronicTop(), Idx_PF(), deltaR_PF(),collectionMerger(input=["PFCands"], output="PFCands", sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None), nanoprepro(isMC=1),nanoprepro_partonFlavour(isMC=1),nanoTopcand(isMC=1)], friend=False, postfix=f"_topcand_PF_{max_entries}", provenance=True, fwkJobReport=True, maxEntries=max_entries) # histFileName=histo_name, histDirName=histo_dir maxEntries=10000

p.run()
print('DONE')
#/eos/user/f/fsalerno/Data/TT_Mtt-1000toInf.root