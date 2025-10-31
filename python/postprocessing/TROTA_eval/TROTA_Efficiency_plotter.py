#!/usr/bin/env python
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import matplotlib.pyplot as plt
import mplhep as hep
import cmsstyle as CMS
import ROOT
import optparse
from math import sqrt
from ROOT import TEfficiency
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
hep.style.use("CMS")

def plot(h, folder, fillcolor, canv_name = "canv" ,extraTest="Simulation Preliminary", iPos=0, energy="13", lumi = "",  addInfo="", ytitle = "", wp = "", sample_name = ""):

    if type(h)==list:
        h1 = h[0]
        # hist_dict = [k.GetName() for k in h]
    else:
        h1 = h
    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)
    CMS.setCMSStyle()
    
    x_min = h1.GetXaxis().GetXmin()
    x_max = h1.GetXaxis().GetXmax()
    y_min = h1.GetMinimum()
    if y_min !=0: y_min = y_min - 0.2
    y_max = h1.GetMaximum()
    y_max = y_max + 0.3 * (y_max - y_min)
    if "Top mass" in ytitle:
        y_min = 135.
        y_max = 215.
    x_axis_name = h1.GetXaxis().GetTitle()+" [GeV]"
    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,ytitle,square=CMS.kRectangular, extraSpace=20.0, iPos=iPos)
    hdf = CMS.GetcmsCanvasHist(canv)
    # hdf.GetYaxis().SetMaxDigits(2)
    hdf.GetYaxis().SetLabelOffset(0.001)
    hdf.GetYaxis().SetLabelSize(0.045)
    hdf.GetYaxis().SetTitleOffset(1.1)
    hdf.GetYaxis().SetTitleSize(0.045)
    hdf.GetXaxis().SetLabelOffset(0.001)
    hdf.GetXaxis().SetLabelSize(0.045)
    hdf.GetXaxis().SetTitleOffset(1.1)
    hdf.GetXaxis().SetTitleSize(0.045)
    # canv.SetLogy()
    # Shift multiplier position
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    # leg = CMS.cmsLeg(0.5, 0.1, 0.98, 0.5, textSize=0.04)
    if wp !="":
        print("test")
        latex = ROOT.TLatex()
        latex.SetTextFont(42)
        latex.SetTextSize(0.04)
        latex.SetTextAlign(22)
        latex.DrawLatexNDC(0.27, 0.77, sample_name+", WP "+wp+"% fpr")
    CMS.cmsDraw(h1, "" ,lcolor = fillcolor, mcolor = fillcolor, fcolor = ROOT.kWhite, lwidth=2)
    return canv


def plotEfficiency(eff, h_den, h_num, folder, fillcolor, canv_name = "canv" ,extraTest="Simulation Preliminary", iPos=0, energy="13", lumi = "",  addInfo="", ytitle = "", sample_name = "t#bar{t}", ymax=0):
    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)
    CMS.setCMSStyle()
    x_min = h_den.GetXaxis().GetXmin()
    x_max = h_den.GetXaxis().GetXmax()
    y_min = 0.
    if ymax!=0: y_max = ymax
    else: y_max = 1.5#max([eff.GetEfficiency(i) for i in range(eff.GetTotalHistogram().GetNbinsX())]) +0.2
    print(y_max)
    x_axis_name = h_den.GetXaxis().GetTitle()
    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,ytitle,square=CMS.kRectangular, extraSpace=20.0, iPos=iPos) #with_z_axis=True
    hdf = CMS.GetcmsCanvasHist(canv)
    hdf.GetYaxis().SetMaxDigits(1)
    hdf.GetYaxis().SetLabelOffset(0.001)
    hdf.GetYaxis().SetLabelSize(0.045)
    hdf.GetYaxis().SetTitleOffset(1.1)
    hdf.GetYaxis().SetTitleSize(0.045)
    hdf.GetXaxis().SetLabelOffset(0.001)
    hdf.GetXaxis().SetLabelSize(0.045)
    hdf.GetXaxis().SetTitleOffset(1.1)
    hdf.GetXaxis().SetTitleSize(0.045)
    pad = ROOT.gPad
    margin = pad.GetRightMargin()
    pad.SetRightMargin(margin+0.01)
    #canv.SetLogy()
    # Shift multiplier position
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    # leg = CMS.cmsLeg(0.5, 0.1, 0.98, 0.5, textSize=0.04)
    return canv


