import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.TROTA_eval.tools import *
import numpy as np
from array import array
from collections import Counter
import itertools
import json
import os



def check_same_top(topmixed1, topmixed2, resolved = False):
    if not resolved:
        idx_fj_1, idx_j0_1, idx_j1_1, idx_j2_1 = topmixed1.idxFatJet, topmixed1.idxJet0, topmixed1.idxJet1, topmixed1.idxJet2
        idx_fj_2, idx_j0_2, idx_j1_2, idx_j2_2 = topmixed2.idxFatJet, topmixed2.idxJet0, topmixed2.idxJet1, topmixed2.idxJet2
    else:
        idx_fj_1, idx_j0_1, idx_j1_1, idx_j2_1 = -1, topmixed1.idxJet0, topmixed1.idxJet1, topmixed1.idxJet2
        idx_fj_2, idx_j0_2, idx_j1_2, idx_j2_2 = -1, topmixed2.idxJet0, topmixed2.idxJet1, topmixed2.idxJet2
    list_1 = [idx_j0_1, idx_j1_1, idx_j2_1]
    list_2 = [idx_j0_2, idx_j1_2, idx_j2_2]

    intersection = list(set(list_1) & set(list_2))
    check_jets = len(intersection) > 0
    check_fj = (idx_fj_1 == idx_fj_2) and (idx_fj_1 != -1 and idx_fj_2 != -1) 
    return check_jets or check_fj

def selectTop(topmixed, resolved = False, year = 2022):
    if len(topmixed) == 0: return []
    # print([top.TopScore for top in topmixed])
    if resolved==False:
        if year == 2018:
            attr_name = f"TopScore"
        elif year == 2022:
            if model == "TROTA":
                attr_name = f"TopScore_nominal"
            else:
                attr_name = f"TopScore_{model}"
    elif resolved==True:
        if year == 2018:
            attr_name = f"TopScore"
        elif year == 2022:
            if model == "TROTA":
                attr_name = f"TopScore_nominal"
            else:
                attr_name = f"TopScore"

    topmixed_sorted = sorted(topmixed, key=lambda x: getattr(x, attr_name), reverse=True)
   
    # print("sorted ", [top.TopScore for top in topmixed_sorted])
    topselected = []
    for i, top in enumerate(topmixed_sorted):
        if(i==0):
            topselected.append(top)
        else:
            same_top = False
            for bestTop in topselected:
                same_top = check_same_top(top, bestTop, resolved = resolved)
                if same_top: break
            if not same_top:
                topselected.append(top)
    #print("starting number of tops", len(topmixed))
    #print("number of selected tops", len(topselected))
    return topselected

def sortTop(topmixed, resolved = False, year = 2022):
    if len(topmixed) == 0: return []
    # print([top.TopScore for top in topmixed])
    if year == 2018:
        topmixed_sorted = sorted(topmixed, key=lambda x: x.TopScore, reverse=True)
    elif year == 2022:
        score= f"TopScore_nominal" if resolved else f"TopScore"
        topmixed_sorted = sorted(topmixed, key=lambda x: x.TopScore_nominal, reverse=True)
    # print("sorted ", [top.TopScore for top in topmixed_sorted])
    topselected = []
    for i, top in enumerate(topmixed_sorted):
        topselected.append(top)

    return topselected

def removeResolved(topmixed):
    if len(topmixed) == 0: return []
    topselected = []
    for top in topmixed:
        if top.idxFatJet != -1:
            topselected.append(top)
    return topselected

# def matchingTopResGenPart_first(genpart, top_res, jets):
#     top_res_matched_q = []

#     b  = None
#     q  = None
#     q_ = None
#     sign_w = 0
    
#     for part in genpart:
#         #se non è prompt(non generata dai gluoni) e prima copia 
#         if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))): #la parte su statusFlag controlla se il 12esimo bit è 0 o 1 (1 << 12:Sposta il bit "1" di 12 posizioni verso sinistra & controlla bit a bit) il 12 slot indica se è la prima copia della particella
#             #se è un quark non top e la madre è un w e la nonna è un top
#             if(abs(part.pdgId)<6 and abs(genpart[part.genPartIdxMother_prompt].pdgId)==24 and abs(genpart[genpart[part.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId)==6):
#                 sign_w = genpart[part.genPartIdxMother_prompt].pdgId/24
#                 #assegna a q o q_ la particella selezionata (non importa quale a q o q_)
#                 if(q==None): q = part
#                 elif(q_==None): q_ = part
#                 else: continue
#     for part in genpart:
#         if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))):
#             if(part.pdgId ==5*sign_w and abs(genpart[part.genPartIdxMother_prompt].pdgId)==6):
#                 b = part  

#     #print(top_res)
#     for top in top_res:
#         j0 = jets[top.idxJet0]
#         j1 = jets[top.idxJet1]
#         j2 = jets[top.idxJet2]
#         top_jets = [j0, j1, j2]
#         #quarks = [b,q,q_]

#         #se tutti i quark sono stati trovati
#         if (b!=None and q!=None and q_!=None):
#             #!!qui sto introducendo una gerarchia intrinseca tra quark
#             bjet, drb    = closest(b, top_jets)
#             #print("pre remove bjet", top_jets)
#             top_jets.remove(bjet)
#             #print("post remove bjet", top_jets)
#             qjet, drq    = closest(q, top_jets)
#             top_jets.remove(qjet)
#             #print("post remove qjet", top_jets)
#             q_jet, drq_  = closest(q_, top_jets)
#             top_jets.remove(q_jet)
#             #print("post remove q_jet", top_jets
            
#         else:
#             drb, drq, drq_ = 1000, 1000, 1000
#         #se la distanza tra ogni quark e il proprio jet è minore di 0.4 ritorna i 3 oggetti

 
#         if(drb<0.4 and drq<0.4 and drq_<0.4) and len(top_jets)==0:
#             top_res_matched_q.append(top)
#             #print(bjet,qjet,q_jet)

#     return top_res_matched_q

# def matchingTopResGenPart_second(genpart, top_res, jets):
#     top_res_matched_q = []

#     b  = None
#     q  = None
#     q_ = None
#     sign_w = 0
    
#     for part in genpart:
#         #se non è prompt(non generata dai gluoni) e prima copia 
#         if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))): #la parte su statusFlag controlla se il 12esimo bit è 0 o 1 (1 << 12:Sposta il bit "1" di 12 posizioni verso sinistra & controlla bit a bit) il 12 slot indica se è la prima copia della particella
#             #se è un quark non top e la madre è un w e la nonna è un top
#             if(abs(part.pdgId)<6 and abs(genpart[part.genPartIdxMother_prompt].pdgId)==24 and abs(genpart[genpart[part.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId)==6):
#                 sign_w = genpart[part.genPartIdxMother_prompt].pdgId/24
#                 #assegna a q o q_ la particella selezionata (non importa quale a q o q_)
#                 if(q==None): q = part
#                 elif(q_==None): q_ = part
#                 else: continue
#     for part in genpart:
#         if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))):
#             if(part.pdgId ==5*sign_w and abs(genpart[part.genPartIdxMother_prompt].pdgId)==6):
#                 b = part  

#     #print(top_res)
#     for top in top_res:
#         j0 = jets[top.idxJet0]
#         j1 = jets[top.idxJet1]
#         j2 = jets[top.idxJet2]
#         top_jets = [j0, j1, j2]
#         #quarks = [b,q,q_]
#         matched_jets = []
        
#         j_duplicate = []
#         j_not_matched = []
#         #se tutti i quark sono stati trovati
#         if (b!=None and q!=None and q_!=None):
#             #!!qui sto introducendo una gerarchia intrinseca tra quark
#             bjet, drb    = closest(b, top_jets)
#             #print("pre remove bjet", top_jets)
#             #top_jets.remove(bjet)
#             matched_jets.append(bjet)
#             #print("post remove bjet", top_jets)
#             qjet, drq    = closest(q, top_jets)
#             #top_jets.remove(qjet)
#             matched_jets.append(qjet)
#             #print("post remove qjet", top_jets)
#             q_jet, drq_  = closest(q_, top_jets)
#             #top_jets.remove(q_jet)
#             matched_jets.append(q_jet)
#             #print("post remove q_jet", top_jets)
#             j_not_matched = list(set(top_jets) - set(matched_jets))
#             j_duplicate = [elem for elem, count in Counter(matched_jets).items() if count != 1]
#             #print(j_not_matched)
#             #print(j_duplicate)
#             i=0
#             selected_jets=matched_jets
#             while len(j_duplicate)!=0:
#                 i+=1
#                 #print("iterazione", i)
#                 matched_quarks_to_same_jet = []
#                 if j_duplicate[0] == selected_jets[0]:
#                     matched_quarks_to_same_jet.append(b)
#                     #print("b")
#                 if j_duplicate[0] == selected_jets[1]:
#                     matched_quarks_to_same_jet.append(q)
#                     #print("q")
#                 if j_duplicate[0] == selected_jets[2]:
#                     matched_quarks_to_same_jet.append(q_)   
#                     #print("q_")
#                 #print(matched_quarks_to_same_jet)
#                 for j in j_not_matched:
#                     closest_quark, dr = closest(j,matched_quarks_to_same_jet)
#                     if closest_quark == b:
#                         bjet = j
#                         drb=dr
#                     if closest_quark == q:
#                         qjet = j
#                         drq=dr
#                     if closest_quark == q_:
#                         q_jet = j
#                         drq_=dr
#                 selected_jets=[bjet,qjet,q_jet]
#                 #print("selected_jets",selected_jets)
#                 j_not_matched = list(set(top_jets) - set(selected_jets))
#                 #print("j_not_matched",j_not_matched)
#                 j_duplicate = [jet for jet, count in Counter(selected_jets).items() if count > 1]
#         else:
#             drb, drq, drq_ = 1000, 1000, 1000
#         #se la distanza tra ogni quark e il proprio jet è minore di 0.4 ritorna i 3 oggetti
#         selected_jets=[bjet,qjet,q_jet]
#         j_not_matched_2 = []
#         j_duplicate_2 = []
#         j_not_matched_2 = list(set(top_jets) - set(selected_jets))
#         j_duplicate_2 = [jet for jet, count in Counter(selected_jets).items() if count > 1]
#         if len(j_duplicate_2)!=0 :#and (drb<0.4 or drq<0.4 or drq_<0.4):
#                     print("\n CHE SUCCEDE \n")
#                     print("non match before",j_not_matched)
#                     print("non match",j_not_matched_2)
#                     print("match before",matched_jets)
#                     print("match",selected_jets)
#         if(drb<0.4 and drq<0.4 and drq_<0.4):
#             top_res_matched_q.append(top)
#             #print(bjet,qjet,q_jet)

#     return top_res_matched_q


