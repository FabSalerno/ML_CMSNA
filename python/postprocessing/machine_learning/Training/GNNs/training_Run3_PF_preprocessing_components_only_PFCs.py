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
        #"QCD_HT_400_600_MC2022",
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
usage                   = 'python3 training_Run3_PF_jets_preprocessing.py -s component1,component2,component3'
folder                  = "/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/GNN/150_PFCs_boosted_False/h5s"
doCut                   = False
cut                     = 0
verbose                 = True
full                    = False
inFiles=[]
outFiles=[]
for sample in samples:
    inFiles.append(f"{folder}/trainingSet_{sample}.h5")
    if full == False:
        outFiles.append(f"{folder}/trainingSet_{sample}_preprocessed_{cut}_pt.h5")
    elif full == True:
        outFiles.append(f"{folder}/trainingSet_{sample}_preprocessed_full_{cut}_pt.h5")



####### DATASET LOADING AND PREPROCESSING (remove some False Tops and cut on pt if requested) #######

batch_size = 10000  

for file_n, inFile in enumerate(inFiles):
    jet_list, fatjet_list, PFC_list, top_list, labels_list = [], [], [], [], []
    print(f"preprocseeing: {inFile}")
    try:
        with h5py.File(inFile, 'r') as f:
            print("File is a valid HDF5 file")
    except Exception as e:
        print(f"Error: {e}")
    
    with h5py.File(inFile, "r") as f:
        components = f.keys()
        for c in f.keys():
            if c in samples:
                print(f"component: {c}")
                for cat in f[c].keys():
                    if full == False:
                        categories = f[c].keys()
                        idx_truetop  = [i for i, x in tqdm.tqdm(enumerate(f[c][cat]["labels"][:] == 1)) if x==True]
                        idx_falsetop = [i for i, x in tqdm.tqdm(enumerate(f[c][cat]["labels"][:] == 0)) if x==True]
                        print("stiamo selezionando i top per:",c,"",cat)
                        if len(idx_truetop)==0:
                            ids_todrop   = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.9)))
                        elif len(idx_falsetop)>2*len(idx_truetop):    
                            ids_todrop   = random.sample(idx_falsetop, len(idx_falsetop)-2*len(idx_truetop))
                        else:
                            ids_todrop=[]
                        if len(ids_todrop) > 0:
                            # Crea i nuovi dataset senza le righe da eliminare

                            PFC_balanced = np.delete(f[c][cat]["PFC"][:], ids_todrop, axis=0)
                            top_balanced = np.delete(f[c][cat]["top"][:], ids_todrop, axis=0)
                            labels_balanced = np.delete(f[c][cat]["labels"][:], ids_todrop, axis=0)

                            if verbose:
                                print(f"Component: {c}, Category: {cat}")
                                print(f"Number of initial True Tops:            {len(idx_truetop)}")
                                print(f"Number of True Tops after balancing:    {len([i for i, x in enumerate(labels_balanced==1) if x==True])}")
                                print(f"Number of initial False Tops:           {len(idx_falsetop)}")
                                print(f"Number of False Tops after balancing:   {len([i for i, x in enumerate(labels_balanced==0) if x==True])}")
                                print("Number of initial Tops:                 ", len(f[c][cat]["labels"]))
                                print(f"Number of Tops after balancing:         {len(labels_balanced)}")
                                print("\n")


                        PFC_list.append(PFC_balanced) 
                        top_list.append(top_balanced)
                        labels_list.append(labels_balanced)

                            
                        
                    if full == True:
                        num_samples = f[c][cat]["PFC"].shape[0]
                        for i in range(0, num_samples, batch_size):
                            X_PFC = f[c][cat]["PFC"][i : i + batch_size]
                            X_top = f[c][cat]["top"][i : i + batch_size]
                            y = f[c][cat]["labels"][i : i + batch_size]

                        
                        PFC_list.append(X_PFC)
                        top_list.append(X_top)
                        labels_list.append(y)

    PFC_data = np.concatenate(PFC_list, axis=0)
    top_data = np.concatenate(top_list, axis=0)
    print(len(top_data))
    labels_data = np.concatenate(labels_list, axis=0)


    with h5py.File(outFiles[file_n], 'w') as f:
        print("\n OUTPUT:",outFiles[file_n],f)
        group = f.create_group('data')
        
        # Salviamo i dati come dataset all'interno del gruppo 'data'
        print("len top data:",len(top_data))
        group.create_dataset('PFC', data=PFC_data, compression="gzip")
        group.create_dataset('top', data=top_data, compression="gzip" )
        group.create_dataset('labels', data=labels_data, compression="gzip")

    print(f"Dati salvati correttamente in {outFiles[file_n]}")
