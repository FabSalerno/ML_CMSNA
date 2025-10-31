import ROOT
import math
import numpy as np
from array import array
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
#from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *






class truth_comparer(Module):
    def __init__(self):
        pass
        
        
    def beginJob(self):
        pass
        
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree



    def endFile(self, inputFile, outputFile, inputTree,wrappedOutputTree):
        pass


    def analyze(self, event):
        topmixed             = Collection(event, "TopMixed")
        toploresolved        = Collection(event, "TopResolved")
        jets        = Collection(event,"Jet")
        njets       = len(jets)
        fatjets     = Collection(event,"FatJet")
        n_topmixed  = len(topmixed)
        #print(f"Analizzando {n_topmixed} top nell'evento {event.event}")
        for t, top in enumerate(topmixed):
            #print("TopMixed_truth: ", top.truth, "TopMixed_truth_partonFlavour: ", top.truth_partonFlavour)
            if top.truth == 1 or top.truth_partonFlavour == 1 or top.old_truth==1:
                if (top.truth == 1 and top.old_truth == 0) or (top.truth == 0 and top.old_truth == 1):
                    print("\n\nNew truth and old truth are different")
                print("\nTopMixed_old_truth:", top.old_truth, " TopMixed_truth:", top.truth, " TopMixed_truth_partonFlavour:", top.truth_partonFlavour)
                print("Event",event.event,"Top_Idx:",t, "Top_pt:", top.pt) 
                flavs_j0, flavs_j1 = jets[top.idxJet0].pdgId, jets[top.idxJet1].pdgId
                sgns_j0, sgns_j1 = jets[top.idxJet0].pdgIdSign, jets[top.idxJet1].pdgIdSign
                jet_0_flavs_list = get_quark_flavs(flavs_j0, sgns_j0)
                jet_1_flavs_list = get_quark_flavs(flavs_j1, sgns_j1)
                print("Top_mother:",jets[top.idxJet0].topMother)
                print("j0_old_match",jets[top.idxJet0].pdgId, "\tj0_match", jet_0_flavs_list, "     j0_match_partonFlavour", jets[top.idxJet0].partonFlavour)
                #print("\tTop_mother_j1:",jets[top.idxJet1].topMother)
                print("j1_old_match",jets[top.idxJet1].pdgId,"\tj1_match", jet_1_flavs_list, "      j1_match_partonFlavour", jets[top.idxJet1].partonFlavour)
                if top.idxJet2 != -1:
                    flavs_j2 = jets[top.idxJet2].pdgId
                    sgns_j2 = jets[top.idxJet2].pdgIdSign
                    jet_2_flavs_list = get_quark_flavs(flavs_j2, sgns_j2)
                    #print("\tTop_mother_j2:",jets[top.idxJet2].topMother)
                    print("j2_old_match",jets[top.idxJet2].pdgId,"\tj2_match", jet_2_flavs_list, "      j2_match_partonFlavour", jets[top.idxJet2].partonFlavour)
                if top.idxFatJet != -1:
                    flavs_fj = fatjets[top.idxFatJet].pdgId
                    sgns_fj = fatjets[top.idxFatJet].pdgIdSign
                    fj_flavs_list = get_quark_flavs(flavs_fj, sgns_fj)
                    #print("\tTop_mother_fj:",fatjets[top.idxFatJet].topMother)
                    print("fj_old_match", fatjets[top.idxFatJet].pdgId,"\tfj_match", fj_flavs_list)

        return True