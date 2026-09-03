"""Boite de transport / de vente du kit JETBOAT — « Rugged Box » agrandie.

Reprend le dessin de `models/Rugged_Box_Parametric_V2.step` (boite a charniere
et loquets, fournie par l'utilisateur) et le porte a la taille du bateau
assemble, 230.5 x 80.8 x 50.5 mm.

Cotes relevees sur le STEP d'origine (128.5 x 92.5 x 35.8) et conservees telles
quelles, pour que les loquets imprimes du modele d'origine restent compatibles :

    paroi 2.4        fond 2.4 (porte a 3.0 ici, la boite est 2x plus longue)
    conges  exterieur 7.4 / interieur 5.0
    chanfrein de pied   2.9 sur 4.0
    lechefrite du bord  +1.86, de -4.4 a -2.4 sous le plan de joint
    rainure de joint    1.8 de large, offsets -1.17 / +0.63
    languette du capot  1.34 de large, offsets -0.94 / +0.40, 3.4 de haut
    charniere    alesage 3.4, axe a +5.5 hors paroi, au niveau du plan de joint
                 noeuds de 6.2 de large, alternes bac / couvercle
    loquet       2 montants de 3.2, passage libre 23.6, saillie 8.86
                 alesage 3.3 a 7.9 sous le plan de joint, +4.36 hors paroi
                 gache du couvercle : alesage 3.3 au niveau du plan de joint,
                 +4.74 hors paroi

Seule la rainure est approfondie (4.45 au lieu de 2.2) : la languette du modele
d'origine fait 3.4 et ne rentrait pas dans sa propre rainure. A 4.45 il reste
1.05 sous la languette quand les deux plans de joint portent l'un sur l'autre :
le joint plat de 1.4 y est comprime de 25 %, ce qu'une mousse encaisse sans
prendre de deformation permanente.

Repere : X = longueur, Y = largeur, Z = hauteur ; boite centree en X et Y,
Z = 0 au plan de pose. Les deux pieces sont dans leur position d'impression
(bac ouverture en haut, couvercle retourne).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, trimesh
from shapely.geometry import Polygon
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- cotes
WALL, FLOOR = 2.4, 3.0
R_OUT       = 7.4                    # conge exterieur du donneur
CHAMF, CHAMF_H = 2.9, 4.0            # chanfrein de pied
LIP, LIP_A, LIP_B = 1.86, 4.4, 2.4   # lechefrite sous le plan de joint
GRV_I, GRV_O, GRV_D = -1.17, 0.63, 4.45   # rainure de joint
TNG_I, TNG_O, TNG_H = -0.94, 0.40, 3.4    # languette du couvercle
GASKET_T = 1.4

IN_L, IN_W  = 238.0, 134.0           # interieur du bac
OUT_L, OUT_W = IN_L + 2*WALL, IN_W + 2*WALL
BASE_CAV    = 40.0                   # profondeur utile du bac
ZR          = FLOOR + BASE_CAV       # plan de joint du bac
LID_TOP     = 3.0
LID_CAV     = 22.0
LID_H       = LID_TOP + LID_CAV      # plan de joint du couvercle

CHAN_W      = 92.0                   # chenal du bateau
DIV_T       = 2.4                    # cloisons
CRADLE_H    = 8.0                    # hauteur des berceaux
TRAY_Z      = 21.0                   # dessus des tasseaux du tiroir
TRAY_H      = 17.0

# charniere / loquets
HG_BORE, HG_Y, KNUCK = 3.4, 5.5, 6.2
LT_BORE, LT_Y, LT_Z  = 3.3, 4.36, 7.9
LT_POST, LT_GAP, LT_OUT = 3.2, 23.6, 8.86
LK_Y, LK_OUT, LK_W   = 4.74, 8.14, 17.4
LATCH_X = (-60.0, 60.0)

# --------------------------------------------------------- contour + normales
def outline(l, w, r, n_arc=16):
    """Rectangle a coins arrondis : centres d'arc + normales sortantes.
    Le contour decale de `off` vaut centre + (r + off) * normale — exact pour
    un convexe, et le nombre de points ne change pas avec l'offset."""
    cx, cy = l/2 - r, w/2 - r
    cen = [(cx, cy), (-cx, cy), (-cx, -cy), (cx, -cy)]
    P, N = [], []
    for k, c in enumerate(cen):
        for i in range(n_arc + 1):
            a = 0.5*np.pi*(k + i/n_arc)
            P.append(c); N.append((np.cos(a), np.sin(a)))
    P, N = np.array(P, float), np.array(N, float)
    keep = ~(np.all(np.isclose(P, np.roll(P, 1, 0)), 1) &
             np.all(np.isclose(N, np.roll(N, 1, 0)), 1))
    return P[keep], N[keep], r

