#!/usr/bin/env python3
##### FIX SEED #####
seed_value= 0
import os
os.environ['PYTHONHASHSEED']=str(seed_value)

scram_arch = os.getenv('SCRAM_ARCH')
if scram_arch:
    print(f'SCRAM_ARCH is set to: {scram_arch}')
else:
    print('SCRAM_ARCH is not set')

import random
random.seed(seed_value)
import numpy as np
np.random.seed(seed_value)
import tensorflow as tf
print("\nversione TF:\n",tf.__version__)
from tensorflow import keras
#from tensorflow.keras import backend as K
tf.random.set_seed(12345)
#settings delle configurazioni
session_conf = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(), config=session_conf)
#from tensorflow.keras import backend as K
#K.set_session(sess)
tf.compat.v1.keras.backend.set_session(sess)




# import tensorflow as tf
# from tensorflow import keras
import keras_tuner as kt
import h5py 
import multiprocessing
# import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, f1_score, confusion_matrix, auc, roc_curve
from tensorflow.keras.layers import Dense, Dropout, LSTM, concatenate, GRU,Masking, Activation, TimeDistributed, Conv1D, BatchNormalization, Conv2D, MaxPooling1D, Reshape, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras.backend import sigmoid
from tensorflow.keras import regularizers
#from tensorflow.keras.utils.generic_utils import get_custom_objects
import matplotlib.pyplot as plt
import ROOT
import json
import mplhep as hep
hep.style.use(hep.style.CMS)





ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

# Datasets
# from PhysicsTools.NanoAODTools.postprocessing.my_analysis.my_framework.MLstudies.Training.Datasets import *
# import PhysicsTools.NanoAODTools.postprocessing.my_analysis.my_framework.MLstudies.Training.Datasets as Datasets

######### Create arguments to insert from shell #########
example     = 'python3 grid_search_PF_jets.py -save_graphics True -pt_flatten False -path_to_h5_folder /eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets -h5Name trainingSet.h5 -path_to_graphics_folder /eos/user/f/fsalerno/framework/MachineLearning/Grid_search_1/graphics_gridsearch/PF -path_to_model_folder /eos/user/f/fsalerno/framework/MachineLearning/Grid_search_1/grid_search_models/PF_jets -modelName model_base_1'

from argparse import ArgumentParser
parser          = ArgumentParser()
parser.add_argument("-save_graphics",               dest="save_graphics",               default=False,    required=False,    type=bool,   help="True if want to save plots")
parser.add_argument("-pt_flatten",                  dest="pt_flatten",                  default=False,    required=False,    type=bool,   help="True if want to run on pt-flattened dataset")
parser.add_argument("-path_to_h5_folder",          dest="path_to_h5_folder",          default=None,     required=True,     type=str,    help="folder where h5 is saved")
parser.add_argument("-h5Name",                     dest="h5Name",                     default=None,     required=True,     type=str,    help="name of h5 file")
parser.add_argument("-path_to_graphics_folder",     dest="path_to_graphics_folder",     default=None,     required=True,     type=str,    help="folder to save plots to")
parser.add_argument("-path_to_model_folder",        dest="path_to_model_folder",        default=None,     required=True,     type=str,    help="folder to save model to")
parser.add_argument("-modelName",                   dest="modelName",                   default=None,     required=True,     type=str,    help="name of model file (usually .h5)")
options         = parser.parse_args()

### ARGS ###
save_graphics             = options.save_graphics      
pt_flatten                = options.pt_flatten  
path_to_h5_folder         = options.path_to_h5_folder          
h5Name                    = options.h5Name
path_to_graphics_folder   = options.path_to_graphics_folder              
path_to_model_folder      = options.path_to_model_folder              
modelName                 = options.modelName
path_to_model             = f"{path_to_model_folder}/{modelName}"
path_to_h5                = f"{path_to_h5_folder}/{h5Name}"
##prova
print("Current working directory:", os.getcwd())
print("Path to h5 file:", path_to_h5)
#fine prova



#usage="python3 grid_search_hotvr.py -save_graphics {save_graphics} -pt_flatten {pt_flatten} -path_to_h5_folder {path_to_h5_folder} -h5Name  -path_to_graphics_folder {path_to_graphics_folder} -path_to_model_folder /afs/cern.ch/user/f/fsalerno/CMSSW_12_5_2/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/GridSearch/models -modelName {modelName}

