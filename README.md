## Description
The present study relies on a newly developed maize architectural model coupled with the Caribu algorithm (Chelle and Andrieu, 1998), the latter including ray-tracing and nested radiosity methods to simulate light regime over 3D scenes. 

The architectural model, detailed along given code/functions, coupled with the Caribu algorithm is called CORNIBU, and is publicly accessible via : https://www.sciencedirect.com/science/article/pii/S0168169924010858?ref=pdf_download&fr=RR-2&rr=93e7dc8d99740d80

CORNIBU -contraction of Corn-Caribu (Chelle et al. 1998)- allows to simulate the 3D architectural canopy structure of maize plants and renders light interception.

<div align="center">

![CORNIBU.png](CORNIBU_Panel_files/CORNIBU.png)

</div>

## 📝 Citing

If you find this work useful in your research, please consider citing paper :

Identifying maize architectural ideotypes through 3D structural model validated in the field: Assessing the impact of plant architecture and sowing pattern to improve canopy light regime 

Mario Serouart, Raúl López-Lozano, Brigitte Escale, Maëva Baumont, Jean-Charles Deswarte, Lucas Samatan Bernigaud, Marie Weiss and Benoit de Solan. Computers and Electronics in Agriculture.
https://doi.org/10.1016/j.compag.2024.109694

The model is under the CC-BY licence. 
This repository is under the MIT licence

## ⏳ Quick start

```python
from CORNIBU import CORNIBU

dist_func = 'gausshyper'
loc = -7.67
scale = 97.67
args = [1.52,0.79,0.51,1.16]

CORNIBU.CORNIBU(T = 1000, To = 0, DTc = 50, DTs = 1200, S_max = 0.6, N_max = 16, H_max = 2.5, inter_rang = 0.6, density = 9, 
        incli_top = 15, incli_base = 45, l = 0.5, delta = 115, 
        phyllotactic_angle = 180, phyllotactic_deviation = 25, 
        loc = loc, scale = scale, arg = args, dist = dist_func,
        Caribu = True, vizu = True, mode = 'direct', norm = False, DOY = 175, latitude = 43, mode_AgriPV = True)

Expected Console
✅ .txt Scene File created successfully at: /Users/home/Downloads/corn/OOO.txt
✅ .can File created successfully at: /Users/home/Downloads/corn/OOO_CAN.can
✅ .opt File saved successfully at: /Users/home/Downloads/corn/par_panel.opt
✅ Direct light processed ...
✅ ...and displayed
```

![Screenshot 2025-05-11 at 12.11.34.png](<CORNIBU_Panel_files/Screenshot 2025-05-11 at 12.11.34.png>)

Allow wireframe in Mesh #1 panel

Then play with vmax value to calibrate color map/scale : Note if you do want to normalize [0;1] set norm argument of function to "y"

If plot interactive diplay issues : downgrade your widget notebook in VS Code : pip install -U ipywidgets==7.7.1

![Screenshot 2025-05-11 at 12.20.31.png](<CORNIBU_Panel_files/Screenshot 2025-05-11 at 12.20.31.png>)

## Inputs

```python
# T, To, DTc, DTs : Parameters linked to Growing Degree Days and coded to be
#                   integrated to a true FSPM (change size/shape organs according to GDDs). 
#                   This feature is not applied in this repo.

# S_max : Maximum leaf area (one-sided) per plant, in m²
# N_max : Maximum number of leaves, no units
# H_max : Maximum plant height, and therefore whole canopy, in m
# inter_rang : Row spacing, in m
# density : Plant density, in plt.m-²
# incli_top : Inclination angle at insertion of the top leaf, in degrees, range [0:90]
# incli_base : Inclination angle at insertion of the base leaf, in degrees, range [0:90]
# l : Relative leaf length at which inflection point in inclination occurs, no units, range [0:1]
# delta : Difference in inclination between the insertion point and the tip of the base leaf, in degrees, range [0:180/240]
# loc, scale, arg, dist(_func) : Mean plant azimuth relative to rows direction, in degrees, range [0:90] | Type of law, and prameters
# phyllotactic_angle : Standard deviation of individual leaves orientation against mean plant azimuth, in degrees, range [0:90] 
# phyllotactic_deviation : Standard deviation of mean plant azimuth, in degrees, range [0:90] 
        
# Caribu : Activate Ray-Tracing, not just scene/canopy mock-up construction, boolean
# vizu : Activate Scene Display, not just scene/canopy mock-up construction + Raytracing light interception, boolean
# mode : Type of illumination environnement, either 'direct' or 'difuse'
# norm : Normalize the light values of facets, boolean
# DOY : Day Of the Year, it will define sun path and position within sky, in day, range [0:360]
# latitude : it will define sun path and position within sky, range The Earth
# mode_AgriPV : Feature added (not presented in the paper) showing how to add solar panel, in case of AgriPV simulations - Note also linked to .opt parameters
```

