#!/usr/bin/env python3
"""
Mango SpaceQuad, variante GENERICA para clips de cinturon (Anytone y similares, sin medidas oficiales).

    python src/mango_anytone_generico.py stl/mango_spacequad_tripode.stl stl/mango_spacequad_anytone_generico.stl stl/anytone_calzos

Genera el mango (base v1 + placa v3) con:
 - Placa del clip girada 180 grados alrededor del eje vertical de uso (espejo en V respecto a la torre):
   la radio queda orientada al reves y el clip entra desde el extremo opuesto.
 - Ancho libre ajustable con calzos laterales imprimibles (ranuras en la placa, sin tornillos).
 - Base reforzada: el hueco interior del mango se rellena junto a la base y se afina con dos nervios en cruz.
Tambien exporta los calzos (un STL por juego). Todo es ESTIMADO: no hay medidas reales de clips Anytone.
"""
import argparse
from pathlib import Path


def _input_file(value):
    path = Path(value)
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"no existe el archivo de entrada: {value}")
    return str(path)


def _output_file(value):
    path = Path(value)
    if path.exists() and path.is_dir():
        raise argparse.ArgumentTypeError(f"la salida debe ser un archivo: {value}")
    if not path.parent.is_dir():
        raise argparse.ArgumentTypeError(f"no existe el directorio de salida: {path.parent}")
    return str(path)


def _parse_cli():
    parser = argparse.ArgumentParser(
        description="Genera el mango SpaceQuad con soporte ajustable generico para clips de cinturon y sus calzos.",
        epilog="Ejemplo: python src/mango_anytone_generico.py stl/mango_spacequad_tripode.stl "
               "stl/mango_spacequad_anytone_generico.stl stl/anytone_calzos",
    )
    parser.add_argument("source", type=_input_file, help="STL v1 de entrada")
    parser.add_argument("destination", type=_output_file, help="STL del mango de salida")
    parser.add_argument("shim_dir", help="directorio de salida de los STL de calzos (se crea si no existe)")
    args = parser.parse_args()
    if Path(args.source).resolve() == Path(args.destination).resolve():
        parser.error("la entrada y la salida no pueden ser el mismo archivo")
    return args


if __name__ == "__main__":
    _cli_args = _parse_cli()

import numpy as np, trimesh
import shapely.geometry as sg
from geom import *
import mango_v3 as mg

# ---------------------------------------------------------------- PARAMETROS (mm)
V_PIV = (mg.ROOT_V0 + mg.ROOT_V1) / 2     # plano de espejo en V = centro de las raices de las cartelas
LATERAL_PLAY = 0.2                         # holgura calzo-cartela
SLOT_W, SLOT_L = 1.8, 8.0                  # ranura de retencion en la placa (lateral x largo)
TAB_W, TAB_L, TAB_IN = 1.4, 7.6, 0.1       # lengueta del calzo (lateral x largo) y holgura por lado
SLOT_S = (10.0, 30.0)                      # inicio de cada ranura a lo largo de la placa
SHIM_D = (2, 4, 6, 8, 10)                  # espesor lateral de cada calzo; juego 0 = sin calzos
SHIM_S0 = 8.0                              # el calzo ocupa s = SHIM_S0 .. PLATE_L
SHIM_H = mg.MIN_CLEAR - 0.2                # altura bajo la placa (deja 0,2 mm contra la placa)
TAB_H = mg.PLATE_T - 0.5                   # la lengueta queda 0,5 mm por debajo de la cara superior
FIT_CLEAR, FIT_SLACK = 0.6, 5.0            # tolerancia de uso: lengua = hueco - 0,6 ... hueco - 5,0
# base reforzada: relleno del hueco interior (medido en v3) y nervios en cruz
PLUG_X0, RIB_X0, RIB_T = 62.0, 44.0, 3.0   # relleno macizo de x=PLUG_X0 hasta la base; nervios hasta RIB_X0

def clear_width(d):
    return mg.W_IN if d == 0 else mg.W_IN - 2 * (LATERAL_PLAY + d)

