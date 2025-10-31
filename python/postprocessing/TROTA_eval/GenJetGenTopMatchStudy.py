import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import numpy as np
from array import array
import os
import json
def matchingGenJetGenPart(genpart, genjet):
    # GenPart_genPartIdxMother_prompt è diversa da -1 solo per i quark e le W
    # quindi basta distinguere il b proveniente dal top hadronic

    # funziona per tt semilep da modificare se c'è più di 1 top hadr

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

    #se tutti i quark sono stati trovati
    if (b!=None and q!=None and q_!=None): 
        #matcha il più vicino al genjet e ritorna anche la distanza
        bjet, drb    = closest(b, genjet)
        qjet, drq    = closest(q, genjet)
        q_jet, drq_  = closest(q_, genjet)
    else:
        bjet, qjet, q_jet = None, None, None
    #se la distanza tra ogni quark e il proprio jet è minore di 0.4 ritorna i 3 oggetti
    if(drb<0.4 and drq<0.4 and drq_<0.4):
        return [bjet, qjet, q_jet]
    else:
        return [None, None, None]

def matchingGenJetGenTop(gentop, matchedGenJet_wGenPart):
    # if len(gentop)==1:  top = gentop[0] # sempre vero per tt semilep
    match = False
    recoTop = matchedGenJet_wGenPart[0].p4() + matchedGenJet_wGenPart[1].p4() + matchedGenJet_wGenPart[2].p4()
    # controllare questa somma
    dRGenTopRecoTop = deltaR(gentop[0].eta, gentop[0].phi, recoTop.Eta(), recoTop.Phi()) 
    if(dRGenTopRecoTop<0.4): match = True
    return match, dRGenTopRecoTop


year = 2018
if year == 2018: 
    with open("dict_samples.json", "r") as f:
        sample = json.load(f)   
    # file = "root://cms-xrd-global.cern.ch//store/user/acagnott/Run3Analysis_Tprime/TT_semilep_2018/20240731_214516/tree_hadd_755.root"
    # chain = ROOT.TChain('Events')
    # chain.Add(file)
    file_dict = sample["TT_2018"]["TT_semilep_2018"]
    for i in range(0, 1000):
        file = file_dict["strings"][i]
        print(f"Trying file: {file}")
        chain = ROOT.TChain('Events')
        success = chain.Add(file)
        if success > 0:
            # Prova ad accedere ad un evento per verificare che il file sia leggibile
            if chain.GetEntries() > 0:
                print(f"Successfully added file with events: {file}")
                break
            else:
                print(f"File added but contains no events: {file}")
        else:
            print(f"Failed to add file (possibly 3011 error): {file}")

elif year == 2022:
    with open("dict_samples_2022.json", "r") as f:
        sample = json.load(f)
    file_dict = sample["TT_2022"]["TT_semilep_2022"]
    file_idx = file_dict["ntot"].index(max(file_dict["ntot"]))
    file = file_dict["strings"][file_idx]
    chain = ROOT.TChain('Events')
    chain.Add(file)

    # for i in range(0,40):
    #     file=file_dict["strings"][i]
    #     print(f"Using file: {file}")
    #     chain = ROOT.TChain('Events')
    #     chain.Add(file)
    
print(f"Using file: {file}")

tree = InputTree(chain)
if year == 2018: 
    dir_path = "/eos/user/f/fsalerno/Evaluation/TROTA_2018_studies/Histo_files"
    if not os.path.exists(dir_path):  
        os.makedirs(dir_path)   
    outfile = ROOT.TFile(f"{dir_path}/output_RecoJetGenTopMatchStudy_ttsemilep_noResinMix.root","RECREATE")

elif year == 2022:
    dir_path = "/eos/user/f/fsalerno/Evaluation/TROTA_2022_studies/Histo_files"
    if not os.path.exists(dir_path):  
        os.makedirs(dir_path)   
    outfile = ROOT.TFile(f"{dir_path}/output_GenJetGenTopMatchStudy_ttsemilep_noResinMix.root","RECREATE")


