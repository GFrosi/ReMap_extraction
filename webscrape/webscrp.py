from csv import list_dialects
import requests
import pandas as pd
from tqdm import tqdm
from time import sleep
from retry import retry


def get_specie_series(taxid):
    """Receives a taxid to build
    the url and returns a json
    file"""

    url = "http://remap.univ-amu.fr/api/v1/list/experiments/taxid="+str(taxid)
    dict_data = requests.get(url).json() #inbuilt json() constructor for requests.get() method (dict)
    return dict_data


def get_list_experiment(taxid):
    """Receives a dict and returns a
    list with GSEs (experiments from
    GEO database)"""

    dict_data = get_specie_series(taxid)
        
    #accessing each experiment (sample) related with Hs. For each sample, there is a related ID (accession) to be used in the next API
    list_gse = [sample["accession"] for sample in dict_data["experiments"] if "GSE" in sample["accession"]] 
    
    return list_gse

@retry(TimeoutError, tries=5, delay=3)
def get_samples_series(list_gse, taxid):
    '''Receives a list of GSEs and a taxid,
    and returns a master dict. Each key is
    a experiment and the values are a list
    of related samples for each one'''

    dict_master = {}

    for gse in tqdm(list_gse):
        url = "http://remap.univ-amu.fr/api/v1/datasets/findByExperiment/experiment="+str(gse)+"&taxid="+str(taxid) #ok
        gse_data = requests.get(url).json()
        sleep(2)
        dict_master[gse_data["experiment"]] = gse_data["datasets"]

    return dict_master


def dict_to_list_of_list(dict_master):
    """Receives a dict master
    and return a list of lists
    """

    list_df = []

    for k,v in dict_master.items():
        for ele in v:
            
            list_sub = []
            list_sub.append(k)
            list_sub.append(ele['dataset_name'])
            list_sub.append(ele['target_name'])
            list_sub.append(ele['biotype_name'])
            list_sub.append(ele['biotype_modification'])
            list_sub.append(ele['dataset_source'])
            list_sub.append(ele['bed_url'])
            list_df.append(list_sub)
            list_sub = []
    
    return list_df


def create_df(list_df):
    '''Receives a list
    of lists and returns
    a df'''

    df = pd.DataFrame(list_df, columns = ['GSE', 'dataset_name', 'target_name', 'biotype_name', 'biotype_modification', 'dataset_source', 'bed_url'])
    
    return df












    
    
