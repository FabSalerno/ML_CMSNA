import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import matplotlib.pyplot as plt
import json

filepath = "/eos/user/f/fsalerno/FPR_PNet.root"
infile = ROOT.TFile.Open(filepath)
h_score_top_merged_false_tot = infile.Get("score_top_merged_false_tot")


FPR_merged = []
FPR_merged_res = []
score_merged = []
score_merged_res = []

print("integral",h_score_top_merged_false_tot.Integral(-1,101),"getentries",h_score_top_merged_false_tot.GetEntries())
#faccio il for al contrario così inizio da score alti e TPR e FPR bassi
for bin in range (101,-1,-1):
    #se lo score tresh è 0 il TPR è 1
    FPR=0
    if h_score_top_merged_false_tot.Integral(-1,101) !=0:
        FPR = h_score_top_merged_false_tot.Integral(bin,101)/h_score_top_merged_false_tot.GetEntries()
        #print("FPR",FPR)

    else:
        FPR = 0
    score = h_score_top_merged_false_tot.GetBinCenter(bin)

    FPR_merged.append(FPR)
  
    score_merged.append(score)
    
    

for i, fpr in enumerate(FPR_merged):
    if fpr>=0.01:
        print("FPR:",fpr,"\n", "Thr:",score_merged[i])
        break


#