# TROTA PF
## NanoAODTools
Per come installare CMSSW e far funzionare i NanoAODTools ci si può riferire alla [pagina ufficiale](https://github.com/cms-nanoAOD/nanoAOD-tools)
## Pipeline programmi
### From miniAOD to NanoAOD
> **Questo step serve a produrre dei NanoAod con candidati particleflow. 
> Se si lavora con NanoAODv15 questi sono già inclusi e questo step diventa superfluo.**

Per processare miniaod ho dovuto installare una CMMSW 13-0-X seguendo le istruzioni su [pagina GitHub PFNano](https://github.com/cms-jet/PFNano/tree/13_0_7_from124MiniAOD).
Il file base è precompilato ma se ne possono creare altri con altre opzioni.
Il comando di lancio è cmsRun -filename
Ci sono diversi programmi per MC e Data, io ho processato solo MC.
Il programma che giro è nano-mc-Run3-NANO.py, ce ne sono altri con opzioni diverse.
Le simulazioni si possono caricare direttamente con il nome e usando cms.untracked.vstring o prendendole da files direttamente in questo formato.
Dell'output va esplicitato il path.
Il programma si può girare sia localmente o con condor (in quei casi va specificato il numero di eventi e va creato un file di nomi dei dataset formato vstring), sia con CRAB che è la cosa più conveniente.
> **Nota:** CRAB non può girare su file locali, ma è l’ideale se vuoi processare i miniAOD e farli girare poi.
> 
#### Procedura CRAB
- Modifica adeguatamente i file `crab_cfg.py` e `crab.sh` (esempi su git)
- Esegui:
  crab submit crab_cfg.py
- Verranno create delle cartelle con il nome da te assegnato, sul log sono anche presenti il link al DAS 
- Per controllare la situazione:
  crab status
- Per eliminare cartelle usa **davix**.  
- Per vedere i file:
  eval `scram unsetenv -sh`
  gfal-ls davs://stwebdav.pi.infn.it:8443/cms/store/user/fsalerno/PFNano/

#### Links DAS PFNano girati da me
- **TT_inclusive**   
  Output dataset: /TT_TuneCP5_13p6TeV_powheg-pythia8/fsalerno-TT_inclusive_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FTT_TuneCP5_13p6TeV_powheg-pythia8%2Ffsalerno-TT_inclusive_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **TT_Semilep**  
  Output dataset: /TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/fsalerno-TT_semilep_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL]( https://cmsweb.cern.ch/das/request?input=%2FTTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8%2Ffsalerno-TT_semilep_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **TT_hadronic**  
  Output dataset: /TTto4Q_TuneCP5CR1_13p6TeV_powheg-pythia8/fsalerno-TT_hadronic_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FTTto4Q_TuneCP5CR1_13p6TeV_powheg-pythia8%2Ffsalerno-TT_hadronic_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **TTZprimetoTT_M_3000_W_4**  
  Output dataset: /TTZprimetoTT_M-3000_Width4_TuneCP5_13p6TeV_madgraph-pythia8/fsalerno-TTZprimetoTT_M_3000_W_4_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FTTZprimetoTT_M-3000_Width4_TuneCP5_13p6TeV_madgraph-pythia8%2Ffsalerno-TTZprimetoTT_M_3000_W_4_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **Znunu_HT_400_800**  
  Output dataset: /Zto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_400_800_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FZto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8%2Ffsalerno-QCD_HT_400_800_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **Znunu_HT_800_1500**  
  Output dataset: /Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_800_1500_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FZto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8%2Ffsalerno-QCD_HT_800_1500_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **Znunu_HT_1500_2500**  
  Output dataset: /Zto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_1500_2500_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FZto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8%2Ffsalerno-QCD_HT_1500_2500_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **Znunu_HT_2500_inf**  
  Output dataset:     /Zto2Nu-4Jets\_HT-2500\_TuneCP5\_13p6TeV\_madgraphMLM-pythia8/fsalerno-QCD\_HT\_2500\_inf\_2022-0fa328e40e38f44cd311b92489b92b5b/USER
  [Output dataset DAS URL]( https://cmsweb.cern.ch/das/request?input=%2FZto2Nu-4Jets\_HT-2500\_TuneCP5\_13p6TeV\_madgraphMLM-pythia8%2Ffsalerno-QCD\_HT\_2500\_inf\_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER\&instance=prod%2Fphys03)

- **QCD_HT_400_600**  
  Output dataset: /QCD-4Jets_HT-400to600_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_400_600_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FQCD-4Jets_HT-400to600_TuneCP5_13p6TeV_madgraphMLM-pythia8%2Ffsalerno-QCD_HT_400_600_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **QCD_HT_600_800**  
  Output dataset: /QCD-4Jets_HT-600to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_600_800_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
 [ Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FQCD-4Jets_HT-600to800_TuneCP5_13p6TeV_madgraphMLM-pythia8%2Ffsalerno-QCD_HT_600_800_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **QCD_HT_800_1000**  
  Output dataset: /QCD-4Jets_HT-800to1000_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_800_1000_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FQCD-4Jets_HT-800to1000_TuneCP5_13p6TeV_madgraphMLM-pythia8%2Ffsalerno-QCD_HT_800_1000_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **QCD_HT_1000_1200**  
  Output dataset: /QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_1000_1200_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FQCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8%2Ffsalerno-QCD_HT_1000_1200_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **QCD_HT_1200_1500**  
  Output dataset: /QCD-4Jets_HT-1200to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_1200_1500_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FQCD-4Jets_HT-1200to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8%2Ffsalerno-QCD_HT_1200_1500_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **QCD_HT_1500_2000**  
  Output dataset: /QCD-4Jets_HT-1500to2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_1500_2000_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FQCD-4Jets_HT-1500to2000_TuneCP5_13p6TeV_madgraphMLM-pythia8%2Ffsalerno-QCD_HT_1500_2000_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **QCD_HT_2000_inf**  
  Output dataset: /QCD-4Jets_HT-2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_2000_inf_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
 [ Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FQCD-4Jets_HT-2000_TuneCP5_13p6TeV_madgraphMLM-pythia8%2Ffsalerno-QCD_HT_2000_inf_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

- **W_jets**  
  Output dataset: /WtoLNu-4Jets_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-WtoLNu-4Jets_2022-0fa328e40e38f44cd311b92489b92b5b/USER  
  [Output dataset DAS URL](https://cmsweb.cern.ch/das/request?input=%2FWtoLNu-4Jets_TuneCP5_13p6TeV_madgraphMLM-pythia8%2Ffsalerno-WtoLNu-4Jets_2022-0fa328e40e38f44cd311b92489b92b5b%2FUSER&instance=prod%2Fphys03)

  
### Preprocessing dei MC in CMSSW
I Files prodotti prima vanno processati tramite postprocessor per produrre i candidati top.
Questo può essere fatto manualmente o sfruttando get_file_fromdas, personalmente io ho salvato su eos un file per sample da poi processare, ma get_file_fromdas è l'opzione migliore.
Il postprocessor esegue diversi moduli di fila, la pipeline usata da me è:

- event_counter:
  Uno script che crea un istogramma con il numero di eventi processati che permette di tenere quindi questa informazione per eventuali confronti con i dati.
> Nota: In realtà c'è uno script fatto apposta chiamato MCweight_writer.py della collaborazione che fa la stessa cosa ma meglio e conviene utilizzare.
> 
- GenPart\_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'):
  Trova le madri delle particelle a livello generatore.
  la versione _PF salva anche l'indice delle GenParticles, serve per l'hadronic top
  
- GenPart\_hadronicTop()
  Crea una branch GenPart piena di booleani: 1 se la particella è un top che decade adronicamente, 0 altrimenti.

- IDX_PF:
  Crea una branch PFCands con i loro indici per futuro preprocessing

- DeltaR_PF:
  Crea delle branch PFCands con le distanze nel piano $\eta$-$\phi$ da jet, fatjet e booleani per indicare se sono in jets e Fatjets
  
- collectionMerger(input=\["PFCands"], output="PFCands", sortkey=lambda x: x.pt, reverse=True, selector=None, maxObjects=None):
  Modulo della collaborazione per unire più collezioni, io lo uso per ordinare i candidati ParticleFlow in ordine decrescente di $P_T$

- nanoprepro:
  Crea delle branch Jet e Fatjet in cui dice se sono matchati a dei quark provenienti dal decadimento adronico del top, il pdgId del quark e quello del top da cui provengono.
  Ho creato anche una versione che sfrutta il partonFlavour.

- nanotopcand:
  Crea i candidati top e salva per ogni candidato le variabili di top, jet e fatjet utilizzate per l'allenamento.
  Esistono sia versione PF  che standard
  
### Creazione dei dataset per l'allenamento
I file root prodotti precedentemente vanno trasformati in un formato leggibile e utilizzabile per l'allenamento.
Per gli allenamenti precedenti abbiamo usato il formato pkl, tuttavia all'aumentare del numero di dati, con l'introduzione di variabili PFC, per usare un alto numero di particelle e poter fare allenamenti con un maggior numero di samples sono passato al formato .h5.
Questo formato è più robusto, può essere compresso facilmente senza perdita di dati e ha una struttura facilmente utilizzabile per l'allenamento.
Il preprocessing avviene tramite dei file nella cartella python/postprocessing/machine_learning/Training, che contiene diversi files, tra cui gli allenamenti:

* trainingSet:
  Sono gli script utilizzati per trasformare i file in formato h5 o pkl. La versione standard ha solo il formato pkl mentre quella PF ha sia uno script per il formato h5 sia uno per il pkl.

  Utilizza il multiprocessing per gestire diversi batch di dati in contemporanea (1 batch per worker) accelerando il processo.

* training_Run3_PF_jets_preprocessing:
  Sono gli script per ridurre le dimensioni del dataset, fare un primo bilanciamento e dargli una forma più facilmente fruibile per lo script di allenamento.

  Questo step era incluso nell'allenamento prima ma è molto dispendioso a livello di tempi e risorse e conviene farlo a parte, soprattutto quando si vogliono testare diversi modelli.

  Ci sono tre files:
  * * training_Run3_PF_jets_preprocessing:  processa un file con tutte le componenti al suo interno (Da utilizzare eventualmente dopo aver concatenato i files)

  * * training_Run3_PF_jets_preprocessing_components: processa tutti file presenti in una cartella contenenti le singole componenti uno alla volta (migliore nel caso di file troppo grandi)

  * * training\_Run3\_PF\_jets\_preprocessing\_components\_same\_structure: analogo al precedente ma  lascia la struttura del dataset inalterata

* Conc:
  Serve a concatenare i files, può essere usato prima o dopo il preprocessing a seconda delle dimensioni del file e ci siono sia la versione per pkl che per h5.

### Allenamento
Sempre nella stessa cartella ci sono gli script di allenamento dei modello che si sono rivelati maggiormente performanti durante la tesi: 
* training\_Run3\_PF\_jets\_CNN2D  usa una CNN2D per processare solo le features cinematiche dei candidati PFC
* training\_Run3\_PF\_jets\_CNN2D_LSTM  usa una CNN2D per processare  le features cinematiche dei candidati PFC e un LSTM per processare le altre

L'allenamento è stato diviso in due fasi, nella prima si allenava col dataset preprocessed e nella seconda si riducevano ulteriormente le dimensioni del dataset, facendo sì che solo i top con uno score maggiore di quello necessario per avere un 10% di false positive rate venissero usate per aallenare il nuovo modello. Questo permette all'algoritmo di concentrarsi sui casi più difficili e avere migliori performance contro il fondo combinatorio

Per preparare i dataset alla seconda fase si usano gli script:
* update_trainingSet: ci sono due versioni, una per pkl e una per h5 che processa le componenti separatamente (anche in questo caso per motivi di memoria).

### Evaluation
Lo script di training dà di per sè delle importanti metriche per stimare le performance del classificatore, tuttavia, per testarle sui nuovi dati è necessario usare nuovamente il postprocessor.

I moduli utilizzati sono:
* nanoTopevaluate_MultiScore: Crea delle branch con lo score associato ad ogni top per diversi modelli, c'è una versione per TROTA classico e una PF

* event_counter_x_100x: Riempie sempliun istogramma con il numero di eventi che passano un taglio sullo score corrispondente a un certo fpr. Ci sono verioni per fpr corrispondenti al 10%, 5%, 1% e 0.1%.

Per ottenere poi i plot delle efficienze come quelle sulla DP Note di TROTA si usano gli script nella cartella python/postprocessing/TROTA_eval

* TROTA_efficiency_Study: Riempie gli istogrammi con il numero di eventi in cui un almeno un top o esclusivamente il top con lo score migliore ricostruiti, sono matchati con con top generati (da far girare quindi su montecarlo) secondo diversi criteri di matching e evntualmente imonendo anche vincoli sullo score.
  Funziona per diversi modelli

* TROTA_Efficiency_plotter: Calcola le varie efficienze e le loro incertezze con Clopper-Pearson e le plotta in stile CMS

Gli script cut_flow permettono rispettivamente a loro volta di riempire e plottare gli istogrammi per fare cut_flow e confronti allo stresso fpr tra i vari modelli senza passare per i moduli.

Ci sono anche file di studi sul matching dei jet per verificare l'impatto del taglio dei jet con $p_T$ inferiore a 25 GeV 

  