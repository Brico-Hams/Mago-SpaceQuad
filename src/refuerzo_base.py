#!/usr/bin/env python3
"""
Refuerzo de la base de trípode del mango SpaceQuad (post-proceso de cualquier STL de la familia v3).

    python refuerzo_base.py ../stl/mango_spacequad_v3.stl <salida.stl> [informe.json]

El refuerzo vive ahora dentro de mango_v6.py, que reutiliza este modulo (stl/mango_spacequad_v3_refuerzo.stl se elimino).

Diagnóstico medido sobre el STL v3 (no sobre cargas reales): la empuñadura es una cáscara hueca (cavidad
cerrada de ~790 mm2) que termina en un tapón macizo con un escalón plano en X~87,9; la sección pasa de
~590 mm2 a ~1388 mm2 de golpe. Ese escalón es el único salto brusco de rigidez entre el tapón/base y el mango.

Cambio: la cavidad se rellena en rampa cónica (30 mm antes del escalón): la pared interior engrosa de forma
lineal hasta cerrar la cavidad en el escalón. No toca el exterior, la ranura de tuerca, el taladro ni el
acceso al tornillo (todo el relleno queda dentro de la cavidad cerrada, X < ~88).
Al actuar sobre el STL final, sirve para las variantes de clip de otras ramas sin tocar su generador.
"""
import argparse
import json
from pathlib import Path


def _input_file(value):
    path = Path(value)
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"no existe el STL de entrada: {value}")
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
        description="Refuerza la transición base de trípode/mango rellenando en rampa la cavidad del mango.",
        epilog="Ejemplo: python src/refuerzo_base.py stl/mango_spacequad_v3.stl stl/mango_spacequad_v3_refuerzo.stl docs/refuerzo_base_checks.json",
    )
    parser.add_argument("source", type=_input_file, help="STL de entrada (familia v3)")
    parser.add_argument("destination", type=_output_file, help="STL reforzado de salida")
    parser.add_argument("report", nargs="?", type=_output_file, help="JSON con las comprobaciones (opcional)")
    args = parser.parse_args()
    if Path(args.source).resolve() == Path(args.destination).resolve():
        parser.error("la entrada y la salida no pueden ser el mismo archivo")
    return args


if __name__ == "__main__":
    _cli_args = _parse_cli()

import numpy as np, trimesh, manifold3d as mf
import shapely.geometry as sg
from shapely.geometry.polygon import orient

# ---------------------------------------------------------------- PARAMETROS (mm)
BUTT_FACE = 110.0       # cara del culo (X), medida en v3
SCAN_X0 = 95.0          # se busca el escalón del tapón bajando desde aquí
TAPER_L = 30.0          # longitud de la rampa antes del escalón
STEP_DX = 0.4           # paso de laminado del relleno
MIN_VOID_MM3 = 5.0      # huecos cerrados menores se consideran restos numéricos del booleano
OVERLAP = 0.15          # solape del relleno con la pared (fusión limpia)
# alojamiento de tuerca y taladro de v3 (mango_v3.py): zona que el refuerzo no debe tocar
T_YC, T_ZC = 115.2, 15.7
NUT_AF, NUT_T, NUT_HOLE, TRIPOD_SKIN = 11.4, 5.9, 6.6, 1.2
HOLE_X0 = 99.1          # inicio del taladro Ø6,6 de la rosca (BUTT_FACE - 3,0 - NUT_T - 2, mango_v3.py)
SCREW_ACCESS_R, SCREW_ACCESS_L = 13.0, 20.0   # cilindro de acceso del tornillo/placa frente al culo


def to_mf(m):
    return mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32),
                               tri_verts=np.asarray(m.faces, np.uint32)))


def to_tm(M):
    g = M.to_mesh()
    return trimesh.Trimesh(g.vert_properties[:, :3].copy(), g.tri_verts.copy(), process=False)


def load_mesh(path):
    m = trimesh.load(path, process=False)
    m.merge_vertices()
    return m


