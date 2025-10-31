import os
import optparse
import sys
import time
import json
# from samples.samples import *
# from get_file_fromdas import *
# samples
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


usage = "python3 general_h5_submitter.py"
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

#file_name = "update_trainingSet_mp"
file_name = "update_trainingSet_mp_components"
#file_name = "training_Run3_PF_jets_preprocessing_components_new_structure"
def sub_writer(file_name):
    f = open(f"condor_{file_name}.sub", "w")
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
    f.write("+JobFlavour             = \"workday\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write("executable              = runner_"+file_name+".sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = condor/output/"+file_name+".out\n")
    f.write("error                   = condor/error/"+file_name+".err\n")
    f.write("log                     = condor/log/"+file_name+".log\n")
    f.write("queue\n")


def sh_writer(file_name):
    f = open(f"runner_{file_name}.sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/f/fsalerno/CMSSW_13_2_11/src/PhysicsTools/NanoAODTools/python/postprocessing/machine_learning/Training/\n")
    f.write("cmsenv\n")
    f.write("export XRD_NETWORKSTACK=IPv4\n")
    f.write(f"python3 {file_name}.py\n")

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



sh_writer(file_name)    
sub_writer(file_name)
if not dryrun:
    os.popen(f'condor_submit condor_{file_name}.sub')
time.sleep(2)



