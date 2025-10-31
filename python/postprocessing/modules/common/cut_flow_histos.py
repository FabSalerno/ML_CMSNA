from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
import json
from PhysicsTools.NanoAODTools.postprocessing.tools import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
import os

class cut_flow(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)

        path_to_model_folder    = "/eos/user/f/fsalerno/framework/MachineLearning/models/"
        mods                    = ["CNN_2D_old_truth","CNN_2D_LSTM_old_truth","CNN_2D_new_truth","CNN_2D_LSTM_new_truth","CNN_2D_2"]
        cuts                    = ["_0_pt"]
        n_PFCs                  = 60
        models                  = {}

        self.keys=[]
        for mod in mods:
            for cut in cuts:
                key=f"{n_PFCs}_{mod}{cut}"
                if os.path.isfile(f"{path_to_model_folder}/model_{key}.h5"):
                    self.keys.append(key)
        self.keys.append("TROTA")
        
        self.thr_keys =["10%","5%","1%","0.1%"]
        self.threshold = {}                
        for thresh in self.thr_keys:
            self.threshold[thresh] = {}
        for key in self.keys:    
            score_thresholds = f"/eos/user/f/fsalerno/framework/MachineLearning/thresholds/score_thresholds_{key}.json"                                          
            with open(score_thresholds, "r") as fjson:
                thresholds  = json.load(fjson)
                #print(f"thresholds: {thresholds}")
                #print(f"threshold: {threshold}")
                self.threshold["10%"][key]   = thresholds["10%"]["thr"]
                self.threshold["5%"][key]   = thresholds["5%"]["thr"]
                self.threshold["1%"][key]   = thresholds["1%"]["thr"]
                self.threshold["0.1%"][key]   = thresholds["0.1%"]["thr"]


        self.h_nevents_1_per_100 = {}
        self.h_nevents_1_per_1000 = {}
        self.h_nevents_5_per_100 = {}
        self.h_nevents_10_per_100 = {}

        self.h_nevents_no_score_cut = ROOT.TH1F(f"nevents_no_score_cut", f"nevents_no_score_cut", 1, 0, 1)
        for key in self.keys:
            self.h_nevents_10_per_100[key] = ROOT.TH1F(f"nevents_10_per_100_{key}", f"nevents_10_per_100_{key}", 1, 0, 1)
            self.h_nevents_5_per_100[key] = ROOT.TH1F(f"nevents_5_per_100_{key}", f"nevents_5_per_100_{key}", 1, 0, 1)
            self.h_nevents_1_per_100[key] = ROOT.TH1F(f"nevents_1_per_100_{key}", f"nevents_1_per_100_{key}", 1, 0, 1)
            self.h_nevents_1_per_1000[key] = ROOT.TH1F(f"nevents_1_per_1000_{key}", f"nevents_1_per_1000_{key}", 1, 0, 1)
            
        
        for key in self.keys:
            self.addObject(self.h_nevents_1_per_100[key])
            self.addObject(self.h_nevents_1_per_1000[key])
            self.addObject(self.h_nevents_5_per_100[key])
            self.addObject(self.h_nevents_10_per_100[key])
        
        self.addObject(self.h_nevents_no_score_cut)


    def analyze(self, event):
        """Process event, return True (go to next module) or False (fail, go to next event)"""
        tops_mixed = Collection(event, "TopMixed")
        
        for key in self.keys:  
            event_10_per_100 = 0
            event_5_per_100 = 0
            event_1_per_100 = 0
            event_1_per_1000 = 0
            #print("key",key)
            #print("10%",self.threshold["10%"][key],"5%",self.threshold["5%"][key],"1%",self.threshold["1%"][key],"0.1%",self.threshold["0.1%"][key])
            for top in tops_mixed:
                top_score_key = f"TopScore_{key}"
                if hasattr(top, top_score_key):
                    TopScore = getattr(top, top_score_key) 
                #print("TopScore",TopScore)

                if TopScore>= self.threshold["10%"][key]:
                    event_10_per_100 = 1

                if TopScore>= self.threshold["5%"][key]:
                    event_5_per_100 = 1

                if TopScore>= self.threshold["1%"][key]:
                    event_1_per_100 = 1

                if TopScore>= self.threshold["0.1%"][key]:
                    event_1_per_1000 = 1
                    #print("TopScore",TopScore)
            
            
            if event_10_per_100 == 1:
                self.h_nevents_10_per_100[key].Fill(0.5)

            if event_5_per_100 == 1:
                self.h_nevents_5_per_100[key].Fill(0.5)

            if event_1_per_100 == 1:
                self.h_nevents_1_per_100[key].Fill(0.5)

            if event_1_per_1000 == 1:
                self.h_nevents_1_per_1000[key].Fill(0.5)
            #print("integrale 1%", self.h_nevents_1_per_100[key].Integral())
        self.h_nevents_no_score_cut.Fill(0.5)
        #print("integrale no cut", self.h_nevents_no_score_cut.Integral())
        return True
    
#files = ["/eos/user/f/fsalerno/Data/PF/topevaluate/nano_mcRun3_WtoLNu_4Jets_MC2022_topeval_PF_presel_16000000_2.root"]
files = ["/eos/user/f/fsalerno/Data/PF/topevaluate/nano_mcRun3_TT_semilep_MC2022_topeval_PF_presel_100000_2.root"]
file_path="/eos/user/f/fsalerno/Evaluation/Prelim"
#p = PostProcessor(".", files, cut=None, branchsel=None, modules=[cut_flow()], noOut=True, histFileName=f"{file_path}/cut_flow_histos_presel_bkg.root", histDirName="cut_flow_bkg")
p = PostProcessor(".", files, cut=None, branchsel=None, modules=[cut_flow()], noOut=True, histFileName=f"{file_path}/cut_flow_histos_presel_sign.root", histDirName="cut_flow_sign")
p.run()