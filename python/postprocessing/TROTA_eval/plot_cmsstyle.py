import cmsstyle as CMS
import ROOT
import optparse
from math import sqrt
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

usage = 'python3 plot_cmsstyle.py -i inputRootFile.root -o outputFolder'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--inputFile', dest='inputFile', type=str, default = '', help='Please enter a file root')
parser.add_option('-o','--outputFolder', dest='outputFolder', type = str, default="/eos/home-a/acagnott/www/", help='default save all plots in eos/../www/')
(opt, args) = parser.parse_args()

if "tthadr" in opt.inputFile: samplelabel = "t#bar{t} hadronic"
elif "Zprime500" in opt.inputFile: samplelabel = "Z' (M500GeV)"
elif "ttsemilep" in opt.inputFile: samplelabel = "t#bar{t} semilep"
elif "Zprime" in opt.inputFile: samplelabel = "Z' 4tops"

def plotEfficiency(eff, h_den, h_num, folder, fillcolor, canv_name = "canv" ,extraTest="Work in progress", iPos=0, energy="13", lumi = "",  addInfo="", ytitle = "", samplelabel = "t#bar{t}", ymax=0):
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
    # canv.SetLogy()
    # Shift multiplier position
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    # leg = CMS.cmsLeg(0.5, 0.1, 0.98, 0.5, textSize=0.04)
    return canv
    
def plot(h, folder, fillcolor, canv_name = "canv" ,extraTest="Work in progress", iPos=0, energy="13", lumi = "",  addInfo="", ytitle = "", wp = "", samplelabel = ""):

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
        latex.DrawLatexNDC(0.27, 0.77, samplelabel+", WP "+wp+"% fpr")
    CMS.cmsDraw(h1, "" ,lcolor = fillcolor, mcolor = fillcolor, fcolor = ROOT.kWhite, lwidth=2)
    return canv

def plotMassVsPt(x_min, x_max, canv_name = "canv" ,extraTest="Work in progress", iPos=0, energy="13", lumi = "",  addInfo="", ytitle = "", wp = "", samplelabel = ""):

    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)
    CMS.setCMSStyle()
    
    x_min = x_min
    x_max = x_max
    if "Top mass" in ytitle:
        y_min = 80.
        y_max = 280.
    x_axis_name = "Top p_{T} [GeV]"
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
    # ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    # leg = CMS.cmsLeg(0.5, 0.1, 0.98, 0.5, textSize=0.04)
    # CMS.cmsDraw(h1, "" ,lcolor = fillcolor, mcolor = fillcolor, fcolor = ROOT.kWhite, lwidth=2)
    return canv

def plot2D(h1, folder, canv_name = "canv2d" ,extraTest="Work in progress", iPos=0, energy="13", lumi = "",  addInfo="", ztitle="#"):

    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)
    x_min = h.GetXaxis().GetXmin()
    x_max = h.GetXaxis().GetXmax()
    y_min = h.GetYaxis().GetXmin()
    y_max = h.GetYaxis().GetXmax()
    x_axis_name = h.GetXaxis().GetTitle()
    y_axis_name = h.GetYaxis().GetTitle()
    canv = CMS.cmsCanvas(canv_name,x_min, x_max, y_min, y_max,x_axis_name,y_axis_name,square=CMS.kRectangular,extraSpace= 0.01, iPos=iPos, with_z_axis=True)
    ROOT.gStyle.SetPaintTextFormat("1.4f")
    h1.Draw("same colz")
    # Set the CMS official palette
    CMS.SetCMSPalette()
    CMS.UpdatePalettePosition(h1, canv)
    # print("saving")
    return canv

if not opt.inputFile:
    print('Please enter a file root')
    exit()

inputfile = ROOT.TFile.Open(opt.inputFile)
histograms1D = [] 
histograms2D = [] 
for key in inputfile.GetListOfKeys(): 
    obj = key.ReadObj() 
    # print(obj, isinstance(obj, ROOT.TH1), isinstance(obj, ROOT.TH2))
    if isinstance(obj, ROOT.TH1) and not isinstance(obj, ROOT.TH2): histograms1D.append(obj) 
    elif isinstance(obj, ROOT.TH2): histograms2D.append(obj)

for h in histograms2D:
    print(h.GetName())
        # h_topmixedselMedium_ptmass
    if h.Integral() == 0: continue
    canvas = plot2D(h, opt.outputFolder, canv_name=h.GetName())
    CMS.SaveCanvas(canvas, opt.outputFolder+"/"+h.GetName()+".pdf", close=False)
    CMS.SaveCanvas(canvas, opt.outputFolder+"/"+h.GetName()+".png")
for h in histograms1D:
    canvas = plot(h, opt.outputFolder, ROOT.TColor.GetColor("#f89c20"), canv_name=h.GetName())
    CMS.SaveCanvas(canvas, opt.outputFolder+"/"+h.GetName()+".pdf", close=False)
    CMS.SaveCanvas(canvas, opt.outputFolder+"/"+h.GetName()+".png")


color_mix = ROOT.TColor.GetColor("#ffa90e")
color_res = ROOT.TColor.GetColor("#92dadd")
color_mer = ROOT.TColor.GetColor("#bd1f01")
# RECO efficiency
# h_den = inputfile.Get("h_topptgen")
# h_num_mix = inputfile.Get("h_topptselectmix")
# h_num_res = inputfile.Get("h_topptselectres")
# h_num_mer = inputfile.Get("h_topptselectmer")

# efficiency_mix = ROOT.TEfficiency(h_num_mix, h_den)
# efficiency_res = ROOT.TEfficiency(h_num_res, h_den)
# efficiency_mer = ROOT.TEfficiency(h_num_mer, h_den)

