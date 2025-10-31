#!/usr/bin/env python
import os
import sys
import ROOT
import json
ROOT.PyConfig.IgnoreCommandLineOptions = True
import matplotlib.pyplot as plt



dirpath = "/eos/user/f/fsalerno/Evaluation/thr_estimate"
path_to_graphic_folder = "/eos/user/f/fsalerno/Evaluation/thr_estimate"
file_name="fpr_TROTA_PF_wjets.root"
inFile = f"{dirpath}/{file_name}"
histos_file = ROOT.TFile.Open(inFile)
#print(histos_file.ls())
#print(histos_file.Get("fpr").ls())
#print("ENTRIES",histos_file.Get("fpr/score_CNN_2D_new_truth").GetEntries())

h_score_CNN_2D_new_truth = histos_file.Get("fpr/score_CNN_2D_new_truth")
#print("h_score_CNN_2D_new_truth",h_score_CNN_2D_new_truth.GetEntries())
h_score_CNN_2D_LSTM_new_truth = histos_file.Get("fpr/score_CNN_2D_LSTM_new_truth")
h_score_CNN_2D_old_truth = histos_file.Get("fpr/score_CNN_2D_old_truth")
#print("h_score_CNN_2D_old_truth",h_score_CNN_2D_old_truth.GetEntries())
h_score_CNN_2D_LSTM_old_truth = histos_file.Get("fpr/score_CNN_2D_LSTM_old_truth")
h_tops_counter_tot = histos_file.Get("fpr/ntop")


#CICLO FOR PER LA ROC

FPR_CNN_2D_new_truth = []
FPR_CNN_2D_LSTM_new_truth = []
score_CNN_2D_new_truth = []
score_CNN_2D_LSTM_new_truth = []
FPR_CNN_2D_old_truth = []
FPR_CNN_2D_LSTM_old_truth = []
score_CNN_2D_old_truth = []
score_CNN_2D_LSTM_old_truth = []

print("integral",h_score_CNN_2D_new_truth.Integral(-1,1001),"getentries",h_score_CNN_2D_new_truth.GetEntries(),"ntops",h_tops_counter_tot.GetEntries())
#faccio il for al contrario così inizio da score alti e TPR e FPR bassi
for bin in range (1001,-1,-1):
    #se lo score tresh è 0 il TPR è 1
    FPR_2D_new_truth=0
    if h_score_CNN_2D_new_truth.Integral(-1,1001) !=0:
        FPR_2D_new_truth = h_score_CNN_2D_new_truth.Integral(bin,1001)/h_score_CNN_2D_new_truth.GetEntries()
       

    else:
        FPR_2D_new_truth = 0
    score_2D_new_truth = h_score_CNN_2D_new_truth.GetBinCenter(bin)
    #print("bin",bin,"FPR",FPR_2D_new_truth, "score",score_2D_new_truth)
    FPR_CNN_2D_new_truth.append(FPR_2D_new_truth)
    score_CNN_2D_new_truth.append(score_2D_new_truth)
    #print("FPR",FPR_CNN_2D_new_truth)

    FPR_2D_old_truth=0
    if h_score_CNN_2D_old_truth.Integral(-1,1001) !=0:
        FPR_2D_old_truth = h_score_CNN_2D_old_truth.Integral(bin,1001)/h_score_CNN_2D_old_truth.GetEntries()
       

    else:
        FPR_2D_old_truth = 0
    score_2D_old_truth = h_score_CNN_2D_old_truth.GetBinCenter(bin)
    #print("bin",bin,"FPR",FPR_2D_old_truth, "score",score_2D_old_truth)
    FPR_CNN_2D_old_truth.append(FPR_2D_old_truth)
    score_CNN_2D_old_truth.append(score_2D_old_truth)
    #print("FPR",FPR_CNN_2D_old_truth)

    FPR_LSTM_new_truth=0
    if h_score_CNN_2D_new_truth.Integral(-1,1001) !=0:
        FPR_LSTM_new_truth = h_score_CNN_2D_LSTM_new_truth.Integral(bin,1001)/h_score_CNN_2D_LSTM_new_truth.GetEntries()
        #print("FPR",FPR)

    else:
        FPR_LSTM_new_truth = 0
    score_LSTM_new_truth = h_score_CNN_2D_LSTM_new_truth.GetBinCenter(bin)

    FPR_CNN_2D_LSTM_new_truth.append(FPR_LSTM_new_truth)
    
    score_CNN_2D_LSTM_new_truth.append(score_LSTM_new_truth)

    FPR_LSTM_old_truth=0
    if h_score_CNN_2D_old_truth.Integral(-1,1001) !=0:
        FPR_LSTM_old_truth = h_score_CNN_2D_LSTM_old_truth.Integral(bin,1001)/h_score_CNN_2D_LSTM_old_truth.GetEntries()
        #print("FPR",FPR)

    else:
        FPR_LSTM_old_truth = 0
    score_LSTM_old_truth = h_score_CNN_2D_LSTM_old_truth.GetBinCenter(bin)

    FPR_CNN_2D_LSTM_old_truth.append(FPR_LSTM_old_truth)
    
    score_CNN_2D_LSTM_old_truth.append(score_LSTM_old_truth)

    

