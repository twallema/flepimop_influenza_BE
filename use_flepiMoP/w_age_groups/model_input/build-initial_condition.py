"""
generates a flepimop-compatible initial condition
drops one infected individual in Aarlen, NIS 81001
age group is determined ad random
"""

NIS_init = 81001

############################
## Load required packages ##
############################

import os
import random
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

# desired format: 'subpop', 'mc_age', 'mc_infection_stage' (=disease states), 'amount'
subpops = data.index.get_level_values('NIS').unique()
ages = data.index.get_level_values('age').unique()
ages_desired = ['0-5', '5-15', '15-65', '65+']
mc_infection_stages = ['S', 'I', 'R']
idx = pd.MultiIndex.from_product([subpops, ages_desired, mc_infection_stages], names=['subpop', 'mc_age', 'mc_infection_stage'])
new_data = pd.Series(0, index=idx, name='amount')

# loop over subpop/age combinations in original dataframe and use these data to fill in the susceptibles
for subpop in subpops:
    for age,age_desired in zip(ages, ages_desired):
        new_data.loc[subpop, age_desired, 'S'] = data.loc[subpop, age].values

# place the initial infected in Aarlen (random age group)
new_data.loc[NIS_init, random.choice(ages_desired), 'I'] = 1

##########
## save ##
##########

new_data.to_csv('initial_condition.csv')