import h5py
import tqdm
import random
import numpy as np
import os

inFile="/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_60_boosted_0_pt/trainingSet.h5"

print(h5py.__version__)

if os.path.exists(inFile):
    print(f"File found: {inFile}")
else:
    print(f"File not found: {inFile}")




try:
    with h5py.File(inFile, 'r') as f:
        print("File is a valid HDF5 file")
except Exception as e:
    print(f"Error: {e}")

doCut=True
cut=400
verbose=True

jet_list, fatjet_list, PFC_list, top_list, labels_list = [], [], [], [], []

with h5py.File(inFile, "r") as f:
    components = f.keys()
    for c in f.keys():
        print(f"component: {c}")
        for cat in f[c].keys():
            categories = f[c].keys()
            idx_truetop  = [i for i, x in enumerate(f[c][cat]["labels"][:] == 1) if x==True]
            idx_falsetop = [i for i, x in enumerate(f[c][cat]["labels"][:] == 0) if x==True]
            print("stiamo selezionando i top per:",c,"",cat)
            if len(idx_truetop)==0:
                ids_todrop   = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.9)))
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
                jet_list.append(jets_balanced)
                fatjet_list.append(fatjets_balanced)
                PFC_list.append(PFC_balanced) 
                top_list.append(top_balanced)
                labels_list.append(labels_balanced)

                
            if doCut==True:
                ids_todrop_pt=[]
                for i in range(len(top_balanced)):
                    pt_top  = top_balanced[i][2]
                    if pt_top<=cut:
                        ids_todrop_pt.append(i)
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

                jet_list.append(jets_pt_cut)
                fatjet_list.append(fatjets_pt_cut)
                PFC_list.append(PFC_pt_cut)
                top_list.append(top_pt_cut)
                labels_list.append(labels_pt_cut)

jets_data = np.concatenate(jet_list, axis=0)
fatjets_data = np.concatenate(fatjet_list, axis=0)
PFC_data = np.concatenate(PFC_list, axis=0)
top_data = np.concatenate(top_list, axis=0)
labels_data = np.concatenate(labels_list, axis=0)
print(f"Dimensione dei labels modificati pls: {labels_data.shape}")
# Unire i f
#if all_jets:
    #combined_jets = np.concatenate(all_jets, axis=0)
    ##print(f"Dimensione finale dei jets combinati: {combined_jets.shape}")
#else:
    #print("Nessun f 'jets' trovato.")