h_gentop_pt              = ROOT.TH1D("h_gentop_pt","; genTop pT", 20, 0, 1000)
h_gentop_reconstruction_pt    = ROOT.TH1D("h_gentop_reconstruction_pt","; genTop pT", 20, 0, 1000)
h_genjet_pt              = ROOT.TH1D("h_genjet_pt","; genJet pT", 20, 0, 1000)
h2_gentopgenminjet_pt       = ROOT.TH2D("h2_gentopgenminjet_pt", "genTop matched min pt genJet; genTop pT; genJet pT", 20, 0, 1000, 50, 0, 1000)
h2_gentopgenmidjet_pt       = ROOT.TH2D("h2_gentopgenmidjet_pt", "genTop matched mid pt genJet; genTop pT; genJet pT", 20, 0, 1000, 50, 0, 1000)
h2_gentopgenmaxjet_pt       = ROOT.TH2D("h2_gentopgenmaxjet_pt", "genTop matched max pt genJet; genTop pT; genJet pT", 20, 0, 1000, 50, 0, 1000)
# h2_gentopgenminjet_pt       = ROOT.TH2D("h2_gentopgenminjet_pt", "genTop matched min pt genJet; genTop pT; genJet pT", 200, 0, 1000, 200, 0, 1000)
# h2_gentopgenmidjet_pt       = ROOT.TH2D("h2_gentopgenmidjet_pt", "genTop matched mid pt genJet; genTop pT; genJet pT", 200, 0, 1000, 200, 0, 1000)
# h2_gentopgenmaxjet_pt       = ROOT.TH2D("h2_gentopgenmaxjet_pt", "genTop matched max pt genJet; genTop pT; genJet pT", 200, 0, 1000, 200, 0, 1000)
h_gentopgenminjet_pt_50_100       = ROOT.TH1D("h_gentopgenminjet_pt_50_100", "matched min pt genJet for genTop pt 50 100;  genJet pT",  40, 0, 200)
h_gentopgenmidjet_pt_50_100       = ROOT.TH1D("h_gentopgenmidjet_pt_50_100", "matched mid pt genJet for genTop pt 50 100;  genJet pT",  40, 0, 200)
h_gentopgenmaxjet_pt_50_100        = ROOT.TH1D("h_gentopgenmaxjet_pt_50_100", "genTop pt 50 100 matched max pt genJet for genTop pt 50 100;  genJet pT",  40, 0, 200)
h_gentopgenminjet_pt_100_200        = ROOT.TH1D("h_gentopgenminjet_pt_100_200 ", "matched min pt genJet for genTop pt 100 200;  genJet pT",  40, 0, 200)
h_gentopgenmidjet_pt_100_200        = ROOT.TH1D("h_gentopgenmidjet_pt_100_200 ", "matched mid pt genJet for genTop pt 100 200;  genJet pT",  40, 0, 200)
h_gentopgenmaxjet_pt_100_200        = ROOT.TH1D("h_gentopgenmaxjet_pt_100_200 ", " matched max pt genJet for genTop pt 100 200;  genJet pT",  40, 0, 200)
h_gentopgenminjet_pt_200_10000        = ROOT.TH1D("h_gentopgenminjet_pt_200_10000 ", "matched min pt genJet for genTop pt 200 inf;  genJet pT",  40, 0, 200)
h_gentopgenmidjet_pt_200_10000        = ROOT.TH1D("h_gentopgenmidjet_pt_200_10000 ", "matched mid pt genJet for genTop pt 200 inf;  genJet pT",  40, 0, 200)
h_gentopgenmaxjet_pt_200_10000        = ROOT.TH1D("h_gentopgenmaxjet_pt_200_10000 ", "matched max pt genJet for genTop pt 200 inf;  genJet pT",  40, 0, 200)
h_gentopgenminjet_pt_inclusive        = ROOT.TH1D("h_gentopgenminjet_pt_inclusive ", "matched min pt genJet for genTop pt 200 inf;  genJet pT",  40, 0, 200)
h_gentopgenmidjet_pt_inclusive        = ROOT.TH1D("h_gentopgenmidjet_pt_inclusive ", "matched mid pt genJet for genTop pt 200 inf;  genJet pT",  40, 0, 200)
h_gentopgenmaxjet_pt_inclusive        = ROOT.TH1D("h_gentopgenmaxjet_pt_inclusive ", "matched max pt genJet for genTop inclusive;  genJet pT",  40, 0, 200)
h_genJet_minpt_notmatched_50_100   = ROOT.TH1D("h_genJet_minpt_notmatched_50_100","min pT genJet not matched; genJet pT", 200, 0, 1000)
h_genJet_midpt_notmatched_50_100   = ROOT.TH1D("h_genJet_midpt_notmatched_50_100","mid pT genJet not matched; genJet pT", 200, 0, 1000)
h_genJet_maxpt_notmatched_50_100   = ROOT.TH1D("h_genJet_maxpt_notmatched_50_100","max pT genJet not matched; genJet pT", 200, 0, 1000)
h_genJet_minpt_notmatched_100_200   = ROOT.TH1D("h_genJet_minpt_notmatched_100_200","min pT genJet not matched; genJet pT", 200, 0, 1000)
h_genJet_midpt_notmatched_100_200   = ROOT.TH1D("h_genJet_midpt_notmatched_100_200","mid pT genJet not matched; genJet pT", 200, 0, 1000)
h_genJet_maxpt_notmatched_100_200   = ROOT.TH1D("h_genJet_maxpt_notmatched_100_200","max pT genJet not matched; genJet pT", 200, 0, 1000)
h_genJet_minpt_notmatched_200_10000   = ROOT.TH1D("h_genJet_minpt_notmatched_200_10000","min pT genJet not matched; genJet pT", 200, 0, 1000)
h_genJet_midpt_notmatched_200_10000   = ROOT.TH1D("h_genJet_midpt_notmatched_200_10000","mid pT genJet not matched; genJet pT", 200, 0, 1000)
h_genJet_maxpt_notmatched_200_10000   = ROOT.TH1D("h_genJet_maxpt_notmatched_200_10000","max pT genJet not matched; genJet pT", 200, 0, 1000)
h_genJet_notmatched_pt_50_100   = ROOT.TH1D("h_genJet_notmatched_pt_50_100","not matched genJet for genTop pt 50 100; genJet pT", 200, 0, 1000)
h_genJet_notmatched_pt_100_200   = ROOT.TH1D("h_genJet_notmatched_pt_100_200","not matched genJet for genTop pt 50 100", 200, 0, 1000)
h_genJet_notmatched_pt_200_10000   = ROOT.TH1D("h_genJet_notmatched_pt_200_10000","not matched genJet for genTop pt 50 100", 200, 0, 1000)
h_genJet_notmatched_pt_inclusive   = ROOT.TH1D("h_genJet_notmatched_pt_inclusive","not matched genJet for genTop pt 50 100", 200, 0, 1000)