def tongue_range(d):
    wc = clear_width(d)
    return wc - FIT_SLACK, wc - FIT_CLEAR

RANGE_W = (tongue_range(SHIM_D[-1])[0], tongue_range(0)[1])   # ancho de lengua admitido (min, max)

def mirror_point(s, n=0.0):
    v, h = mg.plate_point(s, n)
    return (2 * V_PIV - v, h)

def prism(poly_vh, u0, u1):
    return mg.use_prism(poly_vh, u0, u1)

def plate_box(u0, u1, s0, s1, n0, n1):
    """Caja en coordenadas de placa (u, s, n), con la placa girada 180 grados."""
    return prism([mirror_point(s0, n0), mirror_point(s1, n0), mirror_point(s1, n1), mirror_point(s0, n1)], u0, u1)

def slot_us():
    """(u0, u1) de las dos ranuras, pegadas a la cara interior de cada cartela."""
    a = mg.PLATE_U0 + mg.SIDE_T
    b = mg.PLATE_U0 + mg.PLATE_W - mg.SIDE_T
    return (a, a + SLOT_W), (b - SLOT_W, b)

def clip_holder():
    plate = plate_box(mg.PLATE_U0, mg.PLATE_U0 + mg.PLATE_W, 0, mg.PLATE_L, 0, mg.PLATE_T)
    uc = mg.PLATE_U0 + mg.PLATE_W / 2
    if mg.HOOK_WINDOW:
        plate -= plate_box(uc - mg.WIN_W/2, uc + mg.WIN_W/2, mg.WIN_S, mg.WIN_S + mg.WIN_H, -1, mg.PLATE_T + 1)
    for u0, u1 in slot_us():
        for s in SLOT_S:
            plate -= plate_box(u0, u1, s, s + SLOT_L, -1, mg.PLATE_T + 1)
    gusset = [mirror_point(0, 0.2), mirror_point(mg.PLATE_L, 0.2), (mg.ROOT_V0, mg.ROOT_H0), (mg.ROOT_V1, mg.ROOT_H0)]
    for u in (mg.PLATE_U0, mg.PLATE_U0 + mg.PLATE_W - mg.SIDE_T):
        plate += prism(gusset, u, u + mg.SIDE_T)
    return plate

def shim_local(d, left=True):
    """Calzo en coordenadas locales de impresion: x lateral (0 = cartela), y = s, z = n + SHIM_H + 0,1 (z=0 es su base)."""
    c = min(0.75 * d, 3.0)
    poly = sg.Polygon([(0, SHIM_S0), (d, SHIM_S0), (d, mg.PLATE_L - c), (d - c, mg.PLATE_L), (0, mg.PLATE_L)])
    body = trimesh.creation.extrude_polygon(poly, SHIM_H)
    parts = [body]
    for s in SLOT_S:
        tab = trimesh.creation.box(bounds=[[TAB_IN, s + TAB_IN, SHIM_H - 0.01],
                                            [TAB_IN + TAB_W, s + TAB_IN + TAB_L, SHIM_H + 0.1 + TAB_H]])
        parts.append(tab)
    solid = to_tm(_union(parts))
    solid.apply_translation([LATERAL_PLAY, 0, 0])
    if not left:
        solid.apply_transform(np.diag([-1.0, 1.0, 1.0, 1.0]))
    if solid.volume < 0:
        solid.invert()
    return solid
def _union(meshes):
    out = to_mf(meshes[0])
    for m in meshes[1:]:
        out = out + to_mf(m)
    return out

def shim_in_mango(d):
    """Pareja de calzos colocada en el mango (para verificar). Devuelve un Manifold."""
    u_left = mg.PLATE_U0 + mg.SIDE_T
    u_right = mg.PLATE_U0 + mg.PLATE_W - mg.SIDE_T
    out = None
    for left in (True, False):
        m = shim_local(d, left)
        # local (x lateral, y=s, z=n+SHIM_H+0,1 con z=0 = base del calzo) -> (u, s, n)
        pts = np.c_[(u_left + m.vertices[:, 0]) if left else (u_right + m.vertices[:, 0]),
                    m.vertices[:, 1], m.vertices[:, 2] - (SHIM_H + 0.1)]
        out_m = _to_use(pts, m.faces, left)
        out = out_m if out is None else out + out_m
    return out

