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


class truth_discrimination_histos(Module):
    def __init__(self):
        self.writeHistFile = True

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)

        self.h_score_top_mixed_true_new = ROOT.TH1F(f"score_top_mixed_true_new", f"score_top_mixed_true_new", 100, 0, 1)
        self.h_score_top_mixed_true_old = ROOT.TH1F(f"score_top_mixed_true_old", f"score_top_mixed_true_old", 100, 0, 1)
        self.h_score_top_mixed_true_parton_flav = ROOT.TH1F(f"score_top_mixed_true_parton_flav", f"score_top_mixed_true_parton_flav", 100, 0, 1)
        self.h_score_top_mixed_false_new = ROOT.TH1F(f"score_top_mixed_false_new", f"score_top_mixed_false_new", 100, 0, 1)
        self.h_score_top_mixed_false_old = ROOT.TH1F(f"score_top_mixed_false_old", f"score_top_mixed_false_old", 100, 0, 1)
        self.h_score_top_mixed_false_parton_flav = ROOT.TH1F(f"score_top_mixed_false_parton_flav", f"score_top_mixed_false_parton_flav", 100, 0, 1)

        self.addObject(self.h_score_top_mixed_true_old)
        self.addObject(self.h_score_top_mixed_true_new)  
        self.addObject(self.h_score_top_mixed_true_parton_flav)
        self.addObject(self.h_score_top_mixed_false_old)
        self.addObject(self.h_score_top_mixed_false_new)  
        self.addObject(self.h_score_top_mixed_false_parton_flav)
        
    def analyze(self, event):
        topmixed             = Collection(event, "TopMixed")
        toploresolved        = Collection(event, "TopResolved")
        jets        = Collection(event,"Jet")
        njets       = len(jets)
        fatjets     = Collection(event,"FatJet")
        n_topmixed  = len(topmixed)
        key="60_CNN_2D_LSTM_0_pt"
        #print(f"Analizzando {n_topmixed} top nell'evento {event.event}")
        for top in topmixed:
            top_score_key = f"TopScore_{key}"  
            if hasattr(top, top_score_key):
                TopScore = getattr(top, top_score_key) 


            if top.truth == 1:
                self.h_score_top_mixed_true_new.Fill(TopScore)

            if top.truth == 0:
                self.h_score_top_mixed_false_new.Fill(TopScore)

            if top.old_truth == 1:
                self.h_score_top_mixed_true_old.Fill(TopScore)

            if top.old_truth == 0:
                self.h_score_top_mixed_false_old.Fill(TopScore)

            if top.truth_partonFlavour == 1:
                self.h_score_top_mixed_true_parton_flav.Fill(TopScore)

            if top.truth_partonFlavour == 0:
                self.h_score_top_mixed_false_parton_flav.Fill(TopScore)

           

        return True

component = "TT_semilep_MC2022"
files = [f"/eos/user/f/fsalerno/Data/PF/prova/nano_mcRun3_{component}_topeval_PF_presel_10000.root"]
p = PostProcessor(".", files, branchsel=None, modules=[
                  truth_discrimination_histos()], noOut=True, histFileName="hist_truth_discr.root", histDirName="truth_discrimination")
p.run()

ROOT.gStyle.SetOptStat(0)
#histo def
histos_file = ROOT.TFile.Open("hist_truth_discr.root")
dir_name="truth_discrimination"
h_score_top_mixed_true_old = histos_file.Get(f"{dir_name}/score_top_mixed_true_old")
h_score_top_mixed_true_new = histos_file.Get(f"{dir_name}/score_top_mixed_true_new")
h_score_top_mixed_true_parton_flav = histos_file.Get(f"{dir_name}/score_top_mixed_true_parton_flav")
h_score_top_mixed_false_old = histos_file.Get(f"{dir_name}/score_top_mixed_false_old")
h_score_top_mixed_false_new = histos_file.Get(f"{dir_name}/score_top_mixed_false_new")
h_score_top_mixed_false_parton_flav = histos_file.Get(f"{dir_name}/score_top_mixed_false_parton_flav")
#print(h_score_top_mixed_true_new.GetEntries())
path_to_graphic_folder = "/eos/user/f/fsalerno/Evaluation/truth_study"
outFile = ROOT.TFile(f"{path_to_graphic_folder}/Truth_discrimination_{component}.root", "RECREATE")    
h_score_top_mixed_true_new.Write()
h_score_top_mixed_true_old.Write()
h_score_top_mixed_true_parton_flav.Write()
h_score_top_mixed_false_new.Write()
h_score_top_mixed_false_old.Write()
h_score_top_mixed_false_parton_flav.Write()
outFile.Close()