h_gentop_pt_excluded   = ROOT.TH1D("h_gentop_pt_excluded","Top where genjet are not matched with quark (at least 1); genTop pT", 20, 0, 1000)
h_gentop_pt_notmatched   = ROOT.TH1D("h_gentop_pt_notmatched","Top not matched; genTop pT", 20, 0, 1000)
h_gentop_pt_matched   = ROOT.TH1D("h_gentop_pt_matched","Top matched; genTop pT", 20, 0, 1000)
h_genJet_minpt_notmatched   = ROOT.TH1D("h_genJet_minpt_notmatched","min pt genJet for genTop pt 50 100 not matched; genJet pT", 30, 0, 1000)
h_genJet_midpt_notmatched   = ROOT.TH1D("h_genJet_midpt_notmatched","mid pT genJet not matched; genJet pT", 30, 0, 1000)
h_genJet_maxpt_notmatched   = ROOT.TH1D("h_genJet_maxpt_notmatched","max pT genJet not matched; genJet pT", 30, 0, 1000)
# h_genJet_minpt_notmatched   = ROOT.TH1D("h_genJet_minpt_notmatched","min pT genJet not matched; genJet pT", 200, 0, 1000)
# h_genJet_midpt_notmatched   = ROOT.TH1D("h_genJet_midpt_notmatched","mid pT genJet not matched; genJet pT", 200, 0, 1000)
# h_genJet_maxpt_notmatched   = ROOT.TH1D("h_genJet_maxpt_notmatched","max pT genJet not matched; genJet pT", 200, 0, 1000)
h_dRGenTopGenJetsum   = ROOT.TH1D("h_dRGenTopGenJetsum","#DeltaR GenTop GenJet_sum; #Delta R", 20, 0, 2)
h_dRGenTopGenJetsumgentoppt   = ROOT.TH2D("h_dRGenTopGenJetsumGentoppt","#DeltaR GenTop GenJet_sum Vs genTop pt; #Delta R; genTop pT", 20, 0, 2, 30, 0, 1000)
h_dRGenTopGenJetsumgenjetminpt   = ROOT.TH2D("h_dRGenTopGenJetsumGenjetminpt","#DeltaR GenTop GenJet_sum Vs genJet min pt; #Delta R; genJet pT", 20, 0, 2, 30, 0, 1000)
h_dRGenTopGenJetsumgenjetmaxpt   = ROOT.TH2D("h_dRGenTopGenJetsumGenjetmaxpt","#DeltaR GenTop GenJet_sum Vs genJet max pt; #Delta R; genJet pT", 20, 0, 2, 30, 0, 1000)

