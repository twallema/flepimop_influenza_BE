"""
This script simulates an age-stratified, spatially-explicit SIR model for Belgium using pySODM
"""

__author__      = "Tijs Alleman"
__copyright__   = "Copyright (c) 2024 by T.W. Alleman, IDD Group, Johns Hopkins Bloomberg School of Public Health. All Rights Reserved."

import numpy as np
import matplotlib.pyplot as plt

from utils import name2NIS, \
                    construct_initial_infected, \
                        construct_coordinates_dictionary, \
                            construct_initial_susceptible, \
                                get_contact_matrix, get_mobility_matrix

# coordinates
coordinates = construct_coordinates_dictionary()
# parameters
params = {'beta': 0.03,                                 # infectivity (-)
          'gamma': 5,                                   # duration of infection (d)
          'f_v': 0.1,                                     # fraction of total contacts on visited patch
          'N': get_contact_matrix(),                    # contact matrix
          'M': get_mobility_matrix()                    # origin-destination mobility matrix
          }
# initial states
I0 = construct_initial_infected(loc='Aartselaar', n=5, agedist='demographic')
S0 = construct_initial_susceptible(I0)
init_states = {'S': S0,
               'S_v': np.matmul(S0, params['M']),
               'I': I0
               }

# initialize model
from models import spatial_TL_SIR
model = spatial_TL_SIR(states=init_states, parameters=params, coordinates=coordinates)

# simulate model
out = model.sim(90)

# visualise result
fig,ax=plt.subplots(nrows=3, figsize=(8.3,11.7/2))

ax[0].set_title('Overall')
ax[0].plot(out['time'], out['S'].sum(dim=['age', 'location']), color='green', alpha=0.8, label='S')
ax[0].plot(out['time'], out['I'].sum(dim=['age', 'location']), color='red', alpha=0.8, label='I')
ax[0].plot(out['time'], out['R'].sum(dim=['age', 'location']), color='black', alpha=0.8, label='R')
ax[0].legend(loc=1, framealpha=1)

ax[1].set_title('Infected')
ax[1].plot(out['time'], out['I'].sum(dim='age').sel({'location': name2NIS('Aartselaar')}), linestyle = '-', color='red', alpha=0.8, label='Aartselaar')
ax[1].plot(out['time'], out['I'].sum(dim='age').sel({'location': name2NIS('Aarlen')}), linestyle = '-.', color='red', alpha=0.8, label='Aarlen')
ax[1].plot(out['time'], out['I'].sum(dim='age').sel({'location': name2NIS('Koksijde')}), linestyle = '--', color='red', alpha=0.8, label='Koksijde')
ax[1].legend(loc=1, framealpha=1)

ax[2].set_title('Infected per age group')
ax[2].plot(out['time'], out['I'].sel({'age': '0-5', 'location': name2NIS('Aartselaar')}), linestyle = '-', color='red', alpha=0.8, label='0-5')
ax[2].plot(out['time'], out['I'].sel({'age': '5-15', 'location': name2NIS('Aartselaar')}), linestyle = '-.', color='red', alpha=0.8, label='5-15')
ax[2].plot(out['time'], out['I'].sel({'age': '15-65', 'location': name2NIS('Aartselaar')}), linestyle = '--', color='red', alpha=0.8, label='15-65')
ax[2].plot(out['time'], out['I'].sel({'age': '65+', 'location': name2NIS('Aartselaar')}), linestyle = '-', color='black', alpha=0.8, label='65+')
ax[2].legend(loc=1, framealpha=1)

plt.tight_layout()
plt.show()
plt.close()

# make a GIF
