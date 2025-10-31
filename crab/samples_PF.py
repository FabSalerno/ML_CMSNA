import ROOT
import os
#import json_reader as jr

path = os.path.dirname(os.path.abspath(__file__))

class sample:
    def __init__(self, color, style, fill, leglabel, label):
        self.color = color
        self.style = style
        self.fill = fill
        self.leglabel = leglabel
        self.label = label


################################ WJets ################################
altXSUp=0
kFactorsQCD={
    "WJetsHT100to200" : 1.21,
    "WJetsHT200to400" : 1.21,
    "WJetsHT400to600" : 1.21,
    "WJetsHT600to800" : 1.21,
    "WJetsHT800to1200" : 1.21,
    "WJetsHT1200to2500" : 1.21,
    "WJetsHT2500toInf" : 1.21
}


###############################################################################################################################
##########################################                                           ##########################################
##########################################                    2022                   ##########################################
##########################################                                           ##########################################
###############################################################################################################################
#  EraCD (preEE) più avanti descrizione completa

################################ QCD ################################
# QCD_HT40to70_2022               = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT40to70_2022")
# QCD_HT40to70_2022.sigma         = 311.7*(10**6) #pb
# QCD_HT40to70_2022.year          = 2022
# QCD_HT40to70_2022.dataset       = "/QCD-4Jets_HT-40to70_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3-v1/NANOAODSIM"
# QCD_HT40to70_2022.process       = "QCD_2022"
# QCD_HT40to70_2022.unix_code     = 31000
# QCD_HT40to70_2022.EE            = 0
QCD_HT70to100_2022              = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT70to100_2022")
QCD_HT70to100_2022.sigma        = 58.67*(10**6) #pb
QCD_HT70to100_2022.year         = 2022
QCD_HT70to100_2022.dataset      = "/QCD-4Jets_HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3-v2/NANOAODSIM"
QCD_HT70to100_2022.process      = "QCD_2022"
QCD_HT70to100_2022.unix_code    = 31001
QCD_HT70to100_2022.EE           = 0
QCD_HT100to200_2022             = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT100to200_2022")
QCD_HT100to200_2022.sigma       = 25.14*(10**6) #pb
QCD_HT100to200_2022.year        = 2022
QCD_HT100to200_2022.dataset     = "/QCD-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3-v1/NANOAODSIM"
QCD_HT100to200_2022.process     = "QCD_2022"
QCD_HT100to200_2022.unix_code   = 31002
QCD_HT100to200_2022.EE          = 0
QCD_HT200to400_2022             = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT200to400_2022")
QCD_HT200to400_2022.sigma       = 1.951*(10**6) #pb
QCD_HT200to400_2022.year        = 2022
QCD_HT200to400_2022.dataset     = "/QCD-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3-v2/NANOAODSIM"
QCD_HT200to400_2022.process     = "QCD_2022"
QCD_HT200to400_2022.unix_code   = 31003
QCD_HT200to400_2022.EE          = 0
QCD_HT400to600_2022             = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT400to600_2022")
QCD_HT400to600_2022.sigma       = 96.03*(10**3) #pb
QCD_HT400to600_2022.year        = 2022
QCD_HT400to600_2022.dataset     = "/QCD-4Jets_HT-400to600_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3-v2/NANOAODSIM"
QCD_HT400to600_2022.process     = "QCD_2022"
QCD_HT400to600_2022.unix_code   = 31004
QCD_HT400to600_2022.EE          = 0
QCD_HT600to800_2022             = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT600to800_2022")
QCD_HT600to800_2022.sigma       = 13.51*(10**3) #pb
QCD_HT600to800_2022.year        = 2022
QCD_HT600to800_2022.dataset     = "/QCD-4Jets_HT-600to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3-v1/NANOAODSIM"
QCD_HT600to800_2022.process     = "QCD_2022"
QCD_HT600to800_2022.unix_code   = 31005
QCD_HT600to800_2022.EE          = 0
QCD_HT800to1000_2022            = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT800to1000_2022")
QCD_HT800to1000_2022.sigma      = 3.021*(10**3) #pb
QCD_HT800to1000_2022.year       = 2022
QCD_HT800to1000_2022.dataset    = "/QCD-4Jets_HT-800to1000_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3-v2/NANOAODSIM"
QCD_HT800to1000_2022.process    = "QCD_2022"
QCD_HT800to1000_2022.unix_code  = 31006
QCD_HT800to1000_2022.EE         = 0
QCD_HT1000to1200_2022           = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT1000to1200_2022")
QCD_HT1000to1200_2022.sigma     = 881.4 #pb
QCD_HT1000to1200_2022.year      = 2022
QCD_HT1000to1200_2022.dataset   = "/QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3-v2/NANOAODSIM"
QCD_HT1000to1200_2022.process   = "QCD_2022"
QCD_HT1000to1200_2022.unix_code = 31007
QCD_HT1000to1200_2022.EE        = 0
QCD_HT1200to1500_2022           = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT1200to1500_2022")
QCD_HT1200to1500_2022.sigma     = 384 #pb #881.4 #pb
QCD_HT1200to1500_2022.year      = 2022
QCD_HT1200to1500_2022.dataset   = "/QCD-4Jets_HT-1200to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM"
QCD_HT1200to1500_2022.process   = "QCD_2022"
QCD_HT1200to1500_2022.unix_code = 31007
QCD_HT1200to1500_2022.EE        = 0
QCD_HT1500to2000_2022           = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT1500to2000_2022")
QCD_HT1500to2000_2022.sigma     = 125.2 #pb
QCD_HT1500to2000_2022.year      = 2022
QCD_HT1500to2000_2022.dataset   = "/QCD-4Jets_HT-1500to2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3-v2/NANOAODSIM"
QCD_HT1500to2000_2022.process   = "QCD_2022"
QCD_HT1500to2000_2022.unix_code = 31008
QCD_HT1500to2000_2022.EE        = 0
QCD_HT2000_2022                 = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT2000_2022")
QCD_HT2000_2022.sigma           = 26.36 #pb
QCD_HT2000_2022.year            = 2022
QCD_HT2000_2022.dataset         = "/QCD-4Jets_HT-2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3-v2/NANOAODSIM"
QCD_HT2000_2022.process         = "QCD_2022"
QCD_HT2000_2022.unix_code       = 31009
QCD_HT2000_2022.EE              = 0
QCD_2022                        = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_2022")
QCD_2022.year                   = 2022
QCD_2022.components             = [ 
                                    # QCD_HT40to70_2022, 
                                    QCD_HT70to100_2022, QCD_HT100to200_2022, QCD_HT200to400_2022,
                                    QCD_HT400to600_2022, QCD_HT600to800_2022, QCD_HT800to1000_2022, 
                                    QCD_HT1000to1200_2022, QCD_HT1200to1500_2022,
                                    QCD_HT1500to2000_2022, QCD_HT2000_2022
                                ]


