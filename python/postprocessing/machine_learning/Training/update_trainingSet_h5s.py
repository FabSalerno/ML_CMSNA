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
with h5py.File(inFile, "r") as f, h5py.File(outFile, "w") as f_out:
    for c in f.keys():  # Itera sui gruppi principali
        for cat in f[c].keys():  # Itera sui sottogruppi
            print(f"Processing {c}/{cat}...")

            # Accesso ai dataset
            jets_dataset = f[c][cat]["jets"]
            fatjets_dataset = f[c][cat]["fatjets"]
            PFC_dataset = f[c][cat]["PFC"]
            top_dataset = f[c][cat]["top"]
            labels_dataset = f[c][cat]["labels"]

            num_samples = jets_dataset.shape[0]  # Numero totale di eventi
            
            # Creazione del gruppo nel file di output
            grp = f_out.create_group(f"{c}/{cat}")

            # Liste per accumulare i dati filtrati
            jets_filtered_list = []
            fatjets_filtered_list = []
            PFC_filtered_list = []
            top_filtered_list = []
            labels_filtered_list = []

            # Itera sui batch
            for i in range(0, num_samples, batch_size):
                X_jet = jets_dataset[i : i + batch_size]
                X_fatjet = fatjets_dataset[i : i + batch_size]
                X_PFC = PFC_dataset[i : i + batch_size]
                X_top = top_dataset[i : i + batch_size]
                y = labels_dataset[i : i + batch_size]

                # Calcola il punteggio usando il modello
                score = model({"jet": X_jet, "fatjet": X_fatjet, "PFC": X_PFC, "top": X_top}).numpy().flatten()
                
                # Applica la maschera di selezione
                mask = score > thresholds

                # Filtra i dati
                X_jet_filtered = X_jet[mask]
                X_fatjet_filtered = X_fatjet[mask]
                X_PFC_filtered = X_PFC[mask]
                X_top_filtered = X_top[mask]
                y_filtered = y[mask]

                # Accumula i dati filtrati
                jets_filtered_list.append(X_jet_filtered)
                fatjets_filtered_list.append(X_fatjet_filtered)
                PFC_filtered_list.append(X_PFC_filtered)
                top_filtered_list.append(X_top_filtered)
                labels_filtered_list.append(y_filtered)

                print(f"Batch {i}-{i+batch_size}: {X_jet_filtered.shape[0]} selected tops")

            # Concatenazione finale dei batch filtrati
            jets_filtered = np.concatenate(jets_filtered_list, axis=0) if jets_filtered_list else np.array([])
            fatjets_filtered = np.concatenate(fatjets_filtered_list, axis=0) if fatjets_filtered_list else np.array([])
            PFC_filtered = np.concatenate(PFC_filtered_list, axis=0) if PFC_filtered_list else np.array([])
            top_filtered = np.concatenate(top_filtered_list, axis=0) if top_filtered_list else np.array([])
            labels_filtered = np.concatenate(labels_filtered_list, axis=0) if labels_filtered_list else np.array([])

            # Salva i dati filtrati nel nuovo file HDF5 
            grp.create_dataset("jets", data=jets_filtered, compression="gzip")
            grp.create_dataset("fatjets", data=fatjets_filtered, compression="gzip")
            grp.create_dataset("PFC", data=PFC_filtered, compression="gzip")
            grp.create_dataset("top", data=top_filtered, compression="gzip")
            grp.create_dataset("labels", data=labels_filtered, compression="gzip")

            print(f"Saved {jets_filtered.shape[0]} tops in {c}/{cat}")

print(f"Dataset saved in {outFile}")