# components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeBToTZ_M800_2018", "TprimeBToTZ_M1200_2018", "TprimeBToTZ_M1800_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]
# components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeBToTZ_M1800_2018", "TT_Mtt_1000toInf_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]
# components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeToTZ_1800_2018", "TT_Mtt_1000toInf_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]
samples = [
        "QCD_HT800to1000_2022",
        "QCD_HT1000to1200_2022",
        "QCD_HT1200to1500_2022",
        "QCD_HT1500to2000_2022",
        "QCD_HT2000toinf_2022",
        #"TprimeToTZ_700_2022",
        #"TprimeToTZ_1000_2022",
        #"TprimeToTZ_1800_2022",
        "TT_hadronic_2022",
        "TT_inclusive_2022",
        "TT_semilep_2022",
        #"WJets_2022",
        "ZJetsToNuNu_HT800to1500_2022",
        "ZJetsToNuNu_HT1500to2500_2022",
        "ZJetsToNuNu_HT2500_2022"
        ]



categories    = ["3j1fj", "3j0fj", "2j1fj"]
nPFCs                   = 60
doCut                   = False
cut                     = 0
inFile                  = path_to_h5
verbose                 = True
####### DATASET LOADING AND PREPROCESSING (remove some False Tops and cut on pt if requested) #######
try:
    with h5py.File(inFile, 'r') as f:
        print("File is a valid HDF5 file")
except Exception as e:
    print(f"Error: {e}")

with h5py.File(inFile, 'r') as f:
    print ("Keys: ", list(f.keys()))
    # Verifica che il gruppo e i dataset esistano
    if 'data' in f:
        data_group = f['data']
        
        # Accedere ai dataset
        jets_data = data_group['jets'][:]
        fatjets_data = data_group['fatjets'][:]
        PFC_data = data_group['PFC'][:]
        top_data = data_group['top'][:]
        labels_data = data_group['labels'][:]

        # Verifica i dati letti (ad esempio la forma dei dati)
        print(f"Jets shape: {jets_data.shape}")
        print(f"Fatjets shape: {fatjets_data.shape}")
        print(f"PFC shape: {PFC_data.shape}")
        print(f"Top shape: {top_data.shape}")
        print(f"Labels shape: {labels_data.shape}")
    else:
        print("Il gruppo 'data' non è presente nel file.")



X_jet                     = jets_data # here we use only the samples selected by the user
X_fatjet                  = fatjets_data # here we use only the samples selected by the user
X_PFC                     = PFC_data
X_PFC                     = X_PFC[:,:nPFCs,:]
X_top                     = top_data
y                         = labels_data
data                      = X_jet, X_fatjet, X_PFC, X_top, y





X_jet_train, X_jet_test, X_fatjet_train, X_fatjet_test, X_PFC_train, X_PFC_test,  X_top_train, X_top_test, y_train, y_test = train_test_split(X_jet, X_fatjet, X_PFC, X_top, y, stratify=y, shuffle=True, test_size=0.3)
print(X_jet_train.shape, X_jet_test.shape, X_fatjet_train.shape, X_fatjet_test.shape,  X_PFC_train.shape, X_PFC_test.shape,  X_top_train.shape, X_top_test.shape, y_train.shape, y_test.shape)
print(y_train.shape, y_test.shape)
print(np.sum(y_train), np.sum(y_test))


### Define HYPERMODEL for GridSearch ###
InputShape_FatJet=X_fatjet_train.shape[1]
InputShape_Jet=X_jet_train.shape[2]
InputShape_PFC=X_PFC_train.shape[2]
InputShape_Top=X_top_train.shape[1]
dropout=0.3

# dropout = hp.Boolean("dropout")
# lr = hp.Float("lr", min_value=1e-4, max_value=1e-2, sampling="log")

