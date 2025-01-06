# CORNIBU

<div align="center">
  
![alt text](https://github.com/mserouar/CORNIBU/blob/main/CORNIBU.png)

</div>

# Description
CORNIBU -contraction of Corn-Caribu (Chelle et al. 1998)- allows to simulate the 3D architectural canopy structure of maize plants and renders light interception.

# Content
The present study/model relies on a newly developed maize architectural model coupled with the Caribu algorithm (Chelle and Andrieu, 1998), the latter including ray-tracing and nested radiosity methods to simulate light regime over 3D scenes. The architectural model is detailed along the following publication : Identifying maize architectural ideotypes through 3D structural model validated in the field: Assessing the impact of plant architecture and sowing pattern to improve canopy light regime.

The maize 3D architecture model used in this study simulates different structural characteristics of maize plants: leaves shape and dimensions, leaves inclination and curvature, insertion height and plant/leaves orientation. Compared to previous models (Fournier and Andrieu, 1998, España et al., 1998, López-Lozano et al., 2007), this new one presents a good compromise between details in describing architectural characteristics (like leaves orientation, not sufficiently considered in previous models) while keeping a reduced number of input variables accessible from field measurements.

A whole complete sensitivity analysis concerning the CORNIBU accuracy -faced to actual maize hybrids in fields- is available in the given paper.
Briefly, digital canopies of five maize hybrids grown under different sowing patterns in Southwest France field trial were validated by comparing computed and actual daily 𝑓𝐼𝑃𝐴𝑅 values, and showed a satisfactory fit (𝑅² ∼ 0.6).
Even moren than 0.6, actually, based on not yet published works.

# Available files

| Files      | Description           | 
| :------------- |:-------------|
| CORNIBU.yml    | Python environnement to install. Note you may encounter stability issues with openalea dependencies. | 
| CORNIBU_GITHUB.ipynb  | Notebook of the given CORNIBU model. | 
| Cornibu_Documentation.pdf | Explained code of CORNIBU model.  | 
| nir- and par.opt     | File parameters of optical properties for each optical species present in 3D mock-up -Leaf, Stem, Soil, AgriPV Panel, ...- . | 
| CanestraDoc.pdf     | Copy of Caribu (Chelle et al. 1998) documentation and explanation of optical properties parameters. | 
| fipar.html  | Output .html example. |


## Supplementary Materials
Note a supplementary folder called "Other features".

| Files      | Description           | 
| :------------- |:-------------|
| Folder Other features  | Possible extension of the crop 3D modeling work to other agricultural systems |

Simple considerations can be undertaken, in emerging domains, with very few modifications of this proposed model. 

Agrivoltaics systems hold promise, not only in broadening the diversity of our low-carbon energy mix, but also in its potential to increase energy production alongside agricultural yields. Another interesting aspect would be to provide shade and reduce water resource stresses.  
Therefore, by incorporating solar panels into modeled canopies, we can initiate studies in an agriphotovoltaic context. You have an example in ```_PANEL.ipynb``` where I've modeled a simple solar panel ofver canopy, and its given transmittance properties.


Another consideration, given the structural similarities between maize and sorghum as they belong to the same family, would be to establish a sorghum branch to CORNIBU code.  
The recent emergence of interest in sorghum, particularly in Europe, positions this species as a suitable candidate for studying climate change adaptation. Despite their close relation, maize and sorghum strongly differ agronomically, notably in their genetic potentials. Sorghum is reputed to be less input-intensive than maize and highly resilient to drought and high temperatures. According to Parent et al., sorghum has a reputation for being a highly drought-resistant cereal. This resilience is primarily attributed to its deep root system and the maintenance of stomatal conductance/photosynthesis under very unfavorable water potentials. Generally, it is considered more drought-tolerant than maize.  
Here, again, is available in ```_SORGHO.ipynb```, a dummy example of a sorghum canopy. 

Please note that this is based on nothing. Indeed, no fine parameters were used, to model shorgum canopy I just reduced height, distance between nodes, added more leaf curvature and added a full spheres panicle to let you see multiple simple CORNIBU adaptations.

<div align="center">
  
![alt text](https://github.com/mserouar/CORNIBU/blob/main/Oth_Features.png)

</div>



##  📑Licence <a name="licence"></a>
The model is under the CC-BY licence. 
This repository is under the MIT licence

## 📝 Citing

If you find this work useful in your research, please consider citing paper :

#### Identifying maize architectural ideotypes through 3D structural model validated in the field: Assessing the impact of plant architecture and sowing pattern to improve canopy light regime <a name="Paper"></a>

Mario Serouart, Raúl López-Lozano, Brigitte Escale, Maëva Baumont, Jean-Charles Deswarte, Lucas Samatan Bernigaud, Marie Weiss and Benoit de Solan. Computers and Electronics in Agriculture.
https://doi.org/10.1016/j.compag.2024.109694