# Soglie per FPR
thresholds = [0.1, 0.05, 0.01, 0.001]

# Dizionari per salvare i risultati separati
results_CNN_2D_new_truth = {}
results_CNN_2D_LSTM_new_truth = {}
results_CNN_2D_old_truth = {}
results_CNN_2D_LSTM_old_truth = {}

# Ciclo per FPR_CNN_2D_new_truth
def find_threshold(fpr_list, score_list, thresholds):
    #print("fpr_list",fpr_list)
    #print("score_list",score_list)
    results = {}
    for thr in thresholds:
        print("thr",thr)
        # Costruiamo una lista di tuple (indice, fpr) solo per i valori < thr
        candidates = [(i, fpr) for i, fpr in enumerate(fpr_list) if fpr < thr]
        #print("candidates",candidates)
        if candidates:
            # Prendi il candidato con il massimo fpr
            i, max_fpr = max(candidates, key=lambda x: x[1])
            print("i",i,"max_fpr",max_fpr)
            key = f"{(thr * 100)}%" if thr == 0.001 else f"{int(thr * 100)}%"
            results[key] = {
                "fpr": fpr_list[i],
                "thr": score_list[i]
            }
            print(results[key])
    return results

# Applicazione
print("FPR_CNN_2D_new_truth")
results_CNN_2D_new_truth = find_threshold(FPR_CNN_2D_new_truth, score_CNN_2D_new_truth, thresholds)
print("FPR_CNN_2D_old_truth")
results_CNN_2D_old_truth = find_threshold(FPR_CNN_2D_old_truth, score_CNN_2D_old_truth, thresholds)
print("FPR_CNN_2D_LSTM_new_truth")
results_CNN_2D_LSTM_new_truth = find_threshold(FPR_CNN_2D_LSTM_new_truth, score_CNN_2D_LSTM_new_truth, thresholds)
print("FPR_CNN_2D_LSTM_old_truth")
results_CNN_2D_LSTM_old_truth = find_threshold(FPR_CNN_2D_LSTM_old_truth, score_CNN_2D_LSTM_old_truth, thresholds)

# Scriviamo i dizionari su file JSON separati
with open('/eos/user/f/fsalerno/Evaluation/thr_estimate/score_thresholds_60_CNN_2D_new_truth_0_pt.json', 'w') as json_file:
    json.dump(results_CNN_2D_new_truth, json_file, indent=4)

with open('/eos/user/f/fsalerno/Evaluation/thr_estimate/score_thresholds_60_CNN_2D_LSTM_new_truth_0_pt.json', 'w') as json_file:
    json.dump(results_CNN_2D_LSTM_new_truth, json_file, indent=4)

with open('/eos/user/f/fsalerno/Evaluation/thr_estimate/score_thresholds_60_CNN_2D_old_truth_0_pt.json', 'w') as json_file:
    json.dump(results_CNN_2D_old_truth, json_file, indent=4)

with open('/eos/user/f/fsalerno/Evaluation/thr_estimate/score_thresholds_60_CNN_2D_LSTM_old_truth_0_pt.json', 'w') as json_file:
    json.dump(results_CNN_2D_LSTM_old_truth, json_file, indent=4)


