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
usage                   = 'python3 training_Run3_PF_jets_preprocessing.py -s component1,component2,component3'
folder                  = "/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/150_PFCs"
inFile                  = f"{folder}/trainingSet.h5"
doCut                   = False
cut                     = 0
verbose                 = True
full                    = False
if full == False:
    outFile             = f"{folder}/trainingSet_preprocessed_{cut}_pt.h5"
elif full == True:
    outFile             = f"{folder}/trainingSet_preprocessed_full_{cut}_pt.h5"
samples = [
        #"QCD_HT800to1000_2022",
        #"QCD_HT1000to1200_2022",
        #"QCD_HT1200to1500_2022",
        #"QCD_HT1500to2000_2022",
        #"QCD_HT2000toinf_2022",
        #"TprimeToTZ_700_2022",
        #"TprimeToTZ_1000_2022",
        #"TprimeToTZ_1800_2022",
        #"TT_hadronic_2022",
        #"TT_inclusive_2022",
        "TT_semilep_MC2022",
        #"WJets_2022",
        #"ZJetsToNuNu_HT800to1500_2022",
        #"ZJetsToNuNu_HT1500to2500_2022",
        #"ZJetsToNuNu_HT2500_2022"
        ]


####### DATASET LOADING AND PREPROCESSING (remove some False Tops and cut on pt if requested) #######
PFC_list, top_list, labels_list = [], [], []
batch_size = 10000  
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


                    if doCut==False:
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
labels_data = np.concatenate(labels_list, axis=0)


with h5py.File(outFile, 'w') as f:
    group = f.create_group('data')
    
    # Salviamo i dati come dataset all'interno del gruppo 'data'

    group.create_dataset('PFC', data=PFC_data, compression="gzip")
    group.create_dataset('top', data=top_data, compression="gzip" )
    group.create_dataset('labels', data=labels_data, compression="gzip")

print(f"Dati salvati correttamente in {outFile}")