def section_polys(mesh, x):
    s = mesh.section(plane_origin=[x, 0, 0], plane_normal=[1, 0, 0])
    if s is None:
        return []
    p, _ = s.to_2D(to_2D=trimesh.geometry.plane_transform([x, 0, 0], [1, 0, 0]))
    return p.polygons_full


def main_poly(mesh, x):
    """Sección principal en (y,z). to_2D es isométrica: se devuelve en coordenadas (y,z) del mango."""
    s = mesh.section(plane_origin=[x, 0, 0], plane_normal=[1, 0, 0])
    loops = [np.asarray(e)[:, 1:] for e in s.discrete]
    polys = [sg.Polygon(l).buffer(0) for l in loops if len(l) > 3]
    polys = sorted(polys, key=lambda q: -q.area)
    solid = polys[0]
    for h in polys[1:]:
        if solid.contains(h):
            solid = solid.difference(h)
    return solid


def find_plug_start(mesh):
    """X donde la cavidad hueca termina y la sección salta a maciza (bisección)."""
    area = lambda x: main_poly(mesh, x).area
    a_ref = area(SCAN_X0)
    x_hi, x_lo = SCAN_X0, SCAN_X0
    while area(x_lo) > 0.7 * a_ref:
        x_lo -= 0.5
        if x_lo < 40:
            raise RuntimeError("no se encontró el escalón del tapón")
    x_hi = x_lo + 0.5
    for _ in range(12):
        xm = (x_hi + x_lo) / 2
        if area(xm) > 0.7 * a_ref:
            x_hi = xm
        else:
            x_lo = xm
    return x_hi


def cavity_at(mesh, x):
    solid = main_poly(mesh, x)
    if not solid.interiors:
        return None
    return max((sg.Polygon(i) for i in solid.interiors), key=lambda q: q.area)


def x_prism(poly, x0, x1):
    """Polígono (y,z) extruido a lo largo de X entre x0 y x1."""
    parts = poly.geoms if hasattr(poly, "geoms") else [poly]
    out = []
    for p in parts:
        if p.is_empty or p.area < 0.05 or p.geom_type != "Polygon":
            continue
        m = trimesh.creation.extrude_polygon(orient(p, 1.0), x1 - x0)
        v = m.vertices.copy()
        m = trimesh.Trimesh(np.c_[v[:, 2] + x0, v[:, 0], v[:, 1]], m.faces, process=True)
        if m.volume < 0:
            m.invert()
        out.append(to_mf(m))
    return out


def inscribed_radius(poly):
    lo, hi = 0.0, 30.0
    for _ in range(30):
        mid = (lo + hi) / 2
        if poly.buffer(-mid).is_empty:
            hi = mid
        else:
            lo = mid
    return lo


def ramp_fill(mesh, x_plug):
    """Relleno de la cavidad en rampa cónica: espesor de pared adicional t(x) lineal, 0 en x_plug-TAPER_L."""
    x_start = x_plug - TAPER_L
    r_max = inscribed_radius(cavity_at(mesh, x_plug - 0.5))
    pieces = []
    n = int(round(TAPER_L / STEP_DX))
    for i in range(n + 1):
        x0 = x_start + i * STEP_DX
        x1 = x0 + STEP_DX
        xc = min((x0 + x1) / 2, x_plug - 0.05)
        cav = cavity_at(mesh, xc)
        s = (xc - x_start) / TAPER_L
        core = cav.buffer(-1.02 * r_max * s)
        ring = cav.buffer(OVERLAP).difference(core)
        pieces += x_prism(ring, x0 - 0.01, min(x1, x_plug + 0.1) + 0.01)
    return mf.Manifold.batch_boolean(pieces, mf.OpType.Add), x_start, r_max


def void_tail(mesh, x_plug):
    """Parte de la cavidad que sigue dentro del tapón (rendijas finas tras el escalón), tomada exacta de la malla."""
    comps = [c for c in mesh.split(only_watertight=False) if c.volume < 0]
    if not comps:
        return None
    void = max(comps, key=lambda c: abs(c.volume)).copy()
    void.invert()
    cut = to_mf(trimesh.creation.box(bounds=[[x_plug - 0.05, -500, -500], [BUTT_FACE + 5, 500, 500]]))
    return to_mf(void) ^ cut