# /QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v2/NANOAODSIM


################################ TTbar ################################
TT_semilep_2022             = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_semilep_2022")
TT_semilep_2022.sigma       = 404.0 #pb
TT_semilep_2022.year        = 2022
TT_semilep_2022.dataset     = "/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3_ext1-v2/NANOAODSIM"
TT_semilep_2022.process     = 'TT_2022'
TT_semilep_2022.unix_code   = 31100
TT_semilep_2022.EE          = 0
TT_hadr_2022                = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_hadr_2022")
TT_hadr_2022.sigma          = 422.3
TT_hadr_2022.year           = 2022
TT_hadr_2022.dataset        = "/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3_ext1-v2/NANOAODSIM"
TT_hadr_2022.process        = 'TT_2022'
TT_hadr_2022.unix_code      = 31101
TT_hadr_2022.EE             = 0
TT_2022                     = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_2022")
TT_2022.year                = 2022
TT_2022.components          = [TT_semilep_2022, TT_hadr_2022]

################################ ZJets ################################

ZJetsToNuNu_HT100to200_2022             = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT100to200_2022")
ZJetsToNuNu_HT100to200_2022.sigma       = 273.6 #pb
ZJetsToNuNu_HT100to200_2022.year        = 2022
ZJetsToNuNu_HT100to200_2022.dataset     = "/Zto2Nu-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM"
ZJetsToNuNu_HT100to200_2022.process     = 'ZJetsToNuNu_2022'
ZJetsToNuNu_HT100to200_2022.unix_code   = 31200
ZJetsToNuNu_HT100to200_2022.EE          = 0
ZJetsToNuNu_HT200to400_2022             = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT200to400_2022")
ZJetsToNuNu_HT200to400_2022.sigma       = 76.14 #pb
ZJetsToNuNu_HT200to400_2022.year        = 2022
ZJetsToNuNu_HT200to400_2022.dataset     = "/Zto2Nu-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM"
ZJetsToNuNu_HT200to400_2022.process     = 'ZJetsToNuNu_2022'
ZJetsToNuNu_HT200to400_2022.unix_code   = 31201
ZJetsToNuNu_HT200to400_2022.EE          = 0
ZJetsToNuNu_HT400to800_2022             = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT400to800_2022")
ZJetsToNuNu_HT400to800_2022.sigma       = 13.18 #pb
ZJetsToNuNu_HT400to800_2022.year        = 2022
ZJetsToNuNu_HT400to800_2022.dataset     = "/Zto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM"
ZJetsToNuNu_HT400to800_2022.process     = 'ZJetsToNuNu_2022'
ZJetsToNuNu_HT400to800_2022.unix_code   = 31202
ZJetsToNuNu_HT400to800_2022.EE          = 0
ZJetsToNuNu_HT800to1500_2022            = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT800to1500_2022")
ZJetsToNuNu_HT800to1500_2022.sigma      = 1.366 #pb
ZJetsToNuNu_HT800to1500_2022.year       = 2022
ZJetsToNuNu_HT800to1500_2022.dataset    = "/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM"
ZJetsToNuNu_HT800to1500_2022.process    = 'ZJetsToNuNu_2022'
ZJetsToNuNu_HT800to1500_2022.unix_code  = 31203
ZJetsToNuNu_HT800to1500_2022.EE         = 0
ZJetsToNuNu_HT1500to2500_2022           = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT1500to2500_2022")
ZJetsToNuNu_HT1500to2500_2022.sigma     = 0.09852 #pb
ZJetsToNuNu_HT1500to2500_2022.year      = 2022
ZJetsToNuNu_HT1500to2500_2022.dataset   = "/Zto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM"
ZJetsToNuNu_HT1500to2500_2022.process   = 'ZJetsToNuNu_2022'
ZJetsToNuNu_HT1500to2500_2022.unix_code = 31204
ZJetsToNuNu_HT1500to2500_2022.EE            = 0
ZJetsToNuNu_HT2500_2022                 = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT2500_2022")
ZJetsToNuNu_HT2500_2022.sigma           = 0.006699 #pb
ZJetsToNuNu_HT2500_2022.year            = 2022
ZJetsToNuNu_HT2500_2022.dataset         = "/Zto2Nu-4Jets_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM"
ZJetsToNuNu_HT2500_2022.process         = 'ZJetsToNuNu_2022'
ZJetsToNuNu_HT2500_2022.unix_code       = 31205
ZJetsToNuNu_HT2500_2022.EE              = 0
ZJetsToNuNu_2022                        = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2022")
ZJetsToNuNu_2022.year                   = 2022
ZJetsToNuNu_2022.components             = [
                                            ZJetsToNuNu_HT100to200_2022,
                                            ZJetsToNuNu_HT200to400_2022,
                                            ZJetsToNuNu_HT400to800_2022,
                                            ZJetsToNuNu_HT800to1500_2022,
                                            ZJetsToNuNu_HT1500to2500_2022,
                                            ZJetsToNuNu_HT2500_2022 
                                            ]

