"""Genere la boite de rangement / vente du kit JETBOAT (base + couvercle).

Repere local, commun aux deux pieces et deja oriente pour l'impression :
    X = longueur, Y = largeur, Z = hauteur, coin mini a l'origine.
Le bac s'imprime tel quel (ouverture vers le haut), le couvercle retourne.
"""
import sys; sys.path.insert(0, '.')
import numpy as np, trimesh
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union
from render import load
from slice import slice_pts
from scipy.spatial import ConvexHull

# ---------------------------------------------------------------- cotes
WALL   = 3.2          # parois
FLOOR  = 4.0          # fond du bac / dessus du couvercle
R_OUT  = 10.0         # rayon des angles exterieurs
IN_L, IN_W = 240.0, 122.0     # interieur (longueur x largeur)
BASE_H = 50.0         # hauteur hors-tout du bac
LID_H  = 38.0         # hauteur hors-tout du couvercle
SKIRT_H, SKIRT_T = 8.0, 2.0   # jupe d'emboitement du couvercle
CLR    = 0.4          # jeu d'emboitement
CHAN_W = 94.0         # largeur du chenal bateau
DIV_T  = 3.0          # cloison
RIB_H  = 14.0         # hauteur des berceaux au-dessus du fond
OUT_L, OUT_W = IN_L + 2*WALL, IN_W + 2*WALL

def rrect(l, w, r, x0=0.0, y0=0.0):
    """Rectangle a coins arrondis, coin mini en (x0, y0)."""
    return sbox(x0 + r, y0 + r, x0 + l - r, y0 + w - r).buffer(r, quad_segs=8)

def prism(poly, z0, h):
    m = trimesh.creation.extrude_polygon(poly, h)
    m.apply_translation((0, 0, z0))
    return m

def blk(x0, y0, z0, l, w, h):
    m = trimesh.creation.box((l, w, h))
    m.apply_translation((x0 + l/2, y0 + w/2, z0 + h/2))
    return m

# ------------------------------------------------- section de coque -> polygone
HULL = load('/home/user/JETBOAT/boat_hull.STL')
# Decalage boite -> monde (cf. index.html). Le bateau n'est pas centre sur la
# coque : la tuyere descend jusqu'a Z = -130.5 alors que l'etrave s'arrete a
# +100.05. L'interieur est donc cale sur cet encombrement-la, pas sur la coque.
TX, TZ = -50.2, -138.4

def hull_profile(box_x, clearance=1.4):
    """Silhouette de la coque a la station `box_x`, ramenee dans le repere boite."""
    hz = (box_x + TZ) + 100.0                     # x boite -> Z coque
    q = slice_pts(HULL, 2, hz)
    q = q[q[:, 1] < 30.0]                         # sous le livet
    if len(q) < 12:
        return None
    pts = np.c_[(q[:, 0] - 47.0) - TX, (q[:, 1] - 3.79) + 18.0]   # -> (y, z) boite
    h = ConvexHull(pts)
    return Polygon(pts[h.vertices]).buffer(clearance, quad_segs=6)

# ------------------------------------------------------------------ le bac
def make_base():
    m = prism(rrect(OUT_L, OUT_W, R_OUT), 0, BASE_H)

    # cavite
    cav = rrect(IN_L, IN_W, R_OUT - WALL, WALL, WALL)
    m = m.difference(prism(cav, FLOOR, BASE_H))

    # cloison longitudinale : chenal bateau | rangement accessoires
    y_div = WALL + CHAN_W
    m = m.union(blk(WALL, y_div, FLOOR, IN_L, DIV_T, BASE_H - FLOOR - 6))

    # 2 traverses dans le compartiment accessoires
    y_acc, w_acc = y_div + DIV_T, IN_W - CHAN_W - DIV_T
    for x in (WALL + 80, WALL + 160):
        m = m.union(blk(x, y_acc, FLOOR, DIV_T, w_acc, 26))

    # berceaux : 3 traverses decoupees a la section reelle de la coque
    ribs = []
    for bx in (55.0, 125.0, 195.0):
        rib = blk(bx - 4, WALL, FLOOR, 8, CHAN_W, RIB_H)
        prof = hull_profile(bx)
        if prof is not None:
            # le profil vit dans le plan (y, z) de la boite : on l'extrude puis on
            # bascule l'axe d'extrusion sur X.
            cut = trimesh.creation.extrude_polygon(prof, 40)
            T = np.eye(4); T[:3, :3] = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
            cut.apply_transform(T)
            cut.apply_translation((bx - 20, 0, 0))
            rib = rib.difference(cut)
        ribs.append(rib)
    for r in ribs:
        m = m.union(r)

    # nervures exterieures verticales
    for x in np.arange(28, OUT_L - 20, 34.0):
        m = m.union(blk(x, -2.0, 0, 10, 4.0, BASE_H - 4))
        m = m.union(blk(x, OUT_W - 2.0, 0, 10, 4.0, BASE_H - 4))
    for y in np.arange(30, OUT_W - 24, 34.0):
        m = m.union(blk(-2.0, y, 0, 4.0, 10, BASE_H - 4))
        m = m.union(blk(OUT_L - 2.0, y, 0, 4.0, 10, BASE_H - 4))

    # prises de main en biseau (auto-portantes) aux deux bouts
    for sx in (0, 1):
        wedge = trimesh.creation.box((14, 60, 26))
        wedge.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(38), (0, 1, 0)))
        wedge.apply_translation((sx * OUT_L, OUT_W / 2, BASE_H - 4))
        m = m.difference(wedge)

    # bossages de vissage M3 dans les 4 angles + percages
    for cx, cy in ((11, 11), (OUT_L - 11, 11), (11, OUT_W - 11), (OUT_L - 11, OUT_W - 11)):
        p = trimesh.creation.cylinder(radius=5.0, height=BASE_H - FLOOR, sections=24)
        p.apply_translation((cx, cy, FLOOR + (BASE_H - FLOOR) / 2))
        m = m.union(p)
        h = trimesh.creation.cylinder(radius=1.35, height=26, sections=16)
        h.apply_translation((cx, cy, BASE_H - 11))
        m = m.difference(h)

    # patins de gerbage sous le fond
    for cx, cy in ((34, 22), (OUT_L - 34, 22), (34, OUT_W - 22), (OUT_L - 34, OUT_W - 22)):
        p = trimesh.creation.cylinder(radius=9.0, height=2.4, sections=24)
        p.apply_translation((cx, cy, -1.2))
        m = m.union(p)
    return m