BASE_P, BASE_N, BASE_R = outline(OUT_L, OUT_W, R_OUT)

def ring(off):
    return BASE_P + BASE_N * (BASE_R + off)

def loft(levels, cap=True):
    """Solide engendre par le contour, decale de `off` a la hauteur `z`."""
    rings = [np.c_[ring(o), np.full(len(BASE_P), z)] for z, o in levels]
    n, m = len(BASE_P), len(rings)
    V = np.vstack(rings); F = []
    for j in range(m - 1):
        a, b = j*n, (j+1)*n
        for i in range(n):
            i2 = (i + 1) % n
            F += [[a+i, a+i2, b+i2], [a+i, b+i2, b+i]]
    if cap:
        for j, sgn in ((0, -1), (m-1, 1)):
            c = len(V); V = np.vstack([V, [0, 0, levels[j][0]]])
            for i in range(n):
                i2 = (i + 1) % n
                F.append([c, j*n+i2, j*n+i][::sgn])
    M = trimesh.Trimesh(V, np.array(F), process=True)
    M.fix_normals()
    return M

def prism(off, z0, z1):
    return loft([(z0, off), (z1, off)])

def blk(x0, y0, z0, l, w, h):
    m = trimesh.creation.box((l, w, h))
    m.apply_translation((x0 + l/2, y0 + w/2, z0 + h/2))
    return m

def rod(d, length, centre, axis='x'):
    m = trimesh.creation.cylinder(radius=d/2, height=length, sections=32)
    if axis == 'x':
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, (0, 1, 0)))
    m.apply_translation(centre)
    return m

# ----------------------------------------------------- profils du donneur
def base_profile():
    return [(0.0, -CHAMF), (CHAMF_H, 0.0), (ZR - LIP_A, 0.0),
            (ZR - LIP_B, LIP), (ZR, LIP)]

def lid_profile():
    return [(0.0, -CHAMF), (CHAMF_H, 0.0), (LID_H - LIP_A, 0.0),
            (LID_H - LIP_B, LIP), (LID_H, LIP)]

def groove():
    return loft([(ZR - GRV_D, GRV_I), (ZR + 1, GRV_I)]).difference(
           loft([(ZR - GRV_D - 1, GRV_O), (ZR + 2, GRV_O)]))

def groove_cut():
    """Anneau plein entre les deux offsets de la rainure."""
    outer = prism(GRV_O, ZR - GRV_D, ZR + 1)
    inner = prism(GRV_I, ZR - GRV_D - 1, ZR + 2)
    return outer.difference(inner)

def tongue():
    outer = prism(TNG_O, LID_H - 1, LID_H + TNG_H)
    inner = prism(TNG_I, LID_H - 2, LID_H + TNG_H + 1)
    return outer.difference(inner)

# --------------------------------------------------------- section de coque
def hull_sections():
    """Silhouettes de la coque, en coupe, pour tailler les berceaux."""
    from render import load
    from slice import slice_pts
    H = load(os.path.join(HERE, 'boat_hull.STL'))
    return H

def cradle_cut(hull, box_x, clearance=1.5):
    """Profil du bateau a la station `box_x` (repere boite), dans le plan (Y, Z)."""
    from slice import slice_pts
    hz = box_x - BOAT_C + 100.0               # x boite -> Z coque
    q = slice_pts(hull, 2, hz)
    q = q[q[:, 1] < 34.0]
    if len(q) < 12:
        return None
    pts = np.c_[(q[:, 0] - 47.0) + BOAT_Y, (q[:, 1] - 3.79) + BOAT_Z]   # (Y, Z) boite
    h = ConvexHull(pts)
    return Polygon(pts[h.vertices]).buffer(clearance, quad_segs=6)

