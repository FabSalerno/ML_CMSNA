import ROOT, os, copy
import cmsstyle as CMS
import optparse
from array import array
import matplotlib.pyplot as plt
import mplhep as hep
import ROOT
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
    pad = ROOT.gPad
    margin = pad.GetRightMargin()
    pad.SetRightMargin(margin+0.01)
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
    #CMS.cmsDraw(h1, "" ,lcolor = fillcolor, mcolor = fillcolor, fcolor = ROOT.kWhite, lwidth=2)
    return canv

usage = 'python3 GenJetGenTopMatchPlot.py'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--inputFile', dest='inputFile', type=str, default = '', help='Please enter the sample')
# parser.add_option('-o','--outputFolder', dest='outputFolder', type = str, default="/eos/home-a/acagnott/www/", help='default save all plots in eos/../www/')
(opt, args) = parser.parse_args()

sample = opt.inputFile #"ttsemilep" "Zprime"
year = 2018
if year == 2018:
    histos_file = ROOT.TFile.Open(f"/eos/user/f/fsalerno/Evaluation/TROTA_2018_studies/Histo_files/output_GenJetGenTopMatchStudy_{sample}_noResinMix.root")
    output_dir = "/eos/user/f/fsalerno/Evaluation/TROTA_2018_studies/genjet_genTopMatch_plots_official"
    if not os.path.exists(output_dir):  
        os.makedirs(output_dir)
elif year == 2022:
    histos_file = ROOT.TFile.Open(f"/eos/user/f/fsalerno/Evaluation/TROTA_2022_studies/Histo_files/output_GenJetGenTopMatchStudy_{sample}_noResinMix.root")
    output_dir = "/eos/user/f/fsalerno/Evaluation/TROTA_2022_studies/genjet_genTopMatch_plots_official"
    if not os.path.exists(output_dir):  
        os.makedirs(output_dir)



keys=["50_100", "100_200", "200_10000", "inclusive"]
h_gentopgenminjet_pt = {}
h_gentopgenmidjet_pt = {}
h_gentopgenmaxjet_pt = {}
# h_genJet_minpt_notmatched= {}
# h_genJet_midpt_notmatched= {}
# h_genJet_maxpt_notmatched= {}
h_genJet_notmatched_pt = {}
h_genjet_pt = histos_file.Get(f"h_genjet_pt")
tot_entries = 0
#print(histos_file.ls())
for key in keys:
    print(key)
    h_gentopgenminjet_pt[key] = histos_file.Get(f"h_gentopgenminjet_pt_{key}")
    h_gentopgenmidjet_pt[key] = histos_file.Get(f"h_gentopgenmidjet_pt_{key}")
    h_gentopgenmaxjet_pt[key] = histos_file.Get(f"h_gentopgenmaxjet_pt_{key}")
    h_genJet_notmatched_pt[key] = histos_file.Get(f"h_genJet_notmatched_pt_{key}")
    # h_genJet_minpt_notmatched[key] = histos_file.Get(f"h_genJet_minpt_notmatched_{key}")
    # h_genJet_midpt_notmatched[key] = histos_file.Get(f"h_genJet_midpt_notmatched_{key}")
    # h_genJet_maxpt_notmatched[key] = histos_file.Get(f"h_genJet_maxpt_notmatched_{key}")
    # h_genJet_notmatched_total[key] = h_genJet_minpt_notmatched[key].Clone()
    # h_genJet_notmatched_total[key].Add(h_genJet_midpt_notmatched[key])
    # h_genJet_notmatched_total[key].Add(h_genJet_maxpt_notmatched[key])
    # print(h_gentopgenminjet_pt[key].GetEntries())
    # print(h_gentopgenmidjet_pt[key].GetEntries())
    # print(h_gentopgenmaxjet_pt[key].GetEntries())
    # print(h_genJet_notmatched_pt[key].GetEntries())
    tot_entries += h_gentopgenmaxjet_pt[key].GetEntries()+h_gentopgenminjet_pt[key].GetEntries()+h_gentopgenmidjet_pt[key].GetEntries()+h_genJet_notmatched_pt[key].GetEntries()
    print(tot_entries, h_genjet_pt.GetEntries())
    #print(h_genJet_notmatched_pt[key].GetEntries())

    # h_genJet_minpt_notmatched[key].Reset()
    # h_genJet_midpt_notmatched[key].Reset()
    # h_genJet_maxpt_notmatched[key].Reset()
