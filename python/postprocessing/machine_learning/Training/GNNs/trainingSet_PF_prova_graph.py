#!/usr/bin/env python3
import multiprocessing as mp
import os
import sys
import math
import time
import json
import pickle as pkl
import numpy as np
import h5py
import matplotlib.pyplot as plt
import mplhep as hep
from tqdm import tqdm

import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *

hep.style.use(hep.style.CMS)

###############################################################################
# UTILITIES
###############################################################################

def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj, variables_cluster):
    if fj == None:#3j0fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
        mass_dnn[idx_top, 1] = (j0.p4()+j1.p4()+j2.p4()).M()
        mass_dnn[idx_top, 2] = (j0.p4()+j1.p4()+j2.p4()).Pt()
    elif j2 == None:#2j1fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()).M()
        top                  = top2j1fj(fj, j0, j1)
        mass_dnn[idx_top, 1] = top.M()
        mass_dnn[idx_top, 2] = top.Pt()
    else: #3j1fj
        mass_dnn[idx_top, 0] = (j0.p4()+j1.p4()+j2.p4()).M()
        top                  = top3j1fj(fj, j0, j1, j2)
        mass_dnn[idx_top, 1] = top.M()
        mass_dnn[idx_top, 2] = top.Pt()
    # if isinstance(variables_cluster,list):
    #     mass_dnn[idx_top, 2] = variables_cluster[0]
    #     mass_dnn[idx_top, 3] = variables_cluster[1]
    #     mass_dnn[idx_top, 4] = variables_cluster[2]
    return mass_dnn

def boost_PFC(pt_top, eta_top, phi_top, M_top, pt_PFC, eta_PFC, phi_PFC, M_PFC):
    """Effettua il boost delle coordinate di una PFC nel sistema di riferimento del top."""
    pt_old = pt_PFC
    eta_old = eta_PFC
    phi_old = phi_PFC
    mass_old = M_PFC
    
    particle_old = ROOT.TLorentzVector()
    particle_old.SetPtEtaPhiM(pt_old, eta_old, phi_old, mass_old)

    new_frame = ROOT.TLorentzVector()
    new_frame.SetPtEtaPhiM(pt_top, eta_top, phi_top, M_top)

    boost_vector = new_frame.BoostVector()

    particle_old.Boost(-boost_vector.X(), -boost_vector.Y(), -boost_vector.Z())  

    pt_new = particle_old.Pt()
    eta_new = particle_old.Eta()
    phi_new = particle_old.Phi()
    mass_new = particle_old.M()

    return pt_new, eta_new, phi_new, mass_new


def fill_PFCs(n_PFCs, PFCs_dnn, PFCs, idx_top, pt_top, eta_top, phi_top, M_top, boost): 
    """
    Riempie l'array dei nodi (PFCs) con le feature della particella.
    Le colonne sono: pt, eta, phi, massa, d0, dz, charge, pdgId, pvAssocQuality.
    """
    for i, particle in enumerate(PFCs):
        if i < n_PFCs:  # usa i < n_PFCs per indicizzare correttamente da 0
            if boost:
                pt_boost, eta_boost, phi_boost, mass_boost = boost_PFC(pt_top, eta_top, phi_top, M_top,
                                                                       particle.pt, particle.eta, particle.phi, particle.mass)
            else:
                pt_boost, eta_boost, phi_boost, mass_boost = particle.pt, particle.eta, particle.phi, particle.mass
            PFCs_dnn[idx_top, i, 0] = pt_boost
            PFCs_dnn[idx_top, i, 1] = eta_boost
            PFCs_dnn[idx_top, i, 2] = phi_boost
            PFCs_dnn[idx_top, i, 3] = mass_boost
            PFCs_dnn[idx_top, i, 4] = particle.d0
            PFCs_dnn[idx_top, i, 5] = particle.dz
            PFCs_dnn[idx_top, i, 6] = particle.charge
            PFCs_dnn[idx_top, i, 7] = particle.pdgId
            PFCs_dnn[idx_top, i, 8] = particle.pvAssocQuality  
    return PFCs_dnn

###############################################################################
# FUNZIONE DI PROCESSING BATCH
###############################################################################

