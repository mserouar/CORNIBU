import sys
sys.path.append('/Users/home/Downloads/CORNIBU')

from plante import *
from leafsize import leafsize
from loop_indiv_plant import loop_indiv_plant
from loop_all_leaves import loop_all_leaves
from rotate_translate_panel import rotate_translate_panel
from txt_to_can import txt_to_can
from Direct_Light import Direct_Light
from Diffuse_Light import Diffuse_Light

import os
import numpy as np

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

def CORNIBU(T, To, DTc, DTs, S_max, N_max, H_max, inter_rang, density, incli_top, incli_base, l, delta, phyllotactic_angle, phyllotactic_deviation, loc, scale, arg, dist, Caribu, vizu, mode, norm, DOY, latitude, mode_AgriPV) :

    if 5/(inter_rang*5*density) > inter_rang :                  # Test if the distance between plants is higher than distance between rows                                               
        inter_rang=5/(inter_rang*5*density)                     # If True, distance between plants will become distance between rows. 

    scene_side = inter_rang*5                                   # Scene length will be defined by 5 rows

    [ABC_stem, ABC_leaf, area_shape, longueur] = plante(N_max,S_max,H_max, incli_top, incli_base, l, delta)  # Design the 'mean' plante, that will be replicated | area_shape for LAI computation

    N = [i for i in np.arange(1, N_max+1, 1)]
    T = np.matlib.repmat(T, N_max+1,1)

    Growth = [((To + i*DTc < T[i]) and (To + i*DTc + DTs > T[i]))[0] for i in N] # Originally this is related to calculation of the order of potentially present leaves 
                                                                                 # BUT, see GDD parameter in the README - not used in our case as we focused on single date | Calculation of the leaf presence vector
    I = np.argwhere(np.asarray(Growth)==1)
    ABC_leaf = ABC_leaf[I,:]

    ### Scene Description | Related Density and Inter-rows 
    dist_plt = 5/(scene_side*density)                           # Distance between plants within row
    Li = np.arange(dist_plt/2, scene_side, dist_plt)            # x,y center position of each plant in scene
    y = np.tile(Li,5)
    Lix = np.arange(inter_rang/2, scene_side, inter_rang)
    x = np.tile(Lix,len(y/5))
    x_unique = np.unique(x)
    y_unique = np.unique(y)
    xx, yy = np.meshgrid(x_unique, y_unique)
    xyz = np.stack((xx, yy, np.zeros_like(xx)), axis=-1).reshape(-1, 3)

    ### To avoid a too perfect mathematical simulated crop model, we add some noise around each plant/stem position. 
    ### Thus, up to 10 cm are randomly added in both x- and y-axis
    xydelta = 0.1                                               # Related to noise sowing parameter
    newy = (np.random.rand(len(xyz), 1)*xydelta*2*dist_plt) - (dist_plt*xydelta/2)    # Deviation plants from row x, y noise
    np.asarray(xyz)[:, 1] += newy[:, 0]
    xyz[:, 0] += newy[:, 0]
    #area_soil = np.abs(xyz[0][0] - xyz[-1][0]) * np.abs(xyz[0][1] - xyz[-1][1])

    ABC_couvert = []
    DEF_couvert = []
    N = [i for i in np.arange(1, N_max+1, 1)]
    a=0.59526
    d=1.4158

    SS = []

    N = [i for i in np.arange(1, N_max+1, 1)]
    for i in N :
        S = (1+np.sin((np.pi/a)*((i/N_max)**d)-(np.pi/2)))/2
        SS.append(np.asarray(S)*S_max/np.sum([S for i in N]))   # Leaf area for each leaf order | Normalizing the maximum leaf area produced (redondance with previous 'plant' function for LAI computation accessibility)

    N_biggest = np.argwhere(SS == np.max(SS))
    SS = SS - SS[0]
    SS = (SS[N_biggest[0][0]] - SS) / SS[N_biggest[0][0]]

    a = 3.7 - 0.10*N_max - 0.36*S_max                                                  
    H = (H_max - 0.015) / np.power(N_max,a-1) * np.power(N,a-1) + 0.015      # Heigth of first leaf | Insertion heigth of all leaves (see Espana et al. 1998)

    #teta_mat=[]
    Post_Azi = []
    Leaf_Tri_Count = []
    #SUR_TOT = np.sum(area_shape) * len(xyz)                                  # Total surface (LAI computation) | Kept for checking 

    delta_teta_leaf = 20                                        # Initialize difference in inclination between the first and the largest leaf
    teta_biggest = 45                                           # Initialize inclination of largest leaf
    rand_teta = 2.5                                             # Noise (°) in inclination for each leafx_vec_g

    #   We multiply ’mean’ plants and place them according to sowing pattern already described earlier.
    #   Here we have well positioned plants and N stacked leaves, each one described as a 1D-axis stick of length previously defined.

    # We will now give given orientations to each of these 1D-axis sticks.
    # To do so, we will first give each plant a main direction, according to a probability density function. Then, for each leaf, Gaussian
    # dispersion to this main direction will be then added as noise.
    # Each p (plant) has a main direction according to a probability from a density continuous function (dist.rvs of scipy package). 
    # This given distribution and its args were, in our case, determined in a previous paper (Mario Serouart
    # et al. 2023) 
    # If you do not have a specific or precise idea of your distribution, you can then easily
    # adapt this part to follow a Von Mises behavior. It will closely approach what we have done.

    # Once the direction value is obtained, we input some dispersion around the latter thanks to 'leaf_azimuth'. Note that, as our directions where
    # fitted within a range of [0;90°], we added a random function of probability 0.5 to mirror the final azimuth angle ([0;90°] + Phyllotaxy [0;180°]
    # will give back [0;360°] mock-ups).

    # Then we use rot_3D_triangle to reach the given angle in 3D space (for each leaf, of each plant). It simply uses trigonometric relationships
    # to rotate an element -our stick- following a given angle in a 3D space -here to keep it simple, remember, we only rotate through x,y (soil plane)

    ABC_couvert, DEF_couvert = loop_indiv_plant(N_max, xyz, SS, delta_teta_leaf, teta_biggest, rand_teta, ABC_leaf, dist, loc, scale, phyllotactic_angle, phyllotactic_deviation, Post_Azi, ABC_stem, arg, H)

    Stacked_facets = []
    ALA_ratio =  [] 
                                                      
    incli_base = (incli_base + (np.random.randn(1,1) * rand_teta))[0][0]   # Randomness leaves inclination + curvature on 4 parameters 
    delta = (delta + (np.random.randn(1,1) * rand_teta))[0][0]
    l = (l + (np.random.randn(1,1) * 0.05))[0][0]

    # We consider the z-axis as the y-axis, so the leaf curvature linked to the leaf angle forms a parabola on x,z or y,z (again depending on rotations).
    # 'leaf_shape_rank' will determine each 4 parameters that define shape of leaf curvature. Briefly, it generates x and y coordinates for a
    # leaf profile shape of a single plant -including leaves from base to top-. This function sets the l, inflexion curve value, based on parameters
    # related to the leaf position in the plant and its characteristics. It is calibrated on first leaf and interpolated linearly from incli_base first leaf to
    # incli_top last leaf range.
    # Note that vec_d and vec_g denotes side of the future lamina -g and d for each side of midrib leaf-.

    Stacked_facets = loop_all_leaves(ABC_couvert, N_max, incli_top, incli_base, l, delta, longueur, ALA_ratio, Post_Azi, area_shape, Leaf_Tri_Count, Stacked_facets)

    # Facets creation
    # As we are interested in facets light characterisation -facets are primitive shapes easier to handle-, we create triangles and linking up all
    # points together every 3 vertices, taking into account each side of lamina midrib/nerve

    Stacked_facets = np.concatenate(Stacked_facets, axis=1).T.tolist()    # Stacked list of all facets
    ALA = np.mean(ALA_ratio)
    diff_stem_leaves = len(Stacked_facets * 3)    # 3 being number of vertices for a triangle

    # Stems are added at the very end, as it was easier with mesh format.
    # Each stem is defined as 4 long triangles (as a cone/pyramid).
    for tt in DEF_couvert :
        Stacked_facets.append( [tt[0], tt[3], tt[6], tt[1], tt[4], tt[7], tt[2], tt[5], tt[8]] )    # Adding stems triangles
        
    # Same for Soil surface
    Stacked_facets.append([xyz[0][0] - inter_rang/2, xyz[-1][0] + inter_rang/2, xyz[0][0] - inter_rang/2, xyz[0][1] - dist_plt/2, xyz[0][1] - dist_plt/2, xyz[-1][1] + dist_plt/2, 0, 0, 0])    # Soil BBox
    Stacked_facets.append([xyz[-1][0] + inter_rang/2, xyz[0][1] - dist_plt/2, xyz[-1][0] + inter_rang/2, xyz[-1][0] + inter_rang/2, xyz[-1][1] + dist_plt/2, xyz[0][0] - inter_rang/2, 0, 0, 0])

    # There is a feature not presented in the paper, showing how to add solar panel, in case of AgriPV simulations - Not also linked to .opt parameters
    if mode_AgriPV == True :
        Square_panel = rotate_translate_panel((xyz[0][0] - inter_rang/2)/2, (xyz[-1][0] + inter_rang/2)/2, (xyz[-1][0] + inter_rang/2)/2, (xyz[0][0] - inter_rang/2)/2, (xyz[0][1] - dist_plt/2), (xyz[0][1] - dist_plt/2), (xyz[-1][1] + dist_plt/2), (xyz[-1][1] + dist_plt/2), 4, 4, 4, 4, 45)
        Stacked_facets.append([Square_panel[0],Square_panel[2],Square_panel[3], Square_panel[4], Square_panel[6], Square_panel[7], Square_panel[8], Square_panel[10], Square_panel[11]])
        Stacked_facets.append([Square_panel[0],Square_panel[1],Square_panel[2], Square_panel[4], Square_panel[5], Square_panel[6], Square_panel[8], Square_panel[9], Square_panel[10]])

    # Setting Bounding Box to activate the 'infinite replicated scene' mode in Caribu | Avoid artificial effects
    BBox = [ (DEF_couvert[0][0] - inter_rang/2), (DEF_couvert[0][1] - dist_plt), (DEF_couvert[-1][0] + inter_rang/2), (DEF_couvert[-1][1] + dist_plt) ]  # Normal BBox Dir. NS
    #area_soil_LAI = (np.abs((DEF_couvert[0][0] - inter_rang/2) - (DEF_couvert[-1][0] + inter_rang/2)) * (np.abs((DEF_couvert[0][1] - dist_plt) - (DEF_couvert[-1][1] + dist_plt))))

    # MESH.txt to MESH.can format facets cloud
    # Following part is entirely according to CanestraDoc.pdf documentation -available in the Github repo- and obviously the excellent work
    # on which relies Caribu raycasting model: Chelle, Michael & Andrieu, Bruno. (1998).

    # The required .can file contains the geometric descriptions of a vegetation canopy. Exactly as our matrix Stacked_facets saved in .txt file,
    # but which is in the wrong format and will need to be tranformed. The .can format allows to associate information of optics, facets,
    # leaves, stems and plants through IDs allocation. Making easier interpretation in final output file that permit quantifying intercepted light by
    # facets, leaves, stems and plants. This ASCII file contains then one line by facets.

    # Here is what it looks like (.can format)
        # For a given facet : p 2 100001001001 9 3 0.35 0.06 0.35 0.35 0.06 0.35 0.35 0.06 0.35
        # p : polygon
        # 2 : The number of args that will be declared before number of polygon vertices
        # 100001001001: Optical species (1) + Plant no. (00001) + Organ no. (001) + Facet no. (001)
        # 9 : Number of elements in triplet (3) * xyz coordinates (3)
        # 3 : Number of polygon vertices
        # 0.35 0.06 ... 0.35 : Vertices coordinates

    path = '/Users/home/Downloads/corn/'
    np.savetxt(path + 'OOO.txt', Stacked_facets)     # 1 row : [3 vertices x 3 coordinates xxxyyyyzzz]
    print(f"✅ .txt Scene File created successfully at: {path + 'OOO.txt'}")
                                           
    txt_to_can(path, Leaf_Tri_Count, diff_stem_leaves, N_max) 
    print(f"✅ .can File created successfully at: {path + 'OOO_CAN.can'}")

    # 'Ray Tracing' Computation
    if Caribu == True :

        # Settings light parameters
        # In our case Optical species goes from 1 (Leaf) to 2 (Stem) and finally 3 (Soil) (+ 4 Panel if enabled). 

        # Each line, each espece (Species in french) is defined as :
        # e : New declared species
        # d : diffuse
        # 0.10 : Species reflectance (upper surface)
        # 0.05 : Species transmittance (upper surface)
        # d : diffuse
        # 0.10 : Species reflectance (lower surface)
        # 0.05 : Species transmittance (lower surface)

        # Target directory
        filename = 'par_panel.opt'
        filepath = os.path.join(path, filename)
        os.makedirs(path, exist_ok=True)

        # Content of the .opt file
        content = (
        "#     par_panel.opt  MC96\n"
        "#simulation \n"
        "#format e : tige,  feuille sup,  feuille inf\n"
        "# nbre d'especes\n"
        "n 4\n"
        "#1 ESPECES\n"
        "s d 0.5\n"
        "# espece 1\n"
        "e d 0.10   d 0.10 0.05  d 0.10 0.05\n"
        "# espece 2\n"
        "e d 0.01   d 0.01 0.005  d 0.01 0.005\n"
        "# espece 3\n"
        "e d 0.5   d 0.5 0  d 0.5 0\n"
        "# espece 4\n"
        "e d 0.5   d 0.5 0  d 0.5 0\n"
        )

        with open(filepath, 'w') as file:
            file.write(content)

        print(f"✅ .opt File saved successfully at: {filepath}") # filepath = .opt file

        can = path + 'OOO_CAN.can' 

        # Direct light conditions
        # According the sun path you want, you will define the Day Of the Year (int number from 1 to 365). 
        # The energy -PPFD or PAR- is to be defined. We chose to normalize it, our sun source will launch from 0 to 1, and then coupled with real weather station to access True PPFD.
        # To have an accurate sun path, you will define Latitude from your experimental site. 
    
        # This snippet will then extract, for each hour -or to be set here from 11 to 12 am-, the sun position in the sky. 
        # Caribu will define sun as a flat panel with these given positions, from where it will ’cast rays’ - See radiosity method from Caribu paper (SAIL volume based and Z-Buffer)-.

        if mode == 'direct' :
            hour_start = 11
            hour_end = 12
            Direct_Light(filepath, norm, DOY, latitude, can, BBox, vizu, hour_start, hour_end)

        # Diffuse light conditions
        # The principle is the same then Direct. 

        # Except that to simulate a more opaque sky, in which the rays do not have privileged directions, we simulate a sky with "several suns". 
        # According to its position in the sky, a given sun will not have the same energy compared to another one. 
        # Indeed, it depends on their position in the half-sphere they occupy -their cos-.
        # Two systems exist: soc/uoc. We choose s-overcast, hence the position-dependent power.

        if mode == 'diffuse' :
            overcast = 'uoc'
            Diffuse_Light(filepath, overcast, norm, can, BBox, vizu)