def matchingTopResGenPart(genpart, top_res, jets):
    top_res_matched_q = []

    b  = None
    q  = None
    q_ = None
    sign_w = 0
    
    for part in genpart:
        #se non è prompt(non generata dai gluoni) e prima copia 
        if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))): #la parte su statusFlag controlla se il 12esimo bit è 0 o 1 (1 << 12:Sposta il bit "1" di 12 posizioni verso sinistra & controlla bit a bit) il 12 slot indica se è la prima copia della particella
            #se è un quark non top e la madre è un w e la nonna è un top
            if(abs(part.pdgId)<6 and abs(genpart[part.genPartIdxMother_prompt].pdgId)==24 and abs(genpart[genpart[part.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId)==6):
                sign_w = genpart[part.genPartIdxMother_prompt].pdgId/24
                #assegna a q o q_ la particella selezionata (non importa quale a q o q_)
                if(q==None): q = part
                elif(q_==None): q_ = part
                else: continue
    for part in genpart:
        if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))):
            if(part.pdgId ==5*sign_w and abs(genpart[part.genPartIdxMother_prompt].pdgId)==6):
                b = part  

    #print(top_res)
    for top in top_res:
        j0 = jets[top.idxJet0]
        j1 = jets[top.idxJet1]
        j2 = jets[top.idxJet2]
        top_jets = [j0, j1, j2]
        quarks = [b,q,q_]
        #se tutti i quark sono stati trovati
        if (b!=None and q!=None and q_!=None):
            for jets_comb in itertools.permutations(top_jets, len(quarks)):
                # Calcola le distanze per questa combinazione
                valid_combination = True
                for jet, quark in zip(jets_comb, quarks):
                    #questa cosa è fatta jet per jet e quark per quark, l'ordine dei quark rimane invariato, mentre quello dei jet varia a ogni permutazione risultando in tutte le possibili combinazioni
                    #dr = deltaR(quark.eta, quark.phi, jet.eta, jet.phi) 
                    _, dr = closest(quark, [jet]) 
                    if dr >= 0.4:
                        valid_combination = False
                        break  # Se una distanza è maggiore della soglia, salta questa combinazione
        
                if valid_combination==True:                   
                    top_res_matched_q.append(top)
                    #break
                    #print(bjet,qjet,q_jet)

    return top_res_matched_q

def matchingTopMerGenPart(genpart, top_mer):
    top_mer_matched_q = []

    b  = None
    q  = None
    q_ = None
    sign_w = 0
    for part in genpart:
        #se non è prompt(non generata dai gluoni) e prima copia 
        if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))): #la parte su statusFlag controlla se il 12esimo bit è 0 o 1 (1 << 12:Sposta il bit "1" di 12 posizioni verso sinistra & controlla bit a bit) il 12 slot indica se è la prima copia della particella
            #se è un quark non top e la madre è un w e la nonna è un top
            if(abs(part.pdgId)<6 and abs(genpart[part.genPartIdxMother_prompt].pdgId)==24 and abs(genpart[genpart[part.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId)==6):
                sign_w = genpart[part.genPartIdxMother_prompt].pdgId/24
                #assegna a q o q_ la particella selezionata (non importa quale a q o q_)
                if(q==None): q = part
                elif(q_==None): q_ = part
                else: continue
    for part in genpart:
        if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))):
            if(part.pdgId ==5*sign_w and abs(genpart[part.genPartIdxMother_prompt].pdgId)==6):
                b = part 

    for top in top_mer:
        #se tutti i quark sono stati trovati
        if (b!=None and q!=None and q_!=None): 
            #!!qui sto introducendo una gerarchia intrinseca tra quark
            drb    = deltaR(b.eta, b.phi, top.eta, top.phi)
            drq    = deltaR(q.eta, q.phi, top.eta, top.phi)
            drq_   = deltaR(q_.eta, q_.phi, top.eta, top.phi)
        else:
            drb, drq, drq_ = 1000, 1000, 1000
        #se la distanza tra ogni quark e il proprio jet è minore di 0.4 ritorna i 3 oggetti
        if(drb<0.8 and drq<0.8 and drq_<0.8):
            top_mer_matched_q.append(top)

    return top_mer_matched_q

def matchingRecoTopGenTop(gentop, recotop, dR):
    # if len(gentop)==1:  top = gentop[0] # sempre vero per tt semilep
    top_reco_matched = []
    for top_r in recotop: 
        # Funziona solo per semilep
        dRGenTopRecoTop = deltaR(gentop[0].eta, gentop[0].phi, top_r.eta, top_r.phi) 
        if(dRGenTopRecoTop<dR): 
            top_reco_matched.append(top_r)
    return top_reco_matched

def thresholdTopScore(topreco, Top_threshold, top_type, year):
    topselected_loose = []
    topselected_medium = []
    topselected_tight = []
    if top_type == 'Mixed':
        if year == 2018:
            attr_name = f"TopScore"
        elif year == 2022:
            if model == "TROTA":
                attr_name = f"TopScore_nominal"
            else:
                attr_name = f"TopScore_{model}"
    elif top_type == 'Resolved':
        if year == 2018:
            attr_name = f"TopScore"
        elif year == 2022:
            if model == "TROTA":
                attr_name = f"TopScore_nominal"
            else:
                attr_name = f"TopScore"
    elif top_type == 'Merged':
        if year == 2018:
            attr_name = f"particleNet_TvsQCD"
        elif year == 2022:
            attr_name = f"particleNetWithMass_TvsQCD"
    
    for i, t in enumerate(topreco):
        score = getattr(t, attr_name) 
        if score > float(Top_threshold[top_type]['WPloose']):
            topselected_loose.append(t)
        if score > float(Top_threshold[top_type]['WPmedium']):
            topselected_medium.append(t)
        if score > float(Top_threshold[top_type]['WPtight']):
            topselected_tight.append(t)
    return topselected_loose, topselected_medium, topselected_tight 

with open("dict_samples_2022.json", "r") as f:
    sample = json.load(f)

###########INPUTS###########
year = 2022
#model = "60_CNN_2D_LSTM_0_pt" #"TROTA"
model = "60_CNN_2D_2_0_pt"
sample_name = "TT_semilep" #"TT_semilep""TprimeToTZ_1800" 
#sample_name = "TprimeToTZ_1800"
#############################
if year == 2018:   
    if sample_name == "TT_semilep": 
        file = "root://cms-xrd-global.cern.ch//store/user/acagnott/Run3Analysis_Tprime/TT_semilep_2018/20240731_214516/tree_hadd_755.root"
    elif sample_name == "TprimeToTZ_1800":
        file = "root://cms-xrd-global.cern.ch//store/user/acagnott/DM_Run3_v0/TprimeBToTZ_M-1800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/TprimeToTZ_1800_2018/231222_111355/0000/tree_hadd_1.root"
    print(f"Using file: {file}")
    chain = ROOT.TChain('Events')
    chain.Add(file)
elif year == 2022:
    ##########CAMBIA####################
    if model == "TROTA":
        if sample_name == "TT_semilep": 
            file_dict = sample["TT_semilep_2022"]["TT_semilep_2022"]
            file_idx = file_dict["ntot"].index(max(file_dict["ntot"]))
            file = file_dict["strings"][file_idx]
        elif sample_name == "TprimeToTZ_1800":
            file_dict = sample["TprimeToTZ_1800_2022"]["TprimeToTZ_1800_2022"]
            file_idx = file_dict["ntot"].index(max(file_dict["ntot"]))
            file = file_dict["strings"][file_idx]
        chain = ROOT.TChain('Events')
        chain.Add(file)
        print(f"Using file: {file}")
        # for i in range(0,20):
        #     file=file_dict["strings"][i]
        #     print(f"Using file: {file}")
        #     chain.Add(file)
    else:
        file="/eos/user/f/fsalerno/Data/PF/topevaluate/nano_mcRun3_TT_semilep_MC2022_evaluate_presel.root"
        chain = ROOT.TChain('Events')
        chain.Add(file)

tree = InputTree(chain)



dir_path = f"/eos/user/f/fsalerno/Evaluation/{model}_{year}_studies/Histo_files"
if not os.path.exists(dir_path):  
    os.makedirs(dir_path)   
outfile = ROOT.TFile(f"{dir_path}/output_{model}_efficiency_Study_{sample_name}_ResinMix.root","RECREATE") ##RESIn




###############!!! DA CONTROLLARE I WORKING POINTS 2022!!!#############

if year == 2018:
    Top_threshold = {"Resolved" :{'WPloose': "0.24193972", 'WPmedium': "0.5411276", 'WPtight': "0.77197933"},
                    "Mixed"    :{'WPloose': "0.2957885265350342", 'WPmedium': "0.7584613561630249", 'WPtight': "0.9129540324211121"},
                    "Merged"   :{'WPloose': "0.79", 'WPmedium': "0.91", 'WPtight': "0.97"}}

elif year == 2022:
    if model == "TROTA":
        Top_threshold = {"Resolved" :{'WPloose': "0.1422998", 'WPmedium': "0.59264845", 'WPtight': "0.86580896"},
                        "Mixed"    :{'WPloose': "0.7214655876159668", 'WPmedium': "0.9436638951301575", 'WPtight': "0.9789741635322571"},
                        "Merged"   :{'WPloose': "0.04", 'WPmedium': "0.78", 'WPtight': "0.97"}}
    
    elif model == "60_CNN_2D_2_0_pt":
        Top_threshold = {"Resolved" :{'WPloose': "0.1422998", 'WPmedium': "0.59264845", 'WPtight': "0.86580896"},
                        "Mixed"    :{'WPloose': "0.7306278944015503", 'WPmedium': "0.9499862790107727", 'WPtight': "0.9882013201713562"},
                        "Merged"   :{'WPloose': "0.04", 'WPmedium': "0.78", 'WPtight': "0.97"}}
    
    elif model == "60_CNN_2D_LSTM_2_0_pt":
        Top_threshold = {"Resolved" :{'WPloose': "0.1422998", 'WPmedium': "0.59264845", 'WPtight': "0.86580896"},
                        "Mixed"    :{'WPloose': "0.775947093963623", 'WPmedium': "0.9538450837135315", 'WPtight': "0.9883949756622314"},
                        "Merged"   :{'WPloose': "0.04", 'WPmedium': "0.78", 'WPtight': "0.97"}}
    
    elif model == "60_CNN_2D_0_pt":
        Top_threshold = {"Resolved" :{'WPloose': "0.1422998", 'WPmedium': "0.59264845", 'WPtight': "0.86580896"},
                        "Mixed"    :{'WPloose': "0.4034062922000885", 'WPmedium': "0.9563592672348022", 'WPtight': "0.9907968044281006"},
                        "Merged"   :{'WPloose': "0.04", 'WPmedium': "0.78", 'WPtight': "0.97"}}
    
    elif model == "60_CNN_2D_LSTM_0_pt":
        Top_threshold = {"Resolved" :{'WPloose': "0.1422998", 'WPmedium': "0.59264845", 'WPtight': "0.86580896"},
                        "Mixed"    :{'WPloose': "0.46164312958717346", 'WPmedium': "0.9724888205528259", 'WPtight': "0.9925932288169861"},
                        "Merged"   :{'WPloose': "0.04", 'WPmedium': "0.78", 'WPtight': "0.97"}}
    

###############!!! DA CONTROLLARE I WORKING POINTS 2022 !!!#############


