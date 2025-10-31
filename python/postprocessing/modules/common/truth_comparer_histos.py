#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
#from PhysicsTools.NanoAODTools.postprocessing.modules.common import truth_comparer
from importlib import import_module
import os
import sys
import ROOT
import matplotlib.pyplot as plt
import mplhep as hep
import cmsstyle as CMS
hep.style.use("CMS")
ROOT.PyConfig.IgnoreCommandLineOptions = True


class truth_comparer_histos(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)

        self.h_n_top_true_old = ROOT.TH1F('n_top_true_old', 'n_top_true_old',3, 0, 3)
        self.h_n_top_true_new = ROOT.TH1F('n_top_true_new', 'n_top_true_new',3, 0, 3)
        self.h_n_top_true_parton_flav = ROOT.TH1F('n_top_true_parton_flav', 'n_top_true_parton_flav',3, 0, 3)
        self.h_n_top_false_old = ROOT.TH1F('n_top_false_old', 'n_top_false_old',3, 0, 3)
        self.h_n_top_false_new = ROOT.TH1F('n_top_false_new', 'n_top_false_new',3, 0, 3)
        self.h_n_top_false_parton_flav = ROOT.TH1F('n_top_false_parton_flav', 'n_top_false_parton_flav',3, 0, 3)
        self.addObject(self.h_n_top_true_old)
        self.addObject(self.h_n_top_true_new)   
        self.addObject(self.h_n_top_true_parton_flav)
        self.addObject(self.h_n_top_false_old)
        self.addObject(self.h_n_top_false_new)
        self.addObject(self.h_n_top_false_parton_flav)

    def analyze(self, event):
        topmixed             = Collection(event, "TopMixed")
        toploresolved        = Collection(event, "TopResolved")
        jets        = Collection(event,"Jet")
        njets       = len(jets)
        fatjets     = Collection(event,"FatJet")
        n_topmixed  = len(topmixed)

        n_old_true = 0
        n_new_true = 0
        n_parton_flav_true = 0
        n_old_false = 0
        n_new_false = 0
        n_parton_flav_false = 0
        #print(f"Analizzando {n_topmixed} top nell'evento {event.event}")
        for t, top in enumerate(topmixed):
            #print("TopMixed_truth: ", top.truth, "TopMixed_truth_partonFlavour: ", top.truth_partonFlavour)
            if top.truth == 1:
                self.h_n_top_true_new.Fill(1)
                n_new_true += 1
            if top.truth_partonFlavour == 1:
                self.h_n_top_true_parton_flav.Fill(2)
                n_parton_flav_true += 1
            if top.old_truth==1:
                self.h_n_top_true_old.Fill(0)
                n_old_true += 1
            if top.truth == 0:
                self.h_n_top_false_new.Fill(1)
                n_new_false += 1
            if top.truth_partonFlavour == 0:
                self.h_n_top_false_parton_flav.Fill(2)
                n_parton_flav_false += 1
            if top.old_truth==0:
                self.h_n_top_false_old.Fill(0)
                n_old_false += 1
        #print(f"Number of true tops: old_truth: {n_old_true}, new_truth: {n_new_true}, parton_flavour_truth: {n_parton_flav_true}")
        #print(f"Number of false tops: old_truth: {n_old_false}, new_truth: {n_new_false}, parton_flavour_truth: {n_parton_flav_false}")
        return True

component = "TT_inclusive_MC2022"
files = [f"/eos/user/f/fsalerno/Data/PF/truth_comp/nano_mcRun3_TT_inclusive_MC2022_topcand_PF_10000.root"]
p = PostProcessor(".", files, branchsel=None, modules=[
                  truth_comparer_histos()], noOut=True, histFileName="hist_truth_comp.root", histDirName="truth_compare")
p.run()


