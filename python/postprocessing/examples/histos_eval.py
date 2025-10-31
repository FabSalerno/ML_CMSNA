import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class histos_eval(Module):
    def __init__(self):
        self.writeHistFile=True
        pass

    def beginJob(self,histFile,histDirName):
        
        #self.objs = []
        #print("\n e ora?", dir(self))
        Module.beginJob(self,histFile,histDirName+"_evaluation")
        self.h_score_negative_truth_mixed_true = ROOT.TH1F("TopMixed_score_negative_truth_histo_true","score_negative_truth_mixed_true",100,0,1)
        self.h_score_negative_truth_mixed_false_qcd = ROOT.TH1F("TopMixed_score_negative_truth_histo_false_qcd","score_negative_truth_mixed_false_qcd",100,0,1)
        self.h_score_negative_truth_mixed_false_other = ROOT.TH1F("TopMixed_score_negative_truth_histo_false_other","score_negative_truth_mixed_false_other",100,0,1)
        self.h_score_negative_truth_mixed_false_all = ROOT.TH1F("TopMixed_score_negative_truth_histo_false_all","score_negative_truth_mixed_false_all",100,0,1)
        self.h_score_positive_truth_mixed_true = ROOT.TH1F("TopMixed_score_positive_truth_histo_true","score_positive_truth_mixed_true",100,0,1)
        self.h_score_positive_truth_mixed_false_qcd = ROOT.TH1F("TopMixed_score_positive_truth_histo_false_qcd","score_positive_truth_mixed_false_qcd",100,0,1)
        self.h_score_positive_truth_mixed_false_other = ROOT.TH1F("TopMixed_score_positive_truth_histo_false_other","score_positive_truth_mixed_false_other",100,0,1)
        self.h_score_positive_truth_mixed_false_all = ROOT.TH1F("TopMixed_score_positive_truth_histo_false_all","score_positive_truth_mixed_false_all",100,0,1)
        self.addObject(self.h_score_negative_truth_mixed_true)
        self.addObject(self.h_score_negative_truth_mixed_false_qcd)
        self.addObject(self.h_score_negative_truth_mixed_false_other)
        self.addObject(self.h_score_negative_truth_mixed_false_all)
        self.addObject(self.h_score_positive_truth_mixed_true)
        self.addObject(self.h_score_positive_truth_mixed_false_qcd)
        self.addObject(self.h_score_positive_truth_mixed_false_other)
        self.addObject(self.h_score_positive_truth_mixed_false_all)
        

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        tops_mixed = Collection(event, "TopMixed")

        for top in tops_mixed:
            #print(top.truth)
            if (top.truth==1):
                self.h_score_negative_truth_mixed_true.Fill(top.TopScore_negative_truth)
                self.h_score_positive_truth_mixed_true.Fill(top.TopScore_positive_truth)
            if top.truth!=1:
                self.h_score_negative_truth_mixed_false_all.Fill(top.TopScore_negative_truth)
                self.h_score_positive_truth_mixed_false_all.Fill(top.TopScore_positive_truth)
            if top.truth==0:
                self.h_score_negative_truth_mixed_false_qcd.Fill(top.TopScore_negative_truth)
                self.h_score_positive_truth_mixed_false_qcd.Fill(top.TopScore_positive_truth)
            if top.truth==-1:
               self. h_score_negative_truth_mixed_false_other.Fill(top.TopScore_negative_truth)
               self. h_score_positive_truth_mixed_false_other.Fill(top.TopScore_positive_truth)
        
        return True