h_GenTop_pt              = ROOT.TH1D("h_gentop_pt","; genTop pT", 20, 0, 1000)
h_GenTop_pt_exist_resolved              = ROOT.TH1D("h_gentop_pt_exist_resolved","; genTop pT", 20, 0, 1000)
h_GenTop_pt_exist_mixed              = ROOT.TH1D("h_gentop_pt_exist_mixed","; genTop pT", 20, 0, 1000)
h_GenTop_pt_exist_merged              = ROOT.TH1D("h_gentop_pt_exist_merged","; genTop pT", 20, 0, 1000)
h_GenTop_pt_Reconstructable_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_pt_Reconstructable_QuarkMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_Reconstructable_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_pt_Reconstructable_QuarkMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_Reconstructable_QuarkMatch_Merged      = ROOT.TH1D("h_Top_pt_Reconstructable_QuarkMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_Reconstructable_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_pt_Reconstructable_GenTopMatch02_Resolved","; genTop pT matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_pt_Reconstructable_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_pt_Reconstructable_GenTopMatch02_Mixed","; genTop pT matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_pt_Reconstructable_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_pt_Reconstructable_GenTopMatch02_Merged","; genTop pT matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_pt_Reconstructable_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_pt_Reconstructable_GenTopMatch04_Resolved","; genTop pT matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_pt_Reconstructable_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_pt_Reconstructable_GenTopMatch04_Mixed","; genTop pT matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_pt_Reconstructable_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_pt_Reconstructable_GenTopMatch04_Merged","; genTop pT matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_pt_Reconstructable_OldMatch_Resolved    = ROOT.TH1D("h_Top_pt_Reconstructable_OldMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_Reconstructable_OldMatch_Mixed       = ROOT.TH1D("h_Top_pt_Reconstructable_OldMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_Reconstructable_OldMatch_Merged      = ROOT.TH1D("h_Top_pt_Reconstructable_OldMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_Selection_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_pt_Selection_QuarkMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_Selection_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_pt_Selection_QuarkMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_Selection_QuarkMatch_Merged      = ROOT.TH1D("h_Top_pt_Selection_QuarkMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_Selection_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_pt_Selection_GenTopMatch02_Resolved","; genTop pT matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_pt_Selection_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_pt_Selection_GenTopMatch02_Mixed","; genTop pT matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_pt_Selection_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_pt_Selection_GenTopMatch02_Merged","; genTop pT matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_pt_Selection_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_pt_Selection_GenTopMatch04_Resolved","; genTop pT matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_pt_Selection_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_pt_Selection_GenTopMatch04_Mixed","; genTop pT matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_pt_Selection_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_pt_Selection_GenTopMatch04_Merged","; genTop pT matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_pt_Selection_OldMatch_Resolved    = ROOT.TH1D("h_Top_pt_Selection_OldMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_Selection_OldMatch_Mixed       = ROOT.TH1D("h_Top_pt_Selection_OldMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_Selection_OldMatch_Merged      = ROOT.TH1D("h_Top_pt_Selection_OldMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_pt_RealLife_QuarkMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_pt_RealLife_QuarkMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_QuarkMatch_Merged      = ROOT.TH1D("h_Top_pt_RealLife_QuarkMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_OldMatch_Resolved    = ROOT.TH1D("h_Top_pt_RealLife_OldMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_OldMatch_Mixed       = ROOT.TH1D("h_Top_pt_RealLife_OldMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_OldMatch_Merged      = ROOT.TH1D("h_Top_pt_RealLife_OldMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_pt_RealLife_GenTopMatch02_Resolved","; genTop pT matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_pt_RealLife_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_pt_RealLife_GenTopMatch02_Mixed","; genTop pT matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_pt_RealLife_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_pt_RealLife_GenTopMatch02_Merged","; genTop pT matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_pt_RealLife_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_pt_RealLife_GenTopMatch04_Resolved","; genTop pT matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_pt_RealLife_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_pt_RealLife_GenTopMatch04_Mixed","; genTop pT matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_pt_RealLife_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_pt_RealLife_GenTopMatch04_Merged","; genTop pT matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagLooseWP_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_pt_TagLooseWP_QuarkMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_TagLooseWP_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_pt_TagLooseWP_QuarkMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_TagLooseWP_QuarkMatch_Merged      = ROOT.TH1D("h_Top_pt_TagLooseWP_QuarkMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_TagLooseWP_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_pt_TagLooseWP_GenTopMatch02_Resolved","; genTop pT matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagLooseWP_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_pt_TagLooseWP_GenTopMatch02_Mixed","; genTop pT matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagLooseWP_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_pt_TagLooseWP_GenTopMatch02_Merged","; genTop pT matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagLooseWP_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_pt_TagLooseWP_GenTopMatch04_Resolved","; genTop pT matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagLooseWP_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_pt_TagLooseWP_GenTopMatch04_Mixed","; genTop pT matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagLooseWP_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_pt_TagLooseWP_GenTopMatch04_Merged","; genTop pT matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagLooseWP_OldMatch_Resolved    = ROOT.TH1D("h_Top_pt_TagLooseWP_OldMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_TagLooseWP_OldMatch_Mixed       = ROOT.TH1D("h_Top_pt_TagLooseWP_OldMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_TagLooseWP_OldMatch_Merged      = ROOT.TH1D("h_Top_pt_TagLooseWP_OldMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_TagWP_5_100_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_pt_TagWP_5_100_QuarkMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_TagWP_5_100_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_pt_TagWP_5_100_QuarkMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_TagWP_5_100_QuarkMatch_Merged      = ROOT.TH1D("h_Top_pt_TagWP_5_100_QuarkMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_TagWP_5_100_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_pt_TagWP_5_100_GenTopMatch02_Resolved","; genTop pT matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagWP_5_100_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_pt_TagWP_5_100_GenTopMatch02_Mixed","; genTop pT matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagWP_5_100_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_pt_TagWP_5_100_GenTopMatch02_Merged","; genTop pT matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagWP_5_100_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_pt_TagWP_5_100_GenTopMatch04_Resolved","; genTop pT matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagWP_5_100_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_pt_TagWP_5_100_GenTopMatch04_Mixed","; genTop pT matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagWP_5_100_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_pt_TagWP_5_100_GenTopMatch04_Merged","; genTop pT matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_pt_TagMediumWP_QuarkMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_pt_TagMediumWP_QuarkMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_QuarkMatch_Merged      = ROOT.TH1D("h_Top_pt_TagMediumWP_QuarkMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_pt_TagMediumWP_GenTopMatch02_Resolved","; genTop pT matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_pt_TagMediumWP_GenTopMatch02_Mixed","; genTop pT matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_pt_TagMediumWP_GenTopMatch02_Merged","; genTop pT matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_pt_TagMediumWP_GenTopMatch04_Resolved","; genTop pT matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_pt_TagMediumWP_GenTopMatch04_Mixed","; genTop pT matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_pt_TagMediumWP_GenTopMatch04_Merged","; genTop pT matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_OldMatch_Resolved    = ROOT.TH1D("h_Top_pt_TagMediumWP_OldMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_OldMatch_Mixed       = ROOT.TH1D("h_Top_pt_TagMediumWP_OldMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_OldMatch_Merged      = ROOT.TH1D("h_Top_pt_TagMediumWP_OldMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_TagTightWP_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_pt_TagTightWP_QuarkMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_TagTightWP_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_pt_TagTightWP_QuarkMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_TagTightWP_QuarkMatch_Merged      = ROOT.TH1D("h_Top_pt_TagTightWP_QuarkMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_TagTightWP_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_pt_TagTightWP_GenTopMatch02_Resolved","; genTop pT matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagTightWP_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_pt_TagTightWP_GenTopMatch02_Mixed","; genTop pT matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagTightWP_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_pt_TagTightWP_GenTopMatch02_Merged","; genTop pT matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagTightWP_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_pt_TagTightWP_GenTopMatch04_Resolved","; genTop pT matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagTightWP_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_pt_TagTightWP_GenTopMatch04_Mixed","; genTop pT matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagTightWP_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_pt_TagTightWP_GenTopMatch04_Merged","; genTop pT matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagTightWP_OldMatch_Resolved    = ROOT.TH1D("h_Top_pt_TagTightWP_OldMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_TagTightWP_OldMatch_Mixed       = ROOT.TH1D("h_Top_pt_TagTightWP_OldMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_TagTightWP_OldMatch_Merged      = ROOT.TH1D("h_Top_pt_TagTightWP_OldMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_mass_RealLife_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_mass_RealLife_QuarkMatch_Resolved","; genTop mass matched with top resolved with quark", 20, 0, 1000)
h_GenTop_mass_RealLife_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_mass_RealLife_QuarkMatch_Mixed","; genTop mass matched with top mixed with quark", 20, 0, 1000)
h_GenTop_mass_RealLife_QuarkMatch_Merged      = ROOT.TH1D("h_Top_mass_RealLife_QuarkMatch_Merged","; genTop mass matched with top merged with quark", 20, 0, 1000)
h_GenTop_mass_RealLife_OldMatch_Resolved    = ROOT.TH1D("h_Top_mass_RealLife_OldMatch_Resolved","; genTop mass matched with top resolved with quark", 20, 0, 1000)
h_GenTop_mass_RealLife_OldMatch_Mixed       = ROOT.TH1D("h_Top_mass_RealLife_OldMatch_Mixed","; genTop mass matched with top mixed with quark", 20, 0, 1000)
h_GenTop_mass_RealLife_OldMatch_Merged      = ROOT.TH1D("h_Top_mass_RealLife_OldMatch_Merged","; genTop mass matched with top merged with quark", 20, 0, 1000)
h_GenTop_mass_RealLife_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_mass_RealLife_GenTopMatch02_Resolved","; genTop mass matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_mass_RealLife_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_mass_RealLife_GenTopMatch02_Mixed","; genTop mass matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_mass_RealLife_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_mass_RealLife_GenTopMatch02_Merged","; genTop mass matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_mass_RealLife_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_mass_RealLife_GenTopMatch04_Resolved","; genTop mass matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_mass_RealLife_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_mass_RealLife_GenTopMatch04_Mixed","; genTop mass matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_mass_RealLife_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_mass_RealLife_GenTopMatch04_Merged","; genTop mass matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagLooseWP_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_mass_TagLooseWP_QuarkMatch_Resolved","; genTop mass matched with top resolved with quark", 20, 0, 1000)
h_GenTop_mass_TagLooseWP_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_mass_TagLooseWP_QuarkMatch_Mixed","; genTop mass matched with top mixed with quark", 20, 0, 1000)
h_GenTop_mass_TagLooseWP_QuarkMatch_Merged      = ROOT.TH1D("h_Top_mass_TagLooseWP_QuarkMatch_Merged","; genTop mass matched with top merged with quark", 20, 0, 1000)
h_GenTop_mass_TagLooseWP_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_mass_TagLooseWP_GenTopMatch02_Resolved","; genTop mass matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_mass_TagLooseWP_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_mass_TagLooseWP_GenTopMatch02_Mixed","; genTop mass matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_mass_TagLooseWP_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_mass_TagLooseWP_GenTopMatch02_Merged","; genTop mass matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_mass_TagLooseWP_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_mass_TagLooseWP_GenTopMatch04_Resolved","; genTop mass matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagLooseWP_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_mass_TagLooseWP_GenTopMatch04_Mixed","; genTop mass matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagLooseWP_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_mass_TagLooseWP_GenTopMatch04_Merged","; genTop mass matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagLooseWP_OldMatch_Resolved    = ROOT.TH1D("h_Top_mass_TagLooseWP_OldMatch_Resolved","; genTop mass matched with top resolved with quark", 20, 0, 1000)
h_GenTop_mass_TagLooseWP_OldMatch_Mixed       = ROOT.TH1D("h_Top_mass_TagLooseWP_OldMatch_Mixed","; genTop mass matched with top mixed with quark", 20, 0, 1000)
h_GenTop_mass_TagLooseWP_OldMatch_Merged      = ROOT.TH1D("h_Top_mass_TagLooseWP_OldMatch_Merged","; genTop mass matched with top merged with quark", 20, 0, 1000)
h_GenTop_mass_TagWP_5_100_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_mass_TagWP_5_100_QuarkMatch_Resolved","; genTop mass matched with top resolved with quark", 20, 0, 1000)
h_GenTop_mass_TagWP_5_100_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_mass_TagWP_5_100_QuarkMatch_Mixed","; genTop mass matched with top mixed with quark", 20, 0, 1000)
h_GenTop_mass_TagWP_5_100_QuarkMatch_Merged      = ROOT.TH1D("h_Top_mass_TagWP_5_100_QuarkMatch_Merged","; genTop mass matched with top merged with quark", 20, 0, 1000)
h_GenTop_mass_TagWP_5_100_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_mass_TagWP_5_100_GenTopMatch02_Resolved","; genTop mass matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_mass_TagWP_5_100_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_mass_TagWP_5_100_GenTopMatch02_Mixed","; genTop mass matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_mass_TagWP_5_100_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_mass_TagWP_5_100_GenTopMatch02_Merged","; genTop mass matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_mass_TagWP_5_100_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_mass_TagWP_5_100_GenTopMatch04_Resolved","; genTop mass matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagWP_5_100_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_mass_TagWP_5_100_GenTopMatch04_Mixed","; genTop mass matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagWP_5_100_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_mass_TagWP_5_100_GenTopMatch04_Merged","; genTop mass matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagMediumWP_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_mass_TagMediumWP_QuarkMatch_Resolved","; genTop mass matched with top resolved with quark", 20, 0, 1000)
h_GenTop_mass_TagMediumWP_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_mass_TagMediumWP_QuarkMatch_Mixed","; genTop mass matched with top mixed with quark", 20, 0, 1000)
h_GenTop_mass_TagMediumWP_QuarkMatch_Merged      = ROOT.TH1D("h_Top_mass_TagMediumWP_QuarkMatch_Merged","; genTop mass matched with top merged with quark", 20, 0, 1000)
h_GenTop_mass_TagMediumWP_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_mass_TagMediumWP_GenTopMatch02_Resolved","; genTop mass matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_mass_TagMediumWP_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_mass_TagMediumWP_GenTopMatch02_Mixed","; genTop mass matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_mass_TagMediumWP_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_mass_TagMediumWP_GenTopMatch02_Merged","; genTop mass matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_mass_TagMediumWP_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_mass_TagMediumWP_GenTopMatch04_Resolved","; genTop mass matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagMediumWP_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_mass_TagMediumWP_GenTopMatch04_Mixed","; genTop mass matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagMediumWP_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_mass_TagMediumWP_GenTopMatch04_Merged","; genTop mass matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagMediumWP_OldMatch_Resolved    = ROOT.TH1D("h_Top_mass_TagMediumWP_OldMatch_Resolved","; genTop mass matched with top resolved with quark", 20, 0, 1000)
h_GenTop_mass_TagMediumWP_OldMatch_Mixed       = ROOT.TH1D("h_Top_mass_TagMediumWP_OldMatch_Mixed","; genTop mass matched with top mixed with quark", 20, 0, 1000)
h_GenTop_mass_TagMediumWP_OldMatch_Merged      = ROOT.TH1D("h_Top_mass_TagMediumWP_OldMatch_Merged","; genTop mass matched with top merged with quark", 20, 0, 1000)
h_GenTop_mass_TagTightWP_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_mass_TagTightWP_QuarkMatch_Resolved","; genTop mass matched with top resolved with quark", 20, 0, 1000)
h_GenTop_mass_TagTightWP_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_mass_TagTightWP_QuarkMatch_Mixed","; genTop mass matched with top mixed with quark", 20, 0, 1000)
h_GenTop_mass_TagTightWP_QuarkMatch_Merged      = ROOT.TH1D("h_Top_mass_TagTightWP_QuarkMatch_Merged","; genTop mass matched with top merged with quark", 20, 0, 1000)
h_GenTop_mass_TagTightWP_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_mass_TagTightWP_GenTopMatch02_Resolved","; genTop mass matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_mass_TagTightWP_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_mass_TagTightWP_GenTopMatch02_Mixed","; genTop mass matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_mass_TagTightWP_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_mass_TagTightWP_GenTopMatch02_Merged","; genTop mass matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_mass_TagTightWP_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_mass_TagTightWP_GenTopMatch04_Resolved","; genTop mass matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagTightWP_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_mass_TagTightWP_GenTopMatch04_Mixed","; genTop mass matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagTightWP_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_mass_TagTightWP_GenTopMatch04_Merged","; genTop mass matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_mass_TagTightWP_OldMatch_Resolved    = ROOT.TH1D("h_Top_mass_TagTightWP_OldMatch_Resolved","; genTop mass matched with top resolved with quark", 20, 0, 1000)
h_GenTop_mass_TagTightWP_OldMatch_Mixed       = ROOT.TH1D("h_Top_mass_TagTightWP_OldMatch_Mixed","; genTop mass matched with top mixed with quark", 20, 0, 1000)
h_GenTop_mass_TagTightWP_OldMatch_Merged      = ROOT.TH1D("h_Top_mass_TagTightWP_OldMatch_Merged","; genTop mass matched with top merged with quark", 20, 0, 1000)
h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Resolved","; num candidates vs genTop pT matched with top resolved with quark", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Mixed","; num candidates vs genTop pT matched with top mixed with quark", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Merged","; num candidates vs genTop pT matched with top merged with quark", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Resolved","; num candidates vs num candidates vs genTop pT matched with top resolved with dr 0.2", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.2", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Merged","; num candidates vs genTop pT matched with top merged with dr 0.2", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Resolved","; num candidates vs genTop pT matched with top resolved with dr 0.4", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.4", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Merged","; num candidates vs genTop pT matched with top merged with dr 0.4", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Resolved","; num candidates vs genTop pT matched with top resolved with quark", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Mixed","; num candidates vs genTop pT matched with top mixed with quark", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Merged","; num candidates vs genTop pT matched with top merged with quark", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Resolved","; num candidates vs genTop pT matched with top resolved with dr 0.2", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.2", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Merged","; num candidates vs genTop pT matched with top merged with dr 0.2", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Resolved","; num candidates vs genTop pT matched with top resolved with dr 0.4", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.4", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Merged","; num candidates vs genTop pT matched with top merged with dr 0.4", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Resolved","; num candidates vs genTop pT matched with top resolved with quark", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Mixed","; num candidates vs genTop pT matched with top mixed with quark", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Merged","; num candidates vs genTop pT matched with top merged with quark", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Resolved","; num candidates vs num candidates vs genTop pT matched with top resolved with dr 0.2", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.2", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Merged","; num candidates vs genTop pT matched with top merged with dr 0.2", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Resolved","; num candidates vs genTop pT matched with top resolved with dr 0.4", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.4", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Merged","; num candidates vs genTop pT matched with top merged with dr 0.4", 20, 0, 1000, 10, 0, 10)
h2_Top_Cat_GenTop_pt_Best_matched_RealLife_OldMatch_Mixed      = ROOT.TH2D("h2_Top_Cat_GenTop_pt_Best_matched_RealLife_OldMatch_Mixed","; RecoTop category vs genTop pT matched with top Mixed with dr 0.4", 20, 0, 1000, 3, 0, 3)
h2_Top_Cat_GenTop_pt_Best_matched_Reconstructable_OldMatch_Mixed      = ROOT.TH2D("h2_Top_Cat_GenTop_pt_Best_matched_Reconstructable_OldMatch_Mixed","; RecoTop category vs genTop pT matched with top Mixed with dr 0.4", 20, 0, 1000, 3, 0, 3)

h2_DeltaR_BestTop_GenTop_pt_Resolved       = ROOT.TH2D("h2_DeltaR_BestTop_GenTop_pt_Resolved","DeltaR besttop-gentop vs genTop pT for top resolved", 20, 0, 1000, 100, 0, 10)
h2_DeltaR_BestTop_GenTop_pt_Mixed       = ROOT.TH2D("h2_DeltaR_BestTop_GenTop_pt_Mixed","DeltaR besttop-gentop vs genTop pT for top mixed", 20, 0, 1000, 100, 0, 10)
h2_DeltaR_BestTop_GenTop_pt_Merged       = ROOT.TH2D("h2_DeltaR_BestTop_GenTop_pt_Merged","DeltaR besttop-gentop vs genTop pT for top merged", 20, 0, 1000, 100, 0, 10)
# h2_Num_cand_DeltaR_GenTop_pt_QuarkMatch_Mixed          = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_QuarkMatch_Mixed","; num candidates vs genTop pT matched with top mixed with quark", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_QuarkMatch_Merged         = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_QuarkMatch_Merged","; num candidates vs genTop pT matched with top merged with quark", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch02_Resolved    = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch02_Resolved","; num candidates vs genTop pT matched with top resolved with dr 0.2", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch02_Mixed       = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch02_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.2", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch02_Merged      = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch02_Merged","; num candidates vs genTop pT matched with top merged with dr 0.2", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch04_Resolved    = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch04_Resolved","; num candidates vs genTop pT matched with top resolved with dr 0.4", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch04_Mixed       = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch04_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.4", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch04_Merged      = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch04_Merged","; num candidates vs genTop pT matched with top merged with dr 0.4", 20, 0, 1000, 10, 0, 100)

nEvRecoTopGenQuarktMatched = 0
nEvRecoTopGenTop02Matched = 0
nEvRecoTopGenTop04Matched = 0
nEvBestRecoTopGenQuarktMatched = 0
nEvBestRecoTopGenTop02Matched = 0
nEvBestRecoTopGenTop04Matched = 0
nEvNoTopHadr = 0
nEvNoTprime = 0

for i in range(tree.GetEntries()):
    event = Event(tree,i)
    genpart = Collection(event, "GenPart")
    if tree.GetListOfBranches().FindObject("TopGenTopPart"):
        topgen = Collection(event, "TopGenTopPart", lenVar = "nTopGenHadr")
    else:
        is_hadronic_top = np.zeros(len(genpart), dtype=int)
        hadronic_top_idx =[]
        quark_flavs = [int(1),int(2),int(3),int(4)]
        for particle in genpart:
            #print("la particella analizzata è", particle.pdgId, "con indice della madre:", particle.genPartIdxMother, "ed è:", genpart[0].pdgId)
            mom_id = particle.genPartIdxMother
            #se è un quark nella catena del top
            if abs(int(particle.pdgId)) in quark_flavs and mom_id!=-1: 
                #Print("è un quark")
                #se non è la propagazione di sè stessa
                if int(genpart[mom_id].pdgId) != int(particle.pdgId):
                    mom = genpart[mom_id] 
                    grandmom_id = mom.genPartIdxMother
                    #Print("non è propagato e la madre è:",mom.pdgId)
                    #se la madre è un w
                    if abs(int(mom.pdgId))==24 and grandmom_id!=-1:
                        #Print("la madre è un w prodotto di decadimento")
                        grandmom = genpart[grandmom_id]
                        #Print("la nonna è:",grandmom.pdgId)
                        #se non è la propagazione di sè stessa
                        if int(grandmom.pdgId) != int(mom.pdgId):
                            #se la madre della w è un top
                            #print("non è propagato")
                            if abs(grandmom.pdgId) == 6:
                                #Print("la nonna è un top")
                                top = grandmom
                                top_id = grandmom_id
                                top_mom_id = top.genPartIdxMother
                                top_mom = genpart[top.genPartIdxMother]
                                #metti 1 nella posizione corrispondete al top
                                if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                            print("1) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                is_hadronic_top[top_id]=int(1)
                                hadronic_top_idx.append(top_id)
                                #Print("salvato indice:",is_hadronic_top)
                                #fai lo stesso per i top da cui è stato propagato
                                while top_mom.pdgId==top.pdgId:
                                    #print("1:",genpart[top_id].pdgId,genpart[top_mom_id].pdgId)
                                    if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                            print("2.0) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                    top=top_mom
                                    top_id = top_mom_id
                                    top_mom_id = top_mom.genPartIdxMother
                                    top_mom=genpart[top_mom.genPartIdxMother]
                                    #print("2:",genpart[top_id].pdgId)
                                    if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                            print("2) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                    is_hadronic_top[top_id]=int(1)
                                    hadronic_top_idx.append(top_id)
                                    #Print("salvato indice:",is_hadronic_top)

                        else:
                           #print("è propagato")
                           while (grandmom.pdgId==mom.pdgId): 
                                mom=grandmom
                                mom_id = grandmom_id
                                grandmom= genpart[mom.genPartIdxMother]  
                                grandmom_id = mom.genPartIdxMother
                                #Print("la nuova nonna è:",grandmom.pdgId)
                                #se la madre della w è un top
                                if abs(grandmom.pdgId) == 6:
                                    top = grandmom
                                    top_id = grandmom_id
                                    top_mom_id = top.genPartIdxMother
                                    top_mom = genpart[top.genPartIdxMother]
                                    #print("la nonna era ", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                    #metti 1 nella posizione corrispondete al top
                                    if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                            print("3) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                    is_hadronic_top[top_id]=int(1)
                                    hadronic_top_idx.append(top_id)
                                    #Print("salvato indice:",is_hadronic_top)
                                    #fai lo stesso per i top da cui è stato propagato
                                    while top_mom.pdgId==top.pdgId:
                                        top=top_mom
                                        top_id = top_mom_id
                                        top_mom_id = top_mom.genPartIdxMother
                                        top_mom=genpart[top_mom.genPartIdxMother]
                                        if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                            print("4) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                        is_hadronic_top[top_id]=int(1)
                                        hadronic_top_idx.append(top_id)
                                        #Print("salvato indice:",is_hadronic_top
        topgen = [particle for particle, is_hadr_top in zip(genpart, is_hadronic_top) if is_hadr_top==1]
    # topgen = [genpart[i] for i in hadronic_top_idx]
    if sample_name =="TprimeToTZ_1800": #"TT_semilep""TprimeToTZ_1800":
        if len(topgen) < 0:
            print("numero di top hadronici trovati:", len(topgen))
            print("top hadronici trovati:", [top.pdgId for top in topgen])
            print("hadronic top idx:", hadronic_top_idx)
            print("i top sono:", [genpart[idx].pdgId for idx in hadronic_top_idx])
            for i,part in enumerate(genpart):
                print("idx:",i,"part pdgId:", part.pdgId, "e idx madre:", part.genPartIdxMother)
    if year == 2022:
        for top in topgen:
            if top.pdgId != 6 and top.pdgId != -6:
                print("top hadronico trovato con pdgId:", top.pdgId, "e pt:", top.pt)
    jets = Collection(event, "Jet")
    nTopGenHadr = len(topgen)
    flagT = False
    for part in genpart:
        if abs(part.pdgId) == 8000001:
            flagT = True
            break
    if not flagT:
        nEvNoTprime += 1
    if nTopGenHadr >0:    #Tutti i topreco
        topresolved = Collection(event, "TopResolved")
        topmixed = Collection(event, "TopMixed")
        topmerged = Collection(event, "FatJet")
        #topMixedNoRes = removeResolved(topmixed)
        topMixedNoRes = topmixed

        #### fill del pt dei top hadronic (pre emissione soft) posso farlo perchè ce n'è uno solo per evento#####
        h_GenTop_pt.Fill(topgen[0].pt)

        ####HISTO PT PER EFFICIENZA "RICOSTRUIBILI" ALMENO UN TOP RICOSTRUITO MATCHATO#####
        #quark match
        #lista dei top matchati secondo il criterio dei quark
        topResolvedQuarkMatch = matchingTopResGenPart(genpart, topresolved, jets)
        topMixedQuarkMatch = list(filter(lambda x : x.truth==1, topMixedNoRes)) #qui uso la truth per "almeno un quark matchato"
        topMergedQuarkMatch = matchingTopMerGenPart(genpart, topmerged)
        if len(topResolvedQuarkMatch) != 0:
            h_GenTop_pt_Reconstructable_QuarkMatch_Resolved.Fill(topgen[0].pt)
            #print(len(topResolvedQuarkMatch))
            h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topresolved))
            #h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topResolvedQuarkMatch))
            nEvRecoTopGenQuarktMatched += 1
        if len(topMixedQuarkMatch) != 0:
            h_GenTop_pt_Reconstructable_QuarkMatch_Mixed.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topmixed))
            #h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topMixedQuarkMatch))

        if len(topMergedQuarkMatch) != 0:
            h_GenTop_pt_Reconstructable_QuarkMatch_Merged.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topmerged))
            #h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topMergedQuarkMatch))
        #gentop match dr=0.4
        topResolvedGenTopMatch_04 = matchingRecoTopGenTop(topgen, topresolved, 0.4)
        topMixedGenTopMatch_04 = matchingRecoTopGenTop(topgen, topMixedNoRes, 0.4)
        topMergedGenTopMatch_04 = matchingRecoTopGenTop(topgen, topmerged, 0.4)
        if len(topResolvedGenTopMatch_04) != 0:
            h_GenTop_pt_Reconstructable_GenTopMatch04_Resolved.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Resolved.Fill(topgen[0].pt, len(topresolved))
            nEvRecoTopGenTop04Matched += 1
        if len(topMixedGenTopMatch_04) != 0:
            h_GenTop_pt_Reconstructable_GenTopMatch04_Mixed.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Mixed.Fill(topgen[0].pt, len(topmixed))
        if len(topMergedGenTopMatch_04) != 0:
            h_GenTop_pt_Reconstructable_GenTopMatch04_Merged.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Merged.Fill(topgen[0].pt, len(topmerged))
        #gentop match dr=0.2
        topResolvedGenTopMatch_02 = matchingRecoTopGenTop(topgen, topresolved, 0.2)
        topMixedGenTopMatch_02 = matchingRecoTopGenTop(topgen, topMixedNoRes, 0.2)
        topMergedGenTopMatch_02 = matchingRecoTopGenTop(topgen, topmerged, 0.2)
        if len(topResolvedGenTopMatch_02) != 0:
            h_GenTop_pt_Reconstructable_GenTopMatch02_Resolved.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Resolved.Fill(topgen[0].pt, len(topresolved))
            nEvRecoTopGenTop02Matched += 1
        if len(topMixedGenTopMatch_02) != 0:
            h_GenTop_pt_Reconstructable_GenTopMatch02_Mixed.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Mixed.Fill(topgen[0].pt, len(topmixed))
        if len(topMergedGenTopMatch_02) != 0:
            h_GenTop_pt_Reconstructable_GenTopMatch02_Merged.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Merged.Fill(topgen[0].pt, len(topmerged))

        ####HISTO PT PER EFFICIENZA "DI SELEZIONE" E "REAL LIFE" IL MIGLIOR CANDIDATO TROTA è MATCHATO  #####
        #Lista dei topmixed non sovrapposti ordinati per score
        topResolvedSelect = selectTop(topresolved, resolved = True, year=year)
        #print("topResolvedSelect",isinstance(topResolvedSelect,list), topResolvedSelect[0].pt)
        #Lista dei topmixed senza resolved non sovrapposti ordinati per score
        topMixedSelect = selectTop(topMixedNoRes, resolved = False, year=year)
        #lista dei topmerged ordinati per score
        if year == 2018:
            topMergedSelect = sorted(topmerged, key=lambda x: x.particleNet_TvsQCD, reverse=True)
        elif year == 2022:
            topMergedSelect = sorted(topmerged, key=lambda x: x.particleNetWithMass_TvsQCD, reverse=True)
        #Esiste almeno un candidato TROTA
        if len(topResolvedSelect) != 0:
            h_GenTop_pt_exist_resolved.Fill(topgen[0].pt)
        if len(topMixedSelect) != 0:
            h_GenTop_pt_exist_mixed.Fill(topgen[0].pt)
        if len(topMergedSelect) != 0:
            h_GenTop_pt_exist_merged.Fill(topgen[0].pt)
        
        
        if len(topResolvedSelect) !=0:
            h2_DeltaR_BestTop_GenTop_pt_Resolved.Fill(topgen[0].pt, deltaR(topResolvedSelect[0], topgen[0]))
            #Il miglior candidato TROTA è matchato con i quark
            if len(matchingTopResGenPart(genpart, [topResolvedSelect[0]], jets))!=0:
                h_GenTop_pt_Selection_QuarkMatch_Resolved.Fill(topgen[0].pt)
                h_GenTop_pt_RealLife_QuarkMatch_Resolved.Fill(topgen[0].pt)
                h_GenTop_mass_RealLife_QuarkMatch_Resolved.Fill(topgen[0].mass)
                h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topresolved))
                #h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topResolvedSelect))

                nEvBestRecoTopGenQuarktMatched += 1
                top_resolved_selected_loose_QuarkMatch, top_resolved_selected_medium_QuarkMatch, top_resolved_selected_tight_QuarkMatch = thresholdTopScore([topResolvedSelect[0]], Top_threshold, 'Resolved', year)
                if len(top_resolved_selected_loose_QuarkMatch) != 0:
                    h_GenTop_pt_TagLooseWP_QuarkMatch_Resolved.Fill(topgen[0].pt)
                    h_GenTop_mass_TagLooseWP_QuarkMatch_Resolved.Fill(topgen[0].mass)
                if len(top_resolved_selected_medium_QuarkMatch) != 0:
                    h_GenTop_pt_TagMediumWP_QuarkMatch_Resolved.Fill(topgen[0].pt)
                    h_GenTop_mass_TagMediumWP_QuarkMatch_Resolved.Fill(topgen[0].mass)
                if len(top_resolved_selected_tight_QuarkMatch) != 0:
                    h_GenTop_pt_TagTightWP_QuarkMatch_Resolved.Fill(topgen[0].pt)
                    h_GenTop_mass_TagTightWP_QuarkMatch_Resolved.Fill(topgen[0].mass)

            else:
                h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topresolved))
            #Il miglior candidato TROTA è matchato con un topgen con dr = 0.4
            if len(matchingRecoTopGenTop(topgen, [topResolvedSelect[0]], 0.4))!=0:
                h_GenTop_pt_Selection_GenTopMatch04_Resolved.Fill(topgen[0].pt)
                h_GenTop_pt_RealLife_GenTopMatch04_Resolved.Fill(topgen[0].pt)
                h_GenTop_mass_RealLife_GenTopMatch04_Resolved.Fill(topgen[0].mass)
                h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Resolved.Fill(topgen[0].pt, len(topresolved))
                nEvBestRecoTopGenTop04Matched += 1
                top_resolved_selected_loose_GenTopMatch04_Resolved, top_resolved_selected_medium_GenTopMatch04_Resolved, top_resolved_selected_tight_GenTopMatch04_Resolved = thresholdTopScore([topResolvedSelect[0]], Top_threshold, 'Resolved', year)  
                if len(top_resolved_selected_loose_GenTopMatch04_Resolved) != 0:
                    h_GenTop_pt_TagLooseWP_GenTopMatch04_Resolved.Fill(topgen[0].pt)
                    h_GenTop_mass_TagLooseWP_GenTopMatch04_Resolved.Fill(topgen[0].mass)
                if len(top_resolved_selected_medium_GenTopMatch04_Resolved) != 0:
                    h_GenTop_pt_TagMediumWP_GenTopMatch04_Resolved.Fill(topgen[0].pt)
                    h_GenTop_mass_TagMediumWP_GenTopMatch04_Resolved.Fill(topgen[0].mass)
                if len(top_resolved_selected_tight_GenTopMatch04_Resolved) != 0:
                    h_GenTop_pt_TagTightWP_GenTopMatch04_Resolved.Fill(topgen[0].pt)
                    h_GenTop_mass_TagTightWP_GenTopMatch04_Resolved.Fill(topgen[0].mass)
            else:
                h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Resolved.Fill(topgen[0].pt, len(topresolved))
            #Il miglior candidato TROTA è matchato con un topgen con dr = 0.2
            if len(matchingRecoTopGenTop(topgen, [topResolvedSelect[0]], 0.2))!=0:
                h_GenTop_pt_Selection_GenTopMatch02_Resolved.Fill(topgen[0].pt)
                h_GenTop_pt_RealLife_GenTopMatch02_Resolved.Fill(topgen[0].pt)
                h_GenTop_mass_RealLife_GenTopMatch02_Resolved.Fill(topgen[0].mass)
                h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Resolved.Fill(topgen[0].pt, len(topresolved))
                nEvBestRecoTopGenTop02Matched += 1
                top_resolved_selected_loose_GenTopMatch02_Resolved, top_resolved_selected_medium_GenTopMatch02_Resolved, top_resolved_selected_tight_GenTopMatch02_Resolved = thresholdTopScore([topResolvedSelect[0]], Top_threshold, 'Resolved', year)
                if len(top_resolved_selected_loose_GenTopMatch02_Resolved) != 0:
                    h_GenTop_pt_TagLooseWP_GenTopMatch02_Resolved.Fill(topgen[0].pt)
                    h_GenTop_mass_TagLooseWP_GenTopMatch02_Resolved.Fill(topgen[0].mass)
                if len(top_resolved_selected_medium_GenTopMatch02_Resolved) != 0:
                    h_GenTop_pt_TagMediumWP_GenTopMatch02_Resolved.Fill(topgen[0].pt)
                    h_GenTop_mass_TagMediumWP_GenTopMatch02_Resolved.Fill(topgen[0].mass)
                if len(top_resolved_selected_tight_GenTopMatch02_Resolved) != 0:
                    h_GenTop_pt_TagTightWP_GenTopMatch02_Resolved.Fill(topgen[0].pt)
                    h_GenTop_mass_TagTightWP_GenTopMatch02_Resolved.Fill(topgen[0].mass)

            else:
                h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Resolved.Fill(topgen[0].pt, len(topresolved))

        if len(topMixedSelect) != 0:
            h2_DeltaR_BestTop_GenTop_pt_Mixed.Fill(topgen[0].pt, deltaR(topMixedSelect[0], topgen[0]))
            #Il miglior candidato TROTA è matchato con quark
            if topMixedSelect[0].truth == 1:
                h_GenTop_pt_Selection_QuarkMatch_Mixed.Fill(topgen[0].pt)
                h_GenTop_pt_RealLife_QuarkMatch_Mixed.Fill(topgen[0].pt)
                h_GenTop_mass_RealLife_QuarkMatch_Mixed.Fill(topgen[0].mass)
                h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topmixed))
                #h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topMixedSelect))
                top_mixed_selected_loose_QuarkMatch, top_mixed_selected_medium_QuarkMatch, top_mixed_selected_tight_QuarkMatch = thresholdTopScore([topMixedSelect[0]], Top_threshold, 'Mixed', year)
                if len(top_mixed_selected_loose_QuarkMatch) != 0:
                    h_GenTop_pt_TagLooseWP_QuarkMatch_Mixed.Fill(topgen[0].pt)
                    h_GenTop_mass_TagLooseWP_QuarkMatch_Mixed.Fill(topgen[0].mass)
                if len(top_mixed_selected_medium_QuarkMatch) != 0:
                    h_GenTop_pt_TagMediumWP_QuarkMatch_Mixed.Fill(topgen[0].pt)
                    h_GenTop_mass_TagMediumWP_QuarkMatch_Mixed.Fill(topgen[0].mass)
                if len(top_mixed_selected_tight_QuarkMatch) != 0:
                    h_GenTop_pt_TagTightWP_QuarkMatch_Mixed.Fill(topgen[0].pt)
                    h_GenTop_mass_TagTightWP_QuarkMatch_Mixed.Fill(topgen[0].mass)
            else:
                h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topmixed))
            #Il miglior candidato TROTA è matchato con un topgen con dr = 0.4
            if len(matchingRecoTopGenTop(topgen, [topMixedSelect[0]], 0.4))!=0:
                h_GenTop_pt_Selection_GenTopMatch04_Mixed.Fill(topgen[0].pt)
                h_GenTop_pt_RealLife_GenTopMatch04_Mixed.Fill(topgen[0].pt)
                h_GenTop_mass_RealLife_GenTopMatch04_Mixed.Fill(topgen[0].mass)
                h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Mixed.Fill(topgen[0].pt, len(topmixed))
                top_mixed_selected_loose_GenTopMatch04_Mixed, top_mixed_selected_medium_GenTopMatch04_Mixed, top_mixed_selected_tight_GenTopMatch04_Mixed = thresholdTopScore([topMixedSelect[0]], Top_threshold, 'Mixed', year)
                if len(top_mixed_selected_loose_GenTopMatch04_Mixed) != 0:
                    h_GenTop_pt_TagLooseWP_GenTopMatch04_Mixed.Fill(topgen[0].pt)
                    h_GenTop_mass_TagLooseWP_GenTopMatch04_Mixed.Fill(topgen[0].mass)
                if len(top_mixed_selected_medium_GenTopMatch04_Mixed) != 0:
                    h_GenTop_pt_TagMediumWP_GenTopMatch04_Mixed.Fill(topgen[0].pt)
                    h_GenTop_mass_TagMediumWP_GenTopMatch04_Mixed.Fill(topgen[0].mass)
                if len(top_mixed_selected_tight_GenTopMatch04_Mixed) != 0:
                    h_GenTop_pt_TagTightWP_GenTopMatch04_Mixed.Fill(topgen[0].pt)
                    h_GenTop_mass_TagTightWP_GenTopMatch04_Mixed.Fill(topgen[0].mass)
            else:
                h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Mixed.Fill(topgen[0].pt, len(topmixed))
            #Il miglior candidato TROTA è matchato con un topgen con dr = 0.2
            if len(matchingRecoTopGenTop(topgen, [topMixedSelect[0]], 0.2))!=0:
                h_GenTop_pt_Selection_GenTopMatch02_Mixed.Fill(topgen[0].pt)
                h_GenTop_pt_RealLife_GenTopMatch02_Mixed.Fill(topgen[0].pt)
                h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Mixed.Fill(topgen[0].pt, len(topmixed))
                top_mixed_selected_loose_GenTopMatch02_Mixed, top_mixed_selected_medium_GenTopMatch02_Mixed, top_mixed_selected_tight_GenTopMatch02_Mixed = thresholdTopScore([topMixedSelect[0]], Top_threshold, 'Mixed', year)
                if len(top_mixed_selected_loose_GenTopMatch02_Mixed) != 0:
                    h_GenTop_pt_TagLooseWP_GenTopMatch02_Mixed.Fill(topgen[0].pt)
                if len(top_mixed_selected_medium_GenTopMatch02_Mixed) != 0:
                    h_GenTop_pt_TagMediumWP_GenTopMatch02_Mixed.Fill(topgen[0].pt)
                if len(top_mixed_selected_tight_GenTopMatch02_Mixed) != 0:
                    h_GenTop_pt_TagTightWP_GenTopMatch02_Mixed.Fill(topgen[0].pt)
            else:
                h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Mixed.Fill(topgen[0].pt, len(topmixed))
        if len(topMergedSelect) != 0:
            h2_DeltaR_BestTop_GenTop_pt_Merged.Fill(topgen[0].pt, deltaR(topMergedSelect[0], topgen[0]))
            #Il miglior candidato TROTA è matchato con quark
            if len(matchingTopMerGenPart(genpart, [topMergedSelect[0]]))!=0:
                h_GenTop_pt_Selection_QuarkMatch_Merged.Fill(topgen[0].pt)
                h_GenTop_pt_RealLife_QuarkMatch_Merged.Fill(topgen[0].pt)
                h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topmerged))
                #h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topMergedSelect))
                top_merged_selected_loose_QuarkMatch, top_merged_selected_medium_QuarkMatch, top_merged_selected_tight_QuarkMatch = thresholdTopScore([topMergedSelect[0]], Top_threshold, 'Merged', year)
                if len(top_merged_selected_loose_QuarkMatch) != 0:
                    h_GenTop_pt_TagLooseWP_QuarkMatch_Merged.Fill(topgen[0].pt)
                if len(top_merged_selected_medium_QuarkMatch) != 0:
                    h_GenTop_pt_TagMediumWP_QuarkMatch_Merged.Fill(topgen[0].pt)
                if len(top_merged_selected_tight_QuarkMatch) != 0:
                    h_GenTop_pt_TagTightWP_QuarkMatch_Merged.Fill(topgen[0].pt)
            else:
                h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topmerged))
            #Il miglior candidato TROTA è matchato con un topgen con dr = 0.4
            if len(matchingRecoTopGenTop(topgen, [topMergedSelect[0]], 0.4))!=0:
                h_GenTop_pt_Selection_GenTopMatch04_Merged.Fill(topgen[0].pt)
                h_GenTop_pt_RealLife_GenTopMatch04_Merged.Fill(topgen[0].pt)
                h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Merged.Fill(topgen[0].pt, len(topmerged))
                top_merged_selected_loose_GenTopMatch04_Merged, top_merged_selected_medium_GenTopMatch04_Merged, top_merged_selected_tight_GenTopMatch04_Merged = thresholdTopScore([topMergedSelect[0]], Top_threshold, 'Merged', year)
                if len(top_merged_selected_loose_GenTopMatch04_Merged) != 0:
                    h_GenTop_pt_TagLooseWP_GenTopMatch04_Merged.Fill(topgen[0].pt)
                if len(top_merged_selected_medium_GenTopMatch04_Merged) != 0:
                    h_GenTop_pt_TagMediumWP_GenTopMatch04_Merged.Fill(topgen[0].pt)
                if len(top_merged_selected_tight_GenTopMatch04_Merged) != 0:
                    h_GenTop_pt_TagTightWP_GenTopMatch04_Merged.Fill(topgen[0].pt)
            else:
                h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Merged.Fill(topgen[0].pt, len(topmerged))
            #Il miglior candidato TROTA è matchato con un topgen con dr = 0.2
            if len(matchingRecoTopGenTop(topgen, [topMergedSelect[0]], 0.2))!=0:
                h_GenTop_pt_Selection_GenTopMatch02_Merged.Fill(topgen[0].pt)
                h_GenTop_pt_RealLife_GenTopMatch02_Merged.Fill(topgen[0].pt)
                h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Merged.Fill(topgen[0].pt, len(topmerged))
                top_merged_selected_loose_GenTopMatch02_Merged, top_merged_selected_medium_GenTopMatch02_Merged, top_merged_selected_tight_QuarkMatch02_Merged = thresholdTopScore([topMergedSelect[0]], Top_threshold, 'Merged', year)
                if len(top_merged_selected_loose_GenTopMatch02_Merged) != 0:
                    h_GenTop_pt_TagLooseWP_GenTopMatch02_Merged.Fill(topgen[0].pt)
                if len(top_merged_selected_medium_GenTopMatch02_Merged) != 0:
                    h_GenTop_pt_TagMediumWP_GenTopMatch02_Merged.Fill(topgen[0].pt)
                if len(top_merged_selected_tight_QuarkMatch02_Merged) != 0:
                    h_GenTop_pt_TagTightWP_GenTopMatch02_Merged.Fill(topgen[0].pt)
            else:
                h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Merged.Fill(topgen[0].pt, len(topmerged))
            #il miglior candidato TROTA è matchato con quark e topgen dr=0.4


        if len(topResolvedQuarkMatch) !=0 and len(topResolvedGenTopMatch_04) !=0:
            h_GenTop_pt_Reconstructable_OldMatch_Resolved.Fill(topgen[0].pt)
        if len(topMixedQuarkMatch) !=0 and len(topMixedGenTopMatch_04) !=0:
            h_GenTop_pt_Reconstructable_OldMatch_Mixed.Fill(topgen[0].pt)
            h2_Top_Cat_GenTop_pt_Best_matched_Reconstructable_OldMatch_Mixed.Fill(topgen[0].pt, topcategory(topMixedSelect[0]))
        if len(topMergedQuarkMatch) !=0 and len(topMergedGenTopMatch_04) !=0:
            h_GenTop_pt_Reconstructable_OldMatch_Merged.Fill(topgen[0].pt)

        if len(topResolvedSelect) !=0:
            #Il miglior candidato TROTA è matchato con i quark e topgen dr<0.4
            if len(matchingRecoTopGenTop(topgen, [topResolvedSelect[0]], 0.4))!=0 and len(matchingTopResGenPart(genpart, [topResolvedSelect[0]], jets))!=0:
                h_GenTop_pt_RealLife_OldMatch_Resolved.Fill(topgen[0].pt)
                h_GenTop_pt_Selection_OldMatch_Resolved.Fill(topgen[0].pt)
                top_resolved_selected_loose_OldMatch_Resolved, top_resolved_selected_medium_OldMatch_Resolved, top_resolved_selected_tight_OldMatch_Resolved = thresholdTopScore([topResolvedSelect[0]], Top_threshold, 'Resolved', year)
                if len(top_resolved_selected_loose_OldMatch_Resolved) != 0:
                    h_GenTop_pt_TagLooseWP_OldMatch_Resolved.Fill(topgen[0].pt)
                if len(top_resolved_selected_medium_OldMatch_Resolved) != 0:
                    h_GenTop_pt_TagMediumWP_OldMatch_Resolved.Fill(topgen[0].pt)
                if len(top_resolved_selected_tight_OldMatch_Resolved) != 0:
                    h_GenTop_pt_TagTightWP_OldMatch_Resolved.Fill(topgen[0].pt)
    
        if len(topMixedSelect) != 0:
            #Il miglior candidato TROTA è matchato con quark e topgen dr<0.4
            if topMixedSelect[0].truth == 1 and len(matchingRecoTopGenTop(topgen,[topMixedSelect[0]], 0.4))!=0:
                h_GenTop_pt_RealLife_OldMatch_Mixed.Fill(topgen[0].pt)
                h_GenTop_pt_Selection_OldMatch_Mixed.Fill(topgen[0].pt)
                h2_Top_Cat_GenTop_pt_Best_matched_RealLife_OldMatch_Mixed.Fill(topgen[0].pt, topcategory(topMixedSelect[0]))
                #if topcategory(topMixedSelect[0])==1:
                    #print("top mixed selezionato con pt:", topMixedSelect[0].pt, "e topcategory:", topcategory(topMixedSelect[0]))
                top_mixed_selected_loose_OldMatch_Mixed, top_mixed_selected_medium_OldMatch_Mixed, top_mixed_selected_tight_OldMatch_Mixed = thresholdTopScore([topMixedSelect[0]], Top_threshold, 'Mixed', year)
                if len(top_mixed_selected_loose_OldMatch_Mixed) != 0:
                    h_GenTop_pt_TagLooseWP_OldMatch_Mixed.Fill(topgen[0].pt)
                if len(top_mixed_selected_medium_OldMatch_Mixed) != 0:
                    h_GenTop_pt_TagMediumWP_OldMatch_Mixed.Fill(topgen[0].pt)
                if len(top_mixed_selected_tight_OldMatch_Mixed) != 0:
                    h_GenTop_pt_TagTightWP_OldMatch_Mixed.Fill(topgen[0].pt)
            #Il miglior candidato TROTA è matchato con quark e topgen dr<0.2

        if len(topMergedSelect) != 0:
            if len(matchingTopMerGenPart(genpart, [topMergedSelect[0]]))!=0 and len(matchingRecoTopGenTop(topgen, [topMergedSelect[0]], 0.4))!=0:
                h_GenTop_pt_RealLife_OldMatch_Merged.Fill(topgen[0].pt)
                h_GenTop_pt_Selection_OldMatch_Merged.Fill(topgen[0].pt)
                top_merged_selected_loose_OldMatch_Merged, top_merged_selected_medium_OldMatch_Merged, top_merged_selected_tight_OldMatch_Merged = thresholdTopScore([topMergedSelect[0]], Top_threshold, 'Merged', year)   
                if len(top_merged_selected_loose_OldMatch_Merged) != 0:
                    h_GenTop_pt_TagLooseWP_OldMatch_Merged.Fill(topgen[0].pt)
                if len(top_merged_selected_medium_OldMatch_Merged) != 0:
                    h_GenTop_pt_TagMediumWP_OldMatch_Merged.Fill(topgen[0].pt)
                if len(top_merged_selected_tight_OldMatch_Merged) != 0:
                    h_GenTop_pt_TagTightWP_OldMatch_Merged.Fill(topgen[0].pt)

    else:
        #print("Nessun top hadronico trovato in questo evento")
        nEvNoTopHadr+=1