def _to_use(uvn, faces, left):
    """(u, s, n) -> coordenadas del mango, con la misma transformacion espejo que la placa."""
    a = np.deg2rad(mg.ANGLE)
    u, s, n = uvn[:, 0], uvn[:, 1], uvn[:, 2]
    v = 2 * V_PIV - (mg.PLATE_V0 + s * np.cos(a) - n * np.sin(a))
    h = mg.PLATE_H0 + s * np.sin(a) + n * np.cos(a)
    mesh = trimesh.Trimesh(np.c_[-h, v, u], faces, process=False)
    if mesh.volume < 0:
        mesh.invert()
    return to_mf(mesh)

def base_reinforcement(body):
    """Rellena el hueco interior desde PLUG_X0 hasta su cierre y anade dos nervios en cruz hacia RIB_X0."""
    void = None
    for c in body.decompose():
        if c.volume() < 0:
            void = c
    assert void is not None, "no se encontro el hueco interior"
    vm = to_tm(void)
    (x0, y0, z0), (x1, y1, z1) = vm.bounds
    yc, zc = (y0 + y1) / 2, (z0 + z1) / 2
    vm.invert()
    # Relleno algo mayor que el hueco (casco convexo, +2 % en y/z, +1 mm en el cierre) para solapar la pared y no dejar caras coincidentes
    v = vm.vertices.copy()
    v[:, 1] = yc + (v[:, 1] - yc) * 1.02
    v[:, 2] = zc + (v[:, 2] - zc) * 1.02
    v[v[:, 0] > x1 - 0.01, 0] += 1.0
    fill = to_mf(trimesh.convex.convex_hull(v))
    box_plug = to_mf(trimesh.creation.box(bounds=[[PLUG_X0, y0 - 1, z0 - 1], [x1 + 2, y1 + 1, z1 + 1]]))
    plug = fill ^ box_plug
    rib_y = to_mf(trimesh.creation.box(bounds=[[RIB_X0, y0 - 1.5, zc - RIB_T/2], [PLUG_X0 + 1, y1 + 1.5, zc + RIB_T/2]]))
    rib_z = to_mf(trimesh.creation.box(bounds=[[RIB_X0, yc - RIB_T/2, z0 - 1.5], [PLUG_X0 + 1, yc + RIB_T/2, z1 + 1.5]]))
    ribs = (rib_y + rib_z) ^ fill
    return body + plug + ribs

def build(src, dst, shim_dir):
    m = trimesh.load(src); m.merge_vertices()
    body = to_mf(m)
    print("v1:", body.status(), round(body.volume()/1000, 1), "cm3")
    fill = box(-9.2, -2.6, TY0, YC + 5.9, mg.OLD_Z - 5.8, mg.OLD_Z + 5.8) + cyl_u(YC, mg.OLD_Z, 3.45, -19.3, 0.2)
    body = body + fill + clip_holder()
    body = mg.tripod_fix(body, m.vertices)
    body = base_reinforcement(body)
    out = to_tm(body)
    out.export(dst)
    print("OK ->", dst, np.round(out.extents, 1), "mm", round(body.volume()/1000, 1), "cm3", body.status())
    sd = Path(shim_dir); sd.mkdir(parents=True, exist_ok=True)
    for d in SHIM_D:
        pair = trimesh.util.concatenate([shim_local(d, True),
                                         shim_local(d, False).copy().apply_translation([2 * d + 6, 0, 0])])
        lo, hi = tongue_range(d)
        path = sd / f"calzos_d{d:02d}_lengua_{lo:.1f}-{hi:.1f}.stl"
        pair.export(path)
        print("calzo ->", path.name, "ancho libre", round(clear_width(d), 1))

if __name__ == "__main__":
    build(_cli_args.source, _cli_args.destination, _cli_args.shim_dir)
