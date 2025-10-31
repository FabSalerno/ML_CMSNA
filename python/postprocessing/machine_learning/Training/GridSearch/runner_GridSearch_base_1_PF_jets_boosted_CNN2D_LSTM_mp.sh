#!/usr/bin/bash
cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/GridSearch/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 grid_search_PF_jets_CNN2D_LSTM.py -save_graphics True -pt_flatten False -path_to_h5_folder /eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/Full -h5Name trainingSet_preprocessed_0_pt.h5 -path_to_graphics_folder /eos/user/f/fsalerno/framework/MachineLearning/Grid_search_1/graphics_gridsearch/PF_jets_boosted_CNN2D_LSTM_mp -path_to_model_folder /eos/user/f/fsalerno/framework/MachineLearning/Grid_search_1/grid_search_models/PF_jets_boosted_CNN2D_LSTM_mp -modelName model_base_1