outfile.cd()
h_GenTop_pt.Write()
h_GenTop_pt_exist_resolved.Write()
h_GenTop_pt_exist_mixed.Write()
h_GenTop_pt_exist_merged.Write()
h_GenTop_pt_Reconstructable_QuarkMatch_Resolved.Write()
h_GenTop_pt_Reconstructable_QuarkMatch_Mixed.Write()
h_GenTop_pt_Reconstructable_QuarkMatch_Merged.Write()
h_GenTop_pt_Reconstructable_GenTopMatch02_Resolved.Write()
h_GenTop_pt_Reconstructable_GenTopMatch02_Mixed.Write()
h_GenTop_pt_Reconstructable_GenTopMatch02_Merged.Write()
h_GenTop_pt_Reconstructable_GenTopMatch04_Resolved.Write() 
h_GenTop_pt_Reconstructable_GenTopMatch04_Mixed.Write()
h_GenTop_pt_Reconstructable_GenTopMatch04_Merged.Write()
h_GenTop_pt_Selection_QuarkMatch_Resolved.Write()
h_GenTop_pt_Selection_QuarkMatch_Mixed.Write()
h_GenTop_pt_Selection_QuarkMatch_Merged.Write()
h_GenTop_pt_Selection_GenTopMatch02_Resolved.Write()
h_GenTop_pt_Selection_GenTopMatch02_Mixed.Write()
h_GenTop_pt_Selection_GenTopMatch02_Merged.Write()
h_GenTop_pt_Selection_GenTopMatch04_Resolved.Write()
h_GenTop_pt_Selection_GenTopMatch04_Mixed.Write()
h_GenTop_pt_Selection_GenTopMatch04_Merged.Write()
h_GenTop_pt_RealLife_QuarkMatch_Resolved.Write()
h_GenTop_pt_RealLife_QuarkMatch_Mixed.Write()
h_GenTop_pt_RealLife_QuarkMatch_Merged.Write()
h_GenTop_pt_RealLife_GenTopMatch02_Resolved.Write()
h_GenTop_pt_RealLife_GenTopMatch02_Mixed.Write()
h_GenTop_pt_RealLife_GenTopMatch02_Merged.Write()
h_GenTop_pt_RealLife_GenTopMatch04_Resolved.Write()
h_GenTop_pt_RealLife_GenTopMatch04_Mixed.Write()
h_GenTop_pt_RealLife_GenTopMatch04_Merged.Write()
h_GenTop_pt_TagLooseWP_QuarkMatch_Resolved.Write()
h_GenTop_pt_TagLooseWP_QuarkMatch_Mixed.Write()
h_GenTop_pt_TagLooseWP_QuarkMatch_Merged.Write()
h_GenTop_pt_TagLooseWP_GenTopMatch02_Resolved.Write()
h_GenTop_pt_TagLooseWP_GenTopMatch02_Mixed.Write()
h_GenTop_pt_TagLooseWP_GenTopMatch02_Merged.Write()
h_GenTop_pt_TagLooseWP_GenTopMatch04_Resolved.Write()
h_GenTop_pt_TagLooseWP_GenTopMatch04_Mixed.Write()
h_GenTop_pt_TagLooseWP_GenTopMatch04_Merged.Write() 
h_GenTop_pt_TagMediumWP_QuarkMatch_Resolved.Write()
h_GenTop_pt_TagMediumWP_QuarkMatch_Mixed.Write()
h_GenTop_pt_TagMediumWP_QuarkMatch_Merged.Write()
h_GenTop_pt_TagMediumWP_GenTopMatch02_Resolved.Write()
h_GenTop_pt_TagMediumWP_GenTopMatch02_Mixed.Write()
h_GenTop_pt_TagMediumWP_GenTopMatch02_Merged.Write()
h_GenTop_pt_TagMediumWP_GenTopMatch04_Resolved.Write()
h_GenTop_pt_TagMediumWP_GenTopMatch04_Mixed.Write()
h_GenTop_pt_TagMediumWP_GenTopMatch04_Merged.Write()  
h_GenTop_pt_TagTightWP_QuarkMatch_Resolved.Write()
h_GenTop_pt_TagTightWP_QuarkMatch_Mixed.Write()
h_GenTop_pt_TagTightWP_QuarkMatch_Merged.Write()
h_GenTop_pt_TagTightWP_GenTopMatch02_Resolved.Write()
h_GenTop_pt_TagTightWP_GenTopMatch02_Mixed.Write()
h_GenTop_pt_TagTightWP_GenTopMatch02_Merged.Write()
h_GenTop_pt_TagTightWP_GenTopMatch04_Resolved.Write()
h_GenTop_pt_TagTightWP_GenTopMatch04_Mixed.Write()
h_GenTop_pt_TagTightWP_GenTopMatch04_Merged.Write()      
h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Resolved.Write()
h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Mixed.Write()
h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Merged.Write()
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Resolved.Write()
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Mixed.Write()       
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Merged.Write()
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Resolved.Write()
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Mixed.Write()
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Merged.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Resolved.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Mixed.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Merged.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Resolved.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Mixed.Write()       
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Merged.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Resolved.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Mixed.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Merged.Write()
h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Resolved.Write()
h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Mixed.Write()   
h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Merged.Write()
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Resolved.Write()
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Mixed.Write()
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Merged.Write()
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Resolved.Write()
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Mixed.Write()
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Merged.Write()
h2_DeltaR_BestTop_GenTop_pt_Resolved.Write()
h2_DeltaR_BestTop_GenTop_pt_Mixed.Write()
h2_DeltaR_BestTop_GenTop_pt_Merged.Write() 
h_GenTop_pt_RealLife_OldMatch_Merged.Write()
h_GenTop_pt_RealLife_OldMatch_Mixed.Write()
h_GenTop_pt_RealLife_OldMatch_Resolved.Write()
h_GenTop_pt_Selection_OldMatch_Merged.Write()
h_GenTop_pt_Selection_OldMatch_Mixed.Write()
h_GenTop_pt_Selection_OldMatch_Resolved.Write()
h_GenTop_pt_Reconstructable_OldMatch_Merged.Write()
h_GenTop_pt_Reconstructable_OldMatch_Mixed.Write()
h_GenTop_pt_Reconstructable_OldMatch_Resolved.Write()
h_GenTop_pt_TagLooseWP_OldMatch_Merged.Write()
h_GenTop_pt_TagLooseWP_OldMatch_Mixed.Write()
h_GenTop_pt_TagLooseWP_OldMatch_Resolved.Write()
h_GenTop_pt_TagMediumWP_OldMatch_Merged.Write()
h_GenTop_pt_TagMediumWP_OldMatch_Mixed.Write()
h_GenTop_pt_TagMediumWP_OldMatch_Resolved.Write()
h_GenTop_pt_TagTightWP_OldMatch_Resolved.Write()
h_GenTop_pt_TagTightWP_OldMatch_Mixed.Write()   
h_GenTop_pt_TagTightWP_OldMatch_Merged.Write()    
h2_Top_Cat_GenTop_pt_Best_matched_RealLife_OldMatch_Mixed.Write()
h2_Top_Cat_GenTop_pt_Best_matched_Reconstructable_OldMatch_Mixed.Write()