colors = [ ROOT.TColor.GetColor("#5790fc"), ROOT.TColor.GetColor("#f89c20"),  ROOT.TColor.GetColor("#e42536"), ROOT.TColor.GetColor("#964a8b")]
print(tot_entries, h_genjet_pt.GetEntries())
n_top_exc = 0
n_top_tot = 0
n_genjet_exc = 0
n_genjet_tot = 0
c={}
for  key in  keys:
    h_minjet = h_gentopgenminjet_pt[key]
    h_midjet = h_gentopgenmidjet_pt[key]
    h_maxjet = h_gentopgenmaxjet_pt[key]
    h_nomatch = h_genJet_notmatched_pt[key]

    bin_25_matched = h_minjet.FindBin(25)
    print("il bin matched è", bin_25_matched)
    top_excluded = h_minjet.Integral(-1, bin_25_matched -1)
    bin_25_not_matched = h_nomatch.FindBin(25)
    print("il bin not matched è", bin_25_not_matched)
    genjet_not_matched_excluded = h_nomatch.Integral(-1, bin_25_not_matched-1)

    print(key)
    print(f"Top excluded by pt cut at 25 GeV: {top_excluded}")
    n_top_exc += top_excluded
    print(f"All tops in {key} pt range. {h_minjet.GetEntries()}")
    n_top_tot += h_minjet.GetEntries()
    print(f"Ratio: {top_excluded/h_minjet.GetEntries()}")
    print(f"Genjets not matched excluded by pt cut at 25 GeV: {genjet_not_matched_excluded}")
    n_genjet_exc += genjet_not_matched_excluded 
    print(f"All Genjets not matched in {key} pt range. {h_nomatch.GetEntries()}")
    n_genjet_tot += h_nomatch.GetEntries()
    print(f"Ratio: {genjet_not_matched_excluded/h_nomatch.GetEntries()}")




    # h_minjet.GetXaxis().SetRangeUser(0, 200)
    # h_midjet.GetXaxis().SetRangeUser(0, 200)
    # h_maxjet.GetXaxis().SetRangeUser(0, 200)
    #h_nomatch.GetXaxis().SetMaximun(200)

    h_minjet.SetMarkerStyle(1)
    h_midjet.SetMarkerStyle(1)
    h_maxjet.SetMarkerStyle(1)
    h_nomatch.SetMarkerStyle(1)
    h_minjet.SetMarkerSize(0)
    h_midjet.SetMarkerSize(0)
    h_maxjet.SetMarkerSize(0)
    h_nomatch.SetMarkerSize(0)
    h_minjet.SetLineStyle(5)
    h_midjet.SetLineStyle(1)
    h_maxjet.SetLineStyle(9)
    h_nomatch.SetLineStyle(10)
        
    h_minjet.SetMarkerColor(colors[0])
    h_midjet.SetMarkerColor(colors[1])
    h_maxjet.SetMarkerColor(colors[2])
    h_nomatch.SetMarkerColor(colors[3])
    h_minjet.SetLineColor(colors[0])
    h_minjet.SetLineWidth(2)
    h_midjet.SetLineColor(colors[1])
    h_midjet.SetLineWidth(2)
    h_maxjet.SetLineColor(colors[2])
    h_maxjet.SetLineWidth(2)
    h_nomatch.SetLineColor(colors[3])
    h_nomatch.SetLineWidth(2)
    h_minjet.SetTitle(f"GenJet pt for {key} GeV gentop pt {year}")
    h_minjet.GetYaxis().SetTitle(f"Events")
    #h_minjet.GetXaxis().SetTitle("Jet p^{ptcl}_{T}")
    h_minjet.GetXaxis().SetTitle("Jet p_{T}")
    h_minjet.SetMinimum(1)   
    h_minjet.SetMaximum(3.5*1e6*1.5)  

    #print("PROVAAAAAAAAA:", h_minjet.GetXaxis().GetXmax())
    if year==2022:    
        c[key]=plot(h_minjet, output_dir, colors[3], canv_name="genjet_pt", ytitle=h_minjet.GetYaxis().GetTitle(), sample_name=sample, energy="13.6") 
    elif year==2018:
        c[key]=plot(h_minjet, output_dir, colors[3], canv_name="genjet_pt", ytitle=h_minjet.GetYaxis().GetTitle(), sample_name=sample, energy="13") 
    c[key].SetLogy()
    line = ROOT.TLine(25, 0, 25, 3.5*1e6*1.5)  
    line.SetLineColor(ROOT.kBlack)       
    line.SetLineStyle(2)                
    line.SetLineWidth(3)    

    CMS.cmsDraw(h_minjet, "" , marker=1, msize=0, lstyle=1, lcolor = colors[0], mcolor = colors[0], fcolor = ROOT.kWhite, lwidth=2)
    CMS.cmsDraw(h_midjet, "" , marker=1, msize=0, lstyle=9, lcolor = colors[1], mcolor = colors[1], fcolor = ROOT.kWhite, lwidth=2)
    CMS.cmsDraw(h_maxjet, "" , marker=1, msize=0, lstyle=5, lcolor = colors[2], mcolor = colors[2], fcolor = ROOT.kWhite, lwidth=2)
    CMS.cmsDraw(h_nomatch, "" , marker=1, msize=0, lstyle=10, lcolor = colors[3], mcolor = colors[3], fcolor = ROOT.kWhite, lwidth=2)    
    CMS.cmsDrawLine(line, lcolor = ROOT.kBlack, lstyle=2, lwidth=2)       
   

    legend = CMS.cmsLeg(0.45, 0.65, 1.0, 0.85, textSize=0.04)

    legend.AddEntry(h_minjet, "Third-leading top matched p_{T}", "l")
    legend.AddEntry(h_midjet, "Subleading top matched p_{T}", "l")
    legend.AddEntry(h_maxjet, "Leading top matched p_{T}", "l")
    legend.AddEntry(h_nomatch, "No top matched p_{T}", "l")
    #legend.Draw()
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.04)
    latex.SetTextAlign(13)
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextAlign(11)  
    pt_extremes = key.split("_")
    if len(pt_extremes) == 2:
        if pt_extremes[1] == "10000":
            pt_range_string = f"p^{{ptcl, top}}_{{T}}>{pt_extremes[0]} GeV"
        else:
            pt_range_string = f"{pt_extremes[0]} < p^{{ptcl, top}}_{{T}} \\leq {pt_extremes[1]} GeV"
    else:
        pt_range_string = "inclusive"

    if sample == "ttsemilep":
        #sample_string = "#it{t#bar{t} #rightarrow l + jets}"
        sample_string = ""
    else:
        sample_string = sample
    #latex.DrawLatexNDC(0.20, 0.80, sample_string)
    latex.DrawLatexNDC(0.22, 0.85, pt_range_string)
    #c.SaveAs(f"{output_dir}/genjet_pt_projection_{key}.png")
    CMS.SaveCanvas(c[key], f"{output_dir}/genjet_pt_projection_{key}.pdf", close=False)
    CMS.SaveCanvas(c[key], f"{output_dir}/genjet_pt_projection_{key}.png")

