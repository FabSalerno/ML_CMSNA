import h5py
from tqdm import tqdm
import argparse
import os
import tqdm

# Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-y", "--year", dest="year", type=int, default=2022, help="Year of the training")
args = parser.parse_args()
year = args.year

# Definisci il percorso in base all'anno
if year == 2018:
    path_to_training_folder = "/eos/user/f/fsalerno/framework/MachineLearning/new_ìTraining_HOTVR_2018_1_new_def"
elif year == 2022:
    #path_to_training_folder = "/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/new_truth/60_PFCs"
    path_to_training_folder = "/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/GNN/150_PFCs_boosted_False/h5s"
#path_to_h5_folder = f"{path_to_training_folder}/h5s_preprocessed_10_per_100_60_CNN_2D_LSTM_new_truth_0_pt"
#output_file = f"{path_to_training_folder}/trainingSet_preprocessed_10_per_100_CNN_2D_LSTM.h5"
path_to_h5_folder = f"{path_to_training_folder}"
output_file = f"{path_to_training_folder}/concs/concatenated_trainingSet.h5"

file_paths = [os.path.join(path_to_h5_folder, f) for f in os.listdir(path_to_h5_folder) if f.endswith(".h5") and not f.startswith(".") and "preprocessed" not in f]
print(f"Files found: {file_paths}")
def copy_new_datasets(source_group, target_group):
    """
    Copia solo i dataset che non esistono già nel file di destinazione,
    evitando di caricare l'intero file in RAM.
    """
    for key, item in source_group.items():
        if isinstance(item, h5py.Group):
            # Se il gruppo non esiste nel file di destinazione, crealo
            if key not in target_group:
                target_group.create_group(key)
            copy_new_datasets(item, target_group[key])  # Ricorsione nei sottogruppi
        else:
            # Se il dataset non esiste, copiarlo
            if key not in target_group:
                target_group.create_dataset(key, data=item, compression="gzip")
            else:
                print(f"Dataset '{key}' già presente, ignorato.")

# Apri il file di output in modalità append
with h5py.File(output_file, 'a') as f_out:  # 'a' evita di sovrascrivere
    for file_path in tqdm.tqdm(file_paths, desc="Processing files"):
        print(f"Processing dataset from: {file_path}")
        with h5py.File(file_path, 'r') as f_in:
            for group_name in f_in.keys():
                print(f"Processing group: {group_name}")
                if group_name not in f_out:
                    f_out.create_group(group_name)
                copy_new_datasets(f_in[group_name], f_out[group_name])