################################ WJets ################################

WJets_2022           = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_2022")
WJets_2022.sigma     = 63199.9 #pb
WJets_2022.year      = 2022
WJets_2022.dataset   = "/WtoLNu-4Jets_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_v3-v2/NANOAODSIM"
WJets_2022.process   = 'WJets_2022'
WJets_2022.unix_code = 31300
WJets_2022.EE        = 0

#######################################   VLQ T signals   #######################################
TprimeToTZ_700_2022           = sample(ROOT.kGreen, 1, 1001, "T#rightarrow tZ M700GeV", "TprimeToTZ_700_2022")
TprimeToTZ_700_2022.sigma     = 0.07804 #pb  # questa è 2018 non 2022
TprimeToTZ_700_2022.year      = 2022
TprimeToTZ_700_2022.dataset   = '/TprimeBtoTZ_M-700_LH_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/NANOAODSIM'
TprimeToTZ_700_2022.unix_code = 32000
TprimeToTZ_700_2022.EE        = 0

TprimeToTZ_1000_2022           = sample(ROOT.kGreen, 1, 1001, "T#rightarrow tZ M700GeV", "TprimeToTZ_1000_2022")
TprimeToTZ_1000_2022.sigma     = 0.01362 #pb  # questa è 2018 non 2022
TprimeToTZ_1000_2022.year      = 2022
TprimeToTZ_1000_2022.dataset   = '/TprimeBtoTZ_M-1000_LH_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/NANOAODSIM' 
TprimeToTZ_1000_2022.unix_code = 32001
TprimeToTZ_1000_2022.EE        = 0

TprimeToTZ_1800_2022           = sample(ROOT.kGreen+4, 1, 1001, "T#rightarrow tZ M1800GeV", "TprimeToTZ_1800_2022")
TprimeToTZ_1800_2022.sigma     = 0.00045 #pb
TprimeToTZ_1800_2022.year      = 2022
TprimeToTZ_1800_2022.dataset   = '/TprimeBtoTZ_M-1800_LH_TuneCP5_13p6TeV_madgraph-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/NANOAODSIM'
TprimeToTZ_1800_2022.unix_code = 22000
TprimeToTZ_1800_2022.EE        = 0


