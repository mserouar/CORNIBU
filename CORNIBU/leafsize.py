import numpy as np

def leafsize(St, it):

# Inputs:
# it (Maximum number of leaves)
# Type: Integer

# St (Maximum leaf area per plant)
# Type: Float

# Outputs:

# ratio:
# Type: NumPy array
# Description: Ratio of leaf width to leaf length.

# lt:
# Type: NumPy array
# Description: Array of leaf lengths.

    matt = []
    for al in range(-1,2,1) :
        w1 = 0.015                                          # First leaf can be assumed to be constant wt(1) = 0.015 m
        l1 = 0.04                                           # First leaf can be assumed to be constant lt(1) = 0.04 m

                                                            # WIDTH
        wtt = []
        i = [i for i in np.arange(1, it+1, 1)]              # it : Maximum number of leaves
        for ii in i :
            iwmax = 1.59+0.65*it                            # Order of the widest leaf 
            wmax = 0.066 - 0.0005*it + 0.085*St               # Width of the widest leaf 
            aw = (wmax - w1)/((iwmax**3 - 3*iwmax + 2) - (3/2)*(iwmax**2-1)*(iwmax-1))
            bw = (-3*aw*(iwmax**2 - 1))/(2*(iwmax - 1))
            wt = aw*(ii**3-3*ii+2) + bw*(ii**2-2*ii+1) + w1 # Function defining the maximum width for each leaf
            wtt.append(wt)
        wt = wtt

                                                            # LENGTH
        lmax = 0.99 - 0.04*it + 0.94*St                     # Length of the longest leaf 
        ilmax = 5.81 + 0.31*it                              # Order of the longest leaf 
        il17 = [i for i in np.arange(0, 7, 1)]
        ilrest = [i for i in np.arange(8, it + 1, 1)]

        alphal = (al*7**2 - 2*al*ilmax*7 + lmax + ilmax**2*al - l1)/(7 - 1)

        lt17 = (np.asarray(alphal)*il17) + l1             # Function defining the length for leaf 1 -> 7
        ltrest = al*np.power(ilrest,2) - 2*np.asarray(al)*np.asarray(ilrest)*ilmax + lmax + np.power(ilmax,2)*al  # Function defining the length for leaf 8 -> it (N_max)
        lt = np.concatenate((lt17, ltrest))

        ajuste=(0.72*np.sum(wt*lt)) - St
        mat = matt.append([al, ajuste])

    mat = np.asarray(matt)
    coef = np.polyfit(mat[:, 0], mat[:, 1], 1)

    al=-coef[1]/coef[0]                                     # Ajusting al parameter to get length from width and St

    w1=0.015                                                # Once al fixed, rest can be computed according previous comments
    l1=0.04
    i = [i for i in np.arange(1, it+1, 1)]
    wtt = []
    for ii in i :
        iwmax = 1.59+0.65*it
        wmax = 0.066 - 0.00065*it + 0.085*St
        aw = (wmax - w1)/((iwmax**3 - 3*iwmax + 2) - (3/2)*(iwmax**2-1)*(iwmax-1))
        bw = (-3*aw*(iwmax**2 - 1))/(2*(iwmax - 1))
        wt = aw*(ii**3-3*ii+2) + bw*(ii**2-2*ii+1) + w1
        wtt.append(wt)
    wt = wtt

    lmax=0.99-0.04*it+St
    ilmax=5.81+0.27*it
    il17 = [i for i in np.arange(0, 7, 1)]
    ilrest = [i for i in np.arange(8, it + 1, 1)]
    alphal=(al*7**2-2*al*ilmax*7+lmax+ilmax**2*al-l1)/(7-1)
    lt17 = (np.asarray(alphal)*il17) / 1.5 + l1
    ltrest = al*np.power(ilrest,2) - 2*np.asarray(al)*np.asarray(ilrest)*ilmax + lmax + np.power(ilmax,2)*al
    lt = np.concatenate((lt17, ltrest))
    ratio = wt/lt

    return ratio, lt
