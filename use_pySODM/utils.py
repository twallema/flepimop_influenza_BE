"""
This script contains usefull functions for the pySODM-based Belgian Influenza model
"""

__author__      = "Tijs Alleman"
__copyright__   = "Copyright (c) 2024 by T.W. Alleman, IDD Group, Johns Hopkins Bloomberg School of Public Health. All Rights Reserved."

import os
import numpy as np
import pandas as pd

def name2NIS(name):
    """ A function to convert a Belgian municipality name into a NIS code
    """
    # load NIS/name list 
    rel_dir = '../data/interim/census_2011/demography_municipalities_2011_sorted.csv'
    data = pd.read_csv(os.path.join(os.getcwd(),rel_dir))[['NIS','name']]
    # check if name is valid
    if name not in data['name'].values:
        raise ValueError(
            f"name '{name}' is not a valid Belgian municipality name"
        )
    # return NIS code 
    return data['NIS'][data['name'] == name].values[0]

import random
def construct_initial_infected(loc='random', n=1, agedist='demographic'):
    """ A function returning the initial number of infected per municipality and age group

    input
    -----
    loc: str
        Location of initial infected. Either 'random' or a valid Belgian municipality name.
    
    n: int/float
        The number of infected dividuals present in the select location. 
    
    agedist: str
        The distribution of the initial number of infected over the model's age groups. Either 'uniform', 'random' or 'demographic'.
    
    output
    ------
    I0: np.ndarray
        Initial number of infected per municipality and age group. Shape (4, 581). 
    """

    # load 2017 demography
    rel_dir = '../data/interim/demography/demography_municipalities_2017.csv'
    demography = pd.read_csv(os.path.join(os.getcwd(),rel_dir))

    # select a spatial patch
    if loc == 'random':
        init_NIS = random.choice(demography['NIS'].unique().values)
    else:
        init_NIS = name2NIS(loc)

    # distribute over age groups
    demography_NIS = demography[demography['NIS'] == init_NIS]['population'].values
    if agedist == 'demographic':
        agedist_n = np.random.multinomial(n, demography_NIS / sum(demography_NIS))
    elif agedist == 'uniform':
        agedist_n = n/len(demography_NIS) * np.ones(len(demography_NIS))
    elif agedist == 'random':
        agedist_n = np.zeros(len(demography_NIS))
        agedist_n[random.randint(0, len(demography_NIS)-1)] = n
    else:
        raise ValueError(
            f"invalid input {agedist} for input argument 'agedist' "
        )

    # build initial infected
    I0 = demography.set_index(['NIS', 'age'])
    I0['population'] = 0.0
    I0.loc[(init_NIS, slice(None)), 'population'] = agedist_n

    # convert to numpy array
    n_age = len(demography['age'].unique())
    n_NIS = len(demography['NIS'].unique())

    return np.transpose(I0.values.reshape(n_NIS, n_age))

def construct_initial_susceptible(I0):
    """ A function to construct the initial number of susceptible individuals
    """
    # load 2017 demography
    rel_dir = '../data/interim/demography/demography_municipalities_2017.csv'
    demography = pd.read_csv(os.path.join(os.getcwd(),rel_dir))

    # convert to numpy array
    n_age = len(demography['age'].unique())
    n_NIS = len(demography['NIS'].unique())
    S0 = demography.set_index(['NIS', 'age'])
    S0 = np.transpose(S0.values.reshape(n_NIS, n_age))

    # subtract initial infected
    S0 = S0 - I0

    return S0

def get_mobility_matrix():
    """ A function to extract the mobility matrix and normalise it with the size of the active population
    """
    # get data and convert to np.array
    rel_dir = '../data/interim/census_2011/mobility_municipalities_2011_sorted.csv'
    mobility = pd.read_csv(os.path.join(os.getcwd(),rel_dir), index_col=0).values

    # get 2011 demography and normalise
    # From overall BE demography 2011 --> 54% of population is between 20-60 years old
    # TODO: technically you should do this at the municipality level
    rel_dir = '../data/interim/census_2011/demography_municipalities_2011_sorted.csv'
    demography = pd.read_csv(os.path.join(os.getcwd(),rel_dir), index_col=0)['inhabitants'].values

    return mobility / demography[:, None] / 0.54

def get_contact_matrix():
    rel_dir = '../data/raw/contacts/belgium_2010_all.xlsx'
    contacts = pd.read_excel(os.path.join(os.getcwd(),rel_dir), sheet_name='integrated', index_col=0, header=0)
    return contacts.values

def construct_coordinates_dictionary():
    """A function returning the model's coordinates
    """
    coordinates = {'age': ['0-5', '5-15', '15-65', '65+'],
                   'location': list(pd.read_csv(os.path.join(os.getcwd(),'../data/interim/census_2011/demography_municipalities_2011_sorted.csv'))['NIS'].values)
                    }
    return coordinates