###############################################################################################################################
##########################################                                           ##########################################
##########################################                   2022EE                  ##########################################
##########################################                                           ##########################################
###############################################################################################################################
# Era EFG del 2022 hanno avuto un proble water leak (controlla bene?) per cui vanno sotto una tag diversa 
# rispetto a era CD, per questo finora abbiamo usato la tag Run3Summer22 e da qui rifacciamo i sample con
# 2022EE --> Run3Summer22EE, ci sono correzioni diverse per i due pezzi quindi invece di cambiare l'anno
# aggiungerò un .EE che sarà True solo per i 2022EE, False per i 2022 e per gli altri anni non definito
# NB per i dati le ere hanno tutti year 2022 perché il golden JSON è lo stesso per tutti
################################ QCD ################################
# QCD_HT40to70_2022EE               = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT40to70_2022EE")
# QCD_HT40to70_2022EE.sigma         = 311.7*(10**6) #pb
# QCD_HT40to70_2022EE.year          = 2022
# QCD_HT40to70_2022EE.dataset       = # NO DATASET
# QCD_HT40to70_2022EE.process       = "QCD_2022EE"
# QCD_HT40to70_2022EE.unix_code     = 41000
# QCD_HT40to70_2022EE.EE            = 1
QCD_HT70to100_2022EE              = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT70to100_2022EE")
QCD_HT70to100_2022EE.sigma        = 58.67*(10**6) #pb
QCD_HT70to100_2022EE.year         = 2022
QCD_HT70to100_2022EE.dataset      = "/QCD-4Jets_HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v1/NANOAODSIM"
QCD_HT70to100_2022EE.process      = "QCD_2022EE"
QCD_HT70to100_2022EE.unix_code    = 41001
QCD_HT70to100_2022EE.EE           = 1
QCD_HT100to200_2022EE             = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT100to200_2022EE")
QCD_HT100to200_2022EE.sigma       = 25.14*(10**6) #pb
QCD_HT100to200_2022EE.year        = 2022
QCD_HT100to200_2022EE.dataset     = "/QCD-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM"
QCD_HT100to200_2022EE.process     = "QCD_2022EE"
QCD_HT100to200_2022EE.unix_code   = 41002
QCD_HT100to200_2022EE.EE          = 1
QCD_HT200to400_2022EE             = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT200to400_2022EE")
QCD_HT200to400_2022EE.sigma       = 1.951*(10**6) #pb
QCD_HT200to400_2022EE.year        = 2022
QCD_HT200to400_2022EE.dataset     = "/QCD-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v2/NANOAODSIM"
QCD_HT200to400_2022EE.process     = "QCD_2022EE"
QCD_HT200to400_2022EE.unix_code   = 41003
QCD_HT200to400_2022EE.EE          = 1
QCD_HT400to600_2022EE             = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT400to600_2022EE")
QCD_HT400to600_2022EE.sigma       = 96.03*(10**3) #pb
QCD_HT400to600_2022EE.year        = 2022
QCD_HT400to600_2022EE.dataset     = "/QCD-4Jets_HT-400to600_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v2/NANOAODSIM"
QCD_HT400to600_2022EE.process     = "QCD_2022EE"
QCD_HT400to600_2022EE.unix_code   = 41004
QCD_HT400to600_2022EE.EE          = 1
QCD_HT600to800_2022EE             = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT600to800_2022EE")
QCD_HT600to800_2022EE.sigma       = 13.51*(10**3) #pb
QCD_HT600to800_2022EE.year        = 2022
QCD_HT600to800_2022EE.dataset     = "/QCD-4Jets_HT-600to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM"
QCD_HT600to800_2022EE.process     = "QCD_2022EE"
QCD_HT600to800_2022EE.unix_code   = 41005
QCD_HT600to800_2022EE.EE          = 1
QCD_HT800to1000_2022EE            = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT800to1000_2022EE")
QCD_HT800to1000_2022EE.sigma      = 3.021*(10**3) #pb
QCD_HT800to1000_2022EE.year       = 2022
QCD_HT800to1000_2022EE.dataset    = "/QCD-4Jets_HT-800to1000_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v2/NANOAODSIM"
QCD_HT800to1000_2022EE.process    = "QCD_2022EE"
QCD_HT800to1000_2022EE.unix_code  = 41006
QCD_HT800to1000_2022EE.EE         = 1
QCD_HT1000to1200_2022EE           = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT1000to1200_2022EE")
QCD_HT1000to1200_2022EE.sigma     = 881.4 #pb
QCD_HT1000to1200_2022EE.year      = 2022
QCD_HT1000to1200_2022EE.dataset   = "/QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v2/NANOAODSIM"
QCD_HT1000to1200_2022EE.process   = "QCD_2022EE"
QCD_HT1000to1200_2022EE.unix_code = 41007
QCD_HT1000to1200_2022EE.EE        = 1
QCD_HT1200to1500_2022EE           = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT1200to1500_2022EE")
QCD_HT1200to1500_2022EE.sigma     = 881.4 #pb
QCD_HT1200to1500_2022EE.year      = 2022
QCD_HT1200to1500_2022EE.dataset   = "/QCD-4Jets_HT-1200to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v2/NANOAODSIM"
QCD_HT1200to1500_2022EE.process   = "QCD_2022EE"
QCD_HT1200to1500_2022EE.unix_code = 41007
QCD_HT1200to1500_2022EE.EE        = 1
QCD_HT1500to2000_2022EE           = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT1500to2000_2022EE")
QCD_HT1500to2000_2022EE.sigma     = 125.2 #pb
QCD_HT1500to2000_2022EE.year      = 2022
QCD_HT1500to2000_2022EE.dataset   = "/QCD-4Jets_HT-1200to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v2/NANOAODSIM"
QCD_HT1500to2000_2022EE.process   = "QCD_2022EE"
QCD_HT1500to2000_2022EE.unix_code = 41008
QCD_HT1500to2000_2022EE.EE        = 1
QCD_HT2000_2022EE                 = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_HT2000_2022EE")
QCD_HT2000_2022EE.sigma           = 26.36 #pb
QCD_HT2000_2022EE.year            = 2022
QCD_HT2000_2022EE.dataset         = "/QCD-4Jets_HT-2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v2/NANOAODSIM"
QCD_HT2000_2022EE.process         = "QCD_2022EE"
QCD_HT2000_2022EE.unix_code       = 41009
QCD_HT2000_2022EE.EE              = 1
QCD_2022EE                        = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_2022EE")
QCD_2022EE.year                   = 2022
QCD_2022EE.components             = [ 
                                    # QCD_HT40to70_2022EE, 
                                    QCD_HT70to100_2022EE, QCD_HT100to200_2022EE, QCD_HT200to400_2022EE,
                                    QCD_HT400to600_2022EE, QCD_HT600to800_2022EE, QCD_HT800to1000_2022EE, 
                                    QCD_HT1000to1200_2022EE,QCD_HT1200to1500_2022EE,
                                    QCD_HT1500to2000_2022EE, QCD_HT2000_2022EE
                                ]


# /QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v2/NANOAODSIM


################################ TTbar ################################
TT_semilep_2022EE             = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_semilep_2022EE")
TT_semilep_2022EE.sigma       = 404.0 #pb
TT_semilep_2022EE.year        = 2022
TT_semilep_2022EE.dataset     = "/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v2/NANOAODSIM"
TT_semilep_2022EE.process     = 'TT_2022EE'
TT_semilep_2022EE.unix_code   = 41100
TT_semilep_2022EE.EE          = 1
TT_hadr_2022EE                = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_hadr_2022EE")
TT_hadr_2022EE.sigma          = 422.3
TT_hadr_2022EE.year           = 2022
TT_hadr_2022EE.dataset        = "/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v2/NANOAODSIM"
TT_hadr_2022EE.process        = 'TT_2022EE'
TT_hadr_2022EE.unix_code      = 41101
TT_hadr_2022EE.EE             = 1
TT_2022EE                     = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_2022EE")
TT_2022EE.year                = 2022
TT_2022EE.components          = [TT_semilep_2022EE, TT_hadr_2022EE]

################################ ZJets ################################

