#!/usr/bin/env python
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import matplotlib.pyplot as plt
import mplhep as hep
import cmsstyle as CMS
hep.style.use("CMS")

def plot_cut_flow_cms(h_temp, h_0, h_cut, h_10_per_100, h_5_per_100, h_1_per_100, h_1_per_1000, canv_name = "canv" ,extraTest="Work in progress", iPos=0, energy="13.6", lumi = "",  addInfo="", ytitle = "", samplelabel = "t#bar{t}", ymax=0):
    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)
    CMS.setCMSStyle()
    x_min = h_temp.GetXaxis().GetXmin()
    x_max = h_temp.GetXaxis().GetXmax()
    y_min = h_1_per_1000.GetBinContent(1)/10
    #print(h_0.GetEntries())
    if h_0==0:
        y_max = 1.2*h_cut.GetBinContent(1)
    else:
        y_max = 1.2*h_0.GetBinContent(1)
    #print(y_max)
    x_axis_name = h_temp.GetXaxis().GetTitle()
    ytitle = h_temp.GetYaxis().GetTitle()
    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,ytitle,square=CMS.kRectangular, extraSpace=20.0, iPos=iPos)
    hdf = CMS.GetcmsCanvasHist(canv)
    #name=hdf.GetName()
    #title=hdf.GetTitle()
    #hdf = ROOT.TH1F(name, title,6, 0, 6)
    hdf.GetYaxis().SetMaxDigits(1)
    hdf.GetYaxis().SetLabelOffset(0.001)
    hdf.GetYaxis().SetLabelSize(0.045)
    hdf.GetYaxis().SetTitleOffset(1.1)
    hdf.GetYaxis().SetTitleSize(0.045)
    hdf.GetXaxis().SetLabelOffset(0.001)
    hdf.GetXaxis().SetLabelSize(0.045)
    hdf.GetXaxis().SetTitleOffset(1.1)
    hdf.GetXaxis().SetTitleSize(0.045)

    if h_0==0:
        h_temp.GetXaxis().SetBinLabel(1, "preselection")
    else:
        h_temp.GetXaxis().SetBinLabel(1, "no selection")
    hdf.GetXaxis().SetBinLabel(2*(750//6), "preselection")
    hdf.GetXaxis().SetBinLabel(3*(750//6), f"10% ")
    h_temp.GetXaxis().SetBinLabel(4, f"5% ")
    h_temp.GetXaxis().SetBinLabel(5, f"1% ")
    h_temp.GetXaxis().SetBinLabel(6, f"0.1% ")
    h_temp.SetTitle(f"Cut flow for {canv_name}")
    

    source_bin = 1
    if h_0==0:
        source_content_1 = h_cut.GetBinContent(source_bin)
    else:
        source_content_1 = h_0.GetBinContent(source_bin)
    h_temp.SetBinContent(1, source_content_1)

    source_content_2 = h_cut.GetBinContent(source_bin)
    h_temp.SetBinContent(2, source_content_2)

    source_content_3 = h_10_per_100.GetBinContent(source_bin)
    h_temp.SetBinContent(3, source_content_3)
    
    source_content_4 = h_5_per_100.GetBinContent(source_bin)
    h_temp.SetBinContent(4, source_content_4)

    source_content_5 = h_1_per_100.GetBinContent(source_bin)
    h_temp.SetBinContent(5,  source_content_5)

    source_content_6 = h_1_per_1000.GetBinContent(source_bin)
    h_temp.SetBinContent(6, source_content_6)
    
    h_temp.SetLineColor(ROOT.kBlack)
    h_temp.SetLineWidth(2)
    h_temp.Draw("HIST SAME")
    
    canv.SetLogy()
    # Shift multiplier position
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")

    #leg = CMS.cmsLeg(0.5, 0.1, 0.98, 0.5, textSize=0.04)
    return canv

def plot_cut_flow(h_temp, h_0, h_cut, h_10_per_100, h_5_per_100, h_1_per_100, h_1_per_1000, canv_name = "canv" ):
    canv = ROOT.TCanvas(canv_name, canv_name, 800, 600)
    if h_0==0:
        h_temp.GetXaxis().SetBinLabel(1, "preselection")
    else:
        h_temp.GetXaxis().SetBinLabel(1, "no selection")
    h_temp.GetXaxis().SetBinLabel(2, "preselection")
    h_temp.GetXaxis().SetBinLabel(3, f"10% ")
    h_temp.GetXaxis().SetBinLabel(4, f"5% ")
    h_temp.GetXaxis().SetBinLabel(5, f"1% ")
    h_temp.GetXaxis().SetBinLabel(6, f"0.1% ")


    source_bin = 1
    if h_0==0:
        source_content_1 = h_cut.GetBinContent(source_bin)
    else:
        source_content_1 = h_0.GetBinContent(source_bin)
    h_temp.SetBinContent(1, source_content_1)

    source_content_2 = h_cut.GetBinContent(source_bin)
    h_temp.SetBinContent(2, source_content_2)

    source_content_3 = h_10_per_100.GetBinContent(source_bin)
    h_temp.SetBinContent(3, source_content_3)
    
    source_content_4 = h_5_per_100.GetBinContent(source_bin)
    h_temp.SetBinContent(4, source_content_4)

    source_content_5 = h_1_per_100.GetBinContent(source_bin)
    h_temp.SetBinContent(5,  source_content_5)

    source_content_6 = h_1_per_1000.GetBinContent(source_bin)
    h_temp.SetBinContent(6, source_content_6)
    
    h_temp.SetLineColor(ROOT.kBlue)
    h_temp.SetLineWidth(2)
    h_temp.SetStats(0)
    h_temp.Draw("HISTO")
    
    canv.SetLogy()
    
    return canv


def plot_comparison(keys, h_temp, h_comparison, canv_name = "canv"):
    canv = ROOT.TCanvas(canv_name, canv_name, 800, 600)
    canv.SetBottomMargin(0.2)   
    h_temp.GetXaxis().SetTitle("Model")
    h_temp.GetXaxis().SetTitleOffset(0.5)
    h_temp.GetYaxis().SetTitle("Event Number #")
    for i,key in enumerate(keys):
        h_temp.GetXaxis().SetBinLabel(i+1, f"{key}")
        h_temp.SetBinContent(i+1, h_comparison[key].GetBinContent(1))
    '''
    h_temp.GetXaxis().SetBinLabel(1, f"{keys[0]}")
    h_temp.GetXaxis().SetBinLabel(2, f"{keys[1]}")
    h_temp.GetXaxis().SetBinLabel(3, f"{keys[2]}")
    h_temp.GetXaxis().SetBinLabel(4, f"{keys[3]}")
    h_temp.GetXaxis().SetBinLabel(5, f"{keys[4]}")
    h_temp.GetXaxis().SetBinLabel(6, f"{keys[5]}")
    #h_temp.GetXaxis().SetBinLabel(7, f"{keys[6]}")
    #hist.SetMaximum(35)
    h_temp.SetBinContent(1, h_comparison[keys[0]].GetBinContent(1))
    print(f"\nl'histo è: {h_comparison[keys[0]]}","\ncon valore:",h_temp.GetBinContent(1))
    h_temp.SetBinContent(2, h_comparison[keys[1]].GetBinContent(1))
    print(f"\nl'histo è: {h_comparison[keys[1]]}","\ncon valore:",h_temp.GetBinContent(2))
    h_temp.SetBinContent(3, h_comparison[keys[2]].GetBinContent(1))
    print(f"\nl'histo è: {h_comparison[keys[2]]}","\ncon valore:",h_temp.GetBinContent(3))
    h_temp.SetBinContent(4, h_comparison[keys[3]].GetBinContent(1))
    print(f"\nl'histo è: {h_comparison[keys[3]]}","\ncon valore:",h_temp.GetBinContent(4))
    h_temp.SetBinContent(5, h_comparison[keys[4]].GetBinContent(1))
    print(f"\nl'histo è: {h_comparison[keys[4]]}","\ncon valore:",h_temp.GetBinContent(5))
    h_temp.SetBinContent(6, h_comparison[keys[5]].GetBinContent(1))
    print(f"\nl'histo è: {h_comparison[keys[5]]}","\ncon valore:",h_temp.GetBinContent(6))
    '''
    #h_temp.SetBinContent(7, h_comparison[keys[6]].GetBinContent(1))
    #print(f"\nl'histo è: {h_comparison[keys[6]]}","\ncon valore:",h_temp.GetBinContent(7))
    h_temp.SetStats(0)
    h_temp.SetLineColor(ROOT.kBlue)
    h_temp.SetLineWidth(2)
    h_temp.Draw("HISTO")
    canv.SetLogy()
    return canv

dirpath = "/eos/user/f/fsalerno/Evaluation/Prelim"
path_to_graphic_folder = "/eos/user/f/fsalerno/Evaluation/cut_flow"
file_name_sign="cut_flow_histos_presel_sign.root"
file_name_bkg="cut_flow_histos_presel_bkg.root"
inFile_sign = f"{dirpath}/{file_name_sign}"
histos_file_sign = ROOT.TFile.Open(inFile_sign)
cartella_sign = histos_file_sign.Get("cut_flow_sign")
inFile_bkg = f"{dirpath}/{file_name_bkg}"
histos_file_bkg = ROOT.TFile.Open(inFile_bkg)
cartella_bkg = histos_file_bkg.Get("cut_flow_bkg")
print(cartella_sign.ls())
keys = ["TROTA","60_CNN_2D_old_truth_0_pt","60_CNN_2D_LSTM_old_truth_0_pt","60_CNN_2D_new_truth_0_pt","60_CNN_2D_LSTM_new_truth_0_pt","60_CNN_2D_2_0_pt"]
h_nevents_1_per_100_sign = {}
h_nevents_1_per_1000_sign = {}
h_nevents_5_per_100_sign = {}
h_nevents_10_per_100_sign = {}
h_nevents_1_per_100_bkg = {}
h_nevents_1_per_1000_bkg = {}
h_nevents_5_per_100_bkg = {}
h_nevents_10_per_100_bkg = {}

for key in keys:
    #print(f"nevents_10_per_100_{key}")
    h_nevents_10_per_100_sign[key] = histos_file_sign.Get(f"cut_flow_sign/nevents_10_per_100_{key}") ###NIENTE h nel nome
    h_nevents_5_per_100_sign[key] = histos_file_sign.Get(f"cut_flow_sign/nevents_5_per_100_{key}")
    h_nevents_1_per_100_sign[key] = histos_file_sign.Get(f"cut_flow_sign/nevents_1_per_100_{key}")
    h_nevents_1_per_1000_sign[key] = histos_file_sign.Get(f"cut_flow_sign/nevents_1_per_1000_{key}")

    h_nevents_10_per_100_bkg[key] = histos_file_bkg.Get(f"cut_flow_bkg/nevents_10_per_100_{key}") ###NIENTE h nel nome
    h_nevents_5_per_100_bkg[key] = histos_file_bkg.Get(f"cut_flow_bkg/nevents_5_per_100_{key}")
    h_nevents_1_per_100_bkg[key] = histos_file_bkg.Get(f"cut_flow_bkg/nevents_1_per_100_{key}")
    h_nevents_1_per_1000_bkg[key] = histos_file_bkg.Get(f"cut_flow_bkg/nevents_1_per_1000_{key}")

print(f"Sign 10% TROTA:",h_nevents_10_per_100_sign["TROTA"].GetBinContent(1))
print(f"Sign 5% TROTA:",h_nevents_5_per_100_sign["TROTA"].GetBinContent(1))
print(f"Sign 1% TROTA:",h_nevents_1_per_100_sign["TROTA"].GetBinContent(1))
print(f"Sign 0.1% TROTA:",h_nevents_1_per_1000_sign["TROTA"].GetBinContent(1))
print(f"Sign 10% 60_CNN_2D_2_0_pt:",h_nevents_10_per_100_sign["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Sign 5% 60_CNN_2D_2_0_pt:",h_nevents_5_per_100_sign["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Sign 1% 60_CNN_2D_2_0_pt:",h_nevents_1_per_100_sign["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Sign 0.1% 60_CNN_2D_2_0_pt:",h_nevents_1_per_1000_sign["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Sign 10% 60_CNN_2D_new_truth_0_pt:",h_nevents_10_per_100_sign["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Sign 5% 60_CNN_2D_new_truth_0_pt:",h_nevents_5_per_100_sign["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Sign 1% 60_CNN_2D_new_truth_0_pt:",h_nevents_1_per_100_sign["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Sign 0.1% 60_CNN_2D_new_truth_0_pt:",h_nevents_1_per_1000_sign["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))

print(f"Ratio sign 10% TROTA/60_CNN_2D_2_0_pt:",h_nevents_10_per_100_sign["TROTA"].GetBinContent(1)/h_nevents_10_per_100_sign["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Ratio sign 5% TROTA/60_CNN_2D_2_0_pt:",h_nevents_5_per_100_sign["TROTA"].GetBinContent(1)/h_nevents_5_per_100_sign["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Ratio sign 1% TROTA/60_CNN_2D_2_0_pt:",h_nevents_1_per_100_sign["TROTA"].GetBinContent(1)/h_nevents_1_per_100_sign["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Ratio sign 0.1% TROTA/60_CNN_2D_2_0_pt:",h_nevents_1_per_1000_sign["TROTA"].GetBinContent(1)/h_nevents_1_per_1000_sign["60_CNN_2D_2_0_pt"].GetBinContent(1))

print(f"Ratio sign 10% TROTA/60_CNN_2D_new_truth_0_pt:",h_nevents_10_per_100_sign["TROTA"].GetBinContent(1)/h_nevents_10_per_100_sign["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Ratio sign 5% TROTA/60_CNN_2D_new_truth_0_pt:",h_nevents_5_per_100_sign["TROTA"].GetBinContent(1)/h_nevents_5_per_100_sign["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Ratio sign 1% TROTA/60_CNN_2D_new_truth_0_pt:",h_nevents_1_per_100_sign["TROTA"].GetBinContent(1)/h_nevents_1_per_100_sign["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Ratio sign 0.1% TROTA/60_CNN_2D_new_truth_0_pt:",h_nevents_1_per_1000_sign["TROTA"].GetBinContent(1)/h_nevents_1_per_1000_sign["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))

print(f"Bkg 10% TROTA:",h_nevents_10_per_100_bkg["TROTA"].GetBinContent(1))
print(f"Bkg 5% TROTA:",h_nevents_5_per_100_bkg["TROTA"].GetBinContent(1))
print(f"Bkg 1% TROTA:",h_nevents_1_per_100_bkg["TROTA"].GetBinContent(1))
print(f"Bkg 0.1% TROTA:",h_nevents_1_per_1000_bkg["TROTA"].GetBinContent(1))
print(f"Bkg 10% 60_CNN_2D_2_0_pt:",h_nevents_10_per_100_bkg["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Bkg 5% 60_CNN_2D_2_0_pt:",h_nevents_5_per_100_bkg["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Bkg 1% 60_CNN_2D_2_0_pt:",h_nevents_1_per_100_bkg["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Bkg 0.1% 60_CNN_2D_2_0_pt:",h_nevents_1_per_1000_bkg["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Bkg 10% 60_CNN_2D_new_truth_0_pt:",h_nevents_10_per_100_bkg["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Bkg 5% 60_CNN_2D_new_truth_0_pt:",h_nevents_5_per_100_bkg["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Bkg 1% 60_CNN_2D_new_truth_0_pt:",h_nevents_1_per_100_bkg["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Bkg 0.1% 60_CNN_2D_new_truth_0_pt:",h_nevents_1_per_1000_bkg["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))

print(f"Ratio bkg 10% TROTA/60_CNN_2D_2_0_pt:",h_nevents_10_per_100_bkg["TROTA"].GetBinContent(1)/h_nevents_10_per_100_bkg["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Ratio bkg 5% TROTA/60_CNN_2D_2_0_pt:",h_nevents_5_per_100_bkg["TROTA"].GetBinContent(1)/h_nevents_5_per_100_bkg["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Ratio bkg 1% TROTA/60_CNN_2D_2_0_pt:",h_nevents_1_per_100_bkg["TROTA"].GetBinContent(1)/h_nevents_1_per_100_bkg["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Ratio bkg 0.1% TROTA/60_CNN_2D_2_0_pt:",h_nevents_1_per_1000_bkg["TROTA"].GetBinContent(1)/h_nevents_1_per_1000_bkg["60_CNN_2D_2_0_pt"].GetBinContent(1))

print(f"Ratio bkg 10% TROTA/60_CNN_2D_new_truth_0_pt:",h_nevents_10_per_100_bkg["TROTA"].GetBinContent(1)/h_nevents_10_per_100_bkg["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Ratio bkg 5% TROTA/60_CNN_2D_new_truth_0_pt:",h_nevents_5_per_100_bkg["TROTA"].GetBinContent(1)/h_nevents_5_per_100_bkg["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Ratio bkg 1% TROTA/60_CNN_2D_new_truth_0_pt:",h_nevents_1_per_100_bkg["TROTA"].GetBinContent(1)/h_nevents_1_per_100_bkg["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Ratio bkg 0.1% TROTA/60_CNN_2D_new_truth_0_pt:",h_nevents_1_per_1000_bkg["TROTA"].GetBinContent(1)/h_nevents_1_per_1000_bkg["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))

print(f"Ratio sign/bkg 10% TROTA:",h_nevents_10_per_100_sign["TROTA"].GetBinContent(1)/h_nevents_10_per_100_bkg["TROTA"].GetBinContent(1))
print(f"Ratio sign/bkg 5% TROTA:",h_nevents_5_per_100_sign["TROTA"].GetBinContent(1)/h_nevents_5_per_100_bkg["TROTA"].GetBinContent(1))
print(f"Ratio sign/bkg 1% TROTA:",h_nevents_1_per_100_sign["TROTA"].GetBinContent(1)/h_nevents_1_per_100_bkg["TROTA"].GetBinContent(1))
print(f"Ratio sign/bkg 0.1% TROTA:",h_nevents_1_per_1000_sign["TROTA"].GetBinContent(1)/h_nevents_1_per_1000_bkg["TROTA"].GetBinContent(1))

print(f"Ratio sign/bkg 10% 60_CNN_2D_2_0_pt:",h_nevents_10_per_100_sign["60_CNN_2D_2_0_pt"].GetBinContent(1)/h_nevents_10_per_100_bkg["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Ratio sign/bkg 5% 60_CNN_2D_2_0_pt:",h_nevents_5_per_100_sign["60_CNN_2D_2_0_pt"].GetBinContent(1)/h_nevents_5_per_100_bkg["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Ratio sign/bkg 1% 60_CNN_2D_2_0_pt:",h_nevents_1_per_100_sign["60_CNN_2D_2_0_pt"].GetBinContent(1)/h_nevents_1_per_100_bkg["60_CNN_2D_2_0_pt"].GetBinContent(1))
print(f"Ratio sign/bkg 0.1% 60_CNN_2D_2_0_pt:",h_nevents_1_per_1000_sign["60_CNN_2D_2_0_pt"].GetBinContent(1)/h_nevents_1_per_1000_bkg["60_CNN_2D_2_0_pt"].GetBinContent(1))

print(f"Ratio sign/bkg 10% 60_CNN_2D_new_truth_0_pt:",h_nevents_10_per_100_sign["60_CNN_2D_new_truth_0_pt"].GetBinContent(1)/h_nevents_10_per_100_bkg["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Ratio sign/bkg 5% 60_CNN_2D_new_truth_0_pt:",h_nevents_5_per_100_sign["60_CNN_2D_new_truth_0_pt"].GetBinContent(1)/h_nevents_5_per_100_bkg["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Ratio sign/bkg 1% 60_CNN_2D_new_truth_0_pt:",h_nevents_1_per_100_sign["60_CNN_2D_new_truth_0_pt"].GetBinContent(1)/h_nevents_1_per_100_bkg["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))
print(f"Ratio sign/bkg 0.1% 60_CNN_2D_new_truth_0_pt:",h_nevents_1_per_1000_sign["60_CNN_2D_new_truth_0_pt"].GetBinContent(1)/h_nevents_1_per_1000_bkg["60_CNN_2D_new_truth_0_pt"].GetBinContent(1))

h_0_sign = ROOT.TH1F("h_0_sign", "eventi iniziali segnale", 1, 0, 1)
h_0_sign.SetBinContent(1, 100000) #per ora mentre aspetto che giri la statistica
h_nevents_no_score_cut_sign = histos_file_sign.Get(f"cut_flow_sign/nevents_no_score_cut")
h_0_bkg = ROOT.TH1F("h_0_bkg", "eventi iniziali segnale", 1, 0, 1)
h_0_bkg.SetBinContent(1, 16000000) #per ora mentre aspetto che giri la statistica
h_nevents_no_score_cut_bkg = histos_file_bkg.Get(f"cut_flow_bkg/nevents_no_score_cut")
#print(h_nevents_no_score_cut)

c_cut_flow_sign={}
for key in keys:
    n_bins = len(keys)
    h_cut_flow = ROOT.TH1F("h_cut_flow", "cut_flow",6, 0, 6)
    h_cut_flow.SetMaximum(h_nevents_no_score_cut_sign.GetBinContent(1)*1.1)
    h_cut_flow.SetMinimum(h_nevents_no_score_cut_sign.GetBinContent(1)/100)
    h_cut_flow.SetTitle(f"Cut flow for {key}")
    h_cut_flow.GetXaxis().SetTitle("Cuts")
    h_cut_flow.GetYaxis().SetTitle("Event Number #")
    c_cut_flow_sign[key]=plot_cut_flow( h_temp=h_cut_flow, h_0=h_0_sign, h_cut=h_nevents_no_score_cut_sign, h_10_per_100=h_nevents_10_per_100_sign[key], h_5_per_100=h_nevents_5_per_100_sign[key], h_1_per_100=h_nevents_1_per_100_sign[key], h_1_per_1000=h_nevents_1_per_1000_sign[key], canv_name=f"c_cut_flow_sign_{key}") 
    c_cut_flow_sign[key].SaveAs(f"{path_to_graphic_folder}/cut_flow_sign_{key}.png")
    c_cut_flow_sign[key]=plot_cut_flow( h_temp=h_cut_flow, h_0=0, h_cut=h_nevents_no_score_cut_sign, h_10_per_100=h_nevents_10_per_100_sign[key], h_5_per_100=h_nevents_5_per_100_sign[key], h_1_per_100=h_nevents_1_per_100_sign[key], h_1_per_1000=h_nevents_1_per_1000_sign[key], canv_name=f"c_cut_flow_sign_{key}") 
    c_cut_flow_sign[key].SaveAs(f"{path_to_graphic_folder}/cut_flow_sign_{key}_no_h_0.png")
   
c_cut_flow_bkg={}
for key in keys:
    h_cut_flow = ROOT.TH1F("h_cut_flow", "cut_flow",6, 0, 6)
    h_cut_flow.SetMaximum(h_nevents_no_score_cut_bkg.GetBinContent(1)*1.1)
    h_cut_flow.SetMinimum(h_nevents_no_score_cut_bkg.GetBinContent(1)/10000)
    h_cut_flow.SetTitle(f"Cut flow for {key}")
    h_cut_flow.GetXaxis().SetTitle("Cuts")
    h_cut_flow.GetYaxis().SetTitle("Event Number #")
    c_cut_flow_bkg[key]=plot_cut_flow( h_temp=h_cut_flow, h_0=h_0_bkg, h_cut=h_nevents_no_score_cut_bkg, h_10_per_100=h_nevents_10_per_100_bkg[key], h_5_per_100=h_nevents_5_per_100_bkg[key], h_1_per_100=h_nevents_1_per_100_bkg[key], h_1_per_1000=h_nevents_1_per_1000_bkg[key], canv_name=f"c_cut_flow_bkg_{key}") 
    c_cut_flow_bkg[key].SaveAs(f"{path_to_graphic_folder}/cut_flow_bkg_{key}.png")
    c_cut_flow_bkg[key]=plot_cut_flow( h_temp=h_cut_flow, h_0=0, h_cut=h_nevents_no_score_cut_bkg, h_10_per_100=h_nevents_10_per_100_bkg[key], h_5_per_100=h_nevents_5_per_100_bkg[key], h_1_per_100=h_nevents_1_per_100_bkg[key], h_1_per_1000=h_nevents_1_per_1000_bkg[key], canv_name=f"c_cut_flow_bkg_{key}") 
    c_cut_flow_bkg[key].SaveAs(f"{path_to_graphic_folder}/cut_flow_bkg_{key}_no_h_0.png")

h_temp = ROOT.TH1F("h_comparison", "comparison", 7, 0, 7)
h_temp.SetMaximum(h_nevents_no_score_cut_sign.GetBinContent(1)*1.1)
h_temp.SetMinimum(h_nevents_no_score_cut_sign.GetBinContent(1)/100)
h_temp.SetTitle(f"Comparison for 10% cut")
c_comparison = plot_comparison(keys=keys, h_temp=h_temp, h_comparison=h_nevents_10_per_100_sign, canv_name="c_comparison_10_per_100_sign")
c_comparison.SaveAs(f"{path_to_graphic_folder}/comparison_10_per_100_sign.png")

h_temp.SetTitle(f"Comparison for 5% cut")
c_comparison = plot_comparison(keys=keys, h_temp=h_temp, h_comparison=h_nevents_5_per_100_sign, canv_name="c_comparison_5_per_100_sign")
c_comparison.SaveAs(f"{path_to_graphic_folder}/comparison_5_per_100_sign.png")

h_temp.SetTitle(f"Comparison for 1% cut")
c_comparison = plot_comparison(keys=keys, h_temp=h_temp, h_comparison=h_nevents_1_per_100_sign, canv_name="c_comparison_1_per_100_sign")
c_comparison.SaveAs(f"{path_to_graphic_folder}/comparison_1_per_100_sign.png")

h_temp.SetTitle(f"Comparison for 0.1% cut")
c_comparison = plot_comparison(keys=keys, h_temp=h_temp, h_comparison=h_nevents_1_per_1000_sign, canv_name="c_comparison_1_per_1000_sign")
c_comparison.SaveAs(f"{path_to_graphic_folder}/comparison_1_per_1000_sign.png")


h_temp = ROOT.TH1F("h_comparison", "comparison", 7, 0, 7)
h_temp.SetMaximum(h_nevents_no_score_cut_bkg.GetBinContent(1)*1.1)
h_temp.SetMinimum(h_nevents_no_score_cut_bkg.GetBinContent(1)/1000)
h_temp.SetTitle(f"Comparison for 10% cut")
c_comparison = plot_comparison(keys=keys, h_temp=h_temp, h_comparison=h_nevents_10_per_100_bkg, canv_name="c_comparison_10_per_100_bkg")
c_comparison.SaveAs(f"{path_to_graphic_folder}/comparison_10_per_100_bkg.png")

h_temp.SetTitle(f"Comparison for 5% cut")
c_comparison = plot_comparison(keys=keys, h_temp=h_temp, h_comparison=h_nevents_5_per_100_bkg, canv_name="c_comparison_5_per_100_bkg")
c_comparison.SaveAs(f"{path_to_graphic_folder}/comparison_5_per_100_bkg.png")

h_temp.SetTitle(f"Comparison for 1% cut")
c_comparison = plot_comparison(keys=keys, h_temp=h_temp, h_comparison=h_nevents_1_per_100_bkg, canv_name="c_comparison_1_per_100_bkg")
c_comparison.SaveAs(f"{path_to_graphic_folder}/comparison_1_per_100_bkg.png")

h_temp.SetTitle(f"Comparison for 0.1% cut")
c_comparison = plot_comparison(keys=keys, h_temp=h_temp, h_comparison=h_nevents_1_per_1000_bkg, canv_name="c_comparison_1_per_1000_bkg")
c_comparison.SaveAs(f"{path_to_graphic_folder}/comparison_1_per_1000_bkg.png")

"""
c_cut_flow[key].Draw("same")
c_cut_flow[key].SaveAs(f"{path_to_graphic_folder}/cut_flow_{key}_no_h_0.png")
    h_cut_flow.Draw("HIST")

    c_cut_flow[key].SaveAs(f"{path_to_graphic_folder}/cut_flow_{key}_no_h_0.png")


h_comparison = ROOT.TH1F("h_comparison", "comparison", 6, 0, 6)
h_cut_flow.SetTitle(f"Cut flow for {key}")
h_cut_flow.GetXaxis().SetTitle("Cuts")
h_cut_flow.GetYaxis().SetTitle("Event Number #")
#print("key nel plotter", key)
c_cut_flow[key]=plot_comparison(h_temp=h_cut_flow, h_cut=h_nevents_10_per_100_sign, canv_name=f"c_comparison_10_per_100_sign") 

c_cut_flow[key].Draw("same")

"""

