def section_props(mesh, x):
    """Área y módulos resistentes de la sección en X=x (y,z): Z_debil con flexión en el plano X-Z (canto en z)."""
    p = main_poly(mesh, x)
    p = orient(p, 1.0)

    def raw(c):
        c = np.asarray(c)
        y, z = c[:, 0], c[:, 1]
        y1, z1 = np.roll(y, -1), np.roll(z, -1)
        cr = y * z1 - y1 * z
        return (cr.sum() / 2, ((y + y1) * cr).sum() / 6, ((z + z1) * cr).sum() / 6,
                ((z * z + z * z1 + z1 * z1) * cr).sum() / 12, ((y * y + y * y1 + y1 * y1) * cr).sum() / 12)

    r = [raw(p.exterior.coords)] + [raw(i.coords) for i in p.interiors]
    A = sum(t[0] for t in r)
    cy = sum(t[1] for t in r) / A
    cz = sum(t[2] for t in r) / A
    Iy = sum(t[3] for t in r) - A * cz * cz     # inercia alrededor del eje Y: flexión X-Z (débil)
    Iz = sum(t[4] for t in r) - A * cy * cy     # inercia alrededor del eje Z: flexión X-Y (fuerte)
    b = p.bounds
    return dict(x=float(x), area=A, Z_debil=Iy / max(cz - b[1], b[3] - cz), Z_fuerte=Iz / max(cy - b[0], b[2] - cy),
                outer_area=sg.Polygon(p.exterior).area)


def mesh_report(m):
    m = m.copy()
    m.merge_vertices()
    _, cnt = np.unique(m.edges_sorted, axis=0, return_counts=True)
    return dict(vertices=len(m.vertices), faces=len(m.faces), watertight=bool(m.is_watertight),
                winding_consistent=bool(m.is_winding_consistent), euler=int(m.euler_number),
                open_edges=int((cnt == 1).sum()), nonmanifold_edges=int((cnt > 2).sum()),
                degenerate_faces=int((m.area_faces < 1e-9).sum()), components=len(m.split(only_watertight=False)),
                volume_cm3=round(float(m.volume) / 1000, 3), bounds=np.round(m.bounds, 3).tolist())


def keepouts():
    """Volúmenes (mango, mm) que el refuerzo no puede invadir."""
    x1 = BUTT_FACE - TRIPOD_SKIN
    slot = trimesh.creation.box(bounds=[[x1 - NUT_T, T_YC - NUT_AF / 2, -1], [x1, T_YC + NUT_AF / 2, T_ZC]])
    hole = trimesh.creation.cylinder(radius=NUT_HOLE / 2, height=BUTT_FACE + 1 - HOLE_X0, sections=48)
    hole.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    hole.apply_translation([(BUTT_FACE + 1 + HOLE_X0) / 2, T_YC, T_ZC])
    access = trimesh.creation.cylinder(radius=SCREW_ACCESS_R, height=SCREW_ACCESS_L, sections=48)
    access.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    access.apply_translation([BUTT_FACE + SCREW_ACCESS_L / 2, T_YC, T_ZC])
    return {"ranura_tuerca": to_mf(slot), "taladro_rosca": to_mf(hole), "acceso_tornillo_placa": to_mf(access)}


