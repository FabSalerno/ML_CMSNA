import os
import random
import numpy as np
import sys
from curses import keyname
import time
import ROOT
import json
import mplhep as hep
hep.style.use(hep.style.CMS)
import h5py
import tqdm

t0=time.time()


############################################
########### STARTING THE SCRIPT ############
############################################

########### KEY VARIABLES ############

samples = [
        "TT_inclusive_MC2022",
        "TT_semilep_MC2022",
        "TT_Mtt_700_1000_MC2022",
        "TT_Mtt_1000_inf_MC2022",
        #"TTZprimetoTT_M_3000_W_4_MC2022",
        "QCD_HT_400_600_MC2022",
        "QCD_HT_600_800_MC2022",
        "QCD_HT_800_1000_MC2022",
        "QCD_HT_1000_1200_MC2022",
        "QCD_HT_1200_1500_MC2022",
        "QCD_HT_1500_2000_MC2022",
        "QCD_HT_2000_inf_MC2022",
        "TT_hadronic_MC2022",
        "Z_nunu_1500_2500_MC2022",
        "Z_nunu_800_1500_MC2022",
        "Z_nunu_2500_inf_MC2022",
        "Z_nunu_400_800_MC2022"
        ]
model_name="60_CNN_2D_LSTM_new_truth_0_pt"
usage                   = 'python3 training_Run3_PF_jets_preprocessing.py -s component1,component2,component3'
folder                  = f"/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/new_truth/60_PFCs/h5s_10_per_100_{model_name}"
outfolder               = f"/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/new_truth/60_PFCs/h5s_preprocessed_10_per_100_{model_name}"
doCut                   = False
cut                     = 0
verbose                 = True
full                    = False
nPFCs=60

cut=0

inFiles=[]
outFiles=[]
for sample in samples:
    inFiles.append(f"{folder}/trainingSet_{sample}_10_per_100_{model_name}.h5")
    if full == False:
        outFiles.append(f"{outfolder}/trainingSet_{sample}_preprocessed_{model_name}.h5")
    elif full == True:
        outFiles.append(f"{outfolder}/trainingSet_{sample}_preprocessed_full_{model_name}.h5")
#/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/new_truth/60_PFCs/h5s_10_per_100_60_{model_name}_new_truth_0_pt/trainingSet_TT_inclusive_MC2022_10_per_100_60_{model_name}_new_truth_0_pt.h5






