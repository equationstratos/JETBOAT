# 🚤 JETBOAT — Visualiseur 3D RC Mini Jet Boat

Visualiseur 3D interactif du **RC Mini Jet Boat** conçu par [jtronics](https://cults3d.com/en/users/jtronics/creations).

**Live demo** → [https://equationstratos.github.io/JETBOAT/](https://equationstratos.github.io/JETBOAT/)

![preview](https://img.shields.io/badge/Three.js-0.170-black?logo=threedotjs) ![license](https://img.shields.io/badge/models-jtronics-blue)

## Fonctionnalités

Au chargement, **les 70 pièces sont posées à plat sur le plan de travail**.
Le bouton **Assembler** les fait converger vers leur position de montage,
dans l’ordre du montage réel ; **Démonter** rejoue l’animation à l’envers.

| Commande | Description |
|------|-------------|
| **Guide pas-à-pas** | 19 étapes, chacune avec sa fiche, sa nomenclature et son angle de caméra |
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
│   ├── case_gen.py            # ancienne boîte à jupe (conservée pour mémoire)
│   └── rugged_box.py          # Génère la boîte Rugged Box par CSG (trimesh + manifold3d)
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
    ├── Rugged_Box_Parametric_V2.step   # boîte d'origine (fournie), 128.5 × 92.5
    ├── case_base.STL          # bac de la boîte
    ├── case_lid.STL           # couvercle de boîte
    ├── case_tray.STL          # tiroir de rangement amovible
    ├── case_gasket.STL        # joint plat (TPU)
    └── case_latch.STL         # loquet, pièce d'origine reprise telle quelle
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
| 4 bossages Ø3.25, entraxes 45 / 50 mm, dessus à `Y = 39.80` (arrière) et `44.26` (avant) | inserts + vis du couvercle |
| 2 bossages Ø3.25 sur l’axe, entraxe 40 mm, dessus à `Y = 29.4` | inserts + vis du support électronique |
| 2 plots de 8.5 mm de large, centrés sur l’axe, entraxe 19.5 mm, à `Y = 31.57` | tablette + vis du servo |
| Traverses de la platine, dessous à `Y = 32.57` sur les bacs et `29.40` sur l’axe | passage des accus sous la plaque |
| 2 × 2 perçages M2 en bas du tableau, entraxe 6 mm | trims (absents de la partlist) |
| 2 trous Ø2.6 à `X = 39 / 55`, `Z = 106`, entraxe **16 mm** | vis + platine du moteur |
| 2 gouttières Ø18.68 (!), axes `(25.90, 22.72)` et `(68.10, 22.72)` | logement des accus 18650 |
| Épaulement moulé dans la gouttière à `Z = 10.72` | butée arrière des accus |
| Chambre Ø2.78 de `Z = 58` à `76`, sièges Ø5 aux extrémités | 2 paliers laiton + graisse |
| Trou Ø1.8 à `(47, 25.57, 74.3)`, débouchant dans cette chambre | vis d’huile M2×8 |
| Passage Ø2.25 du tableau arrière à `(37.2, 33.4)` | tube laiton + tringle de servo |
| 3 trous M2 à R16 autour de l’axe du jet | vis M2×8 du stator |
| 2 × 2 trous M2 en bas du tableau, entraxe 6 mm | trims |

Trois recoupements valident le calage : l’entraxe moteur relevé fait
**exactement 16 mm**, la cote « vis 16 mm » de la partlist ; le diamètre des
deux gouttières fait **Ø18.68 mm**, soit le diamètre d’un 18650 ; et la tige
Ø2×100 couvre exactement la distance accouplement → impulseur.

**Accus et couplage 2S** : les gouttières sont ouvertes vers le haut sur 135°
(on y clipse la cellule par le dessus). Les cellules passent **sous la platine
électronique** : celle-ci s’arque au-dessus des deux bacs, son dessous y
remontant à `Y = 32.57` quand il est à `29.40` sur l’axe. Le haut des cellules
est à `32.02` — elles affleurent la bordure de la plaque, avec 0.55 mm de jeu.

Vers l’avant la gouttière n’a pas de mur : elle se referme peu à peu. Un tir de
rayons sur le cercle `Ø18.6` place la vraie butée du corps à `Z = 106.05`. Les
cellules y sont poussées à 1 mm près : corps bâbord jusqu’à `104.70`, tribord
jusqu’à `105.50`. Elles sont posées **tête-bêche**, comme l’exige un
montage 2S (7.4 V pour l’ESC et le BEC RECOM) : liaison série à l’avant, fils
de sortie à l’arrière.

Le couplage est modélisé : une barrette soudée sur chacun des quatre pôles, la
liaison série à l’arrière et les deux fils de sortie à l’avant, vers l’ESC. La
liaison série n’est pas une barrette droite — **elle passerait en plein dans le
tunnel du jet** — mais un fil qui l’enjambe, au plus près à 0.7 mm de la paroi.

**Portée du capot** : elle **n’est pas horizontale**. Le dessus des bossages
arrière est à `Y = 39.80`, celui des bossages avant à `Y = 44.26` — 4.46 mm sur
88.2 mm d’entraxe, soit une pente de **2.90° nez en l’air**. Le capot et son
cordon de mousse reçoivent cette inclinaison ; posés à plat, ils s’enfonçaient
jusqu’à 11 mm dans le pont vers l’étrave.

**Cordon de mousse** : son tracé est le contour de la portée du capot rentré de
**6.0 mm**. À 2.4 mm — le tracé précédent — il passait en plein sur les quatre
vis M2 du capot (0.3 mm de leurs axes) et son axe était 0.94 mm *dans* la
matière du rebord. À 6.0 mm il repose exactement sur le fond de feuillure —
écart mesuré `0.00` à `0.06` mm sur 144 points — et laisse 3.87 mm entre son axe
et l’axe des vis, soit 0.5 mm entre le cordon et le lamage `Ø4.7`. La feuillure
n’accepte le cordon qu’entre 5.0 et 6.4 mm de retrait : au-delà il retombe dans
la matière des bossages. Périmètre **273 mm**, pour un cordon fourni en
2×200 mm.

**Servo** : le GOTECK GS-2502 mesure **16.0 × 8.0 × 20.0 mm** (2.2 g). Il est
**couché sur le flanc** : longueur dans la longueur du bateau, hauteur en
travers, épaisseur à la verticale.

Sa baie **n’est pas une tablette pleine**. Ce sont **quatre nervures de
0.7 mm** — `x = 42.75-43.45`, `45.30-46.00`, `47.00-47.70`, `50.55-51.25` —
qui montent du toit du tunnel d’arbre, à `y = 23.55`, jusqu’à `y = 31.57`, sur
`z = 35.05` à `59.55`. Posé dessus, le servo reste perché 8 mm trop haut ;
c’est pour cela que **jtronics les coupe au cutter dans sa vidéo de montage**.

`tools/hull_servo_pocket.py` fait la même chose sur le maillage : il retire
**383 mm³** de nervure sur les 16.6 mm du boîtier et écrit
`models/boat_hull_cut.STL`, que charge le viewer. `boat_hull.STL`, le fichier
d’origine, n’est pas touché. Les talons avant et arrière subsistent : ils
calent le servo en longueur et portent les deux vis M2×6. Le boîtier repose
alors sur le toit du tunnel et **son dessus affleure ces talons — 31.55 pour
31.57**. Collision servo / coque après perçage : **0.00 mm³**.

Ses **languettes d’origine sont coupées** : c’est ce qui permet au boîtier de
descendre entre les plots. Les deux vis M2×6 ne le vissent donc pas — elles
l’encadrent et le calent. Le calcul tombe juste : les deux vis Ø2 sont à
`Z = 37.3` et `56.8`, soit 17.5 mm d’écart libre, pour un boîtier de 16 mm.
0.75 mm de jeu de chaque côté.

Deux réserves, à ne pas prendre pour des cotes relevées :

- **Vis M2×8** : la partlist en annonce 6 mais n’en détaille que 4
  (3 stator + 1 huile). Seules ces 4 sont placées.
- **Position de l’ESC, du BEC et du récepteur** : la coque n’a pas de logement
  dédié pour ces trois éléments. Ils sont posés sur la platine aux bonnes
  dimensions, mais à un emplacement **indicatif**. Tout le reste — accus,
  moteur, servo, transmission, visserie — est calé sur des relevés.

## Boîte de transport / de vente

La boîte reprend le dessin **« Rugged Box Parametric V2 »** fourni par
l’utilisateur — `models/Rugged_Box_Parametric_V2.step`, une boîte à charnière
et à loquets de 128.5 × 92.5 × 35.8 mm. Elle est trop petite pour le bateau ;
`tools/rugged_box.py` la **reconstruit à la bonne taille en conservant sa
section et ses interfaces**, mesurées une à une sur le STEP :

| Relevé sur le STEP | Valeur | Repris |
|---|---|---|
| Paroi | 2.40 mm | oui |
| Congés | 7.4 ext. / 5.0 int. | oui |
| Chanfrein de pied | 2.9 sur 4.0 | oui |
| Lèchefrite du bord | +1.86, de −4.4 à −2.4 sous le plan de joint | oui |
| Rainure de joint | 1.8 de large, offsets −1.17 / +0.63 | largeur oui, **profondeur portée à 4.45** |
| Languette du couvercle | 1.34 de large, 3.4 de haut | oui |
| Charnière | alésage Ø3.4, axe à +5.5 hors paroi, au plan de joint, noeuds de 6.2 | oui |
| Loquet | montants de 3.2, passage 23.6, saillie 8.86, alésage Ø3.3 à −7.9 | oui |
| Gâche | alésage Ø3.3 au plan de joint, +4.74 hors paroi | oui |

La seule cote modifiée est la **profondeur de rainure** : à 2.2 mm, la
languette de 3.4 du modèle d’origine ne rentrait pas dans sa propre rainure. À
4.45 il reste 1.05 mm sous la languette quand les deux plans de joint portent
l’un sur l’autre — le joint plat de 1.4 y est comprimé de 25 %.

Le **loquet est la pièce du fichier d’origine, reprise telle quelle**
(`case_latch.STL`, 23.2 × 8.8 × 31.1 mm) : ce sont ses deux alésages qui ont
servi à coter l’interface. Sa cinématique en position fermée n’a pas été
vérifiée et reste à valider sur un tirage d’essai.

### Les pièces

| | Emprise | Matière | Hauteur |
|---|---|---|---|
| `case_base.STL`   | 246.8 × 156.3 mm | ≈ 256 cm³ | 49.5 mm |
| `case_lid.STL`    | 246.8 × 155.5 mm | ≈ 160 cm³ | 29.1 mm |
| `case_tray.STL`   | 237 × 38.6 mm    | ≈ 38 cm³  | 17 mm |
| `case_gasket.STL` | 243.7 × 139.7 mm | ≈ 1.5 cm³ | 1.4 mm (à tirer en TPU) |
| `case_latch.STL`  | 23.2 × 8.8 mm    | ≈ 2.8 cm³ | 31.1 mm (×2) |

Les quatre pièces générées sont **étanches au sens maillage**. Quincaillerie :
un axe **Ø3 × 214 mm** pour la charnière, deux **Ø3 × 32 mm** pour les loquets.

### Intérieur et rangements

- **Chenal du bateau** 92 mm, avec **trois berceaux découpés d’après les
  sections réelles de la coque** — le profil est relevé dans `boat_hull.STL`
  aux trois stations puis soustrait de la traverse avec 1.5 mm de jeu.
- **Quatre cases cloisonnées** le long du flanc (39.6 mm de large, 18 mm de
  profondeur) pour les accessoires.
- **Un tiroir amovible** de six cases par-dessus, posé sur le dessus des
  cloisons à 21 mm du fond, avec deux prises de doigt. Il ne couvre que la
  bande de rangement : au-dessus du bateau il n’y a pas la hauteur.
- Nervures extérieures sur les quatre faces, patins et empreintes de gerbage,
  cartouche d’étiquette en creux (160 × 64 mm) sur le dessus.

Le bateau assemblé mesure **230.5 × 80.8 × 50.5 mm** (tuyère à `Z = -130.5`,
étrave à `+100`). Une fois posé sur ses berceaux il occupe, dans le repère de
la boîte, `x = ±115.2`, `y = -63.6 à 17.1`, `z = 10.8 à 61.4`. Marges mesurées :

| | Marge |
|---|---|
| Arrière / avant | 3.8 mm |
| Bâbord / tribord | 5.7 mm |
| Sous les nervures du couvercle | 0.6 mm |

L’interférence entre le bac et le couvercle fermé a été calculée par booléen :
**0.0000 cm³**. Hauteur fermée **70.4 mm**.

**Impression** : les deux coques s’impriment sans support, le bac ouverture
vers le haut, le couvercle retourné (dessus sur le plateau). L’emprise de
246.8 × 156.3 mm demande un plateau de 250 × 160, ou 250 × 250 en diagonale.

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
