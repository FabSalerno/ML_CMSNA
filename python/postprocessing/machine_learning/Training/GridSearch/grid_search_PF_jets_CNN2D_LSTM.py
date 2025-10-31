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
inFile                  = "/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_60_boosted_0_pt/trainingSet.h5"
verbose                 = True
####### DATASET LOADING AND PREPROCESSING (remove some False Tops and cut on pt if requested) #######
jet_list, fatjet_list, PFC_list, top_list, labels_list = [], [], [], [], []

try:
    with h5py.File(inFile, 'r') as f:
        print("File is a valid HDF5 file")
except Exception as e:
    print(f"Error: {e}")
'''
with h5py.File(inFile, "r") as f:
    components = f.keys()
    for c in f.keys():
        if c in samples:
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
                    if len(ids_todrop_pt) > 0:
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




X_jet           = np.concatenate(jet_list, axis=0)
X_fatjet        = np.concatenate(fatjet_list, axis=0)
X_PFC           = np.concatenate(PFC_list, axis=0) 
X_PFC           = X_PFC[:,:nPFCs,:]
X_top           = np.concatenate(top_list, axis=0)        
y               = np.concatenate(labels_list, axis=0)
'''
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


    # Input Layers

    # Input Layers
    fj_inputs           = tf.keras.Input(shape=(InputShape_FatJet,),   name="fatjet")               #x
    jet_inputs          = tf.keras.Input(shape=(None,InputShape_Jet,), name="jet")                  #y
    PFC_inputs          = tf.keras.Input(shape=(nPFCs,InputShape_PFC,), name="PFC")                  #z
    top_inputs          = tf.keras.Input(shape=(InputShape_Top,),      name="top")                  #t                #t
    print("\nJet",jet_inputs ,"FatJet",fj_inputs ,"PFC",PFC_inputs,"top",top_inputs)

    ### Operations on FATJET Input Layer ###
    x = BatchNormalization()(fj_inputs)
    # Tune parameters for FatJet Input Layer #
#     fj_units              = hp.Int("fj_units", min_value=1, max_value=20, step=1)
    fj_units              = hp.Int("fj_units", min_value=1, max_value=10, step=1)
    fj_activation         = hp.Choice("fj_activation", values=["relu", "sigmoid", "tanh"])
#     fj_kernel_initializer = hp.Choice("fj_kernel_initializer", values=["glorot_uniform", "glorot_normal", "random_uniform", "random_normal", "zeros", "ones"])
    fj_kernel_initializer = hp.Choice("fj_kernel_initializer", values=["random_uniform", "random_normal"])
    x                     = Dense(units=fj_units,
                                  activation=fj_activation,
                                  kernel_initializer=fj_kernel_initializer
                                 )(x)
    ### Operations on JET Input Layer ###
    y = Masking(mask_value=0.)(jet_inputs)
    y = BatchNormalization()(y)
    # Tune parameters for Jet Input Layer #
    # j_units              = hp.Int("j_units", min_value=1, max_value=20, step=1)
    j_units              = hp.Int("j_units", min_value=2, max_value=20, step=2)
    j_activation         = hp.Choice("j_activation", values=["relu", "sigmoid", "tanh"])
    # j_activation         = hp.Choice("j_activation", values=["relu"])
#     j_kernel_initializer = hp.Choice("j_kernel_initializer", values=["glorot_uniform", "glorot_normal", "random_uniform", "random_normal", "zeros", "ones"])
    j_kernel_initializer = hp.Choice("j_kernel_initializer", values=["random_uniform", "random_normal"])
    j_dropout            = hp.Choice("j_dropout", values=list(np.arange(0,1,0.3)))