# Le bateau : centre en Y sur le chenal, pose sur les berceaux.
Y_CHAN  = -IN_W/2 + CHAN_W/2                  # axe du chenal
# Le bateau n'est pas centre sur l'axe de la coque : il occupe X = -42.6 a 38.1
# dans le repere monde. On le recentre dans le chenal.
BOAT_Y  = Y_CHAN + 2.25
BOAT_Z  = FLOOR + CRADLE_H                    # quille sur le dessus des berceaux
# Le bateau assemble occupe Z = -130.5 (tuyere) a +100.0 (etrave) dans le repere
# monde du viewer ; centre dans la boite, x_boite = Z_monde + BOAT_C.
BOAT_C  = 15.25

# ------------------------------------------------------------------ le bac
def make_base():
    m = loft(base_profile())
    m = m.difference(prism(-WALL, FLOOR, ZR + 2))          # cavite

    # --- cloison longitudinale : chenal bateau | rangements
    y_div = -IN_W/2 + CHAN_W
    m = m.union(blk(-IN_L/2, y_div, FLOOR, IN_L, DIV_T, BASE_CAV - 4))

    # --- 3 traverses : 4 cases de rangement
    y_acc, w_acc = y_div + DIV_T, IN_W/2 - (y_div + DIV_T)
    for x in (-IN_L/2 + 59.5, -IN_L/2 + 119.0, -IN_L/2 + 178.5):
        m = m.union(blk(x - DIV_T/2, y_acc, FLOOR, DIV_T, w_acc, TRAY_Z - FLOOR))

    # --- tasseau du tiroir amovible, le long de la paroi arriere
    m = m.union(blk(-IN_L/2, IN_W/2 - 3.0, TRAY_Z - 2.0, IN_L, 3.0, 2.0))

    # --- berceaux tailles a la section reelle de la coque
    hull = hull_sections()
    for bx in (-70.0, 0.0, 70.0):
        rib = blk(bx - 4, -IN_W/2, FLOOR, 8, CHAN_W, CRADLE_H + 14)
        prof = cradle_cut(hull, bx)
        if prof is not None:
            cut = trimesh.creation.extrude_polygon(prof, 60)
            T = np.eye(4); T[:3, :3] = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
            cut.apply_transform(T); cut.apply_translation((bx - 30, 0, 0))
            rib = rib.difference(cut)
        m = m.union(rib)

    # --- nervures exterieures verticales
    for x in np.arange(-100, 101, 25.0):
        for sy in (-1, 1):
            m = m.union(blk(x - 5, sy*(OUT_W/2 - 1) - (0 if sy > 0 else 3.0),
                            CHAMF_H, 10, 3.0, ZR - LIP_A - CHAMF_H))
    for y in np.arange(-45, 46, 30.0):
        for sx in (-1, 1):
            m = m.union(blk(sx*(OUT_L/2 - 1) - (0 if sx > 0 else 3.0), y - 5,
                            CHAMF_H, 3.0, 10, ZR - LIP_A - CHAMF_H))

    # --- charniere : noeuds du bac
    m = m.union(hinge_knuckles(base=True, z_rim=ZR))

    # --- loquets : montants
    for lx in LATCH_X:
        m = m.union(latch_posts(lx, ZR))

    # --- patins de gerbage
    for cx, cy in ((-90, -45), (90, -45), (-90, 45), (90, 45)):
        p = trimesh.creation.cylinder(radius=10.0, height=2.4, sections=32)
        p.apply_translation((cx, cy, -1.2))
        m = m.union(p)

    m = m.difference(groove_cut())                          # rainure de joint
    return m

