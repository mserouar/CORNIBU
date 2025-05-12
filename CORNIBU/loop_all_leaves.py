import numpy as np
import math
from leaf_shape_rank import leaf_shape_rank
from triangle_area import triangle_area
from leaf_morpho_rel import leaf_morpho_rel

def calculate_value(value):
    if 0 <= value <= 90:
        return 90 - value
    else:
        return 90 + abs(value)

def loop_all_leaves(ABC_couvert, N_max, incli_top, incli_base, l, delta, longueur, ALA_ratio, Post_Azi, area_shape, Leaf_Tri_Count, Stacked_facets):

    for n_leaf in range(len(ABC_couvert))  :     

        Stacked_facets_corr = []    # Rework on each leaf (flat and inclined for now)

        Leaf_OI = np.mod(n_leaf, N_max)  
        # Curvature and inclination function 
        x_max, y_max = leaf_shape_rank(rank = Leaf_OI, incli_top = incli_top, incli_base = incli_base, l = l, delta = delta, nb_segment = int(longueur[Leaf_OI]*100))       
        
        # Resolution : If 1 point per cm, then remove lines, else it would consider 1 point per 10 cm
        # MacOS may have difficulties rendering in Web-based display. Increase this number to deal with.
        x_max = x_max[::10]
        y_max = y_max[::10]

        angle = math.atan2(np.median(y_max), np.median(x_max))
        angle_degrees = math.degrees(angle)

        fin = calculate_value(np.mean(angle_degrees))
        ALA_ratio.append(fin)

        # Reminder : leaf_shape_rank codes for half a lamina
        # Note that vec_d and vec_g denotes side of the future lamina -g (left) and d (right) for each side of midrib leaf-.
        x_vec_g = (x_max/100 * math.cos(np.radians(Post_Azi[n_leaf])))+ ABC_couvert[n_leaf][0]
        y_vec_g = (x_max/100 * math.sin(np.radians(Post_Azi[n_leaf]))) + ABC_couvert[n_leaf][1]

        x_vec_d = (x_max/100 * math.cos(np.radians(Post_Azi[n_leaf]))) + ABC_couvert[n_leaf][6]
        y_vec_d = (x_max/100 * math.sin(np.radians(Post_Azi[n_leaf]))) + ABC_couvert[n_leaf][7]

        z_vec_g = ABC_couvert[n_leaf][2] + y_max/100
        z_vec_g_corr = ABC_couvert[n_leaf][2] + y_max/100

        # Waffling function TODO : Non prehistoric function !
        z_vec_d = z_vec_g
        xin_array = np.linspace(0, int(longueur[Leaf_OI]*100), len(y_max))   
        yout_array = np.sin(xin_array/ (Leaf_OI/1.25))* 0.01
        z_vec_g = z_vec_g + yout_array
        yout_array = np.sin(-xin_array/ (Leaf_OI/1.25))* 0.01
        z_vec_d = z_vec_d - yout_array


        # From this point, adding leaves width derived from the initial model would give us unrealistic isosceles triangles leaves, 
        # where the leaf base is equal to max width.

        # We then need to transform modelled leaf surface into a realistic leaf shape.

        # Thanks to leaf_morpho_rel we are able to do so. 
        # This function is derived from the excellent course available here : https://github.com/openalea-training/hmba312_training. 
        # Again, we fixed x as the length of leaf, and y the value it must takes to be realistic (wanted one).
        # Note : While keeping the previous estimated value of surface from España et al. model defined in the document. 
        
        # The shape is normalized to be adapted for each leaf rank (s and r are multiplied to length and width, respectively).
        # Tips: Care must be taken at this stage, as area is a 2D concept. Simple rotation generates errors in the shape.
        
        # Refer to Figure in .pdf document
        # In the following figure, the red line corresponds to the previous Inclination fitted leaf profile, for a given leaf as example. The green line
        # corresponds to the predicted leaf width at each length point -according to the midrib-. Then, if we simply add z-values of red points to the
        # green line, we get the blue line. In this specific case, area under the green curve (on x,y plane) is different from the area under the blue curve (always on x,y plane).

        #######################################################################
        ########## Getting cumulative area to correct this effect #############
        #######################################################################

        leaf_area = area_shape[Leaf_OI] / 2   # Lamina shape

        w0=0.5+0.01*Leaf_OI
        lm=0.5+(-.02)*Leaf_OI
        wl_min=0.08+Leaf_OI*0.001

        s,r=leaf_morpho_rel(nb_segment=len(x_max)-1, w0=w0, lm=lm) 

        l_min= longueur[Leaf_OI] 
        w_min=l_min*wl_min
        s_min,r_min = s*l_min, r*w_min

        integral = np.trapz(r_min,s_min)
        w_min = w_min * (leaf_area / integral)
        s_min,r_min = s*l_min, (r*w_min)
        
        px_p = np.empty(len(x_vec_g))
        py_p = np.empty(len(y_vec_g))
        px_n = np.empty(len(x_vec_g))
        py_n = np.empty(len(y_vec_g))
        for idx in range(len(x_vec_g)-1):
            x0, y0, xa, ya = x_vec_g[idx], y_vec_g[idx], x_vec_g[idx+1], y_vec_g[idx+1]
            dx_p, dy_p = xa-x0, ya-y0
            norm_p = np.hypot(dx_p, dy_p) * 1/r_min[idx]
            px_p[idx] = x0-dy_p/norm_p
            py_p[idx] = y0+dx_p/norm_p

            dx_n, dy_n = xa-x0, ya-y0
            norm_n = np.hypot(dx_n, dy_n) * 1/-r_min[idx]
            px_n[idx] = x0-dy_n/norm_n
            py_n[idx] = y0+dx_n/norm_n

        x_vec_g_corr = np.insert(px_p, 0, px_p[0])
        y_vec_g_corr = np.insert(py_p, 0, py_p[0])
        x_vec_d_corr = np.insert(px_n, 0, px_n[0])
        y_vec_d_corr = np.insert(py_n, 0, py_n[0])

        pp = np.arange(len(x_max)-1)
        Stacked_facets_corr.append([x_vec_g_corr[pp], x_vec_g_corr[pp+1], x_vec_d_corr[pp], y_vec_g_corr[pp], y_vec_g_corr[pp+1], y_vec_d_corr[pp], z_vec_g_corr[pp], z_vec_g_corr[pp+1], z_vec_g_corr[pp]])                 # Facets triangles building
        Stacked_facets_corr.append([x_vec_g_corr[pp+1], x_vec_d_corr[pp+1], x_vec_d_corr[pp], y_vec_g_corr[pp+1], y_vec_d_corr[pp+1], y_vec_d_corr[pp], z_vec_g_corr[pp+1], z_vec_g_corr[pp+1], z_vec_g_corr[pp]])

        cumulative_area = 0
        for triangle in np.concatenate(Stacked_facets_corr, axis=1).T.tolist() :
            x1, x2, x3, y1, y2, y3, z1, z2, z3 = triangle
            area = triangle_area(x1, x2, x3, y1, y2, y3, z1, z2, z3)
            cumulative_area += area
        
        ###################################################################################################################################
        ########## Code not well optimized on this specific feature, but ensures that the leaf area is corrected and verified #############
        ####################### TODO : Create one function that does both, with parameter boolean correction or not #######################
        ###################################################################################################################################

        leaf_area = area_shape[Leaf_OI] / 2                                                                              # Lamina shape

        w0=0.5+0.01*Leaf_OI
        lm=0.5+(-.02)*Leaf_OI
        wl_min=0.08+Leaf_OI*0.001

        s,r=leaf_morpho_rel(nb_segment=len(x_max)-1, w0=w0, lm=lm) 

        l_min= longueur[Leaf_OI] 
        w_min=l_min*wl_min
        s_min,r_min = s*l_min, r*w_min

        integral = np.trapz(r_min,s_min)
        w_min = w_min * (leaf_area / integral)
        s_min,r_min = s*l_min, (r*w_min)* (area_shape[Leaf_OI] / cumulative_area) # Here is the correction

        px_p = np.empty(len(x_vec_g))
        py_p = np.empty(len(y_vec_g))
        px_n = np.empty(len(x_vec_g))
        py_n = np.empty(len(y_vec_g))
        for idx in range(len(x_vec_g)-1):
            x0, y0, xa, ya = x_vec_g[idx], y_vec_g[idx], x_vec_g[idx+1], y_vec_g[idx+1]
            dx_p, dy_p = xa-x0, ya-y0
            norm_p = np.hypot(dx_p, dy_p) * 1/r_min[idx]
            px_p[idx] = x0-dy_p/norm_p
            py_p[idx] = y0+dx_p/norm_p

            dx_n, dy_n = xa-x0, ya-y0
            norm_n = np.hypot(dx_n, dy_n) * 1/-r_min[idx]
            px_n[idx] = x0-dy_n/norm_n
            py_n[idx] = y0+dx_n/norm_n
        x_vec_g = np.insert(px_p, 0, px_p[0])
        y_vec_g = np.insert(py_p, 0, py_p[0])
        x_vec_d = np.insert(px_n, 0, px_n[0])
        y_vec_d = np.insert(py_n, 0, py_n[0])

        Leaf_Tri_Count.append(np.arange(1, (len(x_max)-1)*2+1))

        pp = np.arange(len(x_max)-1)
        Stacked_facets.append([x_vec_g[pp], x_vec_g[pp+1], x_vec_d[pp], y_vec_g[pp], y_vec_g[pp+1], y_vec_d[pp], z_vec_g[pp], z_vec_g[pp+1], z_vec_g[pp]])                 # Facets triangles building
        Stacked_facets.append([x_vec_g[pp+1], x_vec_d[pp+1], x_vec_d[pp], y_vec_g[pp+1], y_vec_d[pp+1], y_vec_d[pp], z_vec_g[pp+1], z_vec_g[pp+1], z_vec_g[pp]])

    return Stacked_facets