ZJetsToNuNu_HT100to200_2022EE             = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT100to200_2022EE")
ZJetsToNuNu_HT100to200_2022EE.sigma       = 273.6 #pb
ZJetsToNuNu_HT100to200_2022EE.year        = 2022
ZJetsToNuNu_HT100to200_2022EE.dataset     = "/Zto2Nu-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM"
ZJetsToNuNu_HT100to200_2022EE.process     = 'ZJetsToNuNu_2022EE'
ZJetsToNuNu_HT100to200_2022EE.unix_code   = 31200
ZJetsToNuNu_HT100to200_2022EE.EE          = 1
ZJetsToNuNu_HT200to400_2022EE             = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT200to400_2022EE")
ZJetsToNuNu_HT200to400_2022EE.sigma       = 76.14 #pb
ZJetsToNuNu_HT200to400_2022EE.year        = 2022
ZJetsToNuNu_HT200to400_2022EE.dataset     = "/Zto2Nu-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM"
ZJetsToNuNu_HT200to400_2022EE.process     = 'ZJetsToNuNu_2022EE'
ZJetsToNuNu_HT200to400_2022EE.unix_code   = 31201
ZJetsToNuNu_HT200to400_2022EE.EE          = 1
ZJetsToNuNu_HT400to800_2022EE             = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT400to800_2022EE")
ZJetsToNuNu_HT400to800_2022EE.sigma       = 13.18 #pb
ZJetsToNuNu_HT400to800_2022EE.year        = 2022
ZJetsToNuNu_HT400to800_2022EE.dataset     = "/Zto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM"
ZJetsToNuNu_HT400to800_2022EE.process     = 'ZJetsToNuNu_2022EE'
ZJetsToNuNu_HT400to800_2022EE.unix_code   = 31202
ZJetsToNuNu_HT400to800_2022EE.EE          = 1
ZJetsToNuNu_HT800to1500_2022EE            = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT800to1500_2022EE")
ZJetsToNuNu_HT800to1500_2022EE.sigma      = 1.366 #pb
ZJetsToNuNu_HT800to1500_2022EE.year       = 2022
ZJetsToNuNu_HT800to1500_2022EE.dataset    = "/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1/NANOAODSIM"
ZJetsToNuNu_HT800to1500_2022EE.process    = 'ZJetsToNuNu_2022EE'
ZJetsToNuNu_HT800to1500_2022EE.unix_code  = 31203
ZJetsToNuNu_HT800to1500_2022EE.EE         = 1
ZJetsToNuNu_HT1500to2500_2022EE           = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT1500to2500_2022EE")
ZJetsToNuNu_HT1500to2500_2022EE.sigma     = 0.09852 #pb
ZJetsToNuNu_HT1500to2500_2022EE.year      = 2022
ZJetsToNuNu_HT1500to2500_2022EE.dataset   = "/Zto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM"
ZJetsToNuNu_HT1500to2500_2022EE.process   = 'ZJetsToNuNu_2022EE'
ZJetsToNuNu_HT1500to2500_2022EE.unix_code = 31204
ZJetsToNuNu_HT1500to2500_2022EE.EE        = 1
ZJetsToNuNu_HT2500_2022EE                 = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_HT2500_2022EE")
ZJetsToNuNu_HT2500_2022EE.sigma           = 0.006699 #pb
ZJetsToNuNu_HT2500_2022EE.year            = 2022
ZJetsToNuNu_HT2500_2022EE.dataset         = "/Zto2Nu-4Jets_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM"
ZJetsToNuNu_HT2500_2022EE.process         = 'ZJetsToNuNu_2022EE'
ZJetsToNuNu_HT2500_2022EE.unix_code       = 31205
ZJetsToNuNu_HT2500_2022EE.EE              = 1
ZJetsToNuNu_2022EE                        = sample(ROOT.kAzure+6, 1, 1001, "ZJets #rightarrow #nu#nu", "ZJetsToNuNu_2022EE")
ZJetsToNuNu_2022EE.year                   = 2022
ZJetsToNuNu_2022EE.components             = [
                                            ZJetsToNuNu_HT100to200_2022EE, ZJetsToNuNu_HT200to400_2022EE, ZJetsToNuNu_HT400to800_2022EE,
                                            ZJetsToNuNu_HT800to1500_2022EE, ZJetsToNuNu_HT1500to2500_2022EE, ZJetsToNuNu_HT2500_2022EE 
                                            ]

################################ WJets ################################

WJets_2022EE           = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_2022EE")
WJets_2022EE.sigma     = 63199.9 #pb
WJets_2022EE.year      = 2022
WJets_2022EE.dataset   = "/WtoLNu-4Jets_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22EENanoAODv12-JMENano12p5_132X_mcRun3_2022_realistic_postEE_v4-v2/NANOAODSIM"
WJets_2022EE.process   = 'WJets_2022EE'
WJets_2022EE.unix_code = 41300
WJets_2022EE.EE        = 1


##################################################################################
########################### DATA 2016 ############################################
##################################################################################

DataHTH_2016           = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTH_2016")  #8.6fb
DataHTH_2016.runP      = 'H'
DataHTH_2016.year      = 2016
DataHTH_2016.dataset   = '/MET/Run2016H-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD'
# DataHTH_2016.unix_code = 

################### DA ELIMINARE QUANDO ABBIAMO LA VERSIONE NUOVA DA CRAB

# DataHTA_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTA_2018")
# DataHTA_2018.runP      = 'A'
# DataHTA_2018.year      = 2018
# DataHTA_2018.dataset   = '/MET/Run2018A-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD' #'/MET/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'
# DataHTA_2018.process   = "DataMET_2018"
# DataHTA_2018.unix_code = 20000



########################### DATA 2018 ############################################
DataMETA_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataMETA_2018")
DataMETA_2018.runP      = 'A'
DataMETA_2018.year      = 2018
DataMETA_2018.dataset   = '/MET/Run2018A-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD' #'/MET/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'
DataMETA_2018.process   = "DataMET_2018"
DataMETA_2018.unix_code = 20000
DataMETB_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataMETB_2018")
DataMETB_2018.runP      = 'B'
DataMETB_2018.year      = 2018
DataMETB_2018.dataset   = '/MET/Run2018B-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD' #'/MET/Run2018B-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'
DataMETB_2018.process   = "DataMET_2018"
DataMETB_2018.unix_code = 20001
DataMETC_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataMETC_2018")
DataMETC_2018.runP      = 'C'
DataMETC_2018.year      = 2018
DataMETC_2018.dataset   = '/MET/Run2018C-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'#'/MET/Run2018C-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD'
DataMETC_2018.process   = "DataMET_2018"
DataMETC_2018.unix_code = 20002
DataMETD_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataMETD_2018")
DataMETD_2018.runP      = 'D'
DataMETD_2018.year      = 2018
DataMETD_2018.dataset   = '/MET/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'#'/MET/Run2018D-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD'
DataMETD_2018.process   = "DataMET_2018"
DataMETD_2018.unix_code = 20003

