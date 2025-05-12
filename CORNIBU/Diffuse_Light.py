
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


def Diffuse_Light(path, overcast, norm, can, BBox, vizu):  # Diffuse radiation
    # 20 solid angle sectors (five zenith angles) | Each sky sector was weighted according to the standard overcast sky (UOC) radiation distribution

    opts =  [path]

    sky_string = GetLight.GetLight(GenSky.GenSky()(1, overcast, 4, 5))      # (Energy, soc/uoc, number of azimuths, number of zeniths)

    sky = []
    for string in sky_string.split('\n'):
        if len(string) != 0:
            string_split = string.split(' ')
            t = tuple((float(string_split[0]), tuple((float(string_split[1]), float(string_split[2]), float(string_split[3])))))
            sky.append(t)

    cs = CaribuScene(scene=can, light=sky, opt=opts, scene_unit='m', pattern=(BBox[0], BBox[1], BBox[2], BBox[3])) 
    raw, agg = cs.run(infinite = True, direct = True)

    scene,values = cs.plot(raw['par_panel']['Ei'], display=False)
    print("✅ Diffuse light processed ...")

    if norm == False :    # Normalize energy values in scene
        v99 = np.percentile(values, 99)
        nvalues=np.array(values)
        nvalues[nvalues>v99]=v99
        values = nvalues.tolist()

    if vizu == True :    # Display scene + values if vizu 
        display(PlantGL(scene, group_by_color=False, property=values)) #, direction=[0,0,0]))

        # Save a moving scene in .html

        # data = PlantGL(scene, group_by_color=False, property=values, mode = 'diffuse', direction=[0,0,0])).get_snapshot()    
        # with open('/home/capte-gpu-2/Downloads/snapshot_standalone.html', 'w') as f:
        #     f.write(data)

    print("✅ ...and displayed")
    return ""

