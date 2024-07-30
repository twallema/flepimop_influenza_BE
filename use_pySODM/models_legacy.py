"""
This script contains an age-stratified spatially-explicit SIR model for use with pySODM.
"""

__author__      = "Tijs Alleman"
__copyright__   = "Copyright (c) 2024 by T.W. Alleman, IDD Group, Johns Hopkins Bloomberg School of Public Health. All Rights Reserved."

import numpy as np
from pySODM.models.base import ODE, JumpProcess

###################
## Deterministic ##
###################

class spatial_ODE_SIR(ODE):
    """
    Stochastic SIR model with age and spatial stratification
    """
    
    states = ['S','I','R']
    parameters = ['beta','gamma', 'f_v', 'N', 'M']
    dimensions = ['age', 'location']

    @staticmethod
    def integrate(t, S, I, R, beta, gamma, f_v, N, M):

        # compute total population 
        T = S + I + R

        # compute visiting populations
        T_v = matmul_2D_3D_matrix(T, M) # M can  be of size (n_loc, n_loc) or (n_loc, n_loc, n_age), representing a different OD matrix in every age group
        I_v = matmul_2D_3D_matrix(I, M)

        # compute force of infection
        l = beta * (1 - f_v) * np.einsum('kj,ikj->ij', I/T, np.atleast_3d(N)) + beta * f_v * np.einsum('jki,lk,ilk->ij', np.atleast_3d(M), I_v/T_v, np.atleast_3d(N))

        # compute differentials
        dS = - l * S
        dI = l * S - 1/gamma*I
        dR = 1/gamma*I

        return dS, dI, dR

###################
### Stochastic ###
###################


class spatial_TL_SIR(JumpProcess):
    """
    Stochastic SIR model with age and spatial stratification
    """
    states = ['S', 'I','R']
    parameters = ['beta','gamma', 'f_v', 'N', 'M']
    dimensions = ['age', 'location']


    @staticmethod
    def compute_rates(t, S, I, R, beta, gamma, f_v, N, M):

        # calculate total population 
        T = S + I + R

        # compute visiting populations
        T_v = matmul_2D_3D_matrix(T, M) # M can  be of size (n_loc, n_loc) or (n_loc, n_loc, n_age), representing a different OD matrix in every age group
        I_v = matmul_2D_3D_matrix(I, M)

        # create a size dummy 
        G = S.shape[0] # age stratification
        H = S.shape[1] # spatial stratification
        size_dummy = np.ones([G,H], np.float64)

        # compute force of infection
        l = beta * (1 - f_v) * np.einsum('kj,ikj->ij', I/T, np.atleast_3d(N)) + beta * f_v * np.einsum('jki,lk,ilk->ij', np.atleast_3d(M), I_v/T_v, np.atleast_3d(N))

        rates = {
            'S': [l],
            'I': [size_dummy*(1/gamma)],
            }
        
        return rates

    @ staticmethod
    def apply_transitionings(t, tau, transitionings, S, I, R, 
                             beta, f_v, gamma, 
                             N, M):
        
        
        S_new = S - transitionings['S'][0]
        I_new = I + transitionings['S'][0]  - transitionings['I'][0]
        R_new = R + transitionings['I'][0]
        
        return(S_new, I_new, R_new)
    
# helper function
def matmul_2D_3D_matrix(X, W):
    """
    Computes the product of a 2D matrix (size n x m) and a 3D matrix (size m x m x n) as an n-dimensional stack of (1xm) and (m,m) products.

    input
    =====
    X: np.ndarray
        Matrix of size (n,m).
    W : np.ndarray
        2D or 3D matrix:
        - If 2D: Shape (m, m). Expanded to size (m, m, n).
        - If 3D: Shape (m, m, n).
          Represents n stacked (m x m) matrices.

    output
    ======
    X_out : np.ndarray
        Matrix product of size (n, m). 
        Element-wise equivalent operation: O_{ij} = \sum_{l} [ s_{il} * w_{lji} ]
    """
    W = np.atleast_3d(W)
    return np.einsum('ik,kji->ij', X, np.broadcast_to(W, (W.shape[0], W.shape[0], X.shape[0])))