####### DATASET LOADING AND PREPROCESSING (remove some False Tops and cut on pt if requested) #######
#jet_list, fatjet_list, PFC_list, top_list, labels_list = [], [], [], [], []
batch_size = 10000  
#spostandolo qui poi li mette tutti nello stesso file e il salvataggio va fatto dopo
#data_dict = {}
#data_dict[data] = {}
for file_n, inFile in enumerate(inFiles):
    jet_list, fatjet_list, PFC_list, top_list, labels_list = [], [], [], [], []
    try:
        with h5py.File(inFile, 'r') as f:
            print("File is a valid HDF5 file")
    except Exception as e:
        print(f"Error: {e}")

    with h5py.File(inFile, "r") as f:
        components = f.keys()
        data_dict = {}
        for c in f.keys():
            if c in samples:
                print(f"component: {c}")
                data_dict[c] = {}
                for cat in f[c].keys():
                    data_dict[c][cat] = {}

                    categories = f[c].keys()
                    idx_truetop  = [i for i, x in tqdm.tqdm(enumerate(f[c][cat]["labels"][:] == 1)) if x==True]
                    idx_falsetop = [i for i, x in tqdm.tqdm(enumerate(f[c][cat]["labels"][:] == 0)) if x==True]
                    print("stiamo selezionando i top per:",c,"",cat)
                    if len(idx_truetop)==0:
                        ids_todrop   = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.66)))
                    elif len(idx_falsetop)>2*len(idx_truetop):    
                        ids_todrop   = random.sample(idx_falsetop, len(idx_falsetop)-2*len(idx_truetop))
                    else:
                        ids_todrop=[]
                    if len(ids_todrop) > 0:
                        # Crea i nuovi dataset senza le righe da eliminare
                        jets_balanced = np.delete(f[c][cat]["jets"][:], ids_todrop, axis=0)
                        fatjets_balanced = np.delete(f[c][cat]["fatjets"][:], ids_todrop, axis=0)
                        PFC_balanced = np.delete(f[c][cat]["PFC"][:], ids_todrop, axis=0)
                        top_balanced = np.delete(f[c][cat]["top"][:], ids_todrop, axis=0)
                        labels_balanced = np.delete(f[c][cat]["labels"][:], ids_todrop, axis=0)

                        if verbose:
                            print(f"Component: {c}, Category: {cat}")
                            print(f"Number of initial True Tops:            {len(idx_truetop)}")
                            print(f"Number of True Tops after balancing:    {len([i for i, x in enumerate(labels_balanced==1) if x==True])}")
                            print(f"Number of initial False Tops:           {len(idx_falsetop)}")
                            print(f"Number of False Tops after balancing:   {len([i for i, x in enumerate(labels_balanced==0) if x==True])}")
                            print("Number of initial Tops:                 ", len(f[c][cat]["top"]))
                            print(f"Number of Tops after balancing:         {len(top_balanced)}")
                            print("\n")

                        if doCut==False:
                            data_dict[c][cat]['jets'] = jets_balanced
                            data_dict[c][cat]['fatjets'] = fatjets_balanced
                            data_dict[c][cat]['PFC'] = PFC_balanced
                            data_dict[c][cat]['top'] = top_balanced
                            data_dict[c][cat]['labels'] = labels_balanced
                    
                        
                    if doCut==True:
                        ids_todrop_pt=[]
                        for i in range(len(top_balanced)):
                            pt_top  = top_balanced[i][2]
                            if pt_top<=cut:
                                ids_todrop_pt.append(i)
                        if len(ids_todrop) > 0:
                            jets_pt_cut = np.delete(jets_balanced, ids_todrop_pt, axis=0)
                            fatjets_pt_cut = np.delete(fatjets_balanced, ids_todrop_pt, axis=0)
                            PFC_pt_cut = np.delete(PFC_balanced, ids_todrop_pt, axis=0)
                            top_pt_cut = np.delete(top_balanced, ids_todrop_pt, axis=0)
                            labels_pt_cut = np.delete(labels_balanced, ids_todrop_pt, axis=0)
                    
                        if verbose:
                            print(f"Component: {c}, Category: {cat}")
                            print(f"Number of balanced True Tops:            {len([i for i, x in enumerate(labels_balanced==1) if x==True])}")
                            print(f"Number of True Tops after pt cut:    {len([i for i, x in enumerate(labels_pt_cut==1) if x==True])}")
                            print(f"Number of balanced False Tops:           {len([i for i, x in enumerate(labels_balanced==0) if x==True])}")
                            print(f"Number of False Tops after pt cut:   {len([i for i, x in enumerate(labels_pt_cut==0) if x==True])}")
                            print(f"Number of balanced Tops:                 {len(top_balanced)}")
                            print(f"Number of Tops after pt cut:         {len(top_pt_cut)}")
                            print("\n")
                        
                        data_dict[c][cat]['jets'] = jets_pt_cut
                        data_dict[c][cat]['fatjets'] = fatjets_pt_cut
                        data_dict[c][cat]['PFC'] = PFC_pt_cut
                        data_dict[c][cat]['top'] = top_pt_cut
                        data_dict[c][cat]['labels'] = labels_pt_cut
                        

    with h5py.File(outFiles[file_n], 'w') as f_out:
        for comp in data_dict:
            grp_comp = f_out.create_group(comp)
            for cat in data_dict[comp]:
                grp_cat = grp_comp.create_group(cat)
                grp_cat.create_dataset('jets', data=data_dict[comp][cat]['jets'], compression="gzip")
                grp_cat.create_dataset('fatjets', data=data_dict[comp][cat]['fatjets'], compression="gzip")
                grp_cat.create_dataset('PFC', data=data_dict[comp][cat]['PFC'], compression="gzip")
                grp_cat.create_dataset('top', data=data_dict[comp][cat]['top'], compression="gzip")
                grp_cat.create_dataset('labels', data=data_dict[comp][cat]['labels'], compression="gzip")
            
    print(f"Dati salvati correttamente in {outFiles[file_n]}")
