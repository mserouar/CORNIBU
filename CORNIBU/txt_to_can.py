import shutil
import numpy as np
from read_data import read_data

def txt_to_can(path, Leaf_Tri_Count, diff_stem_leaves, N_max) :

    with open(path + 'OOO.txt', 'r') as f_input, open(path + 'OOOC.txt', 'w') as f_output:
        for line in f_input:
            xyz = line.split()
            for triple in zip(xyz[0:3], xyz[3:6], xyz[6:9]):
                f_output.write(' '.join(triple) + '\n')

    data = read_data(path + "OOOC.txt")     # 3 rows : [1 vertex x 3 coordinates xyz]  

    shutil.copy(path + "OOOC.txt", path + "SOLAR" + ".txt") # TODO : To delete, no saving files

    a = []
    composite_list = [data[x:x + 3] for x in range(0, len(data), 3)]   # .can (Chelle) structure transformation | Please read CanestraDoc.pdf given in repo

    shutil.copy(path + "OOOC.txt", path + "OOOC.can") #
    text_file = open(path + "OOO_CAN.can", "w")

    Leaf = 1
    Plante = 1
    Stem = 1
    Stem_Tri = 1

    tri_counts = np.concatenate(Leaf_Tri_Count)
    for i in range(len(composite_list)):
        tri_type = 1 if i*3 < diff_stem_leaves else 2
        if tri_type == 2:
            if Stem_Tri == 5:
                Stem_Tri = 1
                Stem += 1
            id_str = '2' + str(Stem).zfill(5) + '00000' + str(Stem_Tri)
            Stem_Tri += 1
        else:
            if i != 0:
                if tri_counts[i] == 1:
                    Leaf += 1
                    if Leaf == N_max + 1:
                        Leaf = 1
                        Plante += 1
            id_str = '1' + str(Plante).zfill(5) + str(Leaf).zfill(3) + str(int(tri_counts[i])).zfill(3)
        with open(path + "OOO_CAN.can", "a") as text_file:
            exestr = 'p' + ' ' + '2' + ' ' + id_str + ' ' + '9' + ' ' + '3'
            for j in range(3):
                exestr += ' ' + str(composite_list[i][j][0]) + ' ' + str(composite_list[i][j][1]) + ' ' + str(composite_list[i][j][2])
            text_file.write(exestr + '\n')

    # Soil
    with open(path + 'OOO_CAN.can', 'r') as file:
        lines = file.readlines()
        last_lines = lines[-4:-2]
        modified_lines = []

        idx = 0
        for line in last_lines:
            elements = line.strip().split()

            if idx == 0 :
                    elements[2] = '300001000001'
            else : 
                    elements[2] = '300001000002'

            modified_line = ' '.join(elements) + '\n'
            modified_lines.append(modified_line)
            idx = idx + 1

        lines[-4:-2] = modified_lines
        with open(path + 'OOO_CAN.can', 'w') as file:
            file.writelines(lines)

    # PANEL
    with open(path + 'OOO_CAN.can', 'r') as file:
        lines = file.readlines()
        last_lines = lines[-2:]
        modified_lines = []

        idx = 0
        for line in last_lines:
            elements = line.strip().split()

            if idx == 0 :
                    elements[2] = '400001000001'
            else : 
                    elements[2] = '400001000002'

            modified_line = ' '.join(elements) + '\n'
            modified_lines.append(modified_line)
            idx = idx + 1

        lines[-2:] = modified_lines
        with open(path + 'OOO_CAN.can', 'w') as file:
            file.writelines(lines)

    return ""