def model_builder(hp):
    # Definizione del modello, come nel tuo codice originale.
    fj_inputs = tf.keras.Input(shape=(InputShape_FatJet,), name="fatjet")               #x
    jet_inputs = tf.keras.Input(shape=(None, InputShape_Jet,), name="jet")             #y
    PFC_inputs = tf.keras.Input(shape=(nPFCs, InputShape_PFC,), name="PFC")            #z
    top_inputs = tf.keras.Input(shape=(InputShape_Top,), name="top")                   #t

    # Operazioni per il FatJet, Jet, PFC, Top, come nel tuo codice originale
    x = BatchNormalization()(fj_inputs)
    fj_units = hp.Int("fj_units", min_value=1, max_value=10, step=1)
    fj_activation = hp.Choice("fj_activation", values=["relu", "sigmoid", "tanh"])
    x = Dense(units=fj_units, activation=fj_activation)(x)

    y = Masking(mask_value=0.)(jet_inputs)
    y = BatchNormalization()(y)
    j_units = hp.Int("j_units", min_value=2, max_value=20, step=2)
    j_activation = hp.Choice("j_activation", values=["relu", "sigmoid", "tanh"])
    j_dropout = hp.Choice("j_dropout", values=list(np.arange(0, 1, 0.3)))
    y = tf.keras.layers.LSTM(units=j_units, activation=j_activation, dropout=j_dropout)(y)

    z = PFC_inputs[:, :, :3]
    z = tf.expand_dims(z, axis=-1)
    z = Conv2D(filters=32, kernel_size=3, activation='relu', padding='same')(z)
    z = BatchNormalization()(z)
    z = Flatten()(z)
    z = Dense(256, activation='relu')(z)
    z = Dropout(0.3)(z)

    t = Dense(units=1, activation="relu")(top_inputs)

    x = concatenate([x, y, z, t])
    x = Dense(units=5, activation="relu")(x)

    outputs = Dense(1, activation="sigmoid")(x)
    model = tf.keras.Model(inputs=[fj_inputs, jet_inputs, PFC_inputs, top_inputs], outputs=outputs)

    # Hyperparameter: Learning Rate
    l_rate = hp.Float("learning_rate", 1e-4, 1e-1, sampling="log", default=1e-3)
    trainer = tf.keras.optimizers.Adam(learning_rate=l_rate)
    loss = tf.keras.losses.BinaryCrossentropy()
    model.compile(optimizer=trainer, loss=loss, metrics=[tf.keras.metrics.AUC()])
    
    return model


def main():
    # Caricamento e divisione dei dati (sostituisci con il tuo codice di caricamento dati)
    X_jet_train, X_jet_test, X_fatjet_train, X_fatjet_test, X_PFC_train, X_PFC_test, X_top_train, X_top_test, y_train, y_test = train_test_split(X_jet, X_fatjet, X_PFC, X_top, y, stratify=y, shuffle=True, test_size=0.3)
    
    # Impostazione del numero di CPU
    num_workers = multiprocessing.cpu_count()

    # Impostazioni per il tuner
    epochs = 1000
    batch_size = 250
    objective = kt.Objective("val_auc", direction="max")

    # Creazione del tuner
    tuner = kt.Hyperband(
        model_builder,
        objective=objective,
        max_epochs=epochs,
        factor=3,
        directory=f"{path_to_model_folder}/my_dir",
        project_name="project"
    )
    # Riepilogo dello spazio di ricerca degli iperparametri
    tuner.search_space_summary()

    # Callbacks
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor="val_auc",
        mode="max", 
        patience=40,
        min_delta=1e-5,
        restore_best_weights=True
    )
    
    reduce_LR = tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_auc",
        mode="max", 
        min_delta=1e-10,
        factor=0.1, 
        patience=50, 
        min_lr=1e-15
    )
    
    callback_list = [early_stop, reduce_LR]

    # Esecuzione della ricerca con i dati di addestramento
    tuner.search(
        {"fatjet": X_fatjet_train, "jet": X_jet_train, "PFC": X_PFC_train, "top": X_top_train},
        y_train,
        validation_split=0.3,
        shuffle=True,
        callbacks=callback_list,
        epochs=epochs,
        batch_size=batch_size,
        verbose=1
    )

    # Recupero dei migliori iperparametri
    best_hps = tuner.get_best_hyperparameters(num_trials=1)
    print(f"BEST HPS FOUND:\n{best_hps[0].values}")

    # Salvataggio dei migliori iperparametri in un file JSON
    with open(f"{path_to_model_folder}/best_hps.json", "w") as jsFile:
        json.dump(best_hps[0].values, jsFile, indent=4)


if __name__ == "__main__":
    main()