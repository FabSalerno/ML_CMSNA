import h5py
import tensorflow as tf
import numpy as np
import json
import os
import multiprocessing 
import time
import tqdm


####### PARAMETERS #######
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
folder                  = "/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/new_truth/60_PFCs/h5s"
outfolder               = f"/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/new_truth/60_PFCs/h5s_10_per_100_{model_name}"
nPFCs=60
cut=0

model_to_load      = f"/eos/user/f/fsalerno/framework/MachineLearning/models/model_{model_name}.h5"  
# score thresholds
score_thresholds   = f"/eos/user/f/fsalerno/framework/MachineLearning/thresholds/score_thresholds_{model_name}.json"
thr                = "10%"                                        # threshold to select top candidates
inFiles=[]
outFiles=[]
for sample in samples:
    inFiles.append(f"{folder}/trainingSet_{sample}.h5")

    outFiles.append(f"{outfolder}/trainingSet_{sample}_10_per_100_{model_name}.h5")




####### DATASET LOADING AND PREPROCESSING (remove some False Tops and cut on pt if requested) #######
#jet_list, fatjet_list, PFC_list, top_list, labels_list = [], [], [], [], []
batch_size = 10000  


# Create directory if it doesn't exist
os.makedirs(outfolder, exist_ok=True)
print(f"Directory {outfolder} ready")

# Load threshold
with open(score_thresholds, "r") as fjson:
    thresholds = json.load(fjson)
thresholds = thresholds[thr]["thr"]
print(f"Using threshold: {thresholds}")

# Load model
#model = tf.keras.models.load_model(model_to_load)


def process_category(args):
    """
    Worker per processare una singola categoria (sottogruppo f[c][cat]).
    Apre il file in lettura, carica il modello, processa i dati a batch,
    applica il filtro e concatena i risultati.
    Ritorna una tupla:
      (group_key, cat_key, jets_filtered, fatjets_filtered, PFC_filtered, top_filtered, labels_filtered, num_samples)
    """
    inFile, group_key, cat_key, batch_size, thresholds, model_to_load = args

    # Carica il modello all'interno del processo figlio (evita problemi di pickling)
    model = tf.keras.models.load_model(model_to_load,compile=False)
    
    with h5py.File(inFile, "r") as f:
        cat = f[group_key][cat_key]
        jets_dataset    = cat["jets"]
        fatjets_dataset = cat["fatjets"]
        PFC_dataset     = cat["PFC"]
        top_dataset     = cat["top"]
        labels_dataset  = cat["labels"]
        num_samples = jets_dataset.shape[0]
        true_tops_total = np.sum(labels_dataset == 1)
        false_tops_total = np.sum(labels_dataset == 0)

        jets_filtered_list    = []
        fatjets_filtered_list = []
        PFC_filtered_list     = []
        top_filtered_list     = []
        labels_filtered_list  = []

        for i in range(0, num_samples, batch_size):
            X_jet    = jets_dataset[i : i + batch_size]
            X_fatjet = fatjets_dataset[i : i + batch_size]
            X_PFC    = PFC_dataset[i : i + batch_size]
            X_top    = top_dataset[i : i + batch_size]
            y        = labels_dataset[i : i + batch_size]

            # Calcola il punteggio usando il modello
            score = model({"jet": X_jet, "fatjet": X_fatjet, "PFC": X_PFC, "top": X_top}).numpy().flatten()
            mask = score > thresholds

            jets_filtered_list.append(X_jet[mask])
            fatjets_filtered_list.append(X_fatjet[mask])
            PFC_filtered_list.append(X_PFC[mask])
            top_filtered_list.append(X_top[mask])
            labels_filtered_list.append(y[mask])

            print(f"Category {group_key}/{cat_key}, batch {i}-{i+batch_size}: {X_jet[mask].shape[0]} selected tops")

        # Concatenazione finale dei batch filtrati
        jets_filtered    = np.concatenate(jets_filtered_list, axis=0) if jets_filtered_list else np.array([])
        fatjets_filtered = np.concatenate(fatjets_filtered_list, axis=0) if fatjets_filtered_list else np.array([])
        PFC_filtered     = np.concatenate(PFC_filtered_list, axis=0) if PFC_filtered_list else np.array([])
        top_filtered     = np.concatenate(top_filtered_list, axis=0) if top_filtered_list else np.array([])
        labels_filtered  = np.concatenate(labels_filtered_list, axis=0) if labels_filtered_list else np.array([])

    return (group_key, cat_key, jets_filtered, fatjets_filtered, PFC_filtered, top_filtered, labels_filtered, num_samples, true_tops_total, false_tops_total)

def main():
    for inFile, outFile in zip(inFiles, outFiles):
        print(f"\nProcessing file: {inFile}")

        tasks = []
        with h5py.File(inFile, "r") as f:
            for group_key in f.keys():
                for cat_key in f[group_key].keys():
                    tasks.append((inFile, group_key, cat_key, batch_size, thresholds, model_to_load))

        with multiprocessing.Pool() as pool:
            results = list(tqdm.tqdm(pool.imap_unordered(process_category, tasks),
                                     total=len(tasks),
                                     desc=f"Processing {os.path.basename(inFile)}"))

        # Crea directory di output se necessario
        os.makedirs(os.path.dirname(outFile), exist_ok=True)

        # Scrive i risultati nel file di output
        with h5py.File(outFile, "w") as f_out:
            for res in results:
                group_key, cat_key, jets_filtered, fatjets_filtered, PFC_filtered, top_filtered, labels_filtered, num_samples, true_tops_total, false_tops_total = res

                grp = f_out.create_group(f"{group_key}/{cat_key}")
                grp.create_dataset("jets", data=jets_filtered, compression="gzip")
                grp.create_dataset("fatjets", data=fatjets_filtered, compression="gzip")
                grp.create_dataset("PFC", data=PFC_filtered, compression="gzip")
                grp.create_dataset("top", data=top_filtered, compression="gzip")
                grp.create_dataset("labels", data=labels_filtered, compression="gzip")
                print(f"Saved {jets_filtered.shape[0]} tops in {group_key}/{cat_key}")

        print(f" Dataset saved in {outFile}")

        # Salvataggio riepilogo JSON
        summary_dict = {}
        for res in results:
            group_key, cat_key, jets_filtered, fatjets_filtered, PFC_filtered, top_filtered, labels_filtered, num_samples, true_tops_total, false_tops_total = res


            if group_key not in summary_dict:
                summary_dict[group_key] = {}
            summary_dict[group_key][cat_key] = {
                "n_selected_tops": int(top_filtered.shape[0]),
                "n_selected_true_tops": int(np.sum(labels_filtered == 1)),
                "n_selected_false_tops": int(np.sum(labels_filtered == 0)),
                "n_total_tops": int(num_samples),
                "n_total_true_tops": int(true_tops_total),
                "n_total_false_tops": int(false_tops_total)
            }

        json_filename = outFile.replace(".h5", "_summary.json")
        with open(json_filename, "w") as jf:
            json.dump(summary_dict, jf, indent=4)
        print(f"JSON summary saved: {json_filename}")


if __name__ == "__main__":
    main()