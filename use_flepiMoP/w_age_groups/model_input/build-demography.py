"""
generates a flepimop-compatible demography file
"""

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

data = data.groupby(by='NIS').sum()
data.index.names = ['subpop']

##########
## save ##
##########

data.to_csv('demography.csv')