<div align="center">

![Maize Architectural Ideotypes.jpg](<CORNIBU_Panel_files/Maize Architectural Ideotypes.jpg>)

</div>

# Key Content
The present study/model relies on a newly developed maize architectural model coupled with the Caribu algorithm (Chelle and Andrieu, 1998), the latter including ray-tracing and nested radiosity methods to simulate light regime over 3D scenes. The architectural model is detailed along the following publication : **Identifying maize architectural ideotypes through 3D structural model validated in the field: Assessing the impact of plant architecture and sowing pattern to improve canopy light regime.** https://doi.org/10.1016/j.compag.2024.109694

The maize 3D architecture model used in this study simulates different structural characteristics of maize plants: leaves shape and dimensions, leaves inclination and curvature, insertion height and plant/leaves orientation. Compared to previous models (Fournier and Andrieu, 1998, España et al., 1998, López-Lozano et al., 2007), this new one presents a good compromise between details in describing architectural characteristics (like leaves orientation, not sufficiently considered in previous models) while keeping a reduced number of input variables accessible from field measurements.

A whole complete sensitivity analysis concerning the CORNIBU accuracy -faced to actual maize hybrids in fields- is available in the given paper.
Briefly, digital canopies of five maize hybrids grown under different sowing patterns in Southwest France field trial were validated by comparing computed and actual daily 𝑓𝐼𝑃𝐴𝑅 values, and showed a satisfactory fit (𝑅² ∼ 0.6).
Even moren than 0.6, actually, based on not yet published works.

# Available files

| Files      | Description           | 
| :------------- |:-------------|
| requirements.txt    | Python environnement to install. Note you may encounter stability issues with openalea dependencies. | 
| README.md  | Notebook of the given CORNIBU model. | 
| Cornibu_Documentation.pdf | Explained code of CORNIBU model.  | 
| CanestraDoc.pdf     | Copy of Caribu (Chelle et al. 1998) documentation and explanation of optical properties parameters. | 
| Folder functions  | utils functions |

# Known issues

This model was tested on linux (several times, Ubuntu versions, etc...) and MacOS.

Under MacOS, please use this type of command in bash to create env or install packages in it.
```python
CONDA_SUBDIR=osx-64 conda install openalea.plantgl openalea.deploy openalea.visualea -c fredboudon -c conda-forge
```
Also, concerning resolution : how much final mesh is realistic | Depending of number of facets.
MacOS may have difficulties rendering in Web-based display. Increase number of given line in 'loop_all_leaves,py' function to deal with.


```python
# Small snippet to convert file to .obj and display it under Blender or POVRay.

def txt_triangles_to_obj(txt_path, obj_path):
    with open(txt_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    vertices = []
    faces = []

    for i in range(0, len(lines) - 2, 3): 
        try:
            v1 = tuple(map(float, lines[i].split()))
            v2 = tuple(map(float, lines[i+1].split()))
            v3 = tuple(map(float, lines[i+2].split()))
        except ValueError:
            continue  

        vertices.extend([v1, v2, v3])
        base_index = len(vertices)
        faces.append((base_index - 2, base_index - 1, base_index))

    with open(obj_path, 'w') as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {face[0]} {face[1]} {face[2]}\n")

txt_triangles_to_obj("/Users/home/Downloads/corn//OOOC.txt", "/Users/home/Downloads/corn//OOOC.obj")
```

![Screenshot 2025-05-11 at 18.08.44.png](<CORNIBU_Panel_files/Screenshot 2025-05-11 at 18.08.44.png>)


```python
from CORNIBU import CORNIBU

dist_func = 'gausshyper'
loc = -7.67
scale = 97.67
args = [1.52,0.79,0.51,1.16]

CORNIBU.CORNIBU(T = 1000, To = 0, DTc = 50, DTs = 1200, S_max = 0.6, N_max = 16, H_max = 2.5, inter_rang = 0.6, density = 9, 
        incli_top = 15, incli_base = 45, l = 0.5, delta = 115, 
        phyllotactic_angle = 180, phyllotactic_deviation = 25, 
        loc = loc, scale = scale, arg = args, dist = dist_func,
        Caribu = True, vizu = True, mode = 'direct', norm = False, DOY = 175, latitude = 43, mode_AgriPV = True)
```
