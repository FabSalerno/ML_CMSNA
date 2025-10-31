import os
import optparse
import sys
import time
import json
# from samples.samples import *
# from get_file_fromdas import *
# samples
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


usage = "python3 trainingSet_PF_submitter.py"
parser = optparse.OptionParser(usage)
# parser.add_option('-d', '--dryrun', dest='dryrun', default=True, action='store_false', help='Default do not run')
parser.add_option('-d', '--dryrun',
                  dest='dryrun',
                  default=False, 
                  action='store_true',
                  help='Default do not run')
#parser.add_option('-u', '--user', dest='us', type='string', default = 'ade', help="")
(opt, args) = parser.parse_args()
#Insert here your uid... you can see it typing echo $uid

dryrun = opt.dryrun

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
if username == 'adeiorio':
    uid = 103214
elif username == 'acagnott':
    uid = 140541
elif username == 'lfavilla':
    uid = 159320
elif username == 'fsalerno':
    uid = 171405


def sub_writer(component,n_PFCs,pt_cut,boost):
    f = open(f"condor_{component}_{n_PFCs}_{pt_cut}_boosted_{boost}.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    f.write("should_transfer_files   = YES\n")
    f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    #f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    #f.write('requirements            = (TARGET.OpSysAndVer =?= "CentOS7")\n')
    # make sure it has at least 4 cpus.
    #f.write("requirements            = Cpus >= 64\n")
    # Request up to 8 cpus out of a partitionable slot.
    #f.write("request_cpus = Cpus > 8 ? 8 : Cpus")
    f.write("+JobFlavour             = \"testmatch\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write(f"executable             = runner_{component}_{n_PFCs}_{pt_cut}_boosted_{boost}.sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write(f"output                 = condor/output/{component}_{n_PFCs}_{pt_cut}_boosted_{boost}.out\n")
    f.write(f"error                  = condor/error/{component}_{n_PFCs}_{pt_cut}_boosted_{boost}.err\n")
    f.write(f"log                    = condor/log/{component}_{n_PFCs}_{pt_cut}_boosted_{boost}.log\n")
    f.write("queue\n")


def sh_writer(year, component, n_PFCs, pt_cut, inFile_to_open, nev, path_to_h5, select_top_over_threshold, thr, boost):
    f = open(f"runner_{component}_{n_PFCs}_{pt_cut}_boosted_{boost}.sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/GNNs\n")
    f.write("cmsenv\n")
    f.write("export XRD_NETWORKSTACK=IPv4\n")
    if select_top_over_threshold:
        f.write(f"python3 trainingSet_PF_prova_graph.py -year {year} -component {component} -inFile_to_open {inFile_to_open} -nev {nev} -path_to_h5 {path_to_h5} -select_top_over_threshold -thr {thr} -n {n_PFCs} -pt {pt_cut}\n")
    else:
        f.write(f"python3 trainingSet_PF_prova_graph.py -year {year} -component {component} -inFile_to_open {inFile_to_open} -nev {nev} -path_to_h5 {path_to_h5} -n {n_PFCs} -pt {pt_cut}\n")

if not os.path.exists("condor/output"):
    os.makedirs("condor/output")
if not os.path.exists("condor/error"):
    os.makedirs("condor/error")
if not os.path.exists("condor/log"):
    os.makedirs("condor/log")
if(uid == 0):
    print("Please insert your uid")
    exit()
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

######## LAUNCH CONDOR ########
n_PFCs=150  #number of PFCs 
pt_cut=0 #only top with pt>pt_cut are selected
boost=False
year                        = 2022
#path_to_txt_folder          = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_5_2/src/PhysicsTools/NanoAODTools/crab/macros/files"
path_to_txt_folder          = "/afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/crab/macros/files"
nev                         = 10000 #da problemi con e
verbose                     = False
select_top_over_threshold   = False
# thr                         = 0.4 # 2018 threshold on score_base (fpr=10%)
thr                         = 0.0
if year==2018:
    # path_to_training_folder = "/eos/user/l/lfavilla/my_framework/MLstudies/Training_2"
    path_to_training_folder = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_standard"
    #path_to_training_folder = "/eos/user/g/gmilella/ttX_ntuplizer/test_tt_semilepton.root"
elif year==2022:
    path_to_training_folder = f"/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/GNN/{n_PFCs}_PFCs_boosted_{boost}"
path_to_h5_folder          = "{}/h5s".format(path_to_training_folder)

if not os.path.exists(path_to_training_folder):
    os.makedirs(path_to_training_folder)
if not os.path.exists(path_to_h5_folder):
    os.makedirs(path_to_h5_folder)

if year==2018:
    datasets = [
            #"QCD_HTInf_2018"
            #"QCD_HT2000_2018"
            #"QCD_HT1500_2018"
            #"QCD_HT1000_2018"
            #"TT_Mtt700to1000_2018",
            #"TT_semilep_2018",  
            #"TT_Mtt1000toInf_2018",
            #"TT_2018",
            #"QCD_2018",
            #"ZJetsToNuNu_2018",
            #"WJets_2018",
            #"TprimeToTZ_700_2018",
            #"TprimeToTZ_1000_2018",
            #"TprimeToTZ_1800_2018",
            ]
elif year==2022:
    datasets = [
             "TT_inclusive_MC2022",
             #"TT_Mtt_700_1000_MC2022",
             #"TT_Mtt_1000_inf_MC2022",
             #"TTZprimetoTT_M_3000_W_4_MC2022",
             "TT_hadronic_MC2022",
             "TT_semilep_MC2022",
            #"QCD_HT_400_600_MC2022",
            #"QCD_HT_600_800_MC2022",
            #"QCD_HT_800_1000_MC2022",
            #"QCD_HT_1000_1200_MC2022",
            #"QCD_HT_1200_1500_MC2022",
            #"QCD_HT_1500_2000_MC2022",
            #"QCD_HT_2000_inf_MC2022",
            #"Z_nunu_400_800_MC2022",
            #"Z_nunu_800_1500_MC2022",
            #"Z_nunu_1500_2500_MC2022",
            #"Z_nunu_2500_inf_MC2022",
            # "WJets_MC2022",
            # "TprimeToTZ_700_MC2022",
            # "TprimeToTZ_1000_MC2022",
            # "TprimeToTZ_1800_MC2022",
    
            # 
           
            # "QCD_HT2000_MC2022",
            ]


for dat in datasets:
    path_to_h5             = "{}/trainingSet_{}.h5".format(path_to_h5_folder,dat)
    print(dat, path_to_h5)


    sh_writer(year=year,
              component=dat,
              inFile_to_open=f"/eos/user/f/fsalerno/Data/PF/topcand_new_truth/nano_mcRun3_{dat}_topcand_PF.root",
              nev=nev,
              path_to_h5=path_to_h5,
              select_top_over_threshold=select_top_over_threshold,
              thr=thr, 
              n_PFCs= n_PFCs,
              pt_cut=pt_cut,
              boost= boost  
              )
    sub_writer(component=dat, n_PFCs=n_PFCs, pt_cut=pt_cut, boost=boost)
    if not dryrun:
        os.popen(f"condor_submit condor_{dat}_{n_PFCs}_{pt_cut}_boosted_{boost}.sub")
    time.sleep(2)