def process_batch(batch_indexes, inFile_to_open, component, categories, n_PFCs, year, pt_cut, 
                  select_top_over_threshold, thr, verbose):
    rfile = ROOT.TFile.Open(inFile_to_open)
    tree = InputTree(rfile.Get("Events"))
    doLoop = True
    if tree.GetEntries() == 0:
        doLoop = False
    # Inizializza output con dizionario annidato
    batch_output = {component: {cat: 0 for cat in categories}}
    
    if doLoop:
        if year == 2018:
            data_jets      = np.zeros((1,3,8))
            data_fatjets   = np.zeros((1,12))
        elif year == 2022:
            data_jets           = np.zeros((1,3,8))
            data_fatjets        = np.zeros((1,9))
            data_PFC         = np.zeros((1, n_PFCs, 9))

        # Inizializza data_edges e data_edges_feature come array "vuoti" con dimensioni compatibili
        data_mass      = np.zeros((1,3))
        data_label     = np.zeros((1,1))
        event_category = np.zeros((1,1))
        
        if verbose:
            print(f"Starting event loop for component:\t{component}")
        for i in batch_indexes:
            if verbose:
                print(f"Event:\t{i}")
            event = Event(tree, i)
            jets = Collection(event, "Jet")
            fatjets = Collection(event, "FatJet")
            tops = Collection(event, "TopMixed")
            ntops = len(tops)
            PFCands = Collection(event, "PFCands")
            top_PFC_idx = Collection(event, "Indexes")
            variables_cluster     = None
            
            if ntops == 0:
                continue
            for top_num, t in enumerate(tops):
                if t.pt < pt_cut:
                    continue
                if select_top_over_threshold:
                    if t.score_base < thr:
                        continue
                best_top_category = topcategory(t)  # Funzione da definire: ritorna 0, 1 o altro

                # Inizializza le variabili toappend
                if year == 2022:
                    jet_toappend            = np.zeros((1,3,8))
                    fatjet_toappend         = np.zeros((1,9))
                    PFC_toappend            = np.zeros((1, n_PFCs, 9))

                mass_toappend           = np.zeros((1,3))
                label_toappend          = np.zeros((1,1))
                event_category_toappend = np.zeros((1,1))
                
                PFCs = []
                indexes = []
                
                for idx in top_PFC_idx:    
                    indexes.append(idx.idxPFC)
                
                try:
                    start_index = indexes.index(-(top_num+1))
                    end_index = indexes.index(-(top_num+2))
                except ValueError:
                    continue
                idx_to_append = indexes[start_index+1:end_index]
                for particle in PFCands:
                    if particle.Idx in idx_to_append:
                        PFCs.append(particle)
                
                if t.truth != -1:
                    boost = False
                    PFC_toappend = fill_PFCs(n_PFCs=n_PFCs,
                                             PFCs_dnn=PFC_toappend, 
                                             PFCs=PFCs, 
                                             idx_top=0,
                                             pt_top=t.pt,
                                             eta_top=t.eta,
                                             phi_top=t.phi,
                                             M_top=t.mass,
                                             boost=boost)

                    
                    if best_top_category == 0:  # 3j1fj
                        try:
                            fj = fatjets[t.idxFatJet]
                            j0, j1, j2 = jets[t.idxJet0], jets[t.idxJet1], jets[t.idxJet2]
                        except Exception as e:
                            if verbose:
                                print("Errore accesso agli indici dei jets:", e)
                            continue

                        mass_toappend   = fill_mass(mass_dnn=mass_toappend,
                                                        idx_top=0,
                                                        j0=j0,
                                                        j1=j1,
                                                        j2=j2,
                                                        fj=fj,
                                                        variables_cluster=variables_cluster
                                                        )
                        if "QCD" not in component:
                            label_toappend[0] = truth(fj=fj, j0=j0, j1=j1, j2=j2)
                        event_category_toappend[0] = best_top_category

                    elif best_top_category == 1:  # 3j0fj
                        fj = ROOT.TLorentzVector()
                        fj.SetPtEtaPhiM(0, 0, 0, 0)
                        try:
                            j0, j1, j2 = jets[t.idxJet0], jets[t.idxJet1], jets[t.idxJet2]
                        except Exception as e:
                            if verbose:
                                print("Errore accesso agli indici dei jets:", e)
                            continue

                        mass_toappend   = fill_mass(mass_dnn=mass_toappend,
                                                        idx_top=0,
                                                        j0=j0,
                                                        j1=j1,
                                                        j2=j2,
                                                        fj=None,
                                                        variables_cluster=variables_cluster
                                                        )
                        
                        if "QCD" not in component:
                            label_toappend[0] = truth(j0=j0, j1=j1, j2=j2)
                        event_category_toappend[0] = best_top_category

                    else:  # 2j1fj
                        try:
                            fj = fatjets[t.idxFatJet]
                            j0, j1 = jets[t.idxJet0], jets[t.idxJet1]
                        except Exception as e:
                            if verbose:
                                print("Errore accesso agli indici dei jets:", e)
                            continue

                        mass_toappend   = fill_mass(mass_dnn=mass_toappend,
                                                        idx_top=0,
                                                        j0=j0,
                                                        j1=j1,
                                                        j2=None,
                                                        fj=fj,
                                                        variables_cluster=variables_cluster
                                                        )
                        
                        if "QCD" not in component:
                            label_toappend[0] = truth(fj=fj, j0=j0, j1=j1)
                        event_category_toappend[0] = best_top_category
                    
                    
                    data_PFC        = np.append(data_PFC,       PFC_toappend,            axis=0)
                    data_mass       = np.append(data_mass,      mass_toappend,           axis = 0)
                    data_label      = np.append(data_label,     label_toappend,          axis=0)
                    event_category  = np.append(event_category, event_category_toappend, axis=0)

                    
        
        # Definisce l'output per ogni categoria
        event_category = event_category.flatten()
        for cat in categories:
            if "0fj" in cat:
                n = 1
            elif "2j" in cat:
                n = 2
            else:
                n = 0

            batch_output[component][cat] = [data_PFC[event_category == n],
                                            data_mass[event_category == n],
                                            data_label[event_category == n]]
    rfile.Close()
    return batch_output

