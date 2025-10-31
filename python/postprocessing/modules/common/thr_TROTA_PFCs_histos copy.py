#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
from PhysicsTools.NanoAODTools.postprocessing.tools import *
ROOT.PyConfig.IgnoreCommandLineOptions = True


class thr_TROTA_PFCs(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        self.keys=[]
        self.score_CNN_2D_new_truth = ROOT.TH1F('score_CNN_2D_new_truth', 'score_CNN_2D_new_truth', 1000, 0, 1)
        self.score_CNN_2D_LSTM_new_truth = ROOT.TH1F('score_CNN_2D_LSTM_new_truth', 'score_CNN_2D_LSTM_new_truth', 1000, 0, 1)
        self.score_CNN_2D_old_truth = ROOT.TH1F('score_CNN_2D_old_truth', 'score_CNN_2D_old_truth', 1000, 0, 1)
        self.score_CNN_2D_LSTM_old_truth = ROOT.TH1F('score_CNN_2D_LSTM_old_truth', 'score_CNN_2D_LSTM_old_truth', 1000, 0, 1)
        self.ntop = ROOT.TH1F('ntop', 'ntop', 3, 0, 3)
        self.addObject(self.score_CNN_2D_new_truth)
        self.addObject(self.score_CNN_2D_LSTM_new_truth)
        self.addObject(self.score_CNN_2D_old_truth)
        self.addObject(self.score_CNN_2D_LSTM_old_truth)
        self.addObject(self.ntop)

    def analyze(self, event):
        tops_mixed = Collection(event,"TopMixed") 
        ntopmixed = len(tops_mixed)
        #nessuna pLSTMel su top_mixed
        for top in tops_mixed:
            #print("TopMixed")
            #print("TopScore_60_CNN_2D_new_truth_0_pt",top.TopScore_60_CNN_2D_new_truth_0_pt)
            self.score_CNN_2D_new_truth.Fill(top.TopScore_60_CNN_2D_new_truth_0_pt)
            self.score_CNN_2D_LSTM_new_truth.Fill(top.TopScore_60_CNN_2D_LSTM_new_truth_0_pt)
            self.score_CNN_2D_old_truth.Fill(top.TopScore_60_CNN_2D_old_truth_0_pt)
            self.score_CNN_2D_LSTM_old_truth.Fill(top.TopScore_60_CNN_2D_LSTM_old_truth_0_pt)
            #self.score_CNN_2D_new_truth.Fill(top.particleNet_TvsQCD)
            #self.score_CNN_2D_LSTM_new_truth.Fill(top.particleNet_TvsQCD)
            self.ntop.Fill(1)
        #print(self.score_CNN_2D_new_truth.Integral())
        return True

files=[f"/eos/user/f/fsalerno/Data/PF/topevaluate/nano_mcRun3_WtoLNu_4Jets_MC2022_topeval_PF_presel_16000000.root"]
file_path="/eos/user/f/fsalerno/Evaluation/thr_estimate"
#files = [" root://cms-xrd-global.cern.ch//store/mc/Run3Summer22NanoAODv11/QCD-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/NANOAODSIM/126X_mcRun3_2022_realistic_v2-v2/2810000/0121789a-f0e9-46fb-9cb5-e489a0a4db8b.root"]
p = PostProcessor(".", files, cut=None, branchsel=None, modules=[
                  thr_TROTA_PFCs()], noOut=True, histFileName=f"{file_path}/fpr_TROTA_PF_wjets.root", histDirName=f"fpr")
p.run()

