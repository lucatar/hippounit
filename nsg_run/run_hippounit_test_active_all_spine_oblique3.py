import json
import collections
import pkg_resources
import numpy
import os
from neuron import h
import sys

def run_test(ind_and_params):

    import quantities
    from quantities import mV, nA
    import json
    import collections
    import multiprocessing
    import numpy
    import os

    import sys
    #sys.path.append("./hippounit")
    #sys.path.append('/home/saray/hippounit_Spine_project_20221019/hippounit/')
    import hippounit
    from hippounit import tests
    from hippounit.utils_50Ra_Luca_nmda import ModelLoader_Modellke, ModelLoader_synapse_on_Existing_Spine
    
    ind, parameters = ind_and_params
    print(ind, parameters)

    """**************"""

    """ SET UP MODEL """
    """***************"""

    # path to mod files
    """Edit the line below"""
    mod_files_path = "./model/mechanisms/"

    # user function path
    """Edit the line below"""
    user_function_path = './usr_fun_model_full_rework7_for_allspine.txt'

    #Load cell model
    model = ModelLoader_synapse_on_Existing_Spine(mod_files_path = mod_files_path, user_function_path = user_function_path)  # Change this to existing spines later

    # path to hoc file
    # the model must not display any GUI!!
    """Edit the line below"""
    model.hocpath = "./model/load_model_na_inhomo_minimal_model_full_soma_all_spine_true_diam_active_spine_KA_fact_50Ra_inject.hoc" 

    # If the hoc file doesn't contain a template, this must be None (the default value is None)
    model.template_name = None

    # model.SomaSecList_name should be None, if there is no Section List in the model for the soma, or if the name of the soma section is given by setting model.soma (the default value is None)
    model.SomaSecList_name = None
    # if the soma is not in a section list or to use a specific somatic section, add its name here:
    model.soma = 'soma'

    # For the PSP Attenuation Test, and Back-propagating AP Test a section list containing the trunk sections is needed
    model.TrunkSecList_name = 'trunk'
    model.TuftSecList_name = 'tuft'
    # For the Oblique Integration Test a section list containing the oblique dendritic sections is needed
    model.ObliqueSecList_name = 'oblique_dendrites'

    model.BasalSecList_name = 'basal_dendrites'

    # It is important to set the v_init and the celsius parameters of the simulations here,
    # as if they are only set in the model's files, they will be overwritten with the default values of the ModelLoader class.
    # default values: v_init = -70, celsius = 34 
    model.v_init = -70
    model.celsius = 33

    model.c_step_start = 0.000004
    model.c_step_stop = 0.0000004
    model.c_minmax = numpy.array([0.000004, 0.004])
    
    model.parameters = parameters
    
    # outputs will be saved in folders named like this:
    """Edit the line below"""
    model.name="ca1_pc_"+str(ind)


    """*********"""

    """ RUN TEST """
    """*********"""


    #all the outputs will be saved here. It will be an argument to the test.
    """Edit the line below"""
    base_directory = './Active_all_spine_inject_strict/'

    # Load target data
    """Edit the line below"""
    with open('./target_features/oblique_target_data.json') as f:
        observation = json.load(f, object_pairs_hook=collections.OrderedDict)

    # Instantiate the test class
    test = tests.ObliqueIntegrationTest3(observation = observation, save_all = True, force_run_synapse=False, force_run_bin_search=False, show_plot = False, base_directory = base_directory)

    # Number of parallel processes
    test.npool = multiprocessing.cpu_count()
    
    if numpy.isnan(parameters[0]):
        print('Parameters are nan')
        pass
    else:
        try:
            #Run the test 
            score = test.judge(model)
            #Summarize and print the score achieved by the model on the test using SciUnit's summarize function
            score.summarize()

        except Exception as e:
            print('Model: ' + model.name + ' could not be run')
            print(e)
            pass


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
  
if __name__ == '__main__':

    all_ind_and_params = create_params_list()
    i=int(sys.argv[1])
    run_test(all_ind_and_params[i])
        
   
   

