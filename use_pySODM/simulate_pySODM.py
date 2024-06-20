"""
This script simulates an age-stratified, spatially-explicit SIR model for Belgium using pySODM
"""

__author__      = "Tijs Alleman"
__copyright__   = "Copyright (c) 2024 by T.W. Alleman, IDD Group, Johns Hopkins Bloomberg School of Public Health. All Rights Reserved."

import os
import numpy as np
import matplotlib.pyplot as plt

from utils import name2NIS, \
                    construct_initial_infected, \
                        construct_coordinates_dictionary, \
                            construct_initial_susceptible, \
                                get_contact_matrix, get_mobility_matrix

#################
## Setup model ##
#################

# coordinates
coordinates = construct_coordinates_dictionary()
# parameters
params = {'beta': 0.03,                                 # infectivity (-)
          'gamma': 5,                                   # duration of infection (d)
          'f_v': 0.1,                                   # fraction of total contacts on visited patch
          'N': get_contact_matrix(),                    # contact matrix
          'M': get_mobility_matrix()                    # origin-destination mobility matrix
          }
# initial states
I0 = construct_initial_infected(loc='Aarlen', n=2, agedist='demographic')
S0 = construct_initial_susceptible(I0)
init_states = {'S': S0,
               'S_v': np.matmul(S0, params['M']),
               'I': I0
               }

# initialize model
from models import spatial_TL_SIR
model = spatial_TL_SIR(states=init_states, parameters=params, coordinates=coordinates)


####################
## simulate model ##
####################

out = model.sim(120)

#######################
## visualise results ##
#######################

fig,ax=plt.subplots(nrows=3, figsize=(8.3,11.7/2))

ax[0].set_title('Overall')
ax[0].plot(out['time'], out['S'].sum(dim=['age', 'location']), color='green', alpha=0.8, label='S')
ax[0].plot(out['time'], out['I'].sum(dim=['age', 'location']), color='red', alpha=0.8, label='I')
ax[0].plot(out['time'], out['R'].sum(dim=['age', 'location']), color='black', alpha=0.8, label='R')
ax[0].legend(loc=1, framealpha=1)

ax[1].set_title('Infected')
ax[1].plot(out['time'], out['I'].sum(dim='age').sel({'location': name2NIS('Aarlen')}), linestyle = '-', color='red', alpha=0.8, label='Aarlen')
ax[1].plot(out['time'], out['I'].sum(dim='age').sel({'location': name2NIS('Chimay')}), linestyle = ':', color='red', alpha=0.8, label='Chimay')
ax[1].plot(out['time'], out['I'].sum(dim='age').sel({'location': name2NIS('De Panne')}), linestyle = '--', color='red', alpha=0.8, label='De Panne')
ax[1].legend(loc=1, framealpha=1)

ax[2].set_title('Infected per age group')
ax[2].plot(out['time'], out['I'].sel({'age': '0-5', 'location': name2NIS('Koksijde')}), linestyle = '-', color='red', alpha=0.8, label='0-5')
ax[2].plot(out['time'], out['I'].sel({'age': '5-15', 'location': name2NIS('Koksijde')}), linestyle = ':', color='red', alpha=0.8, label='5-15')
ax[2].plot(out['time'], out['I'].sel({'age': '15-65', 'location': name2NIS('Koksijde')}), linestyle = '--', color='red', alpha=0.8, label='15-65')
ax[2].plot(out['time'], out['I'].sel({'age': '65+', 'location': name2NIS('Koksijde')}), linestyle = '-', color='black', alpha=0.8, label='65+')
ax[2].legend(loc=1, framealpha=1)

plt.tight_layout()
plt.show()
plt.close()

################
## Make a GIF ##
################

import geopandas as gpd
from matplotlib.colors import Normalize
import matplotlib.cm as cm

# load shapefiles and sort dataframe
gdf = gpd.read_file('../data/raw/shape/georef-belgium-municipality-millesime.shp')
gdf = gdf[gdf['year'] == '2021']
gdf = gdf.sort_values(by='mun_code')

# loop over timesteps in simulation
frames = []
for t in out['time'].values:
    # extract simulation and add to geopandas dataframe
    gdf['I'] = np.log10(out.sel(time=t).sum(dim='age')['I'].values+1e-9)

    # make the map
    fig,ax = plt.subplots(nrows=2, figsize=(8.3/2,11.7/3), height_ratios=[3, 1])
    gdf.plot(column='I',  
            cmap='OrRd',  # Choose a color map
            linewidth=0.5,
            edgecolor='black',
            legend=False,
            ax=ax[0],
            vmin=0,
            vmax=5,
            )
    ax[0].set_axis_off()
    ax[0].set_title(f'SIR model with commuter mobility\nt = {t} days')
    # plot the states
    ax[1].plot(out.sel(time=range(t)).sum(dim=['age','location'])['S']/11.5e6*100, color='green', label='S')
    ax[1].plot(out.sel(time=range(t)).sum(dim=['age','location'])['I']/11.5e6*100, color='red', label='I')
    ax[1].plot(out.sel(time=range(t)).sum(dim=['age','location'])['R']/11.5e6*100, color='black', label='R')
    ax[1].set_xlim([0,120])
    ax[1].set_ylim([0,100])
    ax[1].set_xlabel('time (days)', fontsize=8)
    ax[1].set_ylabel('population (%)', fontsize=8)
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)
    ax[1].legend(loc=1, framealpha=1, prop={'size': 8})
    ax[1].tick_params(axis='both', which='major', labelsize=8)

    output_dir = 'frame'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    frame_path = os.path.join(output_dir, f'frame_{t:03d}.png')
    frames.append(frame_path)
    plt.savefig(frame_path, bbox_inches='tight', dpi=150)
    plt.close(fig)

import imageio
# Step 5: Create a GIF from the saved frames
with imageio.get_writer('simulation.gif', mode='I', duration=1) as writer:
    for frame_path in frames:
        image = imageio.imread(frame_path)
        writer.append_data(image)

# Optionally, remove the frame files after creating the GIF
for frame_path in frames:
    os.remove(frame_path)