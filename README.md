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
| **Guide pas-à-pas** | 16 étapes, chacune avec sa fiche, sa nomenclature et son angle de caméra |
| **Assembler / Démonter** | Animation de montage, pièce par pièce |
| **Progression** | Curseur pour parcourir le montage image par image |
| **Éclatement** | Écarte les pièces depuis le bateau monté |
| Inventaire | Afficher / masquer chaque ligne de nomenclature, avec quantités |
| Filaire | Inspection CAO |
| Auto-rotation | Présentation continue |
| Plan de travail | Grille de la table de montage |
| Hélice animée | L’impulseur tourne une fois le bateau monté |
| Panneau rétractable | Chevron en haut à gauche, ou touche <kbd>P</kbd> — replié d’office sous 720 px |
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
├── tools/
│   └── case_gen.py            # Génère la boîte par CSG (trimesh + manifold3d)
└── models/
    ├── boat_cover.STL         # capot plat, utilisé par le visualiseur
    ├── boat_cover_turn.STL    # capot bombé, variante 27 mm
    ├── boat_trim_15.STL
    ├── boat_trim_20.STL
    ├── jet_stator.STL
    ├── jet_propeller.STL
    ├── jet_nozzle.STL
    ├── rc_mount.STL
    ├── servo_clevis.STL
    ├── case_base.STL          # bac de rangement
    └── case_lid.STL           # couvercle de boîte
```

> **Deux capots.** `boat_cover.STL` est le capot **plat** (11.2 mm de haut,
> 15.6 cm³) : c’est celui que charge le visualiseur. `boat_cover_turn.STL` est
> la variante **bombée** (27.2 mm, 25.0 cm³). Les deux n’ont pas le même
> repère : le calage du visualiseur est relevé sur les perçages du capot plat.
> Le choix n’est pas cosmétique — le capot plat ne laisse que **12.9 à 14.9 mm**
> au-dessus de la tablette du servo, contre 27 pour le bombé, ce qui contraint
> la hauteur du servo et impose de coucher le BEC.
> L’historique du dépôt contient aussi `boat_hull_without_batterymount.STL` et
> `jetboat_ikea_mount.STL`, non restaurés.

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
| 2 plots de **8.5 mm de large**, centrés sur l’axe, entraxe 19.5 mm, à `Y = 31.57` | tablette + vis du servo |
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

**Servo** : la tablette est faite de **deux plots de 8.5 mm de large
exactement** — la largeur d’un servo 2 g —, centrés sur l’axe du bateau
(`X = 47`) et espacés de 19.5 mm dans la longueur. Le servo se pose donc
**debout entre les plots**, corps de 8.5 mm de large, pattes portant dessus,
arbre de sortie vertical : c’est la seule position où il ne déborde pas de son
support, et la seule qui garde les deux vis verticales.

Le capot **plat** ne laisse que 12.9 mm au-dessus des plots : le servo modélisé
est donc de faible hauteur (11.2 mm corne comprise). Un servo 2 g courant fait
~20 mm de haut et **ne passerait pas** sous ce capot — il faut soit un servo
extra-plat, soit le capot bombé.

Deux réserves, à ne pas prendre pour des cotes relevées :

- **Vis M2×8** : la partlist en annonce 6 mais n’en détaille que 4
  (3 stator + 1 huile). Seules ces 4 sont placées.
- **Position de l’ESC, du BEC et du récepteur** : la coque n’a pas de logement
  dédié pour ces trois éléments. Ils sont posés sur la platine aux bonnes
  dimensions, mais à un emplacement **indicatif**. Tout le reste — accus,
  moteur, servo, transmission, visserie — est calé sur des relevés.

## Boîte de rangement / de vente

Deux pièces imprimées, générées par CSG (`tools/case_gen.py`, trimesh +
manifold3d), toutes deux étanches au sens maillage :

| | Emprise | Matière | Hauteur |
|---|---|---|---|
| `case_base.STL` | 250 × 132 mm | ≈ 323 cm³ | 52 mm |
| `case_lid.STL`  | 250 × 132 mm | ≈ 207 cm³ | 38 mm |

- **Parois 3.2 mm**, fond 4 mm, angles arrondis R10, nervures verticales
  extérieures sur les quatre faces, colonnes d’angle renforcées.
- **Emboîtement** par une jupe de 8 mm sur le couvercle (jeu 0.4 mm), serrage
  par **4 vis M3×20** dans les angles, lamées côté couvercle.
- **Gerbable** : 4 patins sous le bac, 4 empreintes en face sur le couvercle.
- **Prises de main** en biseau auto-portant aux deux bouts.
- **Cartouche d’étiquette** en creux (150 × 56 mm) sur le dessus — c’est la
  face de vente du kit.
- **Intérieur** : un chenal de 94 mm pour le bateau et un compartiment latéral
  de 25 mm cloisonné en trois pour les accessoires.
- **Les trois berceaux sont découpés d’après les sections réelles de la
  coque** : le profil est relevé dans `boat_hull.STL` aux trois stations, puis
  soustrait de la traverse avec 1.4 mm de jeu.

L’intérieur (240 × 122 × 64 mm) est calé sur l’encombrement réel et non sur la
coque seule : la tuyère descend à `Z = -130.5` quand l’étrave s’arrête à
`+100`, soit 230.5 mm hors-tout. Il reste 4.7 mm de jeu à chaque bout, et 3 mm
au-dessus du capot plat.

**Impression** : les deux pièces s’impriment sans support, le bac ouverture
vers le haut, le couvercle retourné (dessus sur le plateau, pour que le
cartouche et les lamages sortent nets). L’emprise de 250 × 132 mm passe droit
sur un plateau 250 × 210 ; sur un 220 × 220, il faut l’orienter en diagonale.

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