DataMET_2018            = sample(ROOT.kBlack, 1, 1001, "Data", "DataMET_2018")
DataMET_2018.year       = 2018
DataMET_2018.components = [DataMETA_2018, DataMETB_2018, 
                          DataMETC_2018, DataMETD_2018
                          ]

DataSingleMuA_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataSingleMuA_2018")
DataSingleMuA_2018.runP      = 'A'
DataSingleMuA_2018.year      = 2018
DataSingleMuA_2018.dataset   = '/SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'
DataSingleMuA_2018.process   = "DataSingleMu_2018"
DataSingleMuA_2018.unix_code = 20100
DataSingleMuB_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataSingleMuB_2018")
DataSingleMuB_2018.runP      = 'B'
DataSingleMuB_2018.year      = 2018
DataSingleMuB_2018.dataset   = '/SingleMuon/Run2018B-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'
DataSingleMuB_2018.process   = "DataSingleMu_2018"
DataSingleMuB_2018.unix_code = 20101
DataSingleMuC_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataSingleMuC_2018")
DataSingleMuC_2018.runP      = 'C'
DataSingleMuC_2018.year      = 2018
DataSingleMuC_2018.dataset   = '/SingleMuon/Run2018C-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'
DataSingleMuC_2018.process   = "DataSingleMu_2018"
DataSingleMuC_2018.unix_code = 20102
DataSingleMuD_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataSingleMuD_2018")
DataSingleMuD_2018.runP      = 'D'
DataSingleMuD_2018.year      = 2018
DataSingleMuD_2018.dataset   = '/SingleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'
DataSingleMuD_2018.process   = "DataSingleMu_2018"
DataSingleMuD_2018.unix_code = 20103

DataSingleMu_2018            = sample(ROOT.kBlack, 1, 1001, "Data", "DataSingleMu_2018")
DataSingleMu_2018.year       = 2018
DataSingleMu_2018.components = [DataSingleMuA_2018, DataSingleMuB_2018, 
                                DataSingleMuC_2018, DataSingleMuD_2018
                               ]


# DataMETA_2018          = sample(ROOT.kBlack, 1, 1001, "Data", "DataMETA_2018")
# DataMETA_2018.runP     = 'A'
# DataMETA_2018.year     = 2018
# DataMETA_2018.dataset  = '/MET/Run2018A-02Apr2020-v1/NANOAOD' #ReRECO 2018 A

########################### DATA 2022 ############################################

DataJetMETC_2022            = sample(ROOT.kBlack, 1, 1001, "Data", "DataJetMETC_2022")
DataJetMETC_2022.runP       = 'C'
DataJetMETC_2022.year       = 2022
DataJetMETC_2022.dataset    = '/JetMET/Run2022C-22Sep2023-v1/NANOAOD' #/JetMET/Run2022C-JMENano12p5-v1/NANOAOD da capire quale vogliono che usiamo
DataJetMETC_2022.unix_code  = 30000
DataJetMETC_2022.EE         = 0
DataJetMETD_2022            = sample(ROOT.kBlack, 1, 1001, "Data", "DataJetMETD_2022")
DataJetMETD_2022.runP       = 'D'
DataJetMETD_2022.year       = 2022
DataJetMETD_2022.dataset    = '/JetMET/Run2022D-22Sep2023-v1/NANOAOD'
DataJetMETD_2022.unix_code  = 30001
DataJetMETD_2022.EE         = 0
DataJetMETE_2022            = sample(ROOT.kBlack, 1, 1001, "Data", "DataJetMETE_2022")
DataJetMETE_2022.runP       = 'E'
DataJetMETE_2022.year       = 2022
DataJetMETE_2022.dataset    = '/JetMET/Run2022E-22Sep2023-v1/NANOAOD'
DataJetMETE_2022.unix_code  = 30002
DataJetMETE_2022.EE         = 1
DataJetMETF_2022            = sample(ROOT.kBlack, 1, 1001, "Data", "DataJetMETF_2022")
DataJetMETF_2022.runP       = 'F'
DataJetMETF_2022.year       = 2022
DataJetMETF_2022.dataset    = '/JetMET/Run2022F-22Sep2023-v2/NANOAOD'
DataJetMETF_2022.unix_code  = 30003
DataJetMETF_2022.EE         = 1
DataJetMETG_2022            = sample(ROOT.kBlack, 1, 1001, "Data", "DataJetMETG_2022")
DataJetMETG_2022.runP       = 'G'
DataJetMETG_2022.year       = 2022
DataJetMETG_2022.dataset    = '/JetMET/Run2022G-22Sep2023-v2/NANOAOD'
DataJetMETG_2022.unix_code  = 30004
DataJetMETG_2022.EE         = 1
DataJetMET_2022             = sample(ROOT.kBlack, 1, 1001, "Data", "DataJetMET_2022")
DataJetMET_2022.year        = 2022
DataJetMET_2022.components  = [DataJetMETC_2022, DataJetMETD_2022, DataJetMETE_2022, DataJetMETF_2022, DataJetMETG_2022]

