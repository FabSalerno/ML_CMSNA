import h5py

def rename_group(old_name):
    parts = old_name.split("_")  # Divide la stringa sugli underscore
    if len(parts) == 3 and parts[1] == parts[2]:  
        return parts[1]  # Restituisce solo "c" se le ultime due parti sono uguali
    return old_name



file_path = '/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_60_boosted_0_pt/trainingSet.h5'
try:
    with h5py.File(file_path, 'r') as f:
        print("File aperto con successo")
except OSError as e:
    print(f"Errore nell'aprire il file: {e}")

with h5py.File(file_path, 'r+') as f:
    
        for old_group_name in f.keys():
            new_group_name = rename_group(old_group_name)
            # Creare una copia del gruppo con il nuovo nome
            f.copy(old_group_name, new_group_name)  
            del f[old_group_name]
            print(f"Gruppo '{old_group_name}' rinominato in '{new_group_name}' con successo.")
        