# ----------------------------------------------------------- le couvercle
def make_lid():
    m = prism(rrect(OUT_L, OUT_W, R_OUT), 0, LID_H)
    cav = rrect(IN_L, IN_W, R_OUT - WALL, WALL, WALL)
    m = m.difference(prism(cav, 0, LID_H - FLOOR))

    # jupe d'emboitement
    outer = rrect(IN_L - 2*CLR, IN_W - 2*CLR, R_OUT - WALL, WALL + CLR, WALL + CLR)
    inner = rrect(IN_L - 2*CLR - 2*SKIRT_T, IN_W - 2*CLR - 2*SKIRT_T,
                  max(R_OUT - WALL - SKIRT_T, 1), WALL + CLR + SKIRT_T, WALL + CLR + SKIRT_T)
    m = m.union(prism(outer.difference(inner), -SKIRT_H, SKIRT_H))

    # Nervures interieures. Le dome du capot arrive a 3 mm sous le plafond du
    # couvercle : les nervures qui le surplombent restent a 2.5 mm (elles le
    # maintiennent sans le contraindre), celles du compartiment accessoires
    # descendent a 10 mm pour caler les petites pieces.
    y_acc = WALL + CHAN_W + DIV_T
    for x in np.arange(40, OUT_L - 30, 40.0):
        m = m.union(blk(x, WALL, 0, 4.0, CHAN_W + DIV_T, 2.5))
        m = m.union(blk(x, y_acc, 0, 4.0, IN_W - CHAN_W - DIV_T, 10.0))

    # nervures exterieures, alignees sur celles du bac
    for x in np.arange(28, OUT_L - 20, 34.0):
        m = m.union(blk(x, -2.0, 4, 10, 4.0, LID_H - 8))
        m = m.union(blk(x, OUT_W - 2.0, 4, 10, 4.0, LID_H - 8))
    for y in np.arange(30, OUT_W - 24, 34.0):
        m = m.union(blk(-2.0, y, 4, 4.0, 10, LID_H - 8))
        m = m.union(blk(OUT_L - 2.0, y, 4, 4.0, 10, LID_H - 8))

    # cartouche d'etiquette en creux sur le dessus
    lab = rrect(150, 56, 6, (OUT_L - 150) / 2, (OUT_W - 56) / 2)
    m = m.difference(prism(lab, LID_H - 1.4, 2))

    # 4 percages M3 + lamage
    for cx, cy in ((11, 11), (OUT_L - 11, 11), (11, OUT_W - 11), (OUT_L - 11, OUT_W - 11)):
        p = trimesh.creation.cylinder(radius=5.0, height=LID_H - FLOOR, sections=24)
        p.apply_translation((cx, cy, (LID_H - FLOOR) / 2))
        m = m.union(p)
        h = trimesh.creation.cylinder(radius=1.75, height=LID_H + 4, sections=16)
        h.apply_translation((cx, cy, LID_H / 2))
        m = m.difference(h)
        cb = trimesh.creation.cylinder(radius=3.4, height=6.4, sections=24)
        cb.apply_translation((cx, cy, LID_H - 3.2))
        m = m.difference(cb)

    # empreintes de gerbage en face des patins du bac
    for cx, cy in ((34, 22), (OUT_L - 34, 22), (34, OUT_W - 22), (OUT_L - 34, OUT_W - 22)):
        p = trimesh.creation.cylinder(radius=9.6, height=2.8, sections=24)
        p.apply_translation((cx, cy, LID_H - 1.4))
        m = m.difference(p)
    return m

if __name__ == '__main__':
    for name, fn in (('case_base', make_base), ('case_lid', make_lid)):
        m = fn()
        m.merge_vertices()
        try: m.update_faces(m.nondegenerate_faces())
        except Exception: pass
        m.fix_normals()
        b = m.bounds
        print(f'{name:10s} {len(m.faces):6d} faces  etanche={m.is_watertight}  '
              f'volume={m.volume/1000:7.1f} cm3  bbox={np.round(b[1]-b[0],1)}')
        m.export(f'/home/user/JETBOAT/models/{name}.STL')