DataMuonC_2022              = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuonC_2022")
DataMuonC_2022.runP         = 'C'
DataMuonC_2022.year         = 2022
DataMuonC_2022.dataset      = '/Muon/Run2022C-22Sep2023-v1/NANOAOD'
DataMuonC_2022.unix_code    = 30100
DataMuonC_2022.EE           = 0
DataMuonD_2022              = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuonD_2022")
DataMuonD_2022.runP         = 'D'
DataMuonD_2022.year         = 2022
DataMuonD_2022.dataset      = '/Muon/Run2022C-22Sep2023-v1/NANOAOD'
DataMuonD_2022.unix_code    = 30101
DataMuonD_2022.EE           = 0
DataMuonE_2022              = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuonE_2022")
DataMuonE_2022.runP         = 'E'
DataMuonE_2022.year         = 2022
DataMuonE_2022.dataset      = '/Muon/Run2022E-22Sep2023-v1/NANOAOD'
DataMuonE_2022.unix_code    = 30102
DataMuonE_2022.EE           = 1
DataMuonF_2022              = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuonF_2022")
DataMuonF_2022.runP         = 'F'
DataMuonF_2022.year         = 2022
DataMuonF_2022.dataset      = '/Muon/Run2022F-22Sep2023-v2/NANOAOD'
DataMuonF_2022.unix_code    = 30103
DataMuonF_2022.EE           = 1
DataMuonG_2022              = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuonG_2022")
DataMuonG_2022.runP         = 'G'
DataMuonG_2022.year         = 2022
DataMuonG_2022.dataset      = '/Muon/Run2022G-22Sep2023-v2/NANOAOD'
DataMuonG_2022.unix_code    = 30104
DataMuonG_2022.EE           = 1
DataMuon_2022               = sample(ROOT.kBlack, 1, 1001, "Data", "DataMuon_2022")
DataMuon_2022.year          = 2022
DataMuon_2022.components    = [DataMuonC_2022, DataMuonD_2022, DataMuonE_2022, DataMuonF_2022, DataMuonG_2022]

############### UNIX code meanings ################
# XXXXX  5 digits for each sample
# 1st digit: 0 for 2016, 1 for 2017, 2 for 2018, 3 for 2022, 4 for 2022EE, 5 for 2023, 6 for 2023BP
# 2nd digit: 0 for data, 1 for MC bkg, 2 for MC signal
# 3rd digit: for the process (QCD = 0, TT = 1, ZJets = 2, WJets = 3, 
#                             Tprime = 0, tDM = 1, 
#                             Data_MET = 0, Data_SingleMu = 1,...)
# 3rd digit and 4th digit: 2 digits identifies the sample 

# example: QCDHT_100to200_2018 == 21000, QCDHT_200to300_2018 == 21001
#          DATAHTA_2018 == 20600, DATAHTB_2018 == 20601, DATAHTC_2018 == 20602, DATAHTD_2018 == 20603  
### non diamo un codice ai sample con le components --> da capire se serve aggiungerlo


