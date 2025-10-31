import os
import optparse
import sys
import time
import json
# from samples.samples import *
# from get_file_fromdas import *



usage = "python3 training_Run3_PF_submitter.py"
parser = optparse.OptionParser(usage)
# parser.add_option('-d', '--dryrun', dest='dryrun', default=True, action='store_false', help='Default do not run')
parser.add_option('-d', '--dryrun',
                  dest='dryrun',
                  default=False, 
                  action='store_true',
                  help='Default do not run')
#parser.add_option('-u', '--user', dest='us', type='string', default = 'ade', help="")
(opt, args) = parser.parse_args()
dryrun      = opt.dryrun

#Insert here your uid... you can see it typing echo $uid
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


def sub_writer(file_name,nPFCs,model,cut):
    f = open(f"condor_{file_name}_{nPFCs}_{model}_{cut}.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    f.write("should_transfer_files   = YES\n")
    f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    f.write("environment             = \"SCRAM_ARCH=el9_amd64_gcc11\"\n")
    #f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    f.write("+JobFlavour             = \"nextweek\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write(f"executable              = runner_{file_name}_{nPFCs}_{model}_{cut}.sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write(f"output                  = condor/output/{file_name}_{nPFCs}_{model}_{cut}.out\n")
    f.write(f"error                   = condor/error/{file_name}_{nPFCs}_{model}_{cut}.err\n")
    f.write(f"log                     = condor/log/{file_name}_{nPFCs}_{model}_{cut}.log\n")
    f.write("queue")



def sh_writer(file_name, samples, training_set, model_path, outJson_path, graphics_path, nPFCs, model, doCut, cut):
    f = open(f"runner_{file_name}_{nPFCs}_{model}_{cut}.sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/\n")
    f.write("cmsenv\n")
    f.write("export XRD_NETWORKSTACK=IPv4\n")
    f.write(f"python3 {file_name}_{model}.py -s {samples} -i {training_set} -m {model_path} -j {outJson_path} -g {graphics_path} -n {nPFCs} -d {doCut} -c {cut} \n")


if not os.path.exists("condor/output"):
    os.makedirs("condor/output")
if not os.path.exists("condor/error"):
    os.makedirs("condor/error")
if not os.path.exists("condor/log"):
    os.makedirs("condor/log")
if(uid==0):
    print("Please insert your uid")
    exit()
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")




###### Launcher ######
#file_name  = "training_Run3_PF_jets"
nPFCs = 60
file_name  ="training_Run3_PF_jets"
model = "fine_tuning_CNN_2D_LSTM"
doCut = False
cut = 0
# CNN, CNN_2D, CNN_2D_LSTM, LSTM

year = 2022

if year==2018:
    components = [
        'QCD_HT1000_2018', 
        'QCD_HT1500_2018', 
        'QCD_HT2000_2018', 
        'QCD_HTInf_2018', 
        'TT_Mtt1000toInf_2018', 
        'TT_Mtt700to1000_2018', 
        'TT_semilep_2018',
        #"TprimeBToTZ_M1200_2018", 
        #"TprimeBToTZ_M1800_2018", 
        #"TprimeBToTZ_M800_2018", 
        #"ZJetsToNuNu_HT1200To2500_2018", 
        #"ZJetsToNuNu_HT200To400_2018", 
        #"ZJetsToNuNu_HT2500ToInf_2018", 
        #"ZJetsToNuNu_HT400To600_2018", 
        #"ZJetsToNuNu_HT800To1200_2018", 
        #"tDM_Mphi1000_2018", 
        #"tDM_Mphi500_2018", 
        #"tDM_Mphi50_2018"
        ]
    
if year==2022:
    components = [
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
samples         = ','.join(components)

######## Run3, phase 1 & 2 ########
phase               = 3  ##!!!!!ATTENZIONE ALLA FASE!!!!!
if phase == 1:
    training_set    = "/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_60_boosted_0_pt/trainingSet.h5"
    model_path      = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_{nPFCs}_boosted_{cut}_pt/Training_PF_2022_1_jets_{nPFCs}_boosted_{model}_{cut}_pt_full/model.h5"
    outJson_path    = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_{nPFCs}_boosted_{cut}_pt/Training_PF_2022_1_jets_{nPFCs}_boosted_{model}_{cut}_pt_full/score_thresholds_{nPFCs}_{model}_{cut}_pt.json"
    graphics_path   = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_{nPFCs}_boosted_{cut}_pt/Training_PF_2022_1_jets_{nPFCs}_boosted_{model}_{cut}_pt_full/graphics"
elif phase == 2:
    training_set    = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2/Training_PF_2022_2_jets_60_boosted_CNN_2D_LSTM_0_pt/trainingSet.h5"
    model_path      = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2/Training_PF_2022_2_jets_{nPFCs}_boosted_{model}_{cut}_pt/model.h5"
    outJson_path    = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2/Training_PF_2022_2_jets_{nPFCs}_boosted_{model}_{cut}_pt/score_thresholds_{nPFCs}_{model}_{cut}_pt.json"
    graphics_path   = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2/Training_PF_2022_2_jets_{nPFCs}_boosted_{model}_{cut}_pt/graphics"
elif phase == 3:
    training_set    = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2/Training_PF_2022_2_jets_60_boosted_CNN_2D_LSTM_0_pt/trainingSet.h5"
    model_path      = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_fine_tuning/Training_PF_2022_fine_tuning_jets_{nPFCs}_boosted_{model}_{cut}_pt/model.h5"
    outJson_path    = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_fine_tuning/Training_PF_2022_fine_tuning_jets_{nPFCs}_boosted_{model}_{cut}_pt/score_thresholds_{nPFCs}_{model}_{cut}_pt.json"
    graphics_path   = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_fine_tuning/Training_PF_2022_fine_tuning_jets_{nPFCs}_boosted_{model}_{cut}_pt/graphics"
sh_writer(file_name, samples, training_set, model_path, outJson_path, graphics_path,nPFCs,model,doCut, cut)    
sub_writer(file_name,nPFCs,model,cut)
if not dryrun:
    os.popen(f'condor_submit condor_{file_name}_{nPFCs}_{model}_{cut}.sub')
time.sleep(2)
    