# ------------------------------------------------- charniere et loquets
def hinge_x(base=True):
    """Positions des noeuds. Le motif est symetrique en X pour que le couvercle,
    qui se retourne autour de l'axe Y, retombe exactement dans les creneaux du
    bac : noeuds du bac aux demi-pas, noeuds du couvercle aux pas entiers."""
    step, N = 2*KNUCK, 8
    cs = [(k + 0.5)*step for k in range(-N, N)] if base else \
         [k*step for k in range(-N, N + 1)]
    return [(c - KNUCK/2 + 0.2, c + KNUCK/2 - 0.2) for c in cs]

def hinge_knuckles(base, z_rim):
    y0 = OUT_W/2 - WALL                      # face interieure de la paroi arriere
    parts = []
    for a, b in hinge_x(base):
        k = blk(a, y0, z_rim - KNUCK/2 - 1, b - a, HG_Y + WALL + KNUCK/2, KNUCK + 2)
        cyl = rod(2*(HG_Y + KNUCK/2), b - a + 1, (( a + b)/2, OUT_W/2 + HG_Y, z_rim))
        k = k.intersection(cyl.union(blk(a - .5, y0, z_rim - KNUCK/2 - 1,
                                         b - a + 1, HG_Y + WALL, KNUCK + 2)))
        parts.append(k)
    m = trimesh.util.concatenate(parts) if len(parts) > 1 else parts[0]
    m = trimesh.boolean.union(parts)
    # Au-dela du plan de joint, les noeuds doivent rester en dehors du nu de la
    # lechefrite : c'est la que descend la paroi de la piece d'en face.
    m = m.difference(prism(LIP + 0.35, z_rim, z_rim + 12))
    bore = rod(HG_BORE, OUT_L, (0, OUT_W/2 + HG_Y, z_rim))
    return m.difference(bore)

def latch_posts(lx, z_rim):
    """Deux montants ajoures, gousset a 45 deg, alesage d'axe."""
    parts = []
    for sx in (-1, 1):
        x0 = lx + sx*(LT_GAP/2) + (0 if sx > 0 else -LT_POST)
        col = blk(x0, OUT_W/-2, z_rim - 15.4, LT_POST, LT_OUT + WALL, 15.4)
        col.apply_translation((0, -LT_OUT, 0))
        # gousset : coin inferieur retire a 45 deg
        w = trimesh.creation.box((LT_POST + 2, 40, 40))
        w.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(45), (1, 0, 0)))
        w.apply_translation((x0 + LT_POST/2, -OUT_W/2 - LT_OUT - 20*0.7071, z_rim - 15.4))
        col = col.difference(w)
        col = col.union(blk(x0, -OUT_W/2 - LT_OUT, CHAMF_H, LT_POST, LT_OUT + WALL,
                            z_rim - 15.4 - CHAMF_H).difference(w))
        parts.append(col)
    m = trimesh.boolean.union(parts)
    bore = rod(LT_BORE, LT_GAP + 4*LT_POST, (lx, -OUT_W/2 - LT_Y, z_rim - LT_Z))
    return m.difference(bore)

def latch_catch(lx, z_rim):
    """Gache du couvercle : bossage ajoure, alesage au niveau du plan de joint."""
    y0 = -OUT_W/2 - LK_OUT
    b = blk(lx - LK_W/2, y0, z_rim - 4.0, LK_W, LK_OUT + WALL, 8.0)
    w = trimesh.creation.box((LK_W + 2, 40, 40))
    w.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(45), (1, 0, 0)))
    w.apply_translation((lx, -OUT_W/2 - LK_OUT - 20*0.7071, z_rim - 4.0))
    b = b.union(blk(lx - LK_W/2, y0, CHAMF_H, LK_W, LK_OUT + WALL,
                    z_rim - 4.0 - CHAMF_H).difference(w))
    b = b.difference(prism(LIP + 0.35, z_rim, z_rim + 12))
    bore = rod(LT_BORE, LK_W + 4, (lx, -OUT_W/2 - LK_Y, z_rim))
    return b.difference(bore)

