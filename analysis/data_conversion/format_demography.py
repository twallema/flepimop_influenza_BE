############################
## Load required packages ##
############################

import os
import pandas as pd

###############
## Load data ##
###############

rel_dir = '../../data/raw/demography/TF_SOC_POP_STRUCT_2017.xlsx'
data_dir = os.path.join(os.getcwd(),rel_dir)
data = pd.read_excel(data_dir)

#################
## Format data ##
#################

# add a column with desired age groups
desired_age_groups = pd.IntervalIndex.from_tuples([(0,5),(5,15),(15,65),(65,120)],closed='left')
data['age_group'] = pd.cut(data['CD_AGE'], bins=desired_age_groups)

# groupby NIS and age bin, sum over population
grouped = data.groupby(['CD_MUNTY_REFNIS', 'age_group'], observed=False)['MS_POPULATION'].sum().reset_index()

# rename index
grouped.columns = ['NIS', 'age', 'population']

# perform 2019 fusions (https://statbel.fgov.be/nl/over-statbel/methodologie/classificaties/geografie)

# 'Meeuwen-Gruitrode' (72040) + 'Opglabeek' (71047) --> 'Oudsbergen' (72042) 
# 'Neerpelt' (72025) + 'Overpelt' (72029) --> 'Pelt' (72043)
# 'Kruishoutem' (45017) + 'Zingem' (45057) --> 'Kruisem' (45068)
# 'Aalter' (44001) + 'Knesselare' (44029) --> 'Aalter' (44084)
# 'Deinze' (44011) + 'Nevele' (44049) --> 'Deinze' (44083)
# 'Puurs' (12030) + 'Sint-Amands' (12034) --> 'Puurs-Sint-Amands' (12041)
# 'Waarschoot' (44072) + 'Lovendegem' (44036) + 'Zomergem' (44080) --> 'Lievegem' (44085)

old_codes = [
    [72040, 71047],
    [72025, 72029],
    [45017, 45057],
    [44001, 44029],
    [44011, 44049],
    [12030, 12034],
    [44072, 44036, 44080]
]
new_codes = [72042, 72043, 45068, 44084, 44083, 12041, 44085]

for old,new in zip(old_codes, new_codes):
    # filter rows
    to_merge = grouped[grouped['NIS'].isin(old)]
    # sum
    merged_sum = to_merge.groupby('age', observed=False)['population'].sum().reset_index()
    # change area code 
    merged_sum['NIS'] = new
    # remove old area codes from data
    grouped = grouped[~grouped['NIS'].isin(old)]
    # merge new area code in data
    grouped = pd.concat([grouped, merged_sum], ignore_index=True)

# perform 2019 code alterations

old_codes = [55022, 56011, 56085, 56087, 52063, 52043, 55010, 55039, 55023, 54007, 54010]
new_codes = [58001, 58002, 58003, 58004, 55085, 55086, 51067, 51068, 51069, 57096, 57097]
grouped['NIS'] = grouped['NIS'].replace(dict(zip(old_codes, new_codes)))

# sort index
grouped.sort_values(by='NIS', inplace=True)

# set index
grouped.set_index(['NIS', 'age'], inplace=True)

print(f'Dataset contains data for {len(grouped.index.get_level_values('NIS').unique())} municipalities.')

#################
## Save result ##
#################

grouped.to_csv(os.path.join(os.getcwd(),'../../data/interim/demography/demography_municipalities_2017.csv'))
