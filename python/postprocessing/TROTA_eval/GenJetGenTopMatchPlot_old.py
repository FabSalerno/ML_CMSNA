import ROOT, os, copy
import cmsstyle as CMS
import optparse
from array import array
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

usage = 'python3 GenJetGenTopMatchPlot.py'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--inputFile', dest='inputFile', type=str, default = '', help='Please enter the sample')
# parser.add_option('-o','--outputFolder', dest='outputFolder', type = str, default="/eos/home-a/acagnott/www/", help='default save all plots in eos/../www/')
(opt, args) = parser.parse_args()

sample = opt.inputFile #"ttsemilep" "Zprime"

histos_file = ROOT.TFile.Open(f"/eos/user/f/fsalerno/Evaluation/TROTA_2018_studies/Histo_files/output_GenJetGenTopMatchStudy_{sample}_noResinMix.root")

output_dir = "/eos/user/f/fsalerno/Evaluation/TROTA_2018_studies/genjet_genTopMatch_plots_old"
if not os.path.exists(output_dir):  
    os.makedirs(output_dir)


def project_genjet_pt(h2, pt_min, pt_max, name_suffix):
    # Trova i bin corrispondenti all'intervallo di pt dei gentop
    bin_min = h2.GetXaxis().FindBin(pt_min)
    bin_max = h2.GetXaxis().FindBin(pt_max)
    
    # Proietta sull'asse Y (pt dei genjet) per il range di pt gentop
    h1 = h2.ProjectionY(f"projY_{name_suffix}", bin_min, bin_max)
    return h1

h2_gentopgenminjet_pt = histos_file.Get(f"h2_gentopgenminjet_pt")
h2_gentopgenmidjet_pt = histos_file.Get(f"h2_gentopgenmidjet_pt")
h2_gentopgenmaxjet_pt = histos_file.Get(f"h2_gentopgenmaxjet_pt")

h_genJet_minpt_notmathced = histos_file.Get(f"h_genJet_minpt_notmatched")
h_genJet_midpt_notmathced = histos_file.Get(f"h_genJet_minpt_notmatched")
h_genJet_maxpt_notmathced = histos_file.Get(f"h_genJet_minpt_notmatched")

h_genJet_notmatched_total = h_genJet_minpt_notmathced.Clone("h_genJet_minpt_notmathced")
h_genJet_notmatched_total.Add(h_genJet_midpt_notmathced)
h_genJet_notmatched_total.Add(h_genJet_maxpt_notmathced)

pt_ranges = [[50,100], [100,200], [200,1000]]

colors = [ ROOT.kBlue, ROOT.kYellow, ROOT.kGreen + 2, ROOT.kRed]

n_top_exc = 0
n_top_tot = 0
n_genjet_exc = 0
n_genjet_tot = 0

for i, (pt_min, pt_max) in enumerate(pt_ranges):
    h1_minjet = project_genjet_pt(h2_gentopgenminjet_pt, pt_min, pt_max, "minjet")
    h1_midjet = project_genjet_pt(h2_gentopgenmidjet_pt, pt_min, pt_max, "midjet")
    h1_maxjet = project_genjet_pt(h2_gentopgenmaxjet_pt, pt_min, pt_max, "maxjet")

    bin_25_matched = h1_minjet.FindBin(25)
    top_excluded = h1_minjet.Integral(-1, bin_25_matched)

    print(f"Top excluded by pt cut at 25 GeV: {top_excluded}")
    n_top_exc += top_excluded
    print(f"All tops in {(pt_min, pt_max)} pt range. {h1_minjet.GetEntries()}")
    n_top_tot += h1_minjet.GetEntries()
    print(f"Ratio: {top_excluded/h1_minjet.GetEntries()}")
    # print(f"Genjets not matched excluded by pt cut at 25 GeV: {genjet_not_matched_excluded}")
    # n_genjet_exc += genjet_not_matched_excluded 
    # print(f"All Genjets not matched in {key} pt range. {h_nomatch.GetEntries()}")
    # n_genjet_tot += h_nomatch.GetEntries()
    # print(f"Ratio: {genjet_not_matched_excluded/h_nomatch.GetEntries()}")

    h1_minjet.GetXaxis().SetRangeUser(0, 200)
    h1_midjet.GetXaxis().SetRangeUser(0, 200)
    h1_maxjet.GetXaxis().SetRangeUser(0, 200)
    h_genJet_notmatched_total.GetXaxis().SetRangeUser(0, 200)

    # h1_minjet.SetMarkerStyle(21)
    # h1_midjet.SetMarkerStyle(21)
    # h1_maxjet.SetMarkerStyle(21)
    # h_genJet_notmatched_total.SetMarkerStyle(21)
    # h1_minjet.SetFillColor(colors[0])
    # h1_midjet.SetFillColor(colors[1])
    # h1_maxjet.SetFillColor(colors[2])
    # h_genJet_notmatched_total.SetFillColor(colors[3])
    # h1_minjet.SetMarkerColor(colors[0])
    # h1_midjet.SetMarkerColor(colors[1])
    # h1_maxjet.SetMarkerColor(colors[2])
    # h_genJet_notmatched_total.SetMarkerColor(colors[3])
    h1_minjet.SetLineColor(colors[0])
    h1_midjet.SetLineColor(colors[1])
    h1_maxjet.SetLineColor(colors[2])
    h_genJet_notmatched_total.SetLineColor(colors[3])

    c = ROOT.TCanvas(f"c_{pt_min}_{pt_max}", f"GenJet pt projection for {pt_min}-{pt_max} GeV gentop pt", 800, 600)
    c.SetLogy()
    #h_genJet_notmatched_total.Draw("HIST")
    h1_minjet.Draw("HIST SAME")
    h1_midjet.Draw("HIST SAME")
    h1_maxjet.Draw("HIST SAME")

    legend = ROOT.TLegend(0.65, 0.7, 0.88, 0.88)  
    legend.AddEntry(h1_minjet, "Lowest top matched pt", "l")
    legend.AddEntry(h1_midjet, "Mid top matched pt", "l")
    legend.AddEntry(h1_maxjet, "Highest top matched pt", "l")
    #legend.AddEntry(h_genJet_notmatched_total, "No top matched pt", "l")
    legend.Draw()

    c.SaveAs(f"{output_dir}/genjet_pt_projection_{pt_min}_{pt_max}.png")

print("Ratio top excluded total",n_top_exc/n_top_tot)