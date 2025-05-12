
from alinea.caribu.CaribuScene import CaribuScene
from alinea.caribu.sky_tools import GenSky, GetLight, Gensun, GetLightsSun
from IPython.display import display
from openalea.plantgl.all import *
from oawidgets.plantgl import PlantGL

from alinea.caribu.CaribuScene import CaribuScene
from alinea.caribu.data_samples import data_path
from alinea.caribu.sky_tools import GenSky, GetLight, Gensun, GetLightsSun
import numpy as np
from oawidgets.plantgl import *
from IPython.display import display
from openalea.plantgl.all import *
from oawidgets.plantgl import PlantGL

def Direct_Light(path, norm, DOY, latitude, can, BBox, vizu, hour_start, hour_end):   # Direct radiation

    opts =  [path] 

    # Creates sun
    energy = 1              # PAR | Q | Irradiance
    DOY = DOY               # Day Of Year
    latitude = latitude     # Lat.

    for i in range(hour_start, hour_end) : #range(5,20)  # Hours concerned

        getsun = GetLightsSun.GetLightsSun(Gensun.Gensun()(energy, DOY, i, latitude)).split(' ')  # Sun position according to hour, day, Lat., energy
        sun = tuple((float(getsun[0]), tuple((float(getsun[1]), float(getsun[2]), float(getsun[3])))))

        ### ROTATION SUN PATH TO SIMULATE EXPERIMENT WITH DIFFERENT ROW DIRECTION (IN FIELD) FACED TO NS DIRECTION ###
        # theta_z = np.deg2rad(-42)
        # Rz = np.array([[np.cos(theta_z), -np.sin(theta_z), 0],
        #             [np.sin(theta_z), np.cos(theta_z), 0],
        #             [0, 0, 1]])
        # sun = np.array(sun[1]).dot(Rz)
        #################
    
        cs = CaribuScene(scene=can, light=[sun], opt=opts, pattern=(BBox[0], BBox[1], BBox[2], BBox[3]))  
        raw, agg = cs.run(infinite = True, direct = True) 
        scene,values = cs.plot(raw['par_panel']['Ei'], display=False)

        print("✅ Direct light processed ...")

        if norm == False :   # Normalize energy values in scene
            v99 = np.percentile(values, 99)
            nvalues=np.array(values)
            nvalues[nvalues>v99]=v99
            values = nvalues.tolist()
        
        if vizu == True :
            display(PlantGL(scene, group_by_color=False, property=values))

            # Save a moving scene in .html

            #data = PlantGL(scene, group_by_color=False, property=values).get_snapshot()    #direction = [sun[1][0], sun[1][1], sun[1][2]]                            # Save a moving scene in .html
            #with open('/Users/home/Downloads/corn/snapshot_standalone.html', 'w') as f:
            #    f.write(data)
    print("✅ ...and displayed")
    return ""

