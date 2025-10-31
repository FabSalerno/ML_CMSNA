import os
import pickle
import h5py
import numpy as np
from tqdm import tqdm


def save_to_h5(group, data):
    """
    Funzione ricorsiva per salvare dizionari annidati in un file HDF5.
    """
    if isinstance(data, dict):
        # Se il dato è un dizionario, creiamo un gruppo per ogni chiave
        for key, value in data.items():
            subgroup = group.create_group(key)  # Crea un gruppo per ogni chiave
            print(f"subgroup: {subgroup}")
            save_to_h5(subgroup, value)         # Chiamata ricorsiva per i sottogruppi
    else:
        # Se il dato non è un dizionario, creiamo un dataset per il valore
        print(f"data type: {type(data)}")
        # Controlla se il dato è un numpy array (multidimensionale)
        if isinstance(data, np.ndarray):  # Se i dati sono già un array numpy
            print("is an np array")
            group.create_dataset('data', data=data)  # Salva direttamente come dataset
        else:
            # Converti in un array numpy se i dati non sono già in formato array
            array = np.array(data, dtype=object)
            print("is NOT an np array")
            group.create_dataset('data', data=np.array(array))


# Path to the folder containing the .pkl files
path_to_pkl_folder = "/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_60_boosted_0_pt/pkls"
# Path where you want to save the .h5 files
path_to_h5_folder = "/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_60_boosted_0_pt/h5"


# Create the target directory if it does not exist
if not os.path.exists(path_to_h5_folder):
    os.makedirs(path_to_h5_folder)

# Process each .pkl file in the folder
for file_name in tqdm(os.listdir(path_to_pkl_folder)):
    if file_name.endswith(".pkl"):
        # Full path to the current .pkl file
        pkl_file_path = os.path.join(path_to_pkl_folder, file_name)
        
        # Read the .pkl file
        with open(pkl_file_path, 'rb') as f:
            data = pickle.load(f)
        
        # Create an HDF5 file for saving the data
        h5_file_name = file_name.replace('.pkl', '.h5')  # Change file extension to .h5
        h5_file_path = os.path.join(path_to_h5_folder, h5_file_name)
        
        with h5py.File(h5_file_path, 'w') as h5_file:
            # This assumes that your pickle data is a dictionary
            # Loop through the keys of the dictionary and store them as datasets in HDF5
            for component in data.keys():
                # You can adjust this if your structure is different
                print(f"Saving data for key: {component}")
                main_group = h5_file.create_group(component)  # Crea il gruppo principale
                save_to_h5(main_group, data[component])  # Salva i dati annidati all'interno
        
        print(f"Converted {pkl_file_path} to {h5_file_path}")
