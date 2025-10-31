import h5py
import keras
import tensorflow as tf
import numpy as np
import json
import sys
import os
import tqdm
import multiprocessing as mp
####### PARAMETERS #######
nPFCs=60
model_name="CNN_2D_LSTM"
cut=0
#LSTM, CNN, CNN_2D, CNN_2D_prova, transformer, 
path_to_folder= f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2/Training_PF_2022_2_jets_{nPFCs}_boosted_{model_name}_{cut}_pt"
# training set to update
inFile             = f"/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/Full/trainingSet.h5"
# updated training set
outFile            = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2/Training_PF_2022_2_jets_{nPFCs}_boosted_{model_name}_{cut}_pt/trainingSet.h5"
# model to load
model_to_load      = f"//eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_{nPFCs}_boosted_0_pt/Training_PF_2022_1_jets_{nPFCs}_boosted_{model_name}_{cut}_pt/model.h5"  
# score thresholds
score_thresholds   = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_{nPFCs}_boosted_0_pt/Training_PF_2022_1_jets_{nPFCs}_boosted_{model_name}_{cut}_pt/score_thresholds_{nPFCs}_{model_name}_{cut}_pt.json"
thr                = "10%"                                        # threshold to select top candidates

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

    jets_data = np.concatenate(jet_list, axis=0)
    fatjets_data = np.concatenate(fatjet_list, axis=0)
    PFC_data = np.concatenate(PFC_list, axis=0)
    top_data = np.concatenate(top_list, axis=0)
    labels_data = np.concatenate(labels_list, axis=0)




with h5py.File(outFile, 'w') as f:
    group = f.create_group('data')
    
    # Salviamo i dati come dataset all'interno del gruppo 'data'
    group.create_dataset('jets', data=jets_data, compression="gzip")
    group.create_dataset('fatjets', data=fatjets_data, compression="gzip")
    group.create_dataset('PFC', data=PFC_data, compression="gzip")
    group.create_dataset('top', data=top_data, compression="gzip" )
    group.create_dataset('labels', data=labels_data, compression="gzip")

print(f"Dati salvati correttamente in {outFile}")


