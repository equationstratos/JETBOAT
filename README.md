# 🚤 JETBOAT — Visualiseur 3D RC Mini Jet Boat

Visualiseur 3D interactif du **RC Mini Jet Boat** conçu par [jtronics](https://cults3d.com/en/users/jtronics/creations).

**Live demo** → [https://equationstratos.github.io/JETBOAT/](https://equationstratos.github.io/JETBOAT/)

![preview](https://img.shields.io/badge/Three.js-0.170-black?logo=threedotjs) ![license](https://img.shields.io/badge/models-jtronics-blue)

## Fonctionnalités

| Mode | Description |
|------|-------------|
| **Assemblé** | Vue complète avec matériaux PBR |
| **Éclaté** | Slider pour écarter toutes les pièces |
| **Build pas-à-pas** | 9 étapes d’assemblage avec highlight de la pièce courante |
| Arbre d’assemblage | Afficher / masquer chaque pièce individuellement |
| Mode filaire + arêtes | Inspection CAO |
| Auto-rotation | Présentation continue |
| Vues prédéfinies | ISO, dessus, dessous, faces, reset |
| Bilingue | FR / EN |

## Lancer localement

```bash
# n’importe quel serveur statique
python -m http.server 8000
# ou
npx serve .
```

Puis ouvrir http://localhost:8000

Sous Windows : double-cliquer `lancer_visualiseur.bat` ou `lancer_visualiseur.ps1`.

## Structure du dépôt

```
JETBOAT/
├── index.html                 # Visualiseur Three.js (STLLoader)
├── README.md
├── readme.txt                 # Guide original jtronics (montage + BOM)
├── lancer_visualiseur.bat
├── lancer_visualiseur.ps1
├── boat_hull.STL              # Coque principale (~15 MB)
└── models/
    ├── boat_cover.STL
    ├── boat_trim_15.STL
    ├── boat_trim_20.STL
    ├── jet_stator.STL
    ├── jet_propeller.STL
    ├── jet_nozzle.STL
    ├── rc_mount.STL
    └── servo_clevis.STL
```

> Les positions d’assemblage dans le visualiseur sont approximatives  
> (les STL d’origine sont orientés pour l’impression 3D, pas pour un assemblage CAO unique).  
> Tu peux les affiner dans `index.html` (tableau `PARTS`).

## Guide de montage (extrait de readme.txt)

**Taille** : 230 × 75 × 50 mm (avec stator + tuyère)  
**Imprimante** : hauteur de construction > 200 mm  
**Matériau** : PLA (0,10 – 0,20 mm, couches adaptatives recommandées)

### Visserie & composants

| Qté | Élément |
|-----|---------|
| 6× | Vis sans tête M2×3 (hélice, servo) |
| 6× | Vis inbus M2×8 (tuyère, huile) |
| 10× | Vis inbus M2×6 (couvercle, servo, électronique, moteur) |
| 2× | Vis inbus M1.6×5 |
| 6× | Inserts laiton M2×3 (chauffants) |
| 1× | Joint mousse 2×200 mm (étanchéité couvercle) |
| 2× | Accu 18650 3400 mAh |
| 1× | ESC Littlebee 20A PRO |
| 1× | BEC RECOM 7850-1.0 |
| 1× | Moteur DYS BE1806 2300KV (ou équivalent Ø≤23 mm) |
| 1× | Arbre moteur 2×30 mm + tige 2×100 mm + coupleur |
| 1× | Roulement laiton 52B / MR25ZZ |
| 1× | Servo GS-2502 + tige 1 mm |

### Étanchéité

Oui, le bateau est étanche si l’impression de la coque est bonne.  
Le joint d’arbre est réalisé par deux paliers + graisse.  
Le couvercle est scellé par le cordon de mousse 2 mm.  
Pour plus de sécurité : fine couche de vernis voiture transparent.

### Vidéos jtronicsTV

- [Assembly](https://youtu.be/0LeV_MzVAqY)
- [Testing](https://youtu.be/blHpChrLmPY)
- [Sunny day run](https://youtu.be/IM1e0pq5acY)
- [Underwater test](https://youtu.be/qFJwZhQA2NM)

## Crédits

- **Modèles 3D** : [jtronics](https://cults3d.com/en/users/jtronics) — tous droits réservés  
- **Visualiseur** : equationstratos — fourni à des fins éducatives et de visualisation  
- Site original : [jtronics.de](http://www.jtronics.de/3ddruck/3d-druck-rc-mini-jet-boot/)

## Licence

Les fichiers STL restent la propriété de jtronics.  
Ce dépôt et le code du visualiseur sont fournis « as-is » pour usage personnel / éducatif.
