#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class Mtt_branch(Module):
    def __init__(self,isMC=1):
        self.isMC=isMC
        self.counter = 0
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("TT_Mtt",            "F") 
        self.out.branch("TT_top_pt",         "F") 
        self.out.branch("TT_antitop_pt",     "F")    
        self.out.branch("TT_antitop_pt",     "F")
        self.out.branch("TT_truth",          "I")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        if self.isMC==1:
            genpart = Collection(event, "GenPart")
            tops = list(filter(lambda x : int(x.pdgId)==6, genpart))
            antitops = list(filter(lambda x : int(x.pdgId)==-6, genpart))
            n_tops = len(tops)
            n_antitops = len(antitops)
            #print("event is ",event.event)
            #print("n_tops = ",n_tops)
            #print("primo top is ",tops[0].pt)
            #print("secondo top is ",tops[1].pt)
            #print("n_antitops = ",n_antitops)
            #print("primo antitop is ",antitops[0].pt)
            #print("secondo antitop is ",antitops[1].pt)
            if n_tops!=0 and n_antitops!=0:
                top = ROOT.TLorentzVector()
                for t in tops:
                    if t.genPartIdxMother==0:
                        top.SetPtEtaPhiM(t.pt, t.eta, t.phi, t.mass)

                antitop = ROOT.TLorentzVector()
                for antit in antitops:
                    if antit.genPartIdxMother==0:
                        antitop.SetPtEtaPhiM(antit.pt, antit.eta, antit.phi, antit.mass)

                Mtt = (top+antitop).M()
                truth=1
                self.out.fillBranch("TT_Mtt", Mtt)
                self.out.fillBranch("TT_top_pt", top.Pt())
                self.out.fillBranch("TT_antitop_pt", antitop.Pt())

            else:
                truth=0
            self.out.fillBranch("TT_truth", truth)

        return True



