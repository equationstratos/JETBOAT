# 🚤 JETBOAT — Visualiseur 3D RC Mini Jet Boat

Visualiseur 3D interactif du **RC Mini Jet Boat** conçu par [jtronics](https://cults3d.com/en/users/jtronics/creations).

**Live demo** → [https://equationstratos.github.io/JETBOAT/](https://equationstratos.github.io/JETBOAT/)

![preview](https://img.shields.io/badge/Three.js-0.170-black?logo=threedotjs) ![license](https://img.shields.io/badge/models-jtronics-blue)

## Fonctionnalités

Au chargement, **les 54 pièces sont posées à plat sur le plan de travail**.
Le bouton **Assembler** les fait converger vers leur position de montage,
dans l’ordre du montage réel ; **Démonter** rejoue l’animation à l’envers.

| Commande | Description |
|------|-------------|
| **Assembler / Démonter** | Animation de montage, pièce par pièce |
| **Progression** | Curseur pour parcourir le montage image par image |
| **Éclatement** | Écarte les pièces depuis le bateau monté |
| Inventaire | Afficher / masquer chaque ligne de nomenclature, avec quantités |
| Filaire | Inspection CAO |
| Auto-rotation | Présentation continue |
| Plan de travail | Grille de la table de montage |
| Hélice animée | L’impulseur tourne une fois le bateau monté |
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
├── index.html                 # Visualiseur Three.js (STL + pièces paramétriques)
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

### Repère et positions d’assemblage

Chaque STL d’origine est exporté dans **son propre repère d’impression** (posé à plat,
coin de la boîte englobante à l’origine) : un simple `pos: [0,0,0]` empile toutes les
pièces au même endroit. Le tableau `PARTS` d’`index.html` contient donc, pour chaque
pièce, une **rotation** qui la remet dans le repère bateau et une **translation**
calculée sur ses vraies portées / perçages, mesurées dans les maillages :

| Repère monde | |
|---|---|
| `+X` | tribord |
| `+Y` | haut (quille à `Y = 0`) |
| `+Z` | proue (origine au milieu de la coque, longueur 200 mm) |

Références mesurées utilisées pour le calage :

- **Tableau arrière** : plan parfaitement vertical à `Z = −99.95`.
- **Jet** : les 3 perçages M2 du tableau arrière sont à R = 16 mm (±16 en X, +16 en Y)
  autour de l’axe du jet → le stator est retourné (`rot.x = π`) pour que sa 3ᵉ patte
  pointe vers le haut, bride plaquée sur le tableau arrière, tuyère vers l’arrière.
- **Tuyère** : rotule Ø 22.5 mm du stator centrée à `Z = −113.29` ; l’axe de pivot
  vertical de la tuyère et son bras de direction viennent dessus, le bras se retrouvant
  juste sous le passage de tringle Ø 2.25 du tableau arrière.
- **Impulseur** : Ø 19.5 mm dans le tunnel Ø ≈ 20 mm, ogive vers l’avant, pales au ras
  de l’entrée du stator.
- **Couvercle / support RC** : posés sur les bossages à inserts laiton de la coque
  (entraxes 45 / 50 mm pour le capot, 40 mm pour la platine), à `Y = 39.6` et `Y = 29.4`.
- **Trims** : vissés sur les 2 × 2 perçages M2 du bas du tableau arrière (entraxe 6 mm,
  inclinés à ~21.5°, l’angle de carène) ; `boat_trim_15` et `boat_trim_20` sont deux
  **variantes d’angle** de la même pièce — le visualiseur en montre une par bord, en
  vrai on imprime 2× la même.

Longueur totale obtenue coque + stator + tuyère : **230 mm**, conforme au readme
d’origine de jtronics.

### Nomenclature modélisée

Les 8 STL de jtronics ne couvrent que les pièces imprimées. La visserie,
la transmission et l’électronique de la partlist sont **générées
paramétriquement** dans `index.html` à leurs cotes réelles, et posées sur les
points de fixation relevés dans la coque :

| Point relevé dans `boat_hull.STL` | Sert à |
|---|---|
| 4 bossages Ø3.25, entraxes 45 / 50 mm, dessus à `Y = 39.6` | inserts + vis du couvercle |
| 2 bossages Ø3.25 sur l’axe, entraxe 40 mm, dessus à `Y = 29.4` | inserts + vis du support électronique |
| 2 trous Ø1.8 à `X = 48.6`, entraxe 19.5 mm, tablette à `Y = 31.57` | vis + pattes du servo |
| 2 trous Ø2.6 à `X = 39 / 55`, `Z = 106`, entraxe **16 mm** | vis + platine du moteur |
| 2 gouttières Ø18.68 (!), axes `(25.90, 22.72)` et `(68.10, 22.72)` | logement des accus 18650 |
| Chambre Ø2.78 de `Z = 58` à `76`, sièges Ø5 aux extrémités | 2 paliers laiton + graisse |
| Trou Ø1.8 à `(47, 25.57, 74.3)`, débouchant dans cette chambre | vis d’huile M2×8 |
| Passage Ø2.25 du tableau arrière à `(37.2, 33.4)` | tube laiton + tringle de servo |
| 3 trous M2 à R16 autour de l’axe du jet | vis M2×8 du stator |
| 2 × 2 trous M2 en bas du tableau, entraxe 6 mm | trims |

Trois recoupements valident le calage : l’entraxe moteur relevé fait
**exactement 16 mm**, la cote « vis 16 mm » de la partlist ; le diamètre des
deux gouttières fait **Ø18.68 mm**, soit le diamètre d’un 18650 ; et la tige
Ø2×100 couvre exactement la distance accouplement → impulseur.

**Accus** : les gouttières sont ouvertes vers le haut sur 135° (on y clipse la
cellule par le dessus) et fermées à l’arrière par le tableau, à `Z = 0.72` :
l’accu vient en butée sur ce fond, et occupe donc `Z = 2` à `67`.

**Servo** : il est **couché sur le flanc**, axe long selon la longueur du
bateau. C’est ce que montre la photo de montage de jtronics, et c’est la seule
orientation compatible avec les deux perçages relevés — ils sont distants de
19.5 mm *selon la longueur*, donc les pattes débordent à l’avant et à
l’arrière. L’arbre de sortie est de ce fait horizontal et pointe vers bâbord :
la corne balaie le plan vertical longitudinal et pousse la tringle d’avant en
arrière, jusqu’au passage Ø2.25 du tableau.

Deux réserves, à ne pas prendre pour des cotes relevées :

- **Vis M2×8** : la partlist en annonce 6 mais n’en détaille que 4
  (3 stator + 1 huile). Seules ces 4 sont placées.
- **Position de l’ESC, du BEC et du récepteur** : la coque n’a pas de logement
  dédié pour ces trois éléments. Ils sont posés sur la platine aux bonnes
  dimensions, mais à un emplacement **indicatif**. Tout le reste — accus,
  moteur, servo, transmission, visserie — est calé sur des relevés.

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