# test addizionali
h_dRGenTopGen2Jetsum   = ROOT.TH1D("h_dRGenTopGen2Jetsum","#DeltaR GenTop GenJet_sum; #Delta R", 20, 0, 2)
h_deltaetadeltaphi     = ROOT.TH2D("h_deltaetadeltaphi", "delta eta delta phi jetsum gentop; deltaEta; deltaPhi", 18, -6, 6, 18, -3.14, 3.14)

nEvGenJetGenQuarkNotMatched = 0
nEvGenJetSumGenTopNotMatched = 0
nEvGenJetMinptl25 = 0


for i in range(tree.GetEntries()):
# for i in range(1000):
    event   = Event(tree,i)
    genpart = Collection(event, "GenPart")
    if year == 2018:
        gentop = Collection(event, "TopGenTopPart", lenVar = "nTopGenHadr")
    elif year == 2022:
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
        gentop = [particle for particle, is_hadr_top in zip(genpart, is_hadronic_top) if is_hadr_top==1]
    genjet  = Collection(event, "Jet")


    nTopGenHadr = len(gentop)
    nGenJet     = len(genjet)
    nGenPart    = len(genpart)

    #tutti i gentop 
    h_gentop_pt.Fill(gentop[0].pt)
    #per ogni evento riporta la collezione di genjets matchati
    matchedGenJet_wGenPart = matchingGenJetGenPart(genpart, genjet)
    # print(matchedGenJet_wGenPart)
    #se esistono i genjet matchati
    if matchedGenJet_wGenPart[0]!= None:
        #almeno un candidato è matchato
        #h_gentop_pt_matched.Fill(gentop[0].pt)
        #riempio l'histo con i jet non matchati in un evento in cui c'è il match
        notmatchedGenJet_wGenPart = [jet for jet in genjet if jet not in matchedGenJet_wGenPart]
        for no_match_jet in notmatchedGenJet_wGenPart:
            h_genJet_notmatched_pt_inclusive.Fill(no_match_jet.pt)
            if gentop[0].pt>=50 and top.pt<100:
                h_genJet_notmatched_pt_50_100.Fill(no_match_jet.pt)
            elif gentop[0].pt>=100 and top.pt<200: 
                h_genJet_notmatched_pt_100_200.Fill(no_match_jet.pt)
            elif gentop[0].pt>=200 and top.pt<10000:
                h_genJet_notmatched_pt_200_10000.Fill(no_match_jet.pt)
            
        #flagga se è matchato il genjet con il gentop
        flag_matchedGenJet_wGenTop, dRGenTopGenJetsum  = matchingGenJetGenTop(gentop, matchedGenJet_wGenPart)
        #distribuzione di deltaR tra il gentop e la somma dei genjet
        h_dRGenTopGenJetsum.Fill(dRGenTopGenJetsum)
        #collezione di pt dei genjet matchati
        genjetspt = [j.pt for j in matchedGenJet_wGenPart]
        #h2d x: distanza tra il gentop e la somma dei genjet, y: pt del gentop adronico (scelgo il primo pre-soft radiation)
        h_dRGenTopGenJetsumgentoppt.Fill(dRGenTopGenJetsum, gentop[0].pt)
        #h2d x: distanza tra il gentop e la somma dei genjet, y: min e max pt dei genjet
        h_dRGenTopGenJetsumgenjetminpt.Fill(dRGenTopGenJetsum, min(genjetspt))
        h_dRGenTopGenJetsumgenjetmaxpt.Fill(dRGenTopGenJetsum, max(genjetspt))
        #se il minimo pt dei genjet è minore di 25 aumenta il contatore (non passa la presel goodjets)
        if min(genjetspt)<25: nEvGenJetMinptl25+=1
        # test addizionali
        # DeltaR (jet1+jet2, top) jet ordine di pt decr
        # plot 2D (deltaEta, deltaPhi) tra gentop e somma genjet
        #range(len(genjetspt)) genera gli indici che poi sorted ordina in ordine decrescente di pt dei genjet
        idxsorted=  sorted(range(len(genjetspt)), key=lambda i: genjetspt[i], reverse=True)
        # jet matched con il più alto pT tra quelli presenti in matchedGenJet_wGenPart
        genjet1 = matchedGenJet_wGenPart[idxsorted[0]]
        genjet2 = matchedGenJet_wGenPart[idxsorted[1]]
        # if(not flag_matchedGenJet_wGenTop):
        #deltaR tra il gentop e la somma dei 2 genjet
        h_dRGenTopGen2Jetsum.Fill(deltaR(gentop[0].eta, gentop[0].phi, (genjet1.p4()+genjet2.p4()).Phi(), (genjet1.p4()+genjet2.p4()).Eta()))

        recoTop = matchedGenJet_wGenPart[0].p4() + matchedGenJet_wGenPart[1].p4() + matchedGenJet_wGenPart[2].p4()
        h_deltaetadeltaphi.Fill(deltaEta(gentop[0].eta, recoTop.Eta()), deltaPhi(gentop[0].phi, recoTop.Phi())) 


        for jet in matchedGenJet_wGenPart:
            h_genjet_pt.Fill(jet.pt)
        
        h_gentop_reconstruction_pt.Fill(gentop[0].pt)

        top = gentop[0]
        #se il gentop è matchato con i genjet
        if flag_matchedGenJet_wGenTop:
            # genjetspt = [j.pt for j in matchedGenJet_wGenPart]
            h2_gentopgenminjet_pt.Fill(top.pt, min(genjetspt))
            h2_gentopgenmidjet_pt.Fill(top.pt, genjetspt[idxsorted[1]])
            h2_gentopgenmaxjet_pt.Fill(top.pt, max(genjetspt))
            h_gentopgenminjet_pt_inclusive.Fill(min(genjetspt))
            h_gentopgenmidjet_pt_inclusive.Fill(genjetspt[idxsorted[1]])
            h_gentopgenmaxjet_pt_inclusive.Fill(max(genjetspt))
            h_gentop_pt_matched.Fill(top.pt)
            if top.pt>=50 and top.pt<100:
                h_gentopgenminjet_pt_50_100.Fill(min(genjetspt))
                #print("min genjet pt 100: ", min(genjetspt))
                h_gentopgenmidjet_pt_50_100.Fill(genjetspt[idxsorted[1]])
                h_gentopgenmaxjet_pt_50_100.Fill(max(genjetspt))
            elif top.pt>=100 and top.pt<200:
                h_gentopgenminjet_pt_100_200.Fill(min(genjetspt))
                #print("min genjet pt 200: ", min(genjetspt))
                h_gentopgenmidjet_pt_100_200.Fill(genjetspt[idxsorted[1]])
                h_gentopgenmaxjet_pt_100_200.Fill(max(genjetspt))
            elif top.pt>=200 and top.pt<10000:
                h_gentopgenminjet_pt_200_10000.Fill(min(genjetspt))
                #print("min genjet pt inf: ", min(genjetspt))
                h_gentopgenmidjet_pt_200_10000.Fill(genjetspt[idxsorted[1]])
                h_gentopgenmaxjet_pt_200_10000.Fill(max(genjetspt))

        else:
            # aggiugni divisione in top con 1 e 2 match --> prova anche ad allargare il dr
            nEvGenJetSumGenTopNotMatched+=1
            h_gentop_pt_notmatched.Fill(top.pt)
            genjetspt = [j.pt for j in matchedGenJet_wGenPart]
            
            h_genJet_minpt_notmatched.Fill(min(genjetspt))
            h_genJet_midpt_notmatched.Fill(genjetspt[idxsorted[1]])
            h_genJet_maxpt_notmatched.Fill(max(genjetspt))
            #fillo sia se sono matchati i quark ma non il top sia se non sono matchati i quark?
            if top.pt>=50 and top.pt<100:
                h_genJet_minpt_notmatched_50_100.Fill(min(genjetspt))
                h_genJet_midpt_notmatched_50_100.Fill(genjetspt[idxsorted[1]])
                h_genJet_maxpt_notmatched_50_100.Fill(max(genjetspt))

            elif top.pt>=100 and top.pt<200: 
                h_genJet_minpt_notmatched_100_200.Fill(min(genjetspt))
                h_genJet_midpt_notmatched_100_200.Fill(genjetspt[idxsorted[1]])
                h_genJet_maxpt_notmatched_100_200.Fill(max(genjetspt))

            elif top.pt>=200 and top.pt<10000:
                h_genJet_minpt_notmatched_200_10000.Fill(min(genjetspt))
                h_genJet_midpt_notmatched_200_10000.Fill(genjetspt[idxsorted[1]])
                h_genJet_maxpt_notmatched_200_10000.Fill(max(genjetspt))


    else: 
        #top in eventi in cui non ci sono tutti e tre i get matchati
        h_gentop_pt_excluded.Fill(gentop[0].pt)
        nEvGenJetGenQuarkNotMatched+=1
        top = gentop[0]
        for jet in genjet:
            if top.pt>=50 and top.pt<100:
                h_genJet_notmatched_pt_50_100.Fill(jet.pt)
            elif top.pt>=100 and top.pt<200: 
                h_genJet_notmatched_pt_100_200.Fill(jet.pt)
            elif top.pt>=200 and top.pt<10000:
                h_genJet_notmatched_pt_200_10000.Fill(jet.pt)
    