sample_dict = {

    # 'DataHTA_2018': DataHTA_2018,

    ################################## RUN II
    'DataHTH_2016': DataHTH_2016,
    # Data MET 2018   
    'DataMET_2018': DataMET_2018, 'DataMETA_2018': DataMETA_2018, 'DataMETB_2018': DataMETB_2018,
    'DataMETC_2018': DataMETC_2018, 'DataMETD_2018': DataMETD_2018, 
    # 'DataMETA_2018': DataMETA_2018,
    # Data Single Muon 2018
    'DataSingleMu_2018':DataSingleMu_2018, 'DataSingleMuA_2018':DataSingleMuA_2018, 'DataSingleMuB_2018':DataSingleMuB_2018, 
    'DataSingleMuC_2018':DataSingleMuC_2018, 'DataSingleMuD_2018':DataSingleMuD_2018,
    # BKGs 2018
    'QCDHT_100to200_2018':QCDHT_100to200_2018, 'QCDHT_200to300_2018':QCDHT_200to300_2018, 
    'QCDHT_300to500_2018':QCDHT_300to500_2018, 'QCDHT_500to700_2018':QCDHT_500to700_2018, 
    'QCDHT_700to1000_2018':QCDHT_700to1000_2018, 'QCDHT_1000to1500_2018':QCDHT_1000to1500_2018, 
    'QCDHT_1500to2000_2018':QCDHT_1500to2000_2018, 'QCDHT_2000toInf_2018':QCDHT_2000toInf_2018, 
    'QCD_2018':QCD_2018,
    'TT_Mtt700to1000_2018':TT_Mtt700to1000_2018, 'TT_Mtt1000toInf_2018':TT_Mtt1000toInf_2018, 
    'TT_semilep_2018':TT_semilep_2018, 'TT_hadr_2018':TT_hadr_2018,
    'TT_2018':TT_2018,
    'ZJetsToNuNu_HT100to200_2018':ZJetsToNuNu_HT100to200_2018, 'ZJetsToNuNu_HT200to400_2018':ZJetsToNuNu_HT200to400_2018, 
    'ZJetsToNuNu_HT400to600_2018':ZJetsToNuNu_HT400to600_2018, 'ZJetsToNuNu_HT600to800_2018':ZJetsToNuNu_HT600to800_2018, 
    'ZJetsToNuNu_HT800to1200_2018':ZJetsToNuNu_HT800to1200_2018, 'ZJetsToNuNu_HT1200to2500_2018':ZJetsToNuNu_HT1200to2500_2018, 
    'ZJetsToNuNu_HT2500toInf_2018':ZJetsToNuNu_HT2500toInf_2018, 
    'ZJetsToNuNu_2018':ZJetsToNuNu_2018,
    'WJetsHT70to100_2018':WJetsHT70to100_2018,'WJetsHT100to200_2018':WJetsHT100to200_2018,
    'WJetsHT200to400_2018':WJetsHT200to400_2018,'WJetsHT400to600_2018':WJetsHT400to600_2018,
    'WJetsHT600to800_2018':WJetsHT600to800_2018,'WJetsHT800to1200_2018':WJetsHT800to1200_2018,
    'WJetsHT1200to2500_2018':WJetsHT1200to2500_2018,'WJetsHT2500toInf_2018':WJetsHT2500toInf_2018,
    'WJets_2018':WJets_2018,    
    # signals 2018
    'TprimeToTZ_1800_2018' : TprimeToTZ_1800_2018, 
    'TprimeToTZ_1000_2018' : TprimeToTZ_1000_2018, 
    'TprimeToTZ_700_2018' : TprimeToTZ_700_2018,
    'tDM_mPhi50_mChi1_2018' : tDM_mPhi50_mChi1_2018, 'tDM_mPhi500_mChi1_2018' : tDM_mPhi500_mChi1_2018, 'tDM_mPhi1000_mChi1_2018' : tDM_mPhi1000_mChi1_2018,
    
    #######################################
    ############# RUN III ################
    #######################################

    #####################2022
    ############ QCD
    'QCD_2022' : QCD_2022,
    # "QCD_HT40to70_2022": QCD_HT40to70_2022, 
    "QCD_HT70to100_2022": QCD_HT70to100_2022, 
    "QCD_HT100to200_2022": QCD_HT100to200_2022, "QCD_HT200to400_2022": QCD_HT200to400_2022, 
    "QCD_HT400to600_2022": QCD_HT400to600_2022, "QCD_HT600to800_2022": QCD_HT600to800_2022, 
    "QCD_HT800to1000_2022": QCD_HT800to1000_2022, "QCD_HT1000to1200_2022": QCD_HT1000to1200_2022, 
    "QCD_HT1200to1500_2022": QCD_HT1200to1500_2022, "QCD_HT1500to2000_2022": QCD_HT1500to2000_2022, "QCD_HT2000_2022": QCD_HT2000_2022,
    ########### TT
    'TT_2022': TT_2022, 'TT_semilep_2022' : TT_semilep_2022, 'TT_hadr_2022' : TT_hadr_2022,
    ########## WJets
    "WJets_2022":WJets_2022,
    ########## ZJetsToNuNu
    "ZJetsToNuNu_2022":ZJetsToNuNu_2022, "ZJetsToNuNu_HT100to200_2022":ZJetsToNuNu_HT100to200_2022, 
    "ZJetsToNuNu_HT200to400_2022":ZJetsToNuNu_HT200to400_2022, "ZJetsToNuNu_HT400to800_2022":ZJetsToNuNu_HT400to800_2022, 
    "ZJetsToNuNu_HT800to1500_2022":ZJetsToNuNu_HT800to1500_2022, "ZJetsToNuNu_HT1500to2500_2022":ZJetsToNuNu_HT1500to2500_2022, 
    "ZJetsToNuNu_HT2500_2022":ZJetsToNuNu_HT2500_2022,

    ########## SIGNALS
    "TprimeToTZ_700_2022":TprimeToTZ_700_2022,
    "TprimeToTZ_1000_2022":TprimeToTZ_1000_2022,
    "TprimeToTZ_1800_2022":TprimeToTZ_1800_2022,

    #####################2022EE
    ############ QCD
    'QCD_2022EE' : QCD_2022EE,
    # "QCD_HT40to70_2022EE": QCD_HT40to70_2022EE, 
    "QCD_HT70to100_2022EE": QCD_HT70to100_2022EE, 
    "QCD_HT100to200_2022EE": QCD_HT100to200_2022EE, "QCD_HT200to400_2022EE": QCD_HT200to400_2022EE, 
    "QCD_HT400to600_2022EE": QCD_HT400to600_2022EE, "QCD_HT600to800_2022EE": QCD_HT600to800_2022EE, 
    "QCD_HT800to1000_2022EE": QCD_HT800to1000_2022EE, "QCD_HT1000to1200_2022EE": QCD_HT1000to1200_2022EE, 
    "QCD_HT1200to1500_2022EE": QCD_HT1200to1500_2022EE, "QCD_HT1500to2000_2022EE": QCD_HT1500to2000_2022EE, "QCD_HT2000_2022EE": QCD_HT2000_2022EE,
    ########### TT
    'TT_2022EE': TT_2022EE, 'TT_semilep_2022EE' : TT_semilep_2022EE, 'TT_hadr_2022EE' : TT_hadr_2022EE,
    ########## WJets
    "WJets_2022EE":WJets_2022EE,
    ########## ZJetsToNuNu
    "ZJetsToNuNu_2022EE":ZJetsToNuNu_2022EE, "ZJetsToNuNu_HT100to200_2022EE":ZJetsToNuNu_HT100to200_2022EE, 
    "ZJetsToNuNu_HT200to400_2022EE":ZJetsToNuNu_HT200to400_2022EE, "ZJetsToNuNu_HT400to800_2022EE":ZJetsToNuNu_HT400to800_2022EE, 
    "ZJetsToNuNu_HT800to1500_2022EE":ZJetsToNuNu_HT800to1500_2022EE, "ZJetsToNuNu_HT1500to2500_2022EE":ZJetsToNuNu_HT1500to2500_2022EE, 
    "ZJetsToNuNu_HT2500_2022EE":ZJetsToNuNu_HT2500_2022EE,

    ############################################# DATA 
    'DataJetMET_2022': DataJetMET_2022, 'DataJetMETC_2022':DataJetMETC_2022, 'DataJetMETD_2022':DataJetMETD_2022, 
    'DataJetMETE_2022':DataJetMETE_2022, 'DataJetMETF_2022':DataJetMETF_2022, 'DataJetMETG_2022':DataJetMETG_2022,

    "DataMuon_2022":DataMuon_2022, "DataMuonC_2022":DataMuonC_2022, "DataMuonD_2022":DataMuonD_2022, 
    "DataMuonE_2022":DataMuonE_2022, "DataMuonF_2022":DataMuonF_2022, "DataMuonG_2022":DataMuonG_2022,
    }