def build(src, dst, report=None):
    old_tm = load_mesh(src)
    old = to_mf(old_tm)
    print("entrada:", old.status(), round(old.volume() / 1000, 3), "cm3")
    x_plug = find_plug_start(old_tm)
    fill, x_start, r_max = ramp_fill(old_tm, x_plug)
    tail = void_tail(old_tm, x_plug)
    new = old + fill + tail if tail is not None else old + fill
    out = to_tm(new)
    # las rendijas finas de la cavidad dejan restos de volumen ~0 (<0,01 mm3) entre mallas coincidentes: se descartan
    comps = out.split(only_watertight=False)
    keep = [c for c in comps if abs(c.volume) >= MIN_VOID_MM3]
    dropped = len(comps) - len(keep)
    out = trimesh.util.concatenate(keep)
    out.export(dst)
    new_tm = load_mesh(dst)
    print(f"OK -> {dst}  tapon en X={x_plug:.2f}, rampa X={x_start:.1f}..{x_plug:.1f}, volumen {new.volume() / 1000:.3f} cm3")

    added = new - old
    removed = old - new
    ko = {k: round(float((added ^ v).volume()), 6) for k, v in keepouts().items()}
    xs = list(np.arange(40, 110, 2.0)) + [x_plug - 0.5, x_plug + 0.5]
    xs = sorted(set(round(float(x), 2) for x in xs))
    rows = []
    for x in xs:
        if x > BUTT_FACE - 1.0:
            continue
        a, b = section_props(old_tm, x), section_props(new_tm, x)
        rows.append(dict(x=x, area_antes=round(a["area"], 1), area_despues=round(b["area"], 1),
                         Z_debil_antes=round(a["Z_debil"], 0), Z_debil_despues=round(b["Z_debil"], 0),
                         Z_fuerte_antes=round(a["Z_fuerte"], 0), Z_fuerte_despues=round(b["Z_fuerte"], 0),
                         contorno_exterior_igual=bool(abs(a["outer_area"] - b["outer_area"]) < 0.5)))
    base = [r for r in rows if r["x"] >= x_plug - TAPER_L - 0.1]
    grad = lambda key: max(abs(base[i + 1][key] - base[i][key]) / (base[i + 1]["x"] - base[i]["x"]) for i in range(len(base) - 1))
    zone = [r for r in rows if x_plug - TAPER_L <= r["x"] <= x_plug + 0.6]
    res = dict(
        parametros=dict(x_escalon_tapon=round(x_plug, 3), x_inicio_rampa=round(x_start, 3), longitud_rampa=TAPER_L,
                        radio_inscrito_cavidad=round(r_max, 2), paso_laminado=STEP_DX),
        malla_antes=mesh_report(old_tm), malla_despues=mesh_report(new_tm),
        volumen_anadido_mm3=round(float(added.volume()), 1), volumen_eliminado_mm3=round(float(removed.volume()), 3),
        restos_de_hueco_descartados=dropped,
        interferencia_volumen_mm3=ko,
        bbox_igual=bool(np.allclose(old_tm.bounds, new_tm.bounds, atol=1e-3)),
        zona_afectada_x=[round(float(b), 2) for b in max(to_tm(added).split(only_watertight=False), key=lambda c: abs(c.volume)).bounds[:, 0]],
        contorno_exterior_igual_en_todas=all(r["contorno_exterior_igual"] for r in rows),
        gradiente_Z_debil_max_mm3_por_mm=dict(antes=round(grad("Z_debil_antes"), 0), despues=round(grad("Z_debil_despues"), 0)),
        salto_escalon=dict(antes=dict(area=[rows_x(rows, x_plug - 0.5)["area_antes"], rows_x(rows, x_plug + 0.5)["area_antes"]],
                                      Z_debil=[rows_x(rows, x_plug - 0.5)["Z_debil_antes"], rows_x(rows, x_plug + 0.5)["Z_debil_antes"]]),
                           despues=dict(area=[rows_x(rows, x_plug - 0.5)["area_despues"], rows_x(rows, x_plug + 0.5)["area_despues"]],
                                        Z_debil=[rows_x(rows, x_plug - 0.5)["Z_debil_despues"], rows_x(rows, x_plug + 0.5)["Z_debil_despues"]])),
        secciones=rows,
        aviso="Comparación geométrica de secciones del STL; no incluye cargas ni ensayo físico. Sin validación de resistencia real.")
    if report:
        Path(report).write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    return res


def rows_x(rows, x):
    return min(rows, key=lambda r: abs(r["x"] - x))


if __name__ == "__main__":
    r = build(_cli_args.source, _cli_args.destination, _cli_args.report)
    print(json.dumps({k: v for k, v in r.items() if k != "secciones"}, indent=1, ensure_ascii=False))