outfile.cd()
h_gentop_pt.Write()
h_genjet_pt.Write()
h2_gentopgenminjet_pt.Write()
h2_gentopgenmidjet_pt.Write()
h2_gentopgenmaxjet_pt.Write()
h_gentop_pt_notmatched.Write()
h_genJet_minpt_notmatched.Write()
h_genJet_midpt_notmatched.Write()
h_genJet_maxpt_notmatched.Write()
h_dRGenTopGenJetsum.Write()
h_dRGenTopGenJetsumgentoppt.Write()
h_dRGenTopGenJetsumgenjetminpt.Write()
h_dRGenTopGenJetsumgenjetmaxpt.Write()
h_gentop_pt_matched.Write()
h_gentop_pt_excluded.Write()
h_gentopgenminjet_pt_50_100.Write()
h_gentopgenmidjet_pt_50_100.Write()
h_gentopgenmaxjet_pt_50_100.Write()
h_gentopgenminjet_pt_100_200.Write()
h_gentopgenmidjet_pt_100_200.Write()
h_gentopgenmaxjet_pt_100_200.Write()        
h_gentopgenminjet_pt_200_10000.Write()
h_gentopgenmidjet_pt_200_10000.Write()
h_gentopgenmaxjet_pt_200_10000.Write()
h_gentopgenminjet_pt_inclusive.Write()
h_gentopgenmidjet_pt_inclusive.Write()
h_gentopgenmaxjet_pt_inclusive.Write()
h_genJet_minpt_notmatched_50_100.Write()
h_genJet_midpt_notmatched_50_100.Write()
h_genJet_maxpt_notmatched_50_100.Write()
h_genJet_minpt_notmatched_100_200.Write()
h_genJet_midpt_notmatched_100_200.Write()
h_genJet_maxpt_notmatched_100_200.Write()
h_genJet_minpt_notmatched_200_10000.Write()
h_genJet_midpt_notmatched_200_10000.Write()
h_genJet_maxpt_notmatched_200_10000.Write()
h_genJet_notmatched_pt_inclusive.Write()
h_genJet_notmatched_pt_50_100.Write()
h_genJet_notmatched_pt_100_200.Write()
h_genJet_notmatched_pt_200_10000.Write()
# additional plot
# h_dRGenTopGen2Jetsum.Write()
# h_deltaetadeltaphi.Write()

outfile.Close()

print("Fraction of Events where at least 1 genquark is not matched with a genjet: %.4f" %(nEvGenJetGenQuarkNotMatched/tree.GetEntries()))
print("Fraction of Events where gentop is not matched with the genjet sum: %.4f" %(nEvGenJetSumGenTopNotMatched/tree.GetEntries()))
print("Fraction of Events with gentop matched with genJet sum where min genJet pt < 25: %.4f" %(nEvGenJetMinptl25/tree.GetEntries()))

# Fraction of Events where at least 1 genquark is not matched with a genjet: 0.13580660613000511
# Fraction of Events where gentop is not matched with the genjet sum: 0.8004777695317077

# Fraction of Events where at least 1 genquark is not matched with a genjet: 0.1358
# Fraction of Events where gentop is not matched with the genjet sum: 0.1224
# Fraction of Events with gentop matched with genJet sum where min genJet pt < 25: 0.4288