#plotting old
c_old = ROOT.TCanvas("c_old", f"Discrimination 60_CNN_2D_LSTM_0_pt old truth", 900, 600)
h_score_top_mixed_true_old.SetTitle(f"Discrimination 60_CNN_2D_LSTM_0_pt old truth")
h_score_top_mixed_true_old.GetYaxis().SetTitle("Normalized Counts")
h_score_top_mixed_true_old.GetXaxis().SetTitle("Tops score")
h_score_top_mixed_true_old.Scale(1/h_score_top_mixed_true_old.GetEntries())
h_score_top_mixed_true_old.SetLineColor(2)
h_score_top_mixed_true_old.SetLineStyle(1)
h_score_top_mixed_true_old.Draw("histosame")
h_score_top_mixed_false_old.Scale(1/h_score_top_mixed_false_old.GetEntries())
h_score_top_mixed_false_old.SetLineColor(4)
h_score_top_mixed_false_old.SetLineStyle(1)
h_score_top_mixed_false_old.Draw("histosame")
c_old.SaveAs(f"{path_to_graphic_folder}/discrimination_old_{component}.png")


#plotting new
c_new = ROOT.TCanvas("c_new", f"Discrimination 60_CNN_2D_LSTM_0_pt new truth", 900, 600)
h_score_top_mixed_true_new.SetTitle(f"Discrimination 60_CNN_2D_LSTM_0_pt new truth")
h_score_top_mixed_true_new.GetYaxis().SetTitle("Normalized Counts")
h_score_top_mixed_true_new.GetXaxis().SetTitle("Tops score")
h_score_top_mixed_true_new.Scale(1/h_score_top_mixed_true_new.GetEntries())
h_score_top_mixed_true_new.SetLineColor(2)
h_score_top_mixed_true_new.SetLineStyle(1)
h_score_top_mixed_true_new.Draw("histosame")
h_score_top_mixed_false_new.Scale(1/h_score_top_mixed_false_new.GetEntries())
h_score_top_mixed_false_new.SetLineColor(4)
h_score_top_mixed_false_new.SetLineStyle(1)
h_score_top_mixed_false_new.Draw("histosame")
c_new.SaveAs(f"{path_to_graphic_folder}/discrimination_new_{component}.png")

c_parton_flav = ROOT.TCanvas("c_parton_flav", f"Discrimination 60_CNN_2D_LSTM_0_pt parton_flav truth", 900, 600)
h_score_top_mixed_true_parton_flav.SetTitle(f"Discrimination 60_CNN_2D_LSTM_0_pt parton_flav truth")
h_score_top_mixed_true_parton_flav.GetYaxis().SetTitle("Normalized Counts")
h_score_top_mixed_true_parton_flav.GetXaxis().SetTitle("Tops score")
h_score_top_mixed_true_parton_flav.Scale(1/h_score_top_mixed_true_parton_flav.GetEntries())
h_score_top_mixed_true_parton_flav.SetLineColor(2)
h_score_top_mixed_true_parton_flav.SetLineStyle(1)
h_score_top_mixed_true_parton_flav.Draw("histosame")
h_score_top_mixed_false_parton_flav.Scale(1/h_score_top_mixed_false_parton_flav.GetEntries())
h_score_top_mixed_false_parton_flav.SetLineColor(4)
h_score_top_mixed_false_parton_flav.SetLineStyle(1)
h_score_top_mixed_false_parton_flav.Draw("histosame")
c_parton_flav.SaveAs(f"{path_to_graphic_folder}/discrimination_parton_flav_{component}.png")


