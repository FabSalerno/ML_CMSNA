import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class event_counter_pre(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName+"_event_counter_pre")
        self.h_nevents_pre = ROOT.TH1F("nevents_pre","nevents_pre",4,0,4)
        self.addObject(self.h_nevents_pre)


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.h_nevents_pre.Fill(0)
        return True
