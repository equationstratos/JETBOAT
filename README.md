# JETBOAT — Visualiseur 3D RC Mini Jet Boat

Visualiseur 3D interactif du **RC Mini Jet Boat** (jtronics), inspiré de [OPENDRONE](https://github.com/equationstratos/OPENDRONE).

## Fonctionnalités

- **Vue assemblée** : modèle complet avec matériaux PBR
- **Vue éclatée** : slider pour écarter les pièces
- **Build pas-à-pas** : 9 étapes d’assemblage avec mise en évidence de la pièce courante
- **Arbre d’assemblage** : afficher / masquer chaque pièce
- **Mode filaire**, auto-rotation, arêtes CAO
- **Vues prédéfinies** (dessus, dessous, faces, isométrie)
- **Bilingue** FR / EN
- **100 % offline** : Three.js et modèles GLB inclus

## Lancer le visualiseur

### Méthode simple
```bash
python -m http.server 8000
```
Puis ouvrir [http://localhost:8000](http://localhost:8000)

### Windows
Double-cliquer `lancer_visualiseur.bat` (ou `lancer_visualiseur.ps1`)

## Structure

```
JETBOAT/
├── index.html              # Visualiseur principal
├── README.md
├── lancer_visualiseur.bat
├── lancer_visualiseur.ps1
├── libs/three/             # Three.js local
└── models/                 # Pièces GLB (dérivées des STL jtronics)
    ├── boat_hull.glb
    ├── boat_cover.glb
    ├── jet_stator.glb
    ├── jet_propeller.glb
    ├── jet_nozzle.glb
    ├── boat_trim_15.glb / boat_trim_20.glb
    ├── rc_mount.glb
    ├── servo_clevis.glb
    └── boat_hull_seal.glb
```

## Modèle source

- **Auteur original** : [jtronics](https://cults3d.com/en/users/jtronics/creations)
- **Page produit** : [RC controlled Mini Jet Boat](http://www.jtronics.de/3ddruck/3d-druck-rc-mini-jet-boot/)
- Taille : ~230 × 75 × 50 mm (avec stator + tuyère)
- Matériau recommandé : PLA, couches 0,10–0,20 mm

### Visserie & pièces (extrait du readme original)
- 6× M2×3 (hélice, servo)
- 6× M2×8 (tuyère…)
- 10× M2×6
- Inserts M2×3, joint mousse 2 mm, etc.

Vidéos d’assemblage et tests : voir la chaîne YouTube jtronicsTV.

## Notes techniques

Les STL d’origine ont été convertis en GLB et simplifiés pour le web. Les positions d’assemblage sont approximatives (les fichiers d’origine sont orientés pour l’impression, pas pour un assemblage CAO unique). Vous pouvez affiner les offsets dans `index.html` (objet `ASSEMBLY`).

## Licence

Les modèles 3D restent la propriété de jtronics. Ce visualiseur est fourni à des fins éducatives et de visualisation.
