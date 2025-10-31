import h5py
import keras
import tensorflow as tf
import random
import numpy as np
import json
import sys
import os
import tqdm
####### PARAMETERS #######
nPFCs=60
model_name="CNN_2D_LSTM"
#LSTM, CNN, CNN_2D, CNN_2D_prova, transformer, 
doCut=False
cut=0
verbose=True

path_to_folder= f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2/Training_PF_2022_2_jets_{nPFCs}_boosted_{model_name}_{cut}_pt"
# training set to update
inFile             = f"/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/Full/trainingSet.h5"
# updated training set
outFile            = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2/Training_PF_2022_2_jets_{nPFCs}_boosted_{model_name}_{cut}_pt/trainingSet_with_preprocessing.h5"
# model to load
model_to_load      = f"//eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_{nPFCs}_boosted_0_pt/Training_PF_2022_1_jets_{nPFCs}_boosted_{model_name}_{cut}_pt/model.h5"  
# score thresholds
score_thresholds   = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_{nPFCs}_boosted_0_pt/Training_PF_2022_1_jets_{nPFCs}_boosted_{model_name}_{cut}_pt/score_thresholds_{nPFCs}_{model_name}_{cut}_pt.json"
thr                = "10%"                                               # threshold to select top candidates

########## MAKE DIRECTORY #########
if not os.path.exists(path_to_folder):
    os.makedirs(path_to_folder)
    print(f"Directory {path_to_folder} created")

# load model & thresholds #
model           = tf.keras.models.load_model(model_to_load)
with open(score_thresholds, "r") as fjson:
    thresholds  = json.load(fjson)
thresholds   = thresholds[thr]["thr"] #lo fisso perchè è complesso trovare il file
print(thresholds)

####### DATASET LOADING AND PREPROCESSING #######
batch_size = 10000  
jet_selected_list, fatjet_selected_list, PFC_selected_list, top_selected_list, labels_selected_list = [], [], [], [], []
jet_preprocessed_list, fatjet_preprocessed_list, PFC_preprocessed_list, top_preprocessed_list, labels_preprocessed_list = [], [], [], [], []
with h5py.File(inFile, "r") as f:
    components = f.keys()
    for c in f.keys():
        for cat in f[c].keys():
            jet_list, fatjet_list, PFC_list, top_list, labels_list = [], [], [], [], []
            dataset_size = f[c][cat]["jets"].shape[0]
            print(f"Selecting only top candidates with score > {thresholds}, corresponding to fpr={thr} of the dataset.")
            print(f"Processing {c} {cat}") 
            for start in tqdm.tqdm(range(0, dataset_size, batch_size)):
                end = min(start + batch_size, dataset_size)
                categories = f[c].keys()
                
                #if dataset[c][cat]!=0:
                X_jet = f[c][cat]["jets"][start:end]
                X_fatjet = f[c][cat]["fatjets"][start:end]
                X_PFC = f[c][cat]["PFC"][start:end]
                X_top = f[c][cat]["top"][start:end]
                y = f[c][cat]["labels"][start:end]

                score                       = model({"jet": X_jet, "fatjet": X_fatjet, "PFC": X_PFC, "top": X_top})
                #print(score)
                score                       = score.numpy().flatten()
                #print(score)
                mask                        = score > thresholds
                #print(mask)
                jet_list.append(X_jet[mask])
                fatjet_list.append(X_fatjet[mask])
                PFC_list.append(X_PFC[mask])
                top_list.append(X_top[mask])
                labels_list.append(y[mask])
            
            jet_selected_list=np.concatenate(jet_list)
            fatjet_selected_list=np.concatenate(fatjet_list)
            PFC_selected_list=np.concatenate(PFC_list)      
            top_selected_list=np.concatenate(top_list)
            labels_selected_list=np.concatenate(labels_list)
            idx_truetop  = [i for i, x in enumerate(labels_selected_list == 1) if x==True]
            idx_falsetop = [i for i, x in enumerate(labels_selected_list == 0) if x==True]
            print("stiamo selezionando i top per:",c,"",cat)
            if len(idx_truetop)==0:
                ids_todrop   = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.9)))
            elif len(idx_falsetop)>2*len(idx_truetop):    
                ids_todrop   = random.sample(idx_falsetop, len(idx_falsetop)-2*len(idx_truetop))
            else:
                ids_todrop=[]
            if len(ids_todrop) > 0:
                # Crea i nuovi dataset senza le righe da eliminare
                jets_balanced = np.delete(jet_selected_list, ids_todrop, axis=0)
                fatjets_balanced = np.delete(fatjet_selected_list, ids_todrop, axis=0)
                PFC_balanced = np.delete(PFC_selected_list, ids_todrop, axis=0)
                top_balanced = np.delete(top_selected_list, ids_todrop, axis=0)
                labels_balanced = np.delete(labels_selected_list, ids_todrop, axis=0)

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
                jet_preprocessed_list.append(jets_balanced)
                fatjet_preprocessed_list.append(fatjets_balanced)
                PFC_preprocessed_list.append(PFC_balanced) 
                top_preprocessed_list.append(top_balanced)
                labels_preprocessed_list.append(labels_balanced)

                
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

                jet_preprocessed_list.append(jets_pt_cut)
                fatjet_preprocessed_list.append(fatjets_pt_cut)
                PFC_preprocessed_list.append(PFC_pt_cut)
                top_preprocessed_list.append(top_pt_cut)
                labels_preprocessed_list.append(labels_pt_cut)
                

            jets_data = np.concatenate(jet_preprocessed_list, axis=0)
            fatjets_data = np.concatenate(fatjet_preprocessed_list, axis=0)
            PFC_data = np.concatenate(PFC_preprocessed_list, axis=0)
            top_data = np.concatenate(top_preprocessed_list, axis=0)
            labels_data = np.concatenate(labels_preprocessed_list, axis=0)




with h5py.File(outFile, 'w') as f:
    group = f.create_group('data')
    
    # Salviamo i dati come dataset all'interno del gruppo 'data'
    group.create_dataset('jets', data=jets_data, compression="gzip")
    group.create_dataset('fatjets', data=fatjets_data, compression="gzip")
    group.create_dataset('PFC', data=PFC_data, compression="gzip")
    group.create_dataset('top', data=top_data, compression="gzip" )
    group.create_dataset('labels', data=labels_data, compression="gzip")

print(f"Dati salvati correttamente in {outFile}")


