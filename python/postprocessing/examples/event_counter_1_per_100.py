import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
# score thresholds
score_thresholds   = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_NEW_2018_1_positive_truth/score_thresholds.json"
 # threshold to select top candidates
thr                = "1%"                                                
with open(score_thresholds, "r") as fjson:
    thresholds  = json.load(fjson)
threshold   = thresholds[thr]["thr"]
class event_counter_post(Module):
    def __init__(self):
        self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName+"_event_counter_post")
        self.h_nevents_1_per_100 = ROOT.TH1F("nevents","nevents",4,0,4)
        self.addObject(self.h_nevents_1_per_100)


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        tops_mixed= Collection(event, "TopMixed")

        for top in tops_mixed:
            if (top.score>=threshold):
                self.h_nevents_1_per_100.Fill(2)
        return True
