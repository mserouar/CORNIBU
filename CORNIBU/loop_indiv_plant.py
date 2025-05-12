import numpy as np
import scipy.stats as st
import statsmodels.api as sm
import scipy
from scipy.stats._continuous_distns import _distn_names
import copy
import math
from numpy import matlib as mb

from leaf_azimuth import *
from rot_3D_triangle import *

def loop_indiv_plant(N_max, xyz, SS, delta_teta_leaf, teta_biggest, rand_teta, ABC_leaf, dist_func, loc, scale, phyllotactic_angle, phyllotactic_deviation, Post_Azi, ABC_stem, arg, H):

    for p in range(len(xyz)) :  # For each plant

        teta_leaf = SS*delta_teta_leaf + teta_biggest + (np.random.randn(N_max,1)*rand_teta - rand_teta/2)          # Calculation of initial inclination
        ABC_leafind = copy.deepcopy(ABC_leaf)                                                                       # Careful Python language tricks

        if p == 0 :
            teta_mat = teta_leaf[0]
        else :
            teta_mat = np.column_stack((teta_mat,teta_leaf[0]))

        # Inclusion of explicit distributions
        dist = getattr(scipy.stats, dist_func)
        try :
            mOR = dist.rvs(loc=loc, scale=scale, *arg, size = 1)                      # Dealing with several *args length according to selected distribution
        except :
            arg = [arg]
            mOR = dist.rvs(loc=loc, scale=scale, *arg, size = 1)
     
        mOR = mOR[0]

        while mOR < 0 or mOR > 90 :                                                   # Dealing with continuous/discrete distributions ranges
            mOR = dist.rvs(loc=loc, scale=scale, *arg, size = 1)
            mOR = mOR[0]                                                              # mOR : Main azimuthal direction of plant p, selected according to theorical distribution
        
        # Rearrange all leaves according to phyllotactic angle 
        az_max = (leaf_azimuth(size = N_max, phyllotactic_angle = phyllotactic_angle, phyllotactic_deviation = phyllotactic_deviation, plant_orientation = (90 - mOR)) ) * np.pi/180  

        N = [i for i in np.arange(1, N_max+1, 1)] 
        for n_leaf in N  :
            Post_Azi.append(math.degrees(az_max[n_leaf-1]))
            ABC_leafind[n_leaf-1,:] = rot_3D_triangle(ABC_leafind[n_leaf-1,:], [0, 0, 0])                                   # Rotation for leaf inclination
            ABC_leafind[n_leaf-1,:] = rot_3D_triangle(ABC_leafind[n_leaf-1,:], [0, 0, math.degrees(az_max[n_leaf-1])])      # Rotation for leaf azimuth
            ABC_leafind[n_leaf-1,:] = ABC_leafind[n_leaf-1,:] + [0, 0, H[n_leaf-1], 0, 0, H[n_leaf-1], 0, 0, H[n_leaf-1]]   # Rotation for plant azimuth

        ABC_leafind = ABC_leafind.reshape(N_max,9)
        
        ABC = ABC_leafind                                                                                                   # Leaves matrix
        ABC_couvert = ABC + np.tile(xyz[p,:],(len(ABC),3)) if p == 0 else np.vstack([ABC_couvert, ABC + np.tile(xyz[p,:],(len(ABC),3)) ])

        DEF = ABC_stem[0]                                                                                                   # Stem matrix
        DEF_couvert = DEF + np.tile(xyz[0,:],(len(DEF),3))
        for p in range(1, len(xyz)):
            DEF_couvert = np.vstack([DEF_couvert, DEF + np.tile(xyz[p,:],(len(DEF),3)) ])

    return ABC_couvert, DEF_couvert


