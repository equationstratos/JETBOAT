"""Ouvre la poche du servo dans la coque de jtronics.

La baie du servo n'est pas une tablette pleine : ce sont **quatre nervures de
0.7 mm** (x = 42.75-43.45, 45.30-46.00, 47.00-47.70, 50.55-51.25) qui montent
du toit du tunnel d'arbre, a y = 23.55, jusqu'a y = 31.57, sur z = 35.05 a
59.55. Posé dessus, le GS-2502 reste perche 8 mm trop haut.

Dans sa video de montage, jtronics **coupe ces nervures** pour que le nano
servo descende au fond de la baie. C'est exactement ce que fait ce script :
il retire la matiere sur l'emprise du servo (16 mm de long), en laissant les
talons avant et arriere, qui le calent en longueur et portent les deux vis
M2x6. Le servo repose alors sur le toit du tunnel a y = 23.55 et son dessus
affleure les talons a 31.55.

`boat_hull.STL` (le fichier d'origine) n'est pas touche : le resultat est
ecrit dans `models/boat_hull_cut.STL`, et c'est lui que charge le viewer.
"""
import os
import numpy as np, trimesh

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Emprise de la poche : la travee des quatre nervures, sur la longueur du
# boitier plus 0.3 mm de jeu a chaque bout.
X0, X1 = 42.0, 52.0
Y0, Y1 = 23.50, 31.62
Z0, Z1 = 38.75, 55.35

def pocket():
    b = trimesh.creation.box((X1 - X0, Y1 - Y0, Z1 - Z0))
    b.apply_translation(((X0 + X1)/2, (Y0 + Y1)/2, (Z0 + Z1)/2))
    return b

if __name__ == '__main__':
    H = trimesh.load(os.path.join(HERE, 'boat_hull.STL'))
    print('coque d\'origine : %d faces, etanche=%s, %.1f cm3'
          % (len(H.faces), H.is_watertight, H.volume/1000))
    cut = trimesh.boolean.intersection([H, pocket()])
    print('matiere retiree : %.1f mm3 (les quatre nervures sur 16.6 mm)'
          % (0 if cut is None or not len(cut.faces) else cut.volume))
    M = H.difference(pocket())
    if not M.is_watertight:
        M.fill_holes()
    M.fix_normals()
    print('coque percee    : %d faces, etanche=%s, %.1f cm3'
          % (len(M.faces), M.is_watertight, M.volume/1000))
    M.export(os.path.join(HERE, 'models', 'boat_hull_cut.STL'))