print("Ratio top excluded total",n_top_exc/n_top_tot)
print("Ratio genjet excluded total",n_genjet_exc/n_genjet_tot)



def plotEfficiency(h_den, h_eff_merged, h_eff_mixed, h_eff_resolved, g_mer, g_mix, g_res, canv_name = "canv" ,extraTest="Simulation Preliminary", iPos=0, energy="13", lumi = "",  addInfo="", ytitle = "", samplelabel = "t#bar{t}", ymax=0):
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
    x_axis_name = h_den.GetXaxis().GetTitle()
    ytitle = h_den.GetYaxis().GetTitle()
    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,ytitle,square=CMS.kRectangular, extraSpace=20.0, iPos=iPos)
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
    hdf.SetTitle(h_den.GetTitle())
    #g_mer.SetMarkerSize(0)  # oppure graph.SetMarkerStyle(0)
    g_mer.SetLineColor(2) 
    # h_eff_merged.SetMarkerColor(2)
    # h_eff_merged.SetLineColor(2)
    # h_eff_merged.SetMarkerStyle(8)
      
    # h_eff_mixed.SetMarkerColor(ROOT.kOrange-2)
    # h_eff_mixed.SetLineColor(ROOT.kOrange-2)
    # h_eff_mixed.SetMarkerStyle(8)
    # #g_mix.SetMarkerSize(0)  
    # g_mix.SetLineColor(ROOT.kOrange-2)
    h_eff_resolved.SetMarkerColor(7)
    h_eff_resolved.SetLineColor(7)
    h_eff_resolved.SetMarkerStyle(8)
    #g_res.SetMarkerSize(0)
    g_res.SetLineColor(7)
    # h_eff_merged.SetTitle(h_den.GetTitle())
    # h_eff_mixed.SetTitle(h_den.GetTitle())
    h_eff_resolved.SetTitle(h_den.GetTitle())
    #print("titolo", h_den.GetTitle())
    #print("titolo_res", h_eff_resolved.GetTitle())
    # g_mer.Draw("same Z")
    # h_eff_merged.Draw("same P")
    # g_mix.Draw("same Z") 
    # h_eff_mixed.Draw("same P")
    g_res.Draw("same Z")
    h_eff_resolved.Draw("same P")


    title = h_den.GetTitle()
    if title != "":
        title_text = ROOT.TLatex()
        title_text.SetNDC()
        title_text.SetTextFont(42)
        title_text.SetTextSize(0.03)
        title_text.DrawLatex(0.35, 0.88, title)
    # canv.SetLogy()
    # Shift multiplier position
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    # leg = CMS.cmsLeg(0.5, 0.1, 0.98, 0.5, textSize=0.04)
    return canv