outfile.Close()

n_events = tree.GetEntries()
print(f"Number of events: {n_events}")
print("numero di eventi senza T':", nEvNoTprime)
print("numero di eventi senza top hadronici:", nEvNoTopHadr) 
print("Reconstructable efficiency quark criterion resolved: %.4f" %(nEvRecoTopGenQuarktMatched/tree.GetEntries()))
print("Reconstructable efficiency dr=0.4 criterion resolved: %.4f" %(nEvRecoTopGenTop04Matched/tree.GetEntries()))
print("Reconstructable efficiency dr=0.2 criterion resolved: %.4f" %(nEvRecoTopGenTop02Matched/tree.GetEntries()))
print("Selection efficiency quark criterion resolved: %.4f" %(nEvBestRecoTopGenQuarktMatched/nEvRecoTopGenQuarktMatched))
print("Selection efficiency dr=0.4 criterion resolved: %.4f" %(nEvBestRecoTopGenTop04Matched/nEvRecoTopGenTop04Matched))
print("Selection efficiency dr=0.2 criterion resolved: %.4f" %(nEvBestRecoTopGenTop02Matched/nEvRecoTopGenTop02Matched))
print("Real Life efficiency quark criterion resolved: %.4f" %(nEvBestRecoTopGenQuarktMatched/tree.GetEntries()))
print("Real Life efficiency dr=0.4 criterion resolved: %.4f" %(nEvBestRecoTopGenTop04Matched/tree.GetEntries()))
print("Real Life efficiency dr=0.2 criterion resolved: %.4f" %(nEvBestRecoTopGenTop02Matched/tree.GetEntries()))




