"""
generates a flepimop-compatible mobility file
"""

############################
## Load required packages ##
############################

import os
import pandas as pd

###############
## Load data ##
###############

rel_dir = '../../../data/interim/census_2011/mobility_municipalities_2011_sorted.csv'
data_dir = os.path.join(os.getcwd(),rel_dir)
data = pd.read_csv(data_dir, index_col=0)

##########################################
## Convert to a flepi-compatible format ##
##########################################

# desired format: 'ori' (NIS), 'dest' (NIS), 'amount'
spatial_units = data.index.unique()
idx = pd.MultiIndex.from_product([spatial_units,spatial_units], names=['ori', 'dest'])
new_data = pd.Series(0.0, index=idx, name='amount')

# loop over NIS codes and fill in
for su in spatial_units:
    new_data.loc[su, slice(None)] = data.loc[su].values

# flepimop does not accept diagonal elements in the mobility data
new_data = new_data.reset_index()
for su in spatial_units:
    new_data = new_data.drop(new_data[((new_data["ori"] == su) & (new_data["dest"] == su))].index.values)

##########
## save ##
##########

new_data.to_csv('mobility.csv')