c_true_comparison = ROOT.TCanvas("c_true_comparison", f"Discrimination 60_CNN_2D_LSTM_0_pt true tops", 900, 600)
h_score_top_mixed_true_parton_flav.SetTitle(f"Discrimination 60_CNN_2D_LSTM_0_pt true tops")
h_score_top_mixed_true_parton_flav.GetYaxis().SetTitle("Normalized Counts")
h_score_top_mixed_true_parton_flav.GetXaxis().SetTitle("Tops score")
h_score_top_mixed_true_parton_flav.Scale(1/h_score_top_mixed_true_parton_flav.GetEntries())
h_score_top_mixed_true_parton_flav.SetLineColor(2)
h_score_top_mixed_true_parton_flav.SetLineStyle(1)
h_score_top_mixed_true_parton_flav.Draw("histosame")
h_score_top_mixed_true_new.Scale(1/h_score_top_mixed_true_new.GetEntries())
h_score_top_mixed_true_new.SetLineColor(3)
h_score_top_mixed_true_new.SetLineStyle(1)
h_score_top_mixed_true_new.Draw("histosame")
h_score_top_mixed_true_old.Scale(1/h_score_top_mixed_true_old.GetEntries())
h_score_top_mixed_true_old.SetLineColor(4)
h_score_top_mixed_true_old.SetLineStyle(1)
h_score_top_mixed_true_old.Draw("histosame")
legend = ROOT.TLegend(0.3, 0.7, 0.6, 0.9) #x1,y1,x2,y2
legend.SetBorderSize(1)  
legend.SetFillColor(0) 
legend.SetTextSize(0.03)  
legend.AddEntry(h_score_top_mixed_true_old, "Old Truth", "l")
legend.AddEntry(h_score_top_mixed_true_new, "New Truth", "l")
legend.AddEntry(h_score_top_mixed_true_parton_flav, "Parton Flavour Truth", "l")
legend.Draw()
c_true_comparison.SaveAs(f"{path_to_graphic_folder}/discrimination_true_tops_{component}.png")


c_false_comparison = ROOT.TCanvas("c_false_comparison", f"Discrimination 60_CNN_2D_LSTM_0_pt false tops", 900, 600)
h_score_top_mixed_false_parton_flav.SetTitle(f"Discrimination 60_CNN_2D_LSTM_0_pt false tops")
h_score_top_mixed_false_parton_flav.GetYaxis().SetTitle("Normalized Counts")
h_score_top_mixed_false_parton_flav.GetXaxis().SetTitle("Tops score")
h_score_top_mixed_false_parton_flav.Scale(1/h_score_top_mixed_false_parton_flav.GetEntries())
h_score_top_mixed_false_parton_flav.SetLineColor(2)
h_score_top_mixed_false_parton_flav.SetLineStyle(1)
h_score_top_mixed_false_parton_flav.Draw("histosame")
h_score_top_mixed_false_new.Scale(1/h_score_top_mixed_false_new.GetEntries())
h_score_top_mixed_false_new.SetLineColor(3)
h_score_top_mixed_false_new.SetLineStyle(1)
h_score_top_mixed_false_new.Draw("histosame")
h_score_top_mixed_false_old.Scale(1/h_score_top_mixed_false_old.GetEntries())
h_score_top_mixed_false_old.SetLineColor(4)
h_score_top_mixed_false_old.SetLineStyle(1)
h_score_top_mixed_false_old.Draw("histosame")
legend_2 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9) 
legend_2.SetBorderSize(1)  
legend_2.SetFillColor(0) 
legend_2.SetTextSize(0.03)  
legend_2.AddEntry(h_score_top_mixed_false_old, "Old Truth", "l")
legend_2.AddEntry(h_score_top_mixed_false_new, "New Truth", "l")
legend_2.AddEntry(h_score_top_mixed_false_parton_flav, "Parton Flavour Truth", "l")
legend_2.Draw()
c_false_comparison.SaveAs(f"{path_to_graphic_folder}/discrimination_false_tops_{component}.png")