# ----------------------------------------------------------- le couvercle
def make_lid():
    m = loft(lid_profile())
    m = m.difference(prism(-WALL, LID_TOP, LID_H + 2))
    m = m.union(tongue())

    # nervures de maintien : elles plaquent le bateau et les rangements
    y_div = -IN_W/2 + CHAN_W
    for x in np.arange(-100, 101, 40.0):
        m = m.union(blk(x - 2, -IN_W/2, LID_TOP, 4.0, CHAN_W, 3.0))
        m = m.union(blk(x - 2, y_div, LID_TOP, 4.0, IN_W/2 - y_div, 9.0))

    # nervures exterieures, alignees sur celles du bac
    for x in np.arange(-100, 101, 25.0):
        for sy in (-1, 1):
            m = m.union(blk(x - 5, sy*(OUT_W/2 - 1) - (0 if sy > 0 else 3.0),
                            CHAMF_H, 10, 3.0, LID_H - LIP_A - CHAMF_H))
    for y in np.arange(-45, 46, 30.0):
        for sx in (-1, 1):
            m = m.union(blk(sx*(OUT_L/2 - 1) - (0 if sx > 0 else 3.0), y - 5,
                            CHAMF_H, 3.0, 10, LID_H - LIP_A - CHAMF_H))

    m = m.union(hinge_knuckles(base=False, z_rim=LID_H))
    for lx in LATCH_X:
        m = m.union(latch_catch(lx, LID_H))

    # cartouche d'etiquette en creux (le couvercle est imprime a l'envers :
    # le dessus fini est en Z = 0)
    lab = loft([(0.0, -CHAMF), (0.0, -CHAMF)])   # placeholder, remplace ci-dessous
    lab = blk(-80, -32, -0.1, 160, 64, 1.5)
    m = m.difference(lab)

    # empreintes de gerbage en face des patins du bac
    for cx, cy in ((-90, -45), (90, -45), (-90, 45), (90, 45)):
        p = trimesh.creation.cylinder(radius=10.6, height=2.8, sections=32)
        p.apply_translation((cx, cy, 1.4 - 1.4))
        m = m.difference(p)
    return m

# ------------------------------------------------------- tiroir amovible
def make_tray():
    y0 = -IN_W/2 + CHAN_W + DIV_T + 0.5
    y1 = IN_W/2 - 0.5
    L, W = IN_L - 1.0, y1 - y0
    m = blk(-L/2, y0, 0, L, W, TRAY_H)
    m = m.difference(blk(-L/2 + 2.0, y0 + 2.0, 2.0, L - 4.0, W - 4.0, TRAY_H))
    for x in (-L/2 + 39.0, -L/2 + 78.0, -L/2 + 117.0, -L/2 + 156.0, -L/2 + 195.0):
        m = m.union(blk(x - 1.0, y0 + 2.0, 2.0, 2.0, W - 4.0, TRAY_H - 2.0))
    # prises de doigt aux deux bouts
    for sx in (-1, 1):
        c = trimesh.creation.cylinder(radius=11.0, height=W + 4, sections=32)
        c.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, (1, 0, 0)))
        c.apply_translation((sx*(L/2 - 1.0), (y0 + y1)/2, TRAY_H + 4.0))
        m = m.difference(c)
    return m

# ------------------------------------------------------------- le joint
def make_gasket():
    o = prism(GRV_O - 0.2, 0, GASKET_T)
    i = prism(GRV_I + 0.2, -1, GASKET_T + 1)
    return o.difference(i)

def clean(m):
    """Nettoyage prudent : on ne retire des faces que si le solide reste ferme."""
    if not m.is_watertight:
        m.merge_vertices()
    if not m.is_watertight:
        m.fill_holes()
    keep = m.copy()
    try:
        m.update_faces(m.nondegenerate_faces())
        if not m.is_watertight:
            m = keep
    except Exception:
        m = keep
    m.fix_normals()
    return m

if __name__ == '__main__':
    import trimesh as tm
    jobs = (('case_base', make_base), ('case_lid', make_lid),
            ('case_tray', make_tray), ('case_gasket', make_gasket))
    for name, fn in jobs:
        m = clean(fn())
        b = m.bounds
        print(f'{name:12s} {len(m.faces):6d} faces  etanche={m.is_watertight}  '
              f'volume={m.volume/1000:7.1f} cm3  bbox={np.round(b[1]-b[0], 1)}')
        m.export(os.path.join(HERE, 'models', name + '.STL'))