def efficiency_calculator(h_num, h_den, h_eff):
    if not TEfficiency.CheckConsistency(h_num, h_den):
        raise ValueError("Inconsistent histograms: numerator and denominator must be compatible.")

    efficiency = TEfficiency(h_num, h_den)
    efficiency.SetStatisticOption(TEfficiency.kFCP)  # Use Clopper-Pearson for error calculation
    efficiency.SetConfidenceLevel(0.683)  # Set confidence level for error calculation 
    h_eff = efficiency 
    return h_eff

#########################################
#########################################
#########################################
#############Input parameters############
year = 2018
#model = "60_CNN_2D_LSTM_0_pt" #"TROTA"
model = "TROTA"
sample_name = "TT_semilep" ##"TT_semilep""TprimeToTZ_1800"
#sample_name = "TprimeToTZ_1800"

dirpath = f"/eos/user/f/fsalerno/Evaluation/{model}_{year}_studies/Histo_files"
path_to_graphic_folder = f"/eos/user/f/fsalerno/Evaluation/{model}_{year}_studies/RecoEff_{model}_{year}_{sample_name}_plots_official"

if not os.path.exists(path_to_graphic_folder):  
    os.makedirs(path_to_graphic_folder)
file_name=f"output_{model}_efficiency_Study_{sample_name}_noResinMix.root"
#file_name=f"output_TROTA_efficiency_Study_ttsemilep_noResinMix.root"
inFile = f"{dirpath}/{file_name}"
histos_file = ROOT.TFile.Open(inFile)
#########################################
#########################################
#########################################
#########################################

h_den = histos_file.Get("h_gentop_pt")
#print(f"denominator: {h_den.Integral()}")
#print(f"denominator_2: {h_den.GetEntries()}")
#"Selection", "TagLooseWP","TagMediumWP","TagTightWP", "EndLooseWP", "EndTightWP",
eff_types = ["Reconstructable","RealLife","TagMediumWP","EndMediumWP"]#,"TagLooseWP","TagMediumWP","TagTightWP"
top_types = ["Resolved","Mixed","Merged"]
match_types = ["QuarkMatch","GenTopMatch02"]#,"GenTopMatch04","OldMatch"
keys=[]
plot_types = []
for eff_type in eff_types:       
   for match_type in match_types:
        plot_types.append(f"{eff_type}_{match_type}")
        for top_type in top_types:
            key = f"{eff_type}_{match_type}_{top_type}"
            keys.append(key)
    #print(h_reco_num_mixed)

h_Top_pt = {}
for key in keys:
    if "End" in key:
        keytag= key.replace("End", "Tag")
        h_Top_pt[key] = histos_file.Get(f"h_Top_pt_{keytag}")
    else:
        h_Top_pt[key] = histos_file.Get(f"h_Top_pt_{key}")

h_reco_eff = {}
for key in keys:
    print(f"key: {key}")
    h_reco_eff[key] = h_Top_pt[key].Clone()
    #h_reco_eff_mixed[key].Divide(h_den)
    if "Selection" in key:
        den_key = key.replace("Selection", "Reconstructable")
        h_den_selection = h_Top_pt[den_key].Clone()
        #print(f"key: {key}")
        #print(f"den_key: {den_key}")
        #print(f"num: {h_Top_pt[key].Integral()}")
        #print(f"den: {h_den_selection.Integral()}")
        #print(f"num: {h_Top_pt[key].Integral()}")
        h_reco_eff[key] = efficiency_calculator(h_Top_pt[key], h_den_selection, h_reco_eff[key])
    elif "TagLooseWP" in key:
        den_key = key.replace("TagLooseWP", "RealLife")
        #den_key = key.replace("TagLooseWP", "Reconstructable")

        h_den_selection = h_Top_pt[den_key].Clone()
        h_reco_eff[key] = efficiency_calculator(h_Top_pt[key], h_den_selection, h_reco_eff[key])
    elif "TagMediumWP" in key:
        den_key = key.replace("TagMediumWP", "RealLife")
        #den_key = key.replace("TagMediumWP", "Reconstructable")
        h_den_selection = h_Top_pt[den_key].Clone()
        h_reco_eff[key] = efficiency_calculator(h_Top_pt[key], h_den_selection, h_reco_eff[key])
    elif "TagTightWP" in key:
        den_key = key.replace("TagTightWP", "RealLife")
        h_den_selection = h_Top_pt[den_key].Clone()
        h_reco_eff[key] = efficiency_calculator(h_Top_pt[key], h_den_selection, h_reco_eff[key])
    else:
        h_reco_eff[key] = efficiency_calculator(h_Top_pt[key], h_den, h_reco_eff[key])




