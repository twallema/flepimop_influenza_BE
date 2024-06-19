############################
## Load required packages ##
############################

import os
import numpy as np
import pandas as pd

###############
## Load data ##
###############

# vaccine coverage dataset will have same format as demography dataset (NIS + age groups)
rel_dir = '../interim/demography/demography_municipalities_2017.csv'
data_dir = os.path.join(os.getcwd(),rel_dir)
data = pd.read_csv(data_dir)
data = data.set_index(['NIS', 'age'])

#################
## Format data ##
#################

## Vaccine coverages per region
# from demography BE Jan 1, 2018: age group 65+ --> 84.9% 65-85 versus 15.1% 85+

# raw data: 0-5, 5-15, 15-65, 65-85, 85+ 
# source: data/raw/literature/antoine_etal_archpublichealth_2010.pdf (Table 1)
vaccine_coverage = {
    'Flanders': [0.011, 0.015, 0.079, 0.249, 0.443],
    'Wallonia': [0.002, 0.003, 0.011, 0.039, 0.072],
    'Brussels': [0.002, 0.003, 0.014, 0.052, 0.098],
}
# interim data: 0-5, 5-15, 15-65, 65+
vaccine_coverage = {
    'Flanders': [0.011, 0.015, 0.079, 0.278],
    'Wallonia': [0.002, 0.003, 0.011, 0.043],
    'Brussels': [0.002, 0.003, 0.014, 0.059],
}

## Loop over municipality NIS codes, determine region, fill in vaccination coverage
for NIS in data.index.get_level_values('NIS').unique():
    # determine region
    NIS = str(NIS)
    if NIS[0] in ['1', '3', '4', '7']:
        region = 'Flanders'
    elif NIS[0] in ['5', '6', '8', '9']:
        region = 'Wallonia'
    elif NIS[0] == '2':
        if NIS[1] == '1':
            region = 'Brussels'
        elif NIS[1] in ['3', '4']:
            region = 'Flanders'
        elif NIS[1] == '5':
            region = 'Wallonia'
    # fill in vaccine coverage
    data.loc[int(NIS), slice(None)] = vaccine_coverage[region]

#################
## Save result ##
#################

data.to_csv(os.path.join(os.getcwd(),'../interim/vaccination/vaccination_municipalities_2010.csv'))