# canvas_efficiency_mix = plotEfficiency(efficiency_mix, h_den, h_num_mix, opt.outputFolder, color_mix, canv_name="efficiency_mix", ytitle="Reco Efficiency", samplelabel=samplelabel)
# CMS.cmsDraw(efficiency_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# # CMS.SaveCanvas(canvas_efficiency_mix, opt.outputFolder+"/efficiency_mix.pdf")

# # canvas_efficiency_res = plotEfficiency(efficiency_res, h_den, h_num_res, opt.outputFolder, color_res, canv_name="efficiency_res", ytitle="Efficiency", samplelabel=samplelabel)
# CMS.cmsDraw(efficiency_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=1)
# CMS.cmsDraw(efficiency_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=1)
# leg = CMS.cmsLeg(0.6, 0.2, 0.88, 0.4, textSize=0.04)
# leg.AddEntry(efficiency_mer, "Merged", "l")
# leg.AddEntry(efficiency_mix, "Mixed", "l")
# leg.AddEntry(efficiency_res, "Resolved", "l")
# latex = ROOT.TLatex()
# latex.SetTextFont(42)
# latex.SetTextSize(0.04)
# latex.SetTextAlign(22)
# latex.DrawLatexNDC(0.2, 0.77, samplelabel)

# CMS.SaveCanvas(canvas_efficiency_mix, opt.outputFolder+"/efficiency_resmixmer.pdf", close=False)
# CMS.SaveCanvas(canvas_efficiency_mix, opt.outputFolder+"/efficiency_resmixmer.png")


# # RECO+tag efficiency 5%
# h_numtag_mix = inputfile.Get("h_topptgenselectLoosemix")
# h_numtag_res = inputfile.Get("h_topptgenselectLooseres")
# h_numtag_mer = inputfile.Get("h_topptgenselectLoosemer")

# efficiency_tag_mix = ROOT.TEfficiency(h_numtag_mix, h_den)
# efficiency_tag_res = ROOT.TEfficiency(h_numtag_res, h_den)
# efficiency_tag_mer = ROOT.TEfficiency(h_numtag_mer, h_den)
# canvas_efficiency_tag_mix = plotEfficiency(efficiency_tag_mix, h_den, h_numtag_mix, opt.outputFolder, color_mix, canv_name="efficiency_tag_mix", ytitle="Reco*Tagging Efficiency", samplelabel=samplelabel)
# CMS.cmsDraw(efficiency_tag_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# # CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_tag_mix.pdf")

# # canvas_efficiency_tag_res = plotEfficiency(efficiency_tag_res, h_den, h_numtag_res, opt.outputFolder, color_res, canv_name="efficiency_tag_res", ytitle="Efficiency", samplelabel=samplelabel)
# CMS.cmsDraw(efficiency_tag_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=2)
# CMS.cmsDraw(efficiency_tag_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=2)
# leg = CMS.cmsLeg(0.6, 0.2, 0.88, 0.4, textSize=0.04)
# leg.AddEntry(efficiency_tag_mer, "Merged", "l")
# leg.AddEntry(efficiency_tag_mix, "Mixed", "l")
# leg.AddEntry(efficiency_tag_res, "Resolved", "l")
# latex = ROOT.TLatex()
# latex.SetTextFont(42)
# latex.SetTextSize(0.04)
# latex.SetTextAlign(22)
# latex.DrawLatexNDC(0.2, 0.77, samplelabel)

# CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_recotag5fpr_resmixmer.pdf", close=False)
# CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_recotag5fpr_resmixmer.png")

# # RECO+tag efficiency 1%
# h_numtag_mix = inputfile.Get("h_topptgenselectMediummix")
# h_numtag_res = inputfile.Get("h_topptgenselectMediumres")
# h_numtag_mer = inputfile.Get("h_topptgenselectMediummer")

# efficiency_tag_mix = ROOT.TEfficiency(h_numtag_mix, h_den)
# efficiency_tag_res = ROOT.TEfficiency(h_numtag_res, h_den)
# efficiency_tag_mer = ROOT.TEfficiency(h_numtag_mer, h_den)
# canvas_efficiency_tag_mix = plotEfficiency(efficiency_tag_mix, h_den, h_numtag_mix, opt.outputFolder, color_mix, canv_name="efficiency_tag_mix", ytitle="Reco*Tagging Efficiency", samplelabel=samplelabel)
# CMS.cmsDraw(efficiency_tag_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# # CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_tag_mix.pdf")

# # canvas_efficiency_tag_res = plotEfficiency(efficiency_tag_res, h_den, h_numtag_res, opt.outputFolder, color_res, canv_name="efficiency_tag_res", ytitle="Efficiency", samplelabel=samplelabel)
# CMS.cmsDraw(efficiency_tag_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=2)
# CMS.cmsDraw(efficiency_tag_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=2)
# leg = CMS.cmsLeg(0.6, 0.2, 0.88, 0.4, textSize=0.04)
# leg.AddEntry(efficiency_tag_mer, "Merged", "l")
# leg.AddEntry(efficiency_tag_mix, "Mixed", "l")
# leg.AddEntry(efficiency_tag_res, "Resolved", "l")
# latex = ROOT.TLatex()
# latex.SetTextFont(42)
# latex.SetTextSize(0.04)
# latex.SetTextAlign(22)
# latex.DrawLatexNDC(0.2, 0.77, samplelabel)

# CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_recotag1fpr_resmixmer.pdf", close=False)
# CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_recotag5fpr_resmixmer.png")

