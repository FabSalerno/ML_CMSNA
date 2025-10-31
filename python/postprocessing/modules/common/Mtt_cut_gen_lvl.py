import ROOT
import math
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

    
class Mtt_cut_gen_lvl(Module):
    def __init__(self, minMtt=700, maxMtt=1000, max_events=50000):
        self.minMtt = minMtt
        self.maxMtt = maxMtt
        self.max_events = max_events
        self.counter = 0
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        #print(self.counter)
        if self.counter >= self.max_events:
            return False
        save = False
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
        
        top = ROOT.TLorentzVector()
        for t in tops:
            if t.genPartIdxMother==0:
                top.SetPtEtaPhiM(t.pt, t.eta, t.phi, t.mass)

        antitop = ROOT.TLorentzVector()
        for antit in antitops:
            if antit.genPartIdxMother==0:
                antitop.SetPtEtaPhiM(antit.pt, antit.eta, antit.phi, antit.mass)
            
    
        Mtt = (top+antitop).M()
        if Mtt>=self.minMtt and Mtt<=self.maxMtt:
            save = True
            self.counter += 1
            print(f"raggiunti {self.counter} eventi")
        else:
            save = False

        return save
    