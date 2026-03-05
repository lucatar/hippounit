import json
import collections
import pkg_resources
import numpy
import ipyparallel as ipp
import os
from neuron import h
from ipyparallel.controller.heartmonitor import HeartMonitor




def create_params_list():

    """Edit the line below"""
    f = open('./last.csv')
    lines = []
    for l in f.readlines():
        #print l.strip().split(',')
        lines.append(l.strip().split(','))
    f.close()
    
    all_ind_and_params = []

    for i in range(1, len(lines)):
        parameters = [float(j) for j in lines[i]]
        #lines[i].pop(0)
        parameters.pop(0)
        #print(parameters)
        
        all_ind_and_params.append((i, parameters))
        
    return all_ind_and_params
    

def main(i):
    import os

    os.system('python3 run_hippounit_test_active_all_spine_pathway.py ' + str(i))
  
if __name__ == '__main__':


    """start cluster here - should be removed when run on NSG"""
    #os.system("ipcluster start -n 2 --debug &")

    mod_files_path = "./model/mechanisms/"
    #default_NMDA_path = pkg_resources.resource_filename("hippounit", "tests/default_NMDAr/")

    #os.system("cd " + "\'" + mod_files_path + "\'" + "; nrnivmodl")
    
    #os.system("cd " + "\'" + default_NMDA_path  + "\'" + "; nrnivmodl")

    all_ind_and_params = create_params_list()
    #print(all_ind_and_params)
    
    
    """
    HeartMonitor.period = 60000 # ping every minute
    c = ipp.Client(profile=os.getenv('IPYTHON_PROFILE'), timeout=1000)
    v=c[:]
    v.map_sync(run_test, all_ind_and_params)
    #v.map_sync(print_params, all_ind_and_params)
    """

    """I used this for HBP models"""
   
    c = ipp.Client(profile=os.getenv('IPYTHON_PROFILE'), timeout = 1000, debug = True)

    #HeartMonitor.period = 60000 # ping every minute
    #HeartMonitor.max_heartmonitor_misses = 60 #720 # allow 12 hours of interruption before considering an engine gone

    lview=c.load_balanced_view()
    #results=lview.map(run_test, all_ind_and_params)
    #results=lview.map_sync(run_test, all_ind_and_params)
    #results=lview.map_async(run_test, all_ind_and_params)
    lview.map_sync(main, range(0, len(all_ind_and_params)))
   
    """stop cluster here - should be removed when run on NSG"""
    #os.system("ipcluster stop")

    #run_test(all_ind_and_params[0])
   
   