# from ROOT import TEfficiency

# def efficiency_calculator(h_num, h_den, h_eff):
#     if not TEfficiency.CheckConsistency(h_num, h_den):
#         raise ValueError("Inconsistent histograms: numerator and denominator must be compatible.")

#     efficiency = TEfficiency(h_num, h_den)
#     efficiency.SetStatisticOption(TEfficiency.kFCP)  # Use Clopper-Pearson for error calculation
#     efficiency.SetConfidenceLevel(0.683)  # Set confidence level for error calculation 

#     for i in range(0, h_eff.GetNbinsX() + 2):
#         num = h_num.GetBinContent(i)
#         den = h_den.GetBinContent(i)
#         eff = efficiency.GetEfficiency(i)
#         err_up = efficiency.GetEfficiencyErrorUp(i)
#         err_low = efficiency.GetEfficiencyErrorLow(i)
#         # if eff!= 1 and den != 0:
#         #     #print("num",num)
#         #     #print("den",den)
#         #     #print("eff",eff)
#         #     error = ((eff * (1-eff))/den) ** 0.5
#         #     h_eff.SetBinError(i, error)
#         # elif eff== 1:
#         #     h_eff.SetBinError(i, err_low) 
#         #     #h_eff.SetBinError(i, eff.GetEfficiencyErrorUp(i))
#         # elif den == 0:
#         #    #h_eff.SetBinError(i, 0)
#         #    h_eff.SetBinError(i, err_up)
#         h_eff.SetBinContent(i, eff)
#     return h_eff

# def make_efficiency_graph(h_num, h_den, h_eff):
#     n_bins = h_eff.GetNbinsX()
#     g = ROOT.TGraphAsymmErrors(n_bins)
#     efficiency = TEfficiency(h_num, h_den)
#     efficiency.SetStatisticOption(TEfficiency.kFCP)  # Use Clopper-Pearson for error calculation
#     efficiency.SetConfidenceLevel(0.683) 
#     efficiency_1 = TEfficiency(h_num, h_den)
#     efficiency_1.SetStatisticOption(TEfficiency.kFCP)  # Use Clopper-Pearson for error calculation
#     efficiency_1.SetConfidenceLevel(0.841)
#     point = 0
#     for i in range(1, n_bins + 1): #no over e under flow  
#         num = h_num.GetBinContent(i)
#         den = h_den.GetBinContent(i)
#         eff = efficiency.GetEfficiency(i)

        
#         err_up = efficiency_1.GetEfficiencyErrorUp(i)
#         err_low = efficiency_1.GetEfficiencyErrorLow(i)

#         err_up_1 = efficiency.GetEfficiencyErrorUp(i)
#         err_low_1 = efficiency.GetEfficiencyErrorLow(i)


#         x = h_eff.GetBinCenter(i)
#         ex = h_eff.GetBinWidth(i) / 2.0

#         g.SetPoint(point, x, eff)
#         if eff == 1:
#             g.SetPointError(point, ex, ex, err_low_1, 0)
#         elif eff == 0:
#             g.SetPointError(point, ex, ex, 0, 0)
#         else:
#             g.SetPointError(point, ex, ex, err_low, err_up)
#         point += 1

#     return g


# h_gentop_pt_matched = histos_file.Get(f"h_gentop_pt_matched")
# h_genTop_pt = histos_file.Get(f"h_gentop_pt")
# h_reco_eff = h_genTop_pt.Clone()
# g_reco_eff = ROOT.TGraphAsymmErrors()
# h_reco_eff = efficiency_calculator(h_gentop_pt_matched, h_genTop_pt, h_reco_eff)
# g_reco_eff = make_efficiency_graph(h_gentop_pt_matched, h_genTop_pt, h_reco_eff)
# c_reco_eff = plotEfficiency(h_genTop_pt, h_reco_eff, h_reco_eff, h_reco_eff, g_reco_eff, g_reco_eff, g_reco_eff, "c_reco_eff", "Work in progress", iPos=0, energy="13", lumi = "", addInfo="", ytitle = "", samplelabel = "t#bar{t}", ymax=0)
# c_reco_eff.SaveAs(f"{output_dir}/genTop_pt_efficiency.png")