def merge_batch_output(output, batch_output):
    # Unisce gli output per ciascun componente e categoria
    for component, categories in batch_output.items():
        for cat, data_type in categories.items():
            for i in range(len(data_type)):
                output[component][cat][i] = np.concatenate((output[component][cat][i], data_type[i]), axis=0)
    return output

###############################################################################
# INIT E MAIN
###############################################################################

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-year", dest="year", default=2018, required=False, type=int,
                        help="year of the dataset, to select the correct variables")
    parser.add_argument("-component", dest="component", default=None, required=True, type=str,
                        help="component to run")
    parser.add_argument("-inFile_to_open", dest="inFile_to_open", default=None, required=True, type=str,
                        help="path to root file to run")
    parser.add_argument("-path_to_h5", dest="path_to_h5", default="trainingSet.h5", required=False, type=str,
                        help="path where save h5 to")
    parser.add_argument("-nev", dest="nev", default=-1, required=False, type=int,
                        help="number of events to run (default -1 means all events)")
    parser.add_argument("-select_top_over_threshold", dest="select_top_over_threshold", default=False, action="store_true",
                        help="Default do not select tops above threshold")
    parser.add_argument("-thr", dest="thr", default=0, required=False, type=float,
                        help="score threshold to select tops above it")
    parser.add_argument("-verbose", dest="verbose", default=False, action="store_true",
                        help="Default do not print")
    parser.add_argument('-n', '--n_PFCs', dest='n_PFCs', required=True, default=20, type=int,
                        help='number of particles used for training (default "20")')
    parser.add_argument('-pt', '--pt_cut', dest='pt_cut', required=True, default=0, type=float,
                        help='pt cut for particles used for training (default "0")')
    options = parser.parse_args()

    year = options.year
    component = options.component
    inFile_to_open = options.inFile_to_open
    nev = options.nev    
    path_to_h5 = options.path_to_h5
    select_top_over_threshold = options.select_top_over_threshold
    thr = options.thr
    n_PFCs = options.n_PFCs
    pt_cut = options.pt_cut
    verbose = options.verbose

    print(f"year:                           {year}")
    print(f"component:                      {component}")
    print(f"inFile_to_open:                 {inFile_to_open}")
    print(f"nev:                            {nev}")
    print(f"path_to_h5:                    {path_to_h5}")
    print(f"select_top_over_threshold:      {select_top_over_threshold}")
    print(f"thr:                            {thr}")
    print(f"n_PFCs:                         {n_PFCs}")
    print(f"pt_cut:                         {pt_cut}")
    print(f"verbose:                        {verbose}")

    # Apri il file ROOT per determinare il numero di eventi
    rfile = ROOT.TFile.Open(inFile_to_open)
    tree = InputTree(rfile.Get("Events"))
    if nev == -1:
        nev = tree.GetEntries()
    print(f"Number of events to run:\t{nev}")
    print(f"Number of workers:\t{mp.cpu_count()}")
    rfile.Close()

    # Inizializza output per componenti e categorie
    categories = ["3j0fj", "3j1fj", "2j1fj"]
    #output = {component: {cat: [np.empty((1, n_PFCs, 9)),np.empty((1, 2, 1), dtype=int),np.empty((0, 1))]  for cat in categories}}
    output        = {component: {cat: 0 for cat in categories}}
    num_workers = mp.cpu_count()
    batch_size = nev // num_workers
    print(f"Batch size:\t{batch_size}")
    batches = [range(i, min(i + batch_size, nev)) for i in range(0, nev, batch_size)]
    if verbose:
        print(f"batch:\t{batches}")
    
    with mp.Pool(num_workers) as pool:
        batch_outputs = pool.starmap(process_batch, [
            (batch, inFile_to_open, component, categories, n_PFCs, year, pt_cut, select_top_over_threshold, thr, verbose)
            for batch in batches
        ])

    # Merge degli output dei vari batch
    init = batch_outputs[0]
    for batch_output in batch_outputs[1:]:
        output = merge_batch_output(init, batch_output)

    if path_to_h5 is not None:
        print(f"Saving output to: {path_to_h5}")
        with h5py.File(path_to_h5, 'w') as f:
            # Creazione del gruppo per il componente
            component_group = f.create_group(component)
            for cat, data in output[component].items():
                data_group = component_group.create_group(cat)
                data_group.create_dataset('PFC', data=data[0], compression="gzip")
                data_group.create_dataset('top', data=data[1], compression="gzip")
                data_group.create_dataset('labels', data=data[2], compression="gzip")

    end_time = time.time()
    execution_time = end_time - time.time()
    print(f"Tempo di esecuzione: {execution_time:.5f} secondi")
