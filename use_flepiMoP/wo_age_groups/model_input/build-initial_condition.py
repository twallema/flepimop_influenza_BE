"""
generates a flepimop-compatible initial condition
drops one infected individual in Aarlen, NIS 81001
"""

NIS_init = 81001 # Arlon # TODO: give NIS and method as script inputs

############################
## Load required packages ##
############################

import os
import pandas as pd

###############
## Load data ##
###############

rel_dir = '../../../data/interim/demography/demography_municipalities_2017.csv'
data_dir = os.path.join(os.getcwd(),rel_dir)
data = pd.read_csv(data_dir, index_col=[0,1])

##########################################
## Convert to a flepi-compatible format ##
##########################################

# desired format: 'subpop', 'mc_infection_stage' (=disease states), 'amount'
subpops = data.index.get_level_values('NIS').unique()
ages = data.index.get_level_values('age').unique()
mc_infection_stages = ['S', 'I', 'R']
idx = pd.MultiIndex.from_product([subpops, ages, mc_infection_stages], names=['subpop', 'age', 'mc_infection_stage'])
new_data = pd.Series(0, index=idx, name='amount')

# loop over subpop/age combinations in original dataframe and use these data to fill in the susceptibles
for subpop in subpops:
    for age in ages:
        new_data.loc[subpop, age, 'S'] = data.loc[subpop, age].values

# aggregate age groups
new_data = new_data.groupby(by=['subpop', 'mc_infection_stage']).sum()

# place the initial infected in NIS_init
new_data.loc[NIS_init, 'I'] = 1

##########
## save ##
##########

new_data.to_csv('initial_condition.csv')