# # tag efficiency
# h_numtag_mix = inputfile.Get("h_topptgenselectMediummix")
# h_numtag_mix.Divide(h_den)
# # for i in range(1, h_numtag_mix.GetNbinsX()+1): h_numtag_mix.SetBinError(i, efficiency_mix.GetEfficiencyErrorLow(i))
# h_numtag_res = inputfile.Get("h_topptgenselectMediumres")
# h_numtag_res.Divide(h_den)
# # for i in range(1, h_numtag_res.GetNbinsX()+1): h_numtag_res.SetBinError(i, efficiency_res.GetEfficiencyErrorLow(i))
# h_numtag_mer = inputfile.Get("h_topptgenselectMediummer")
# h_numtag_mer.Divide(h_den)
# # for i in range(1, h_numtag_mer.GetNbinsX()+1): h_numtag_mer.SetBinError(i, efficiency_mer.GetEfficiencyErrorLow(i))
# h_den_mix = inputfile.Get("h_topptselectmix")
# h_den_mix.Divide(h_den)
# # for i in range(1, h_den_mix.GetNbinsX()+1): h_den_mix.SetBinError(i, efficiency_mix.GetEfficiencyErrorLow(i))
# h_den_res = inputfile.Get("h_topptselectres")
# h_den_res.Divide(h_den)
# # for i in range(1, h_den_res.GetNbinsX()+1): h_den_res.SetBinError(i, efficiency_res.GetEfficiencyErrorLow(i))
# h_den_mer = inputfile.Get("h_topptselectmer")
# h_den_mer.Divide(h_den)
# # for i in range(1, h_den_mer.GetNbinsX()+1): h_den_mer.SetBinError(i, efficiency_mer.GetEfficiencyErrorLow(i))
# # for i in range(1, h_den_mer.GetNbinsX()+1): print(h_den_mer.GetBinContent(i), h_den_mer.GetBinError(i), efficiency_mer.GetEfficiencyErrorLow(i))

# # efficiency_tagger_mix = ROOT.TEfficiency(h_numtag_mix, h_den_mix)
# # efficiency_tagger_res = ROOT.TEfficiency(h_numtag_res, h_den_res)
# # efficiency_tagger_mer = ROOT.TEfficiency(h_numtag_mer, h_den_mer)
# h_numtag_mix.Divide(h_den_mix)
# h_numtag_res.Divide(h_den_res)
# h_numtag_mer.Divide(h_den_mer)
# canvas_efficiency_tag_mix = plotEfficiency(h_numtag_mix, h_den, h_numtag_mix, opt.outputFolder, color_mix, canv_name="efficiency_tagger_mix", ytitle="Tagger Efficiency", samplelabel=samplelabel)
# CMS.cmsDraw(h_numtag_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# # CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_tag_mix.pdf")

# # canvas_efficiency_tag_res = plotEfficiency(efficiency_tag_res, h_den, h_numtag_res, opt.outputFolder, color_res, canv_name="efficiency_tag_res", ytitle="Efficiency", samplelabel=samplelabel)
# CMS.cmsDraw(h_numtag_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=2)
# CMS.cmsDraw(h_numtag_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=2)
# leg = CMS.cmsLeg(0.6, 0.2, 0.88, 0.4, textSize=0.04)
# leg.AddEntry(h_numtag_mer, "Merged", "l")
# leg.AddEntry(h_numtag_mix, "Mixed", "l")
# leg.AddEntry(h_numtag_res, "Resolved", "l")
# latex = ROOT.TLatex()
# latex.SetTextFont(42)
# latex.SetTextSize(0.04)
# latex.SetTextAlign(22)
# latex.DrawLatexNDC(0.2, 0.77, samplelabel)

# CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_tagger_resmixmer.pdf", close=False)
# CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_tagger_resmixmer.png")




# canvas_wploose  = plotMassVsPt(x_min = 0, x_max = 1000, canv_name="TopMassVsPt_profile_loose",iPos=0, ytitle="Top mass [GeV]", samplelabel = samplelabel, wp = "5")
# h = inputfile.Get("h_topmixedselLoose_ptmass")
# tmp_mix = h.ProfileX()
# tmp_mix.SetErrorOption("s")
# h0 = inputfile.Get("h_topresolvedselLoose_ptmass")
# tmp_res = h0.ProfileX()
# tmp_res.SetErrorOption("s")
# h1 = inputfile.Get("h_topmergedselLoose_ptmass")
# tmp_mer = h1.ProfileX()
# tmp_mer.SetErrorOption("s")
# print(tmp_mix, tmp_res, tmp_mer)
# CMS.cmsDraw(tmp_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# CMS.cmsDraw(tmp_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=1)
# CMS.cmsDraw(tmp_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=1)
# leg = CMS.cmsLeg(0.6, 0.2, 0.88, 0.4, textSize=0.04)
# leg.AddEntry(tmp_mix, "Mixed", "l")
# leg.AddEntry(tmp_res, "Resolved", "l")
# leg.AddEntry(tmp_mer, "Merged", "l")

# latex = ROOT.TLatex()
# latex.SetTextFont(42)
# latex.SetTextSize(0.04)
# latex.SetTextAlign(22)
# latex.DrawLatexNDC(0.27, 0.2, samplelabel+", WP 5% fpr")

# CMS.SaveCanvas(canvas_wploose, opt.outputFolder+"/TopMassVsPt_profile_loose.pdf", close=False)
# CMS.SaveCanvas(canvas_wploose, opt.outputFolder+"/TopMassVsPt_profile_loose.png")


# canvas_wpmedium = plotMassVsPt(x_min = 0, x_max = 1000, canv_name="TopMassVsPt_profile_medium",iPos=0, ytitle="Top mass [GeV]", samplelabel = samplelabel, wp = "1")
# h = inputfile.Get("h_topmixedselMedium_ptmass")
# tmp_mix = h.ProfileX()
# tmp_mix.SetErrorOption("s")
# h0 = inputfile.Get("h_topresolvedselMedium_ptmass")
# tmp_res = h0.ProfileX()
# tmp_res.SetErrorOption("s")
# h1 = inputfile.Get("h_topmergedselMedium_ptmass")
# tmp_mer = h1.ProfileX()
# tmp_mer.SetErrorOption("s")
# print(tmp_mix, tmp_res, tmp_mer)
# CMS.cmsDraw(tmp_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# CMS.cmsDraw(tmp_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=1)
# CMS.cmsDraw(tmp_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=1)
# leg = CMS.cmsLeg(0.6, 0.2, 0.88, 0.4, textSize=0.04)
# leg.AddEntry(tmp_mix, "Mixed", "l")
# leg.AddEntry(tmp_res, "Resolved", "l")
# leg.AddEntry(tmp_mer, "Merged", "l")