#     y = keras.layers.SimpleRNN(5, activation="relu", kernel_initializer="random_normal")(y)
    
    y                    = tf.keras.layers.LSTM(units=j_units,
                                             activation=j_activation,
                                             kernel_initializer=j_kernel_initializer,
                                             dropout=j_dropout
                                            )(y)
    print("Output shape after JET LSTM:", y.shape)
    ### Operations on JET Input Layer ###
    z = Masking(mask_value=0.)(PFC_inputs[:,:,:3])
    z = tf.expand_dims(z, axis=-1)
   
    PFC_activation= hp.Choice("PFC_activation", values=["relu", "sigmoid", "tanh"])
    PFC_kernel_initializer= hp.Choice("PFC_kernel_initializer", values=["random_uniform", "random_normal"])
    dropout_1= hp.Choice("dropout_1", values=[0.3, 0.5])
    dropout_2= hp.Choice("dropout_2", values=[0.3, 0.5])
    lstm_units= hp.Int("lstm_units", min_value=2, max_value=20, step=2)
    #Conv2D layer
    z = Conv2D(filters=32, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01))(z)
    z = BatchNormalization()(z)
    #z = MaxPooling2D(pool_size=2)(z)
    
    z = Conv2D(filters=64, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01))(z)
    z = BatchNormalization()(z)
    #z = MaxPooling2D(pool_size=2)(z)

    z = Conv2D(filters=128, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01))(z)
    z = BatchNormalization()(z)
    
    # Flatten the output for dense layers
    z = Flatten()(z)

    print("pre-dense",z.shape)

    z = Dense(256, activation='relu')(z)  #
    z = Dropout(dropout_1)(z)                   

    # Second Dense layer
    z = Dense(64, activation='relu')(z)   
    z = Dropout(dropout_2)(z)                  

    # Third Dense layer (optional)
    z = Dense(16, activation='relu')(z)   
    z = Dense(4, activation='relu')(z)
    z = BatchNormalization()(z)
    

    
    
    # PFC layer
    p = Masking(mask_value=0.)(PFC_inputs[:,:,3:])
    p = BatchNormalization()(p)
    
    p = LSTM(units=lstm_units, activation=PFC_activation, kernel_initializer=PFC_kernel_initializer, dropout=0.5)(p)


    ### Operations on TOP Input Layer ###
    t = Dense(units=1,
              activation="relu"
              )(top_inputs)
    ### Operations on JET+FATJET Input Layer ###
    x = concatenate([x,y])
    x = concatenate([x,z])
    x = concatenate([x,t])
    print("Shape after concatenation:", x.shape)
    x = Dense(units=5,
              activation="relu",
              kernel_initializer="random_normal"
              )(x)
    #  x = Dropout(dropout)(x)

    outputs = Dense(1, activation="sigmoid")(x) 
    model   = tf.keras.Model(inputs=[fj_inputs, jet_inputs, PFC_inputs, top_inputs], outputs=outputs)
    
    # things
    l_rate  = hp.Float("learning_rate", 1e-4, 1e-1, sampling="log", default=1e-3)
    # trainer = tf.keras.optimizers.Adam(learning_rate=0.05)
    trainer = tf.keras.optimizers.Adam(learning_rate=l_rate)
    loss    = tf.keras.losses.BinaryCrossentropy()
    model.compile(optimizer=trainer, loss=loss, metrics=[tf.keras.metrics.AUC()])
    model.summary()
    return model



########## GRIDSEARCH ##########
epochs        = 1000
# batch_size    = 50
batch_size    = 250
# Define the objective as a Keras Tuner Objective
objective = kt.Objective("val_auc", direction="max")
# keras_tuner.RandomSearch
tuner = kt.Hyperband(model_builder,
                     objective=objective,
                     max_epochs=epochs,
                     factor=3,
                     directory=f"{path_to_model_folder}/my_dir",
                     project_name="project"
                    )

tuner.search_space_summary()

### CALLBACKS FUNCTIONS ###
# early_stop = keras.callbacks.EarlyStopping(monitor="val_loss",
#                                            mode="min", # quantity that has to be monitored(to be minimized in this case)
#                                            patience=40, # number of epochs with no improvement after which training will be stopped.
#                                            min_delta=1e-5,
#                                            restore_best_weights=True) # update the model with the best-seen weights
early_stop = tf.keras.callbacks.EarlyStopping(monitor="val_auc",
                                            mode="max", # quantity that has to be monitored(to be minimized in this case)
                                            patience=40, # number of epochs with no improvement after which training will be stopped.
                                            min_delta=1e-5,
                                            restore_best_weights=True) # update the model with the best-seen weights

# Reduce learning rate when a metric has stopped improving
reduce_LR = tf.keras.callbacks.ReduceLROnPlateau(monitor="val_auc",
                                                mode="max",# quantity that has to be monitored
                                                min_delta=1e-10,
                                                factor=0.1, # factor by which LR has to be reduced...
                                                patience=50, #...after waiting this number of epochs with no improvements on monitored quantity
                                                min_lr=1e-15) 
callback_list = [early_stop, reduce_LR]


### GRIDSEARCH Optimization ###
tuner.search({"fatjet": X_fatjet_train, "jet": X_jet_train, "PFC": X_PFC_train, "top": X_top_train}, y_train,
             validation_split=0.3, shuffle=True, callbacks=callback_list,
             epochs=epochs, batch_size=batch_size, verbose=1
            )

# Get the optimal hyperparameters
best_hps = tuner.get_best_hyperparameters(num_trials=1)
print(f"BEST HPS FOUND:\n{best_hps[0].values}")

# Save best_hps to json file
with open(f"{path_to_model_folder}/best_hps.json", "w") as jsFile:
    # f.write(best_hps[0].values)
    json.dump(best_hps[0].values, jsFile, indent=4)