# Fraction of Events where at least 1 genquark is not matched with a jet: 0.13580660613000511
# Fraction of Events where gentop is not matched with the jet sum: 0.8004777695317077
#first
# Reconstructable efficiency quark criterion resolved: 0.3616
# Reconstructable efficiency dr=0.4 criterion resolved: 0.5860
# Reconstructable efficiency dr=0.2 criterion resolved: 0.3889
# Selection efficiency quark criterion resolved: 0.2880
# Selection efficiency dr=0.4 criterion resolved: 0.3813
# Selection efficiency dr=0.2 criterion resolved: 0.3307
# Real Life efficiency quark criterion resolved: 0.1042
# Real Life efficiency dr=0.4 criterion resolved: 0.2234
# Real Life efficiency dr=0.2 criterion resolved: 0.1286
#newest
# Reconstructable efficiency quark criterion resolved: 0.3619
# Reconstructable efficiency dr=0.4 criterion resolved: 0.5860
# Reconstructable efficiency dr=0.2 criterion resolved: 0.3889
# Selection efficiency quark criterion resolved: 0.2880
# Selection efficiency dr=0.4 criterion resolved: 0.3813
# Selection efficiency dr=0.2 criterion resolved: 0.3307
# Real Life efficiency quark criterion resolved: 0.1042
# Real Life efficiency dr=0.4 criterion resolved: 0.2234
# Real Life efficiency dr=0.2 criterion resolved: 0.1286


##########TPRIME##########
# Number of events: 29732
# numero di eventi senza T': 661
# numero di eventi senza top hadronici: 10576
# Reconstructable efficiency quark criterion resolved: 0.0865
# Reconstructable efficiency dr=0.4 criterion resolved: 0.4626
# Reconstructable efficiency dr=0.2 criterion resolved: 0.3929
# Selection efficiency quark criterion resolved: 0.3377
# Selection efficiency dr=0.4 criterion resolved: 0.4217
# Selection efficiency dr=0.2 criterion resolved: 0.3416
# Real Life efficiency quark criterion resolved: 0.0292
# Real Life efficiency dr=0.4 criterion resolved: 0.1951
# Real Life efficiency dr=0.2 criterion resolved: 0.1342


# numero di top hadronici trovati: 0
# top hadronici trovati: []
# hadronic top idx: []
# i top sono: []
# idx: 0 part pdgId: 2 e idx madre: -1
# idx: 1 part pdgId: 21 e idx madre: -1
# idx: 2 part pdgId: 1 e idx madre: 0
# idx: 3 part pdgId: -5 e idx madre: 0
# idx: 4 part pdgId: 6 e idx madre: 0
# idx: 5 part pdgId: 23 e idx madre: 0
# idx: 6 part pdgId: 23 e idx madre: 5
# idx: 7 part pdgId: 23 e idx madre: 6
# idx: 8 part pdgId: 1 e idx madre: 2
# idx: 9 part pdgId: 23 e idx madre: 7
# idx: 10 part pdgId: 4 e idx madre: -1
# idx: 11 part pdgId: 6 e idx madre: 4
# idx: 12 part pdgId: 23 e idx madre: 9
# idx: 13 part pdgId: 5 e idx madre: 11
# idx: 14 part pdgId: 24 e idx madre: 11
# idx: 15 part pdgId: 2 e idx madre: 12
# idx: 16 part pdgId: -2 e idx madre: 12
# idx: 17 part pdgId: 14 e idx madre: 14
# idx: 18 part pdgId: -13 e idx madre: 14
# idx: 19 part pdgId: -423 e idx madre: -1
# idx: 20 part pdgId: 3 e idx madre: -1
# idx: 21 part pdgId: 2 e idx madre: 15
# idx: 22 part pdgId: 21 e idx madre: 15
# idx: 23 part pdgId: 21 e idx madre: 15
# idx: 24 part pdgId: 21 e idx madre: 16
# idx: 25 part pdgId: 21 e idx madre: 16
# idx: 26 part pdgId: 21 e idx madre: 16
# idx: 27 part pdgId: 21 e idx madre: 16
# idx: 28 part pdgId: -2 e idx madre: 16
# idx: 29 part pdgId: 111 e idx madre: 15
# idx: 30 part pdgId: 3 e idx madre: -1
# idx: 31 part pdgId: -2 e idx madre: -1
# idx: 32 part pdgId: 1 e idx madre: -1
# idx: 33 part pdgId: 21 e idx madre: -1
# idx: 34 part pdgId: 21 e idx madre: -1
# idx: 35 part pdgId: -3 e idx madre: -1
# idx: 36 part pdgId: 2 e idx madre: -1
# idx: 37 part pdgId: 21 e idx madre: -1
# idx: 38 part pdgId: -5 e idx madre: 3
# idx: 39 part pdgId: 513 e idx madre: 36
# idx: 40 part pdgId: 21 e idx madre: 8
# idx: 41 part pdgId: 1 e idx madre: 8
# idx: 42 part pdgId: 4 e idx madre: 10
# idx: 43 part pdgId: 5 e idx madre: 13
# idx: 44 part pdgId: 433 e idx madre: 8
# idx: 45 part pdgId: -533 e idx madre: 8
# idx: 46 part pdgId: 111 e idx madre: 8
# idx: 47 part pdgId: -421 e idx madre: 19
# idx: 48 part pdgId: 22 e idx madre: 29
# idx: 49 part pdgId: 22 e idx madre: 29
# idx: 50 part pdgId: 11 e idx madre: 32
# idx: 51 part pdgId: -11 e idx madre: 32
# idx: 52 part pdgId: 11 e idx madre: 36
# idx: 53 part pdgId: -11 e idx madre: 36
# idx: 54 part pdgId: 511 e idx madre: 39
# idx: 55 part pdgId: 431 e idx madre: 44
# idx: 56 part pdgId: -531 e idx madre: 45
# idx: 57 part pdgId: 11 e idx madre: 8
# idx: 58 part pdgId: -11 e idx madre: 8
# idx: 59 part pdgId: 22 e idx madre: 46
# idx: 60 part pdgId: 11 e idx madre: -1
# idx: 61 part pdgId: -11 e idx madre: -1
# idx: 62 part pdgId: 11 e idx madre: 10
# idx: 63 part pdgId: -11 e idx madre: 10
# idx: 64 part pdgId: 431 e idx madre: 54
# idx: 65 part pdgId: -413 e idx madre: 54
# idx: 66 part pdgId: -431 e idx madre: 56
# idx: 67 part pdgId: -411 e idx madre: 65
# idx: 68 part pdgId: 111 e idx madre: 64
# idx: 69 part pdgId: 111 e idx madre: 64
# idx: 70 part pdgId: 111 e idx madre: 66
# idx: 71 part pdgId: 111 e idx madre: 66
# idx: 72 part pdgId: 22 e idx madre: 68
# idx: 73 part pdgId: 22 e idx madre: 69
# idx: 74 part pdgId: 22 e idx madre: 70
# idx: 75 part pdgId: 22 e idx madre: 71