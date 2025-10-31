import os
from samples_PF import *

def get_files_string(dataset):
    username = str(os.environ.get('USER'))
    inituser = str(os.environ.get('USER')[0])
    if username == 'adeiorio':
        uid = 103214
    elif username == 'acagnott':
        uid = 140541
    elif username == 'fscrivan':
        uid=172801
    elif username == 'fsalerno':
        uid = 171405

    if not hasattr(dataset, "dataset"): 
        return "ERROR: a sample with dataset method is required"
    else:
        if not os.path.exists("/tmp/x509up_u" + str(uid)):
            os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
            os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")
            
        os.popen("export XRD_NETWORKSTACK=IPv4")
        command = 'dasgoclient -query="file dataset='+dataset.dataset+' instance=prod/phys03"'
        out_stream = os.popen(command)
        files_string = out_stream.read()
        out_stream.close()
        return files_string.split('\n')