# latex = ROOT.TLatex()
# latex.SetTextFont(42)
# latex.SetTextSize(0.04)
# latex.SetTextAlign(22)
# latex.DrawLatexNDC(0.27, 0.2, samplelabel+", WP 1% fpr")

# CMS.SaveCanvas(canvas_wpmedium, opt.outputFolder+"/TopMassVsPt_profile_medium.pdf", close=False)
# CMS.SaveCanvas(canvas_wpmedium, opt.outputFolder+"/TopMassVsPt_profile_medium.png")


# canvas_wptight  = plotMassVsPt(x_min = 0, x_max = 1000, canv_name="TopMassVsPt_profile_tight",iPos=0, ytitle="Top mass [GeV]", samplelabel = samplelabel, wp = "0.1")

# h = inputfile.Get("h_topmixedselTight_ptmass")
# tmp_mix = h.ProfileX()
# h0 = inputfile.Get("h_topresolvedselTight_ptmass")
# tmp_res = h0.ProfileX()
# h1 = inputfile.Get("h_topmergedselTight_ptmass")
# tmp_mer = h1.ProfileX()
# print(tmp_mix, tmp_res, tmp_mer)

# tmp_mix.SetErrorOption("s")
# tmp_res.SetErrorOption("s")
# tmp_mer.SetErrorOption("s")

# CMS.cmsDraw(tmp_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# CMS.cmsDraw(tmp_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=1)
# CMS.cmsDraw(tmp_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=1)

# leg = CMS.cmsLeg(0.6, 0.2, 0.88, 0.4, textSize=0.04)
# leg.AddEntry(tmp_mix, "Mixed", "l")
# leg.AddEntry(tmp_res, "Resolved", "l")
# leg.AddEntry(tmp_mer, "Merged", "l")

# latex = ROOT.TLatex()
# latex.SetTextFont(42)
# latex.SetTextSize(0.04)
# latex.SetTextAlign(22)
# latex.DrawLatexNDC(0.27, 0.2, samplelabel+", WP 0.1% fpr")

# CMS.SaveCanvas(canvas_wptight, opt.outputFolder+"/TopMassVsPt_profile_tight.pdf", close=False)
# CMS.SaveCanvas(canvas_wptight, opt.outputFolder+"/TopMassVsPt_profile_tight.png")


# PER FILE ROOT
write = False
if write:
    outputfileroot = ROOT.TFile.Open("tmpttsemilep.root", "RECREATE")
else:
    outputfileroot = ROOT.TFile.Open("tmpttsemilep.root", "update")

# RECO efficiency HIGHESTScore
h_den = inputfile.Get("h_topptgen")
h_num_mix = inputfile.Get("h_highestscoretopmixedreco_pt")
h_num_res = inputfile.Get("h_highestscoretopresolvedreco_pt")
h_num_mer = inputfile.Get("h_highestscoretopmergedreco_pt")

efficiency_mix = ROOT.TEfficiency(h_num_mix, h_den)
efficiency_res = ROOT.TEfficiency(h_num_res, h_den)
efficiency_mer = ROOT.TEfficiency(h_num_mer, h_den)