outFile = ROOT.TFile(f"{path_to_graphic_folder}/RecoEff.root", "RECREATE")    
for key in keys:
    h_reco_eff[key].Write()
outFile.Close()

c_reco={}
color_mix = ROOT.TColor.GetColor("#ffa90e")
color_res = ROOT.TColor.GetColor("#92dadd")
color_mer = ROOT.TColor.GetColor("#bd1f01")
for plot_type in plot_types:
    print("plot_type", plot_type)
    h_den.GetXaxis().SetTitle("p^{ptcl, top}_{T} [GeV]")
    h_den_selection.GetXaxis().SetTitle("p^{ptcl, top}_{T} [GeV]")
    if "Tag" in plot_type:
        h_den.GetYaxis().SetTitle("Tagging efficiency")
        h_den_selection.GetYaxis().SetTitle("Tagging efficiency")
    
    elif "Reconstructable" in plot_type:
        #h_den.GetYaxis().SetTitle("Reconstruction efficiency")
        #h_den_selection.GetYaxis().SetTitle("Reconstruction efficiency")
        h_den.GetYaxis().SetTitle("Acceptance efficiency")
        h_den_selection.GetYaxis().SetTitle("Acceptance efficiency")

    elif "End" in plot_type:
        h_den.GetYaxis().SetTitle("End to end efficiency")
        h_den_selection.GetYaxis().SetTitle("End to end efficiency")
        
    else:
        h_den.GetYaxis().SetTitle("Selection efficiency")
        h_den_selection.GetYaxis().SetTitle("Selection efficiency")
    key_resolved = f"{plot_type}_Resolved"
    key_mixed = f"{plot_type}_Mixed"
    key_merged = f"{plot_type}_Merged"
    if "Selection" in plot_type:
        if year==2022:  
            c_reco[plot_type]=plotEfficiency(h_reco_eff[key_mixed], h_den_selection, h_Top_pt[key], path_to_graphic_folder, color_mix, canv_name="efficiency_mix", ytitle="Selection efficiency", sample_name=sample_name, energy="13.6") 
        elif year==2018:
            c_reco[plot_type]=plotEfficiency(h_reco_eff[key_mixed], h_den_selection, h_Top_pt[key], path_to_graphic_folder, color_mix, canv_name="efficiency_mix", ytitle="Selection efficiency", sample_name=sample_name, energy="13") 
        CMS.cmsDraw(h_reco_eff[key_resolved], "PE" ,marker=20, lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=1)
        CMS.cmsDraw(h_reco_eff[key_mixed], "PE" ,marker=21, lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=1)
        CMS.cmsDraw(h_reco_eff[key_merged], "PE" ,marker=22, lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=1)
    elif "Tag" in plot_type:
        if year==2022:    
            c_reco[plot_type]=plotEfficiency(h_reco_eff[key_mixed], h_den_selection, h_Top_pt[key], path_to_graphic_folder, color_mix, canv_name="efficiency_mix", ytitle=h_den.GetYaxis().GetTitle(), sample_name=sample_name, energy="13.6") 
        elif year==2018:
            c_reco[plot_type]=plotEfficiency(h_reco_eff[key_mixed], h_den_selection, h_Top_pt[key], path_to_graphic_folder, color_mix, canv_name="efficiency_mix", ytitle=h_den.GetYaxis().GetTitle(), sample_name=sample_name, energy="13") 
        CMS.cmsDraw(h_reco_eff[key_resolved], "PE" ,marker=20, lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=1)
        CMS.cmsDraw(h_reco_eff[key_mixed], "PE" ,marker=21, lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=1)
        CMS.cmsDraw(h_reco_eff[key_merged], "PE" ,marker=22, lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=1)   
    else:
        if year==2022:    
            c_reco[plot_type]=plotEfficiency(h_reco_eff[key_mixed], h_den, h_Top_pt[key], path_to_graphic_folder, color_mix, canv_name="efficiency_mix", ytitle=h_den.GetYaxis().GetTitle(), sample_name=sample_name, energy="13.6") 
        elif year==2018:

            c_reco[plot_type]=plotEfficiency(h_reco_eff[key_mixed], h_den, h_Top_pt[key], path_to_graphic_folder, color_mix, canv_name="efficiency_mix", ytitle=h_den.GetYaxis().GetTitle(), sample_name=sample_name, energy="13") 
        CMS.cmsDraw(h_reco_eff[key_resolved], "PE" ,marker=20, lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=1)
        CMS.cmsDraw(h_reco_eff[key_mixed], "PE" ,marker=21, lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=1)
        CMS.cmsDraw(h_reco_eff[key_merged], "PE" ,marker=22, lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=1)

    legend = CMS.cmsLeg(0.60, 0.75, 0.95, 0.89, textSize=0.04)
    legend.SetHeader("Category")
    legend.AddEntry(h_reco_eff[key_merged], "Top merged", "lpe")
    legend.AddEntry(h_reco_eff[key_mixed], "Top mixed", "lpe")
    legend.AddEntry(h_reco_eff[key_resolved], "Top resolved", "lpe")
    legend.Draw()
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.04)
    latex.SetTextAlign(13)
    sample ="#it{t#bar{t} #rightarrow l + jets}"
    plot_type_split = plot_type.split("_")
    reconstruction_type = plot_type_split[1]

    if reconstruction_type == "QuarkMatch":
        reconstruction_string = "#font[12]{#Delta}R(Jet,q) < Jet radius"
    elif reconstruction_type == "GenTopMatch02":
        reconstruction_string = "#font[12]{#Delta}R(t^{cand},t) < 0.2"
    elif reconstruction_type == "GenTopMatch04":
        reconstruction_string = "#font[12]{#Delta}R(t^{cand},t) < 0.4"
    elif reconstruction_type == "=OldMatch":
        reconstruction_string = "#font[12]{#Delta}R(t^{cand},t) < 0.4 \\ #wedge \\#font[12]{#Delta}R(Jet,q) < Jet radius"
        #reconstruction_string = "PROVA"
    efficiency_type = plot_type_split[0]

    if "TagLoose" in efficiency_type:
        efficiency_string="10% false positive rate"
    elif "EndLoose" in efficiency_type:
        efficiency_string="10% false positive rate"
    elif "TagMedium" in efficiency_type:
        efficiency_string="1% false positive rate"
    elif "EndMedium" in efficiency_type:
        efficiency_string="1% false positive rate"
    elif "TagTight"  in efficiency_type:
        efficiency_string="0.1% false positive rate"
    elif "EndTight" in efficiency_type:
        efficiency_string="0.1% false positive rate"
    
    # elif "Reconstructable" in efficiency_type:
    #     efficiency_string="#frac{Events with #geq 1 top matched}{Total events}"
    # elif "Selection" in efficiency_type:
    #     efficiency_string="#frac{Events with best top matched}{Events with #geq 1 top matched}"
    # elif "Real" in efficiency_type:
    #     #efficiency_string="#frac{#text{Events with best top matched}}{#text{Total events}}"
    #     efficiency_string="#frac{Events with best top matched}{Total events}"
    else:
        efficiency_string=""

    
    y_start = 0.85
    dy = 0.05

    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextAlign(11)  # left-aligned

    #latex.DrawLatexNDC(0.15, y_start, sample)
    latex.DrawLatexNDC(0.15, y_start , reconstruction_string)
    latex.DrawLatexNDC(0.15, y_start - dy, f"{efficiency_string}")
    #latex.DrawLatexNDC(0.15, y_start - 2*dy, f"efficiency type: {efficiency_type}")
    #c_reco[plot_type]
    CMS.SaveCanvas(c_reco[plot_type], f"{path_to_graphic_folder}/RecoEff_{plot_type}.pdf", close=False)
    CMS.SaveCanvas(c_reco[plot_type], f"{path_to_graphic_folder}/RecoEff_{plot_type}.png")