#histo def
histos_file = ROOT.TFile.Open("hist_truth_comp.root")
dir_name="truth_compare"
h_n_top_true_old = histos_file.Get(f"{dir_name}/n_top_true_old")
h_n_top_true_new = histos_file.Get(f"{dir_name}/n_top_true_new")
h_n_top_true_parton_flav = histos_file.Get(f"{dir_name}/n_top_true_parton_flav")
h_n_top_false_old = histos_file.Get(f"{dir_name}/n_top_false_old")
h_n_top_false_new = histos_file.Get(f"{dir_name}/n_top_false_new")
h_n_top_false_parton_flav = histos_file.Get(f"{dir_name}/n_top_false_parton_flav")

path_to_graphic_folder = "/eos/user/f/fsalerno/Evaluation/truth_study"
outFile = ROOT.TFile(f"{path_to_graphic_folder}/Truth_compare_{component}.root", "RECREATE")    
h_n_top_true_new.Write()
h_n_top_true_old.Write()
h_n_top_true_parton_flav.Write()
h_n_top_false_new.Write()
h_n_top_false_old.Write()
h_n_top_false_parton_flav.Write()
outFile.Close()
#plotting true
c_true = ROOT.TCanvas("c_true", "True tops for different truth definitions", 800, 600)
h_n_top_true_old.SetTitle(f"True tops for different truth definitions")
h_n_top_true_old.GetYaxis().SetTitle("Number of true tops")
h_n_top_true_old.GetXaxis().SetBinLabel(1, "old_truth")
h_n_top_true_old.GetXaxis().SetBinLabel(2, "new_truth")
h_n_top_true_old.GetXaxis().SetBinLabel(3, "parton_flavour_truth")
h_n_top_true_old.Draw("same")
h_n_top_true_new.Draw("same")
h_n_top_true_parton_flav.Draw("same")
c_true.SaveAs(f"{path_to_graphic_folder}/true_tops_number_comparison_{component}.png")

c_false = ROOT.TCanvas("c_false", "False tops for different truth definitions", 900, 600)
h_n_top_false_old.SetTitle(f"False tops for different truth definitions")
h_n_top_false_old.GetYaxis().SetTitle("Number of false tops")
h_n_top_false_old.GetXaxis().SetBinLabel(1, "old_truth")
h_n_top_false_old.GetXaxis().SetBinLabel(2, "new_truth")
h_n_top_false_old.GetXaxis().SetBinLabel(3, "parton_flavour_truth")
h_n_top_false_old.Draw("same")
h_n_top_false_new.Draw("same")
h_n_top_false_parton_flav.Draw("same")
c_false.SaveAs(f"{path_to_graphic_folder}/false_tops_number_comparison{component}.png")

# Apri un file in modalità scrittura
with open(f"{path_to_graphic_folder}/risultati_{component}.txt", "w") as file:
    # Crea le stringhe con i risultati
    true_tops = f"number of true tops: old_truth: {h_n_top_true_old.GetEntries()} new_truth: {h_n_top_true_new.GetEntries()} parton_flavour_truth: {h_n_top_true_parton_flav.GetEntries()}\n"
    false_tops = f"number of false tops: old_truth: {h_n_top_false_old.GetEntries()} new_truth: {h_n_top_false_new.GetEntries()} parton_flavour_truth: {h_n_top_false_parton_flav.GetEntries()}\n"
    all_tops = f"total number of tops: old_truth: {h_n_top_false_old.GetEntries()+h_n_top_true_old.GetEntries()} new_truth: {h_n_top_false_new.GetEntries()+h_n_top_true_new.GetEntries()} parton_flavour_truth: {h_n_top_false_parton_flav.GetEntries()+h_n_top_true_parton_flav.GetEntries()}\n"
    # Stampa i risultati a schermo
    print(true_tops.strip())
    print(false_tops.strip())
    print(all_tops.strip())

    # Scrivi i risultati nel file
    file.write(true_tops)
    file.write(false_tops)