canvas_efficiency_mix = plotEfficiency(efficiency_mix, h_den, h_num_mix, opt.outputFolder, color_mix, canv_name="efficiency_mix", ytitle="Reco Efficiency", samplelabel=samplelabel)
CMS.cmsDraw(efficiency_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# CMS.SaveCanvas(canvas_efficiency_mix, opt.outputFolder+"/efficiency_mix.pdf")

# canvas_efficiency_res = plotEfficiency(efficiency_res, h_den, h_num_res, opt.outputFolder, color_res, canv_name="efficiency_res", ytitle="Efficiency", samplelabel=samplelabel)
CMS.cmsDraw(efficiency_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=1)
CMS.cmsDraw(efficiency_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=1)
leg = CMS.cmsLeg(0.6, 0.75, 0.88, 0.89, textSize=0.04)
leg.AddEntry(efficiency_mer, "Merged", "l")
leg.AddEntry(efficiency_mix, "Mixed", "l")
leg.AddEntry(efficiency_res, "Resolved", "l")
latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextSize(0.04)
latex.SetTextAlign(22)
latex.DrawLatexNDC(0.2, 0.77, samplelabel)

CMS.SaveCanvas(canvas_efficiency_mix, opt.outputFolder+"/efficiency_resmixmer_HighestScore.pdf", close=False)
CMS.SaveCanvas(canvas_efficiency_mix, opt.outputFolder+"/efficiency_resmixmer_HighestScore.png")
#  PRINT DELLE RECO PER RIPESARE LE ROC
#  for i in range(1, h_num_mix.GetNbinsX()+1):
#     print("PT bin: ",  h_num_mix.GetBinLowEdge(i), h_num_mix.GetBinWidth(i)+h_num_mix.GetBinLowEdge(i))
#     print("Reco resolved efficiency ",  efficiency_res.GetEfficiency(i))
#     print("Reco mixed efficiency ",     efficiency_mix.GetEfficiency(i))
#     print("Reco merged efficiency ",    efficiency_mer.GetEfficiency(i))

if write:
    outputfileroot.cd()
    efficiency_mix.SetName("efficiency_reco_mix")
    efficiency_mix.Write()
    efficiency_res.SetName("efficiency_reco_res")
    efficiency_res.Write()
    efficiency_mer.SetName("efficiency_reco_mer")
    efficiency_mer.Write()

# RECO+tag efficiency 1%
h_numtag_mix = inputfile.Get("h_topptgen_HighestScoreselectMedium_mix")
h_numtag_res = inputfile.Get("h_topptgen_HighestScoreselectMedium_res")
h_numtag_mer = inputfile.Get("h_topptgen_HighestScoreselectMedium_mer")

efficiency_tag_mix_1fpr = ROOT.TEfficiency(h_numtag_mix, h_den)
efficiency_tag_res_1fpr = ROOT.TEfficiency(h_numtag_res, h_den)
efficiency_tag_mer_1fpr = ROOT.TEfficiency(h_numtag_mer, h_den)
canvas_efficiency_tag_mix = plotEfficiency(efficiency_tag_mix_1fpr, h_den, h_numtag_mix, opt.outputFolder, color_mix, canv_name="efficiency_tag_mix", ytitle="Reco*Tagging Efficiency", samplelabel=samplelabel)
CMS.cmsDraw(efficiency_tag_mix_1fpr, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_tag_mix.pdf")

# canvas_efficiency_tag_res = plotEfficiency(efficiency_tag_res, h_den, h_numtag_res, opt.outputFolder, color_res, canv_name="efficiency_tag_res", ytitle="Efficiency", samplelabel=samplelabel)
CMS.cmsDraw(efficiency_tag_res_1fpr, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=2)
CMS.cmsDraw(efficiency_tag_mer_1fpr, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=2)
leg = CMS.cmsLeg(0.6, 0.75, 0.88, 0.89, textSize=0.04)
leg.AddEntry(efficiency_tag_mer_1fpr, "Merged", "l")
leg.AddEntry(efficiency_tag_mix_1fpr, "Mixed", "l")
leg.AddEntry(efficiency_tag_res_1fpr, "Resolved", "l")
latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextSize(0.04)
latex.SetTextAlign(22)
latex.DrawLatexNDC(0.3, 0.8, samplelabel+" WP 1% fpr")

CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_recotag1fpr_HighestScore.pdf", close=False)
CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_recotag1fpr_HighestScore.png")

if write:
    outputfileroot.cd()
    efficiency_tag_mix_1fpr.SetName("efficiency_recotag1fpr_mix")
    efficiency_tag_mix_1fpr.Write()
    efficiency_tag_res_1fpr.SetName("efficiency_recotag1fpr_res")
    efficiency_tag_res_1fpr.Write()
    efficiency_tag_mer_1fpr.SetName("efficiency_recotag1fpr_mer")
    efficiency_tag_mer_1fpr.Write()


# RECO+tag efficiency 5%
h_numtag_mix = inputfile.Get("h_topptgen_HighestScoreselectLoose_mix")
h_numtag_res = inputfile.Get("h_topptgen_HighestScoreselectLoose_res")
h_numtag_mer = inputfile.Get("h_topptgen_HighestScoreselectLoose_mer")

efficiency_tag_mix_5fpr = ROOT.TEfficiency(h_numtag_mix, h_den)
efficiency_tag_res_5fpr = ROOT.TEfficiency(h_numtag_res, h_den)
efficiency_tag_mer_5fpr = ROOT.TEfficiency(h_numtag_mer, h_den)
canvas_efficiency_tag_mix = plotEfficiency(efficiency_tag_mix_5fpr, h_den, h_numtag_mix, opt.outputFolder, color_mix, canv_name="efficiency_tag_mix", ytitle="Reco*Tagging Efficiency", samplelabel=samplelabel)
CMS.cmsDraw(efficiency_tag_mix_5fpr, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_tag_mix.pdf")

# canvas_efficiency_tag_res = plotEfficiency(efficiency_tag_res, h_den, h_numtag_res, opt.outputFolder, color_res, canv_name="efficiency_tag_res", ytitle="Efficiency", samplelabel=samplelabel)
CMS.cmsDraw(efficiency_tag_res_5fpr, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=2)
CMS.cmsDraw(efficiency_tag_mer_5fpr, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=2)
leg = CMS.cmsLeg(0.6, 0.75, 0.88, 0.89, textSize=0.04)
leg.AddEntry(efficiency_tag_mer_5fpr, "Merged", "l")
leg.AddEntry(efficiency_tag_mix_5fpr, "Mixed", "l")
leg.AddEntry(efficiency_tag_res_5fpr, "Resolved", "l")
latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextSize(0.04)
latex.SetTextAlign(22)
latex.DrawLatexNDC(0.3, 0.8, samplelabel+" WP 5% fpr")

CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_recotag5fpr_HighestScore.pdf", close=False)
CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_recotag5fpr_HighestScore.png")

if write:
    outputfileroot.cd()
    efficiency_tag_mix_5fpr.SetName("efficiency_recotag5fpr_mix")
    efficiency_tag_mix_5fpr.Write()
    efficiency_tag_res_5fpr.SetName("efficiency_recotag5fpr_res")
    efficiency_tag_res_5fpr.Write()
    efficiency_tag_mer_5fpr.SetName("efficiency_recotag5fpr_mer")
    efficiency_tag_mer_5fpr.Write()

# ######### PER QUALCHE MOTIVO SE FACCIO DISEGNARE INSIEME QUELLO STTO E QUESTO
############# IL SECONDO NON VIENE DISEGNATO, QUINDI COMMENTARLI UNO ALLA VOLTA
#  Tag Efficiency 1fpr
h_den = inputfile.Get("h_topptgen")

h_numtag_mix_1fpr = inputfile.Get("h_topptgen_HighestScoreselectMedium_mix")
h_numtag_mix_1fpr.Divide(h_den)
h_numtag_res_1fpr = inputfile.Get("h_topptgen_HighestScoreselectMedium_res")
h_numtag_res_1fpr.Divide(h_den)
h_numtag_mer_1fpr = inputfile.Get("h_topptgen_HighestScoreselectMedium_mer")
h_numtag_mer_1fpr.Divide(h_den)

h_den_mix_1fpr = inputfile.Get("h_highestscoretopmixedreco_pt")
h_den_mix_1fpr.Divide(h_den)
h_den_res_1fpr = inputfile.Get("h_highestscoretopresolvedreco_pt")
h_den_res_1fpr.Divide(h_den)
h_den_mer_1fpr = inputfile.Get("h_highestscoretopmergedreco_pt")
h_den_mer_1fpr.Divide(h_den)

h_numtag_mix_1fpr.Divide(h_den_mix_1fpr)
h_numtag_res_1fpr.Divide(h_den_res_1fpr)
h_numtag_mer_1fpr.Divide(h_den_mer_1fpr)
canvas_efficiency_tag1fpr = plotEfficiency(h_numtag_mix_1fpr, h_den, h_numtag_mix_1fpr, opt.outputFolder, color_mix, canv_name="efficiency_tagger1fpr", ytitle="Tagger Efficiency", samplelabel=samplelabel)
CMS.cmsDraw(h_numtag_mix_1fpr, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
CMS.cmsDraw(h_numtag_res_1fpr, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=2)
CMS.cmsDraw(h_numtag_mer_1fpr, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=2)
leg = CMS.cmsLeg(0.6, 0.75, 0.88, 0.89, textSize=0.04)
leg.AddEntry(h_numtag_mer_1fpr, "Merged", "l")
leg.AddEntry(h_numtag_mix_1fpr, "Mixed", "l")
leg.AddEntry(h_numtag_res_1fpr, "Resolved", "l")
latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextSize(0.04)
latex.SetTextAlign(22)
latex.DrawLatexNDC(0.3, 0.8, samplelabel+", WP 1% fpr")
CMS.SaveCanvas(canvas_efficiency_tag1fpr, opt.outputFolder+"/efficiency_tagger1fpr_HighestScore.pdf", close=False)
CMS.SaveCanvas(canvas_efficiency_tag1fpr, opt.outputFolder+"/efficiency_tagger1fpr_HighestScore.png")

if write:
    outputfileroot.cd()
    h_numtag_mix_1fpr.SetName("efficiency_tagger1fpr_mix")
    h_numtag_mix_1fpr.Write()
    h_numtag_res_1fpr.SetName("efficiency_tagger1fpr_res")
    h_numtag_res_1fpr.Write()
    h_numtag_mer_1fpr.SetName("efficiency_tagger1fpr_mer")
    h_numtag_mer_1fpr.Write()

#  Tag Efficiency 5fpr

# h_den = inputfile.Get("h_topptgen")

# h_numtag_mix = inputfile.Get("h_topptgen_HighestScoreselectLoose_mix")
# h_numtag_mix.Divide(h_den)
# h_numtag_res = inputfile.Get("h_topptgen_HighestScoreselectLoose_res")
# h_numtag_res.Divide(h_den)
# h_numtag_mer = inputfile.Get("h_topptgen_HighestScoreselectLoose_mer")
# h_numtag_mer.Divide(h_den)

# h_den_mix = inputfile.Get("h_highestscoretopmixedreco_pt")
# h_den_mix.Divide(h_den)
# h_den_res = inputfile.Get("h_highestscoretopresolvedreco_pt")
# h_den_res.Divide(h_den)
# h_den_mer = inputfile.Get("h_highestscoretopmergedreco_pt")
# h_den_mer.Divide(h_den)

# h_numtag_mix.Divide(h_den_mix)
# h_numtag_res.Divide(h_den_res)
# h_numtag_mer.Divide(h_den_mer)
# canvas_efficiency_tag5fpr = plotEfficiency(h_numtag_mix, h_den, h_numtag_mix, opt.outputFolder, color_mix, canv_name="efficiency_tagger5fpr", ytitle="Tagger Efficiency", samplelabel=samplelabel)
# CMS.cmsDraw(h_numtag_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# CMS.cmsDraw(h_numtag_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=2)
# CMS.cmsDraw(h_numtag_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=2)
# leg = CMS.cmsLeg(0.6, 0.75, 0.88, 0.89, textSize=0.04)
# leg.AddEntry(h_numtag_mer, "Merged", "l")
# leg.AddEntry(h_numtag_mix, "Mixed", "l")
# leg.AddEntry(h_numtag_res, "Resolved", "l")
# latex = ROOT.TLatex()
# latex.SetTextFont(42)
# latex.SetTextSize(0.04)
# latex.SetTextAlign(22)
# latex.DrawLatexNDC(0.3, 0.8, samplelabel+", WP 5% fpr")
# CMS.SaveCanvas(canvas_efficiency_tag5fpr, opt.outputFolder+"/efficiency_tagger5fpr_HighestScore.pdf", close=False)
# CMS.SaveCanvas(canvas_efficiency_tag5fpr, opt.outputFolder+"/efficiency_tagger5fpr_HighestScore.png")

if not write:
    outputfileroot.cd()
    h_numtag_mix.SetName("efficiency_tagger5fpr_mix")
    h_numtag_mix.Write()
    h_numtag_res.SetName("efficiency_tagger5fpr_res")
    h_numtag_res.Write()
    h_numtag_mer.SetName("efficiency_tagger5fpr_mer")
    h_numtag_mer.Write()


#  Pt Mass plot
canvas_wploose  = plotMassVsPt(x_min = 0, x_max = 1000, canv_name="TopMassVsPt_profile_loose",iPos=0, ytitle="Top mass [GeV]", samplelabel = samplelabel, wp = "5")
h = inputfile.Get("h_topmixedselHighestScoreLoose_ptmass")
tmp_mix = h.ProfileX()
tmp_mix.SetErrorOption("s")
h0 = inputfile.Get("h_topresolvedselHighestScoreLoose_ptmass")
tmp_res = h0.ProfileX()
tmp_res.SetErrorOption("s")
h1 = inputfile.Get("h_topmergedselHighestScoreLoose_ptmass")
tmp_mer = h1.ProfileX()
tmp_mer.SetErrorOption("s")
print(tmp_mix, tmp_res, tmp_mer)
CMS.cmsDraw(tmp_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
CMS.cmsDraw(tmp_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=1)
CMS.cmsDraw(tmp_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=1)
leg = CMS.cmsLeg(0.6, 0.2, 0.88, 0.4, textSize=0.04)
leg.AddEntry(tmp_mix, "Mixed", "l")
leg.AddEntry(tmp_res, "Resolved", "l")
leg.AddEntry(tmp_mer, "Merged", "l")

latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextSize(0.04)
latex.SetTextAlign(22)
latex.DrawLatexNDC(0.27, 0.2, samplelabel+", WP 5% fpr")

CMS.SaveCanvas(canvas_wploose, opt.outputFolder+"/TopMassVsPt_profile_loose_HighestScore.pdf", close=False)
CMS.SaveCanvas(canvas_wploose, opt.outputFolder+"/TopMassVsPt_profile_loose_HighestScore.png")

if write:
    outputfileroot.cd()
    tmp_mix.SetName("TopMassVsPt_profile_5fpr_mix")
    tmp_mix.Write()
    tmp_mer.SetName("TopMassVsPt_profile_5fpr_mer")
    tmp_mer.Write()
    tmp_res.SetName("TopMassVsPt_profile_5fpr_res")
    tmp_res.Write()


canvas_wpmedium = plotMassVsPt(x_min = 0, x_max = 1000, canv_name="TopMassVsPt_profile_medium",iPos=0, ytitle="Top mass [GeV]", samplelabel = samplelabel, wp = "1")
h = inputfile.Get("h_topmixedselHighestScoreMedium_ptmass")
tmp_mix = h.ProfileX()
tmp_mix.SetErrorOption("s")
h0 = inputfile.Get("h_topresolvedselHighestScoreMedium_ptmass")
tmp_res = h0.ProfileX()
tmp_res.SetErrorOption("s")
h1 = inputfile.Get("h_topmergedselHighestScoreMedium_ptmass")
tmp_mer = h1.ProfileX()
tmp_mer.SetErrorOption("s")
print(tmp_mix, tmp_res, tmp_mer)
CMS.cmsDraw(tmp_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
CMS.cmsDraw(tmp_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=1)
CMS.cmsDraw(tmp_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=1)
leg = CMS.cmsLeg(0.6, 0.2, 0.88, 0.4, textSize=0.04)
leg.AddEntry(tmp_mix, "Mixed", "l")
leg.AddEntry(tmp_res, "Resolved", "l")
leg.AddEntry(tmp_mer, "Merged", "l")

latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextSize(0.04)
latex.SetTextAlign(22)
latex.DrawLatexNDC(0.27, 0.2, samplelabel+", WP 1% fpr")

CMS.SaveCanvas(canvas_wpmedium, opt.outputFolder+"/TopMassVsPt_profile_medium_HighestScore.pdf", close=False)
CMS.SaveCanvas(canvas_wpmedium, opt.outputFolder+"/TopMassVsPt_profile_medium_HighestScore.png")

if write:
    outputfileroot.cd()
    tmp_mix.SetName("TopMassVsPt_profile_1fpr_mix")
    tmp_mix.Write()
    tmp_mer.SetName("TopMassVsPt_profile_1fpr_mer")
    tmp_mer.Write()
    tmp_res.SetName("TopMassVsPt_profile_1fpr_res")
    tmp_res.Write()

canvas_wptight  = plotMassVsPt(x_min = 0, x_max = 1000, canv_name="TopMassVsPt_profile_tight",iPos=0, ytitle="Top mass [GeV]", samplelabel = samplelabel, wp = "0.1")

h = inputfile.Get("h_topmixedselHighestScoreTight_ptmass")
tmp_mix = h.ProfileX()
h0 = inputfile.Get("h_topresolvedselHighestScoreTight_ptmass")
tmp_res = h0.ProfileX()
h1 = inputfile.Get("h_topmergedselHighestScoreTight_ptmass")
tmp_mer = h1.ProfileX()
print(tmp_mix, tmp_res, tmp_mer)

tmp_mix.SetErrorOption("s")
tmp_res.SetErrorOption("s")
tmp_mer.SetErrorOption("s")

CMS.cmsDraw(tmp_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
CMS.cmsDraw(tmp_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=1)
CMS.cmsDraw(tmp_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=1)


leg = CMS.cmsLeg(0.6, 0.2, 0.88, 0.4, textSize=0.04)
leg.AddEntry(tmp_mix, "Mixed", "l")
leg.AddEntry(tmp_res, "Resolved", "l")
leg.AddEntry(tmp_mer, "Merged", "l")

latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextSize(0.04)
latex.SetTextAlign(22)
latex.DrawLatexNDC(0.27, 0.2, samplelabel+", WP 0.1% fpr")

CMS.SaveCanvas(canvas_wptight, opt.outputFolder+"/TopMassVsPt_profile_tight_HighestScore.pdf", close=False)
CMS.SaveCanvas(canvas_wptight, opt.outputFolder+"/TopMassVsPt_profile_tight_HighestScore.png")

if write:
    outputfileroot.cd()
    tmp_mix.SetName("TopMassVsPt_profile_01fpr_mix")
    tmp_mix.Write()
    tmp_mer.SetName("TopMassVsPt_profile_01fpr_mer")
    tmp_mer.Write()
    tmp_res.SetName("TopMassVsPt_profile_01fpr_res")
    tmp_res.Write()


# RECO efficiency HIGHESTScore+ 3 MATCH
h_den = inputfile.Get("h_topptgen")
h_num_mix = inputfile.Get("h_highestscoretopmixedreco3match_pt")
h_num_res = inputfile.Get("h_highestscoretopresolvedreco3match_pt")
h_num_mer = inputfile.Get("h_highestscoretopmergedreco3match_pt")
#h_toppttruemer
efficiency_mix = ROOT.TEfficiency(h_num_mix, h_den)
efficiency_res = ROOT.TEfficiency(h_num_res, h_den)
efficiency_mer = ROOT.TEfficiency(h_num_mer, h_den)

canvas_efficiency_mix = plotEfficiency(efficiency_mix, h_den, h_num_mix, opt.outputFolder, color_mix, canv_name="efficiency_mix", ytitle="Reco Efficiency", samplelabel=samplelabel, ymax = 1.4)
CMS.cmsDraw(efficiency_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# CMS.SaveCanvas(canvas_efficiency_mix, opt.outputFolder+"/efficiency_mix.pdf")

# canvas_efficiency_res = plotEfficiency(efficiency_res, h_den, h_num_res, opt.outputFolder, color_res, canv_name="efficiency_res", ytitle="Efficiency", samplelabel=samplelabel)
CMS.cmsDraw(efficiency_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=1)
CMS.cmsDraw(efficiency_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=1)
leg = CMS.cmsLeg(0.6, 0.75, 0.88, 0.89, textSize=0.04)
leg.AddEntry(efficiency_mer, "Merged", "l")
leg.AddEntry(efficiency_mix, "Mixed", "l")
leg.AddEntry(efficiency_res, "Resolved", "l")
latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextSize(0.04)
latex.SetTextAlign(22)
latex.DrawLatexNDC(0.2, 0.77, samplelabel)

CMS.SaveCanvas(canvas_efficiency_mix, opt.outputFolder+"/efficiency_resmixmer_HighestScore3match.pdf", close=False)
CMS.SaveCanvas(canvas_efficiency_mix, opt.outputFolder+"/efficiency_resmixmer_HighestScore3match.png")
# PRINT per RIPESARE LE ROC
# for i in range(1, h_num_mix.GetNbinsX()+1):
#     print("PT bin: ",  h_num_mix.GetBinLowEdge(i), h_num_mix.GetBinWidth(i)+h_num_mix.GetBinLowEdge(i))
#     print("Reco resolved efficiency ",  efficiency_res.GetEfficiency(i))
#     print("Reco mixed efficiency ",     efficiency_mix.GetEfficiency(i))
#     print("Reco merged efficiency ",    efficiency_mer.GetEfficiency(i))

if write:
    outputfileroot.cd()
    efficiency_mix.SetName("efficiency_reco3match_mix")
    efficiency_mix.Write()
    efficiency_res.SetName("efficiency_reco3match_res")
    efficiency_res.Write()
    efficiency_mer.SetName("efficiency_reco3match_mer")
    efficiency_mer.Write()


# RECO+tag efficiency
h_numtag_mix = inputfile.Get("h_topptgen_HighestScore3matchselectMedium_mix") 
h_numtag_res = inputfile.Get("h_topptgen_HighestScore3matchselectMedium_res")
h_numtag_mer = inputfile.Get("h_topptgen_HighestScore3matchselectMedium_mer")

efficiency_tag_mix = ROOT.TEfficiency(h_numtag_mix, h_den)
efficiency_tag_res = ROOT.TEfficiency(h_numtag_res, h_den)
efficiency_tag_mer = ROOT.TEfficiency(h_numtag_mer, h_den)
canvas_efficiency_tag_mix = plotEfficiency(efficiency_tag_mix, h_den, h_numtag_mix, opt.outputFolder, color_mix, canv_name="efficiency_tag_mix", ytitle="Reco*Tagging Efficiency", samplelabel=samplelabel, ymax = 1.4)
CMS.cmsDraw(efficiency_tag_mix, "" ,lcolor = color_mix, mcolor = color_mix, fcolor = ROOT.kWhite, lwidth=2)
# CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_tag_mix.pdf")

# canvas_efficiency_tag_res = plotEfficiency(efficiency_tag_res, h_den, h_numtag_res, opt.outputFolder, color_res, canv_name="efficiency_tag_res", ytitle="Efficiency", samplelabel=samplelabel)
CMS.cmsDraw(efficiency_tag_res, "" ,lcolor = color_res, mcolor = color_res, fcolor = ROOT.kWhite, lwidth=2)
CMS.cmsDraw(efficiency_tag_mer, "" ,lcolor = color_mer, mcolor = color_mer, fcolor = ROOT.kWhite, lwidth=2)
leg = CMS.cmsLeg(0.6, 0.75, 0.88, 0.89, textSize=0.04)
leg.AddEntry(efficiency_tag_mer, "Merged", "l")
leg.AddEntry(efficiency_tag_mix, "Mixed", "l")
leg.AddEntry(efficiency_tag_res, "Resolved", "l")
latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextSize(0.04)
latex.SetTextAlign(22)
latex.DrawLatexNDC(0.2, 0.77, samplelabel)

CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_tag_resmixmer_HighestScore3match.pdf", close=False)
CMS.SaveCanvas(canvas_efficiency_tag_mix, opt.outputFolder+"/efficiency_tag_resmixmer_HighestScore3match.png")

if write:
    outputfileroot.cd()
    efficiency_tag_mix.SetName("efficiency_recotag3match1fpr_mix")
    efficiency_tag_mix.Write()
    efficiency_tag_res.SetName("efficiency_recotag3match1fpr_res")
    efficiency_tag_res.Write()
    efficiency_tag_mer.SetName("efficiency_recotag3match1fpr_mer")
    efficiency_tag_mer.Write()