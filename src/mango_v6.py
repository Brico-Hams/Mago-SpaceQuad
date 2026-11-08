#!/usr/bin/env python3
"""
Mango SpaceQuad v6 (Bricohams): v5 corregida. Solo CAD: ni ajuste ni resistencia estan probados fisicamente.

    python mango_v6.py ../stl/mango_spacequad_tripode.stl ../stl/v6 [uvk5v3|rt950pro|todas]
        [--tilt-hacia +V|-V] [--lado-u -U|+U] [--tilt-deg 20] [--sin-brida]

Cambios respecto a la v3/v5:
 1. Posicion D (v6.2). El eje largo de la radio (extremo superior = el del clip) se inclina TILT_DEG sobre la
    horizontal y su extremo superior queda del lado TILT_HACIA en el eje V del boom; por defecto -V (direccion
    confirmada por el usuario sobre la pieza real). La radio, con su placa y el hueco, va al lado LADO_U del eje del
    boom (U = 15,55): "-U" (defecto, lejos del duplexor) es el espejo en U del diseno "+U" anterior. El clip entra
    paralelo a la placa por el borde libre (superior) y la radio apoya en la cara exterior de la placa. La placa se
    sujeta con dos paredes y, en "-U", con un pedestal macizo (alma) fundido con el mango: suelo bajo el hueco, dos paredes
    y la placa forman una funda cerrada, abierta por el borde libre y por el extremo opuesto (v6.3).
 2. Variantes reales por radio. La altura de la placa (PH0) se calcula con la envolvente de cada radio
    (largo x ancho x grueso de perfiles_radio.json) para que su punto mas bajo quede por encima de la torre,
    y el ancho del hueco del clip sale del clip estimado de cada modelo (o del override del JSON).
 3. Zona de la tuerca 1/4"-20 reforzada (la v3 se rompio en una impresion real): piel de cara de 2,0 mm,
    bolsillo hexagonal con esquinas redondeadas y >= 3 mm de material en todos los lados, canal de entrada
    lateral cerrado con labios de retencion, cavidad del mango maciza 36 mm desde el culo con rampa
    conica (logica de refuerzo_base.py) y brida opcional en el culo (cara plana).
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def _parse_cli():
    parser = argparse.ArgumentParser(
        description="Genera las variantes v6 (radio inclinada hacia la empunadura y base de tripode reforzada) desde el STL v1.",
        epilog="Ejemplo: python src/mango_v6.py stl/mango_spacequad_tripode.stl stl/v6 todas",
    )
    parser.add_argument("source", help="STL v1 de entrada")
    parser.add_argument("out_dir", help="directorio de salida")
    parser.add_argument("variant", nargs="?", default="todas")
    parser.add_argument("--tilt-hacia", choices=("+V", "-V"), default="-V",
                        help="lado V hacia el que se inclina el extremo superior de la radio")
    parser.add_argument("--lado-u", choices=("-U", "+U"), default="-U",
                        help="lado del eje del boom (U = 15,55) donde va la radio; -U = posicion D")
    parser.add_argument("--tilt-deg", type=float, default=20.0, help="inclinacion del eje largo de la radio sobre la horizontal")
    parser.add_argument("--sin-brida", action="store_true", help="no anade la brida opcional del culo")
    args = parser.parse_args()
    if not Path(args.source).is_file():
        parser.error(f"no existe el STL de entrada: {args.source}")
    if not 0.0 < args.tilt_deg < 60.0:
        parser.error("--tilt-deg debe estar entre 0 y 60")
    return args


if __name__ == "__main__":
    _cli_args = _parse_cli()

import numpy as np
import trimesh
import manifold3d as mf
import shapely.geometry as sg
from geom import to_mf, to_tm
import mango_v3 as mg
import refuerzo_base as rb

# ---------------------------------------------------------------- PARAMETROS (mm)
TILT_HACIA = "-V"              # "+V" | "-V" (confirmado -V sobre la pieza real)
LADO_U = "-U"                  # "-U" (posicion D, nuevo) | "+U" (diseno anterior)
TILT_DEG = 20.0                # inclinacion del eje largo de la radio sobre la horizontal
BRIDA = True                   # brida opcional del culo

# pedestal macizo (solo LADO_U = "-U"): bloque unico con el mango que lleva la placa al otro lado del boom
U_BOOM = 15.55                 # eje U del tunel del boom
TORRE_U0 = 8.0                 # supuesto: la torre ocupa U ~8..78 hasta H = TOWER_H
EMBED_U = 6.0                  # el pedestal entra esta distancia en U dentro de la torre / bloque del tunel (>= 3 mm)
PED_H0 = 8.75                  # H minimo del pedestal: 1,25 mm sobre la barra del boom (15 x 15 mm, H = +-7,5)
PED_FLOOR_GAP = 0.01           # el suelo del pedestal queda este margen bajo el hueco del clip (evita caras coincidentes)
PED_CHAFLAN = 3.0              # chaflan 45 grados del pedestal sobre la cara superior de la torre (>= 3 mm)

# radio y clip
H_LIBRE = 62.0                 # H minimo de la radio: cara libre de la torre (58,64) + 3,4 mm
POS_CLIP_DEF = 25.0            # distancia estimada del clip al extremo superior de la radio (como R_ABOVE de v3)
CLIP_LAT = 1.0                 # holgura lateral por lado entre lengua y cartelas
CLIP_HOLG_T = 1.0              # holgura en grueso del hueco bajo la placa
RADIO_N0 = mg.PLATE_T + 0.5    # la radio empieza 0,5 mm sobre la cara exterior de la placa
V_RAIZ_C = (mg.ROOT_V0 + mg.ROOT_V1) / 2   # centro en V de la raiz de las cartelas

# tripode: tuerca 1/4"-20 (medidas de tuerca y taladro heredadas de v3)
SKIN_V6 = 2.0                  # piel de la cara del culo (v3: 1,2). Un tornillo de 6+ mm engrana ~4 mm de tuerca
PARED_MIN = 3.0                # material minimo alrededor del bolsillo hexagonal
RELIEF = 4.0                   # taladro de alivio detras de la tuerca para la punta del tornillo
FILL_L = 36.0                  # la cavidad del mango queda maciza al menos FILL_L mm desde el culo
LABIO = 0.4                    # resalte de cada labio de retencion en el canal de entrada
LABIO_L = 2.0                  # profundidad del labio desde la cara exterior
FILETE = 0.8                   # radio de las esquinas del bolsillo
BRIDA_Y, BRIDA_Z, BRIDA_T, BRIDA_CH, BRIDA_R = 50.0, 36.0, 12.0, 5.0, 6.0   # <= 60 x 40 mm
X_P1 = mg.BUTT_FACE - SKIN_V6              # fondo del bolsillo hacia la cara (x)
X_P0 = X_P1 - mg.NUT_T                     # fondo del bolsillo hacia el mango (x)
X_SOLIDO0 = mg.BUTT_FACE - FILL_L          # desde aqui hasta el culo no queda cavidad
X_BRIDA0 = mg.BUTT_FACE - BRIDA_T


def cargar_perfiles():
    return json.loads((HERE / "perfiles_radio.json").read_text(encoding="utf-8"))


def claves_v6():
    return [k for k, v in cargar_perfiles().items() if v.get("stl_v6")]


def resolver_tilt(tilt_hacia=None):
    """+1 = el extremo superior de la radio queda hacia +V; -1 = hacia -V."""
    t = TILT_HACIA if tilt_hacia is None else tilt_hacia
    if t == "+V":
        return 1
    if t == "-V":
        return -1
    raise ValueError(f"TILT_HACIA desconocido: {t}")


def resolver_lado(lado_u=None):
    """Centro U de la placa: espejo en U respecto al eje del boom para '-U'."""
    s = LADO_U if lado_u is None else lado_u
    uc0 = mg.PLATE_U0 + mg.PLATE_W / 2
    if s == "+U":
        return uc0
    if s == "-U":
        return 2 * U_BOOM - uc0
    raise ValueError(f"LADO_U desconocido: {s}")


# ---------------------------------------------------------------- configuracion por radio
def configuracion(key, tilt_hacia=None, tilt_deg=None):
    """Geometria de placa y radio derivada del perfil. Marco (V,H): s = (d cos a, sin a), n = (-d sin a, cos a)."""
    perfil = cargar_perfiles()[key]
    d = resolver_tilt(tilt_hacia)
    deg = TILT_DEG if tilt_deg is None else tilt_deg
    a = np.deg2rad(deg)
    clip = perfil.get("clip") or {}
    radio = perfil["radio"]
    clip_w = clip.get("ancho_mm") or mg.CLIP_W_MAX
    clip_t = clip.get("grueso_max_mm") or mg.CLIP_T_MAX
    pos_clip = radio.get("pos_clip_desde_extremo_A_mm") or POS_CLIP_DEF
    w_in = clip_w + 2 * CLIP_LAT
    plate_w = w_in + 2 * mg.SIDE_T
    min_clear = clip_t + CLIP_HOLG_T
    uc = resolver_lado()
    s1 = mg.PLATE_L + pos_clip                 # extremo superior de la radio
    s_lo = s1 - radio["largo_mm"]              # extremo inferior de la radio
    pv0 = V_RAIZ_C - d * mg.PLATE_L * np.cos(a) / 2
    # H del punto mas bajo de la radio y del hueco del clip con PH0 = 0; ambos deben quedar >= H_LIBRE
    radio_h_min = s_lo * np.sin(a) + RADIO_N0 * np.cos(a)
    hueco_h_min = (mg.PLATE_L - mg.USABLE_L) * np.sin(a) - min_clear * np.cos(a)
    ph0 = max(mg.PLATE_H0, H_LIBRE - radio_h_min, H_LIBRE - hueco_h_min)
    ph0 = float(np.ceil(ph0 * 2) / 2)
    return dict(key=key, perfil=perfil, d=d, deg=float(deg), a=float(a), pv0=float(pv0), ph0=ph0, uc=uc,
                u0=uc - plate_w / 2, plate_w=plate_w, w_in=w_in, min_clear=min_clear,
                clip_w=float(clip_w), clip_t=float(clip_t), pos_clip=float(pos_clip), s1=float(s1),
                radio_w=float(radio["ancho_mm"]), radio_t=float(radio["grueso_mm"]), radio_l=float(radio["largo_mm"]),
                radio_h_min=float(ph0 + radio_h_min), hueco_h_min=float(ph0 + hueco_h_min))


def punto(cfg, s, n=0.0):
    c, sn = np.cos(cfg["a"]), np.sin(cfg["a"])
    return (cfg["pv0"] + cfg["d"] * (s * c - n * sn), cfg["ph0"] + s * sn + n * c)


def caja(cfg, u0, u1, s0, s1, n0, n1):
    """Prisma en el marco de la placa (u transversal, s a lo largo, n normal), en coordenadas del STL."""
    return mg.use_prism([punto(cfg, s0, n0), punto(cfg, s1, n0), punto(cfg, s1, n1), punto(cfg, s0, n1)], u0, u1)


# ---------------------------------------------------------------- placa, cartelas, radio y clip
def cartelas(cfg):
    a, b = sorted([punto(cfg, 0, 0.2), punto(cfg, mg.PLATE_L, 0.2)])   # ordenadas por V
    poly = [a, b, (mg.ROOT_V1, mg.ROOT_H0), (mg.ROOT_V0, mg.ROOT_H0)]
    out = None
    for u in (cfg["u0"], cfg["u0"] + cfg["plate_w"] - mg.SIDE_T):
        p = mg.use_prism(poly, u, u + mg.SIDE_T)
        out = p if out is None else out + p
    return out


def pedestal(cfg):
    """Alma maciza bajo el hueco del clip, fundida con el mango (solo LADO_U = '-U').

    Suelo paralelo a la placa a min_clear (+ PED_FLOOR_GAP) bajo ella; por debajo, el alma baja hasta PED_H0 y se limita
    con un plano inclinado que sube hacia -U (empalme en chaflan con el cuerpo). Cierra con las dos paredes y la
    placa una funda abierta por el borde libre y por el extremo opuesto. Entra EMBED_U en la torre y el bloque del boom.
    """
    n_f = -cfg["min_clear"] - PED_FLOOR_GAP
    u_in = TORRE_U0 + EMBED_U
    f0, f1 = punto(cfg, 0, n_f), punto(cfg, mg.PLATE_L, n_f)
    perfil_vh = [f0, f1, (f1[0], PED_H0), (f0[0], PED_H0)]
    alma = mg.use_prism(perfil_vh, cfg["u0"], u_in)
    # plano inferior: de (U = u_in, H = PED_H0) a (U = u0, H = ROOT_H0), extendido 1 mm mas alla de u0
    pend = (mg.ROOT_H0 - PED_H0) / (u_in - cfg["u0"])
    u_ext = cfg["u0"] - 1.0
    por_encima = sg.Polygon([(mg.FACE_X + PED_H0, u_in), (mg.FACE_X + PED_H0 + pend * (u_in - u_ext), u_ext),
                             (mg.FACE_X + 400.0, u_ext), (mg.FACE_X + 400.0, u_in)])
    v_lo, v_hi = min(f0[0], f1[0]), max(f0[0], f1[0])
    alma = alma ^ mg.prism_y(por_encima, v_lo, v_hi)
    # paredes: de la placa al suelo, a todo lo largo (4 mm de solape con el suelo)
    cuerpo = [punto(cfg, 0, 0.2), punto(cfg, mg.PLATE_L, 0.2), punto(cfg, mg.PLATE_L, n_f - 1.0), punto(cfg, 0, n_f - 1.0)]
    for u in (cfg["u0"], cfg["u0"] + cfg["plate_w"] - mg.SIDE_T):
        alma = alma + mg.use_prism(cuerpo, u, u + mg.SIDE_T)
    # chaflan sobre la cara superior de la torre, en el canto del pedestal (cara +U)
    c, t = PED_CHAFLAN, mg.TOWER_H
    cuna = sg.Polygon([(mg.FACE_X + t - 1.0, u_in - 1.0), (mg.FACE_X + t - 1.0, u_in + c), (mg.FACE_X + t, u_in + c),
                       (mg.FACE_X + t + c, u_in), (mg.FACE_X + t + c, u_in - 1.0)])
    y0, y1 = max(mg.TY0, v_lo), min(mg.TY1, v_hi)
    if y1 > y0:
        alma = alma + mg.prism_y(cuna, y0, y1)
    return alma


def soporte(cfg):
    if LADO_U == "+U":
        return cartelas(cfg)
    return cartelas(cfg) + pedestal(cfg)


def placa(cfg):
    p = caja(cfg, cfg["u0"], cfg["u0"] + cfg["plate_w"], 0, mg.PLATE_L, 0, mg.PLATE_T)
    if mg.HOOK_WINDOW:   # ventana opcional cerca del fondo del hueco (extremo cerrado, lejos del borde libre)
        p -= caja(cfg, cfg["uc"] - mg.WIN_W / 2, cfg["uc"] + mg.WIN_W / 2, mg.WIN_S, mg.WIN_S + mg.WIN_H,
                  -1, mg.PLATE_T + 1)
    return p


def clip_holder(cfg):
    return placa(cfg) + soporte(cfg)


def envolvente_radio(cfg, ancho=None, extra_s=0.0):
    w = cfg["radio_w"] if ancho is None else ancho
    return caja(cfg, cfg["uc"] - w / 2, cfg["uc"] + w / 2, cfg["s1"] - cfg["radio_l"], cfg["s1"] + extra_s,
                RADIO_N0, RADIO_N0 + cfg["radio_t"])


def lengua(cfg, w, prof=None, off=0.5):
    prof = mg.USABLE_L if prof is None else prof
    s0 = mg.PLATE_L - prof
    return caja(cfg, cfg["uc"] - w / 2, cfg["uc"] + w / 2, s0, s0 + mg.USABLE_L, -cfg["clip_t"] - off, -off)


def clip_radio(cfg, w=None):
    w = cfg["clip_w"] if w is None else w
    # puente: mas alla del borde de la placa, hasta dentro de la envolvente de la radio
    puente = caja(cfg, cfg["uc"] - w / 2, cfg["uc"] + w / 2, mg.PLATE_L, mg.PLATE_L + 2,
                  -cfg["clip_t"] - 0.5, RADIO_N0 + 0.5)
    # junta: bajo la placa, solapa lengua y puente para que el clip sea un solo solido
    junta = caja(cfg, cfg["uc"] - w / 2, cfg["uc"] + w / 2, mg.PLATE_L - 0.5, mg.PLATE_L + 0.5,
                 -cfg["clip_t"] - 0.5, -0.5)
    return lengua(cfg, w) + junta + puente


def eje_radio(cfg):
    """Vector unitario (x,y,z del STL) del eje largo de la radio, del extremo inferior al superior."""
    return np.array([-np.sin(cfg["a"]), cfg["d"] * np.cos(cfg["a"]), 0.0])


# ---------------------------------------------------------------- zona del tripode
def hex_poly():
    R = mg.NUT_AF / np.sqrt(3)
    return sg.Polygon([(mg.T_YC + R * np.cos(np.pi / 6 + k * np.pi / 3),
                        mg.T_ZC + R * np.sin(np.pi / 6 + k * np.pi / 3)) for k in range(6)])   # caras planas en +-Y


def bolsillo_2d(z_ext):
    """Hexagono + canal de entrada lateral (hacia -Z) con las esquinas redondeadas (poligono en (y,z))."""
    canal = sg.box(mg.T_YC - mg.NUT_AF / 2, z_ext - 1.0, mg.T_YC + mg.NUT_AF / 2, mg.T_ZC)
    return hex_poly().union(canal).buffer(-FILETE).buffer(FILETE)


def brida_poly():
    return sg.box(mg.T_YC - BRIDA_Y / 2, mg.T_ZC - BRIDA_Z / 2,
                  mg.T_YC + BRIDA_Y / 2, mg.T_ZC + BRIDA_Z / 2).buffer(-BRIDA_R).buffer(BRIDA_R)


def prisma_x(poly, x0, x1):
    partes = rb.x_prism(poly, x0, x1)
    return mf.Manifold.batch_boolean(partes, mf.OpType.Add) if len(partes) > 1 else partes[0]


def cilindro_x(radio, x0, x1, y, z):
    c = trimesh.creation.cylinder(radius=radio, height=x1 - x0, sections=48)
    c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    c.apply_translation([(x0 + x1) / 2, y, z])
    return to_mf(c)


def brida():
    """Brida con chaflan de 45 grados: cara del culo plana en x = BUTT_FACE; el exterior de arriba no cambia."""
    p0, p1 = brida_poly(), brida_poly().buffer(-BRIDA_CH)
    pts = []
    for poly, xs in ((p0, (X_BRIDA0, mg.BUTT_FACE)), (p1, (X_BRIDA0 - BRIDA_CH,))):
        for y, z in np.asarray(poly.exterior.coords)[:-1]:
            pts += [[x, y, z] for x in xs]
    return to_mf(trimesh.convex.convex_hull(np.array(pts)))


def z_exterior(verts):
    """Z de la cara lateral por donde entra la tuerca (minimo del culo, o de la brida si es mas baja)."""
    z = float(verts[verts[:, 0] > mg.BUTT_FACE - 12][:, 2].min())
    return min(z, mg.T_ZC - BRIDA_Z / 2) if BRIDA else z


def rampa_relleno(malla, x_solido):
    """Como rb.ramp_fill, pero tolera secciones sin cavidad al inicio de la rampa."""
    x_ini = x_solido - rb.TAPER_L
    r_max = rb.inscribed_radius(rb.cavity_at(malla, x_solido - 0.5))
    piezas = []
    for i in range(int(round(rb.TAPER_L / rb.STEP_DX)) + 1):
        x0 = x_ini + i * rb.STEP_DX
        x1 = x0 + rb.STEP_DX
        xc = min((x0 + x1) / 2, x_solido - 0.05)
        cav = rb.cavity_at(malla, xc)
        if cav is None:
            continue
        s = (xc - x_ini) / rb.TAPER_L
        anillo = cav.buffer(rb.OVERLAP).difference(cav.buffer(-1.02 * r_max * s))
        piezas += rb.x_prism(anillo, x0 - 0.01, min(x1, x_solido + 0.1) + 0.01)
    return mf.Manifold.batch_boolean(piezas, mf.OpType.Add), x_ini, r_max


_CACHE = {}


def base_reforzada(src):
    """v1 + rosca lateral rellena + cavidad maciza + brida + bolsillo de tuerca. No depende de la radio."""
    clave = str(Path(src).resolve())
    if clave in _CACHE:
        return _CACHE[clave]
    m = trimesh.load(src)
    m.merge_vertices()
    body = to_mf(m)
    print("v1:", body.status(), round(body.volume() / 1000, 1), "cm3")
    # rosca lateral del movil: relleno identico a v3
    body = body + mg.box(-9.2, -2.6, mg.TY0, mg.YC + 5.9, mg.OLD_Z - 5.8, mg.OLD_Z + 5.8) \
        + mg.cyl_u(mg.YC, mg.OLD_Z, 3.45, -19.3, 0.2)
    # nicho de tuerca antiguo de v1: se rellena (como v3) y se vuelve a vaciar mas abajo con otra geometria
    hull = to_mf(trimesh.convex.convex_hull(m.vertices[m.vertices[:, 0] > mg.BUTT_FACE - 12]))
    x_old = mg.BUTT_FACE - mg.OLD_SKIN - mg.NUT_T
    nicho = to_mf(trimesh.creation.box(bounds=[[x_old - 0.1, mg.T_YC - mg.NUT_AF / 2 - 0.1, -1],
                                               [mg.BUTT_FACE - mg.OLD_SKIN + 0.1, mg.T_YC + mg.NUT_AF / 2 + 0.1, mg.T_ZC + 0.1]]))
    body = body + (nicho ^ hull)
    if BRIDA:
        body = body + brida()
    # cavidad maciza desde X_SOLIDO0 hasta el culo, con rampa conica antes (logica de refuerzo_base.py)
    malla = to_tm(body)
    malla.merge_vertices()
    rampa, x_ini, r_max = rampa_relleno(malla, X_SOLIDO0)
    cola = rb.void_tail(malla, X_SOLIDO0)
    body = body + rampa + cola if cola is not None else body + rampa
    comps = to_tm(body).split(only_watertight=False)
    keep = [c for c in comps if abs(c.volume) >= rb.MIN_VOID_MM3]
    body = to_mf(trimesh.util.concatenate(keep))
    print(f"cavidad maciza x={X_SOLIDO0:.1f}..{mg.BUTT_FACE:.1f}, rampa x={x_ini:.1f}..{X_SOLIDO0:.1f}, r_inscrito={r_max:.2f}")
    # bolsillo hexagonal, taladro con alivio y labios de retencion
    z_ext = z_exterior(m.vertices)
    body = body - prisma_x(bolsillo_2d(z_ext), X_P0, X_P1)
    body = body - cilindro_x(mg.NUT_HOLE / 2, X_P0 - RELIEF, mg.BUTT_FACE + 1, mg.T_YC, mg.T_ZC)
    for sgn in (-1, 1):
        y_in = mg.T_YC + sgn * (mg.NUT_AF / 2 - LABIO)
        y_out = mg.T_YC + sgn * (mg.NUT_AF / 2 + 0.3)
        body = body + to_mf(trimesh.creation.box(
            bounds=[[X_P0, min(y_in, y_out), z_ext], [X_P1, max(y_in, y_out), z_ext + LABIO_L]]))
    _CACHE[clave] = (body, z_ext)
    return _CACHE[clave]


def build_variant(src, out_dir, key):
    perfil = cargar_perfiles()[key]
    cfg = configuracion(key)
    base, _ = base_reforzada(src)
    body = base + clip_holder(cfg)
    dst = Path(out_dir) / perfil["stl_v6"]
    out = to_tm(body)
    out.export(dst)
    digest = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f"{key}: tilt {cfg['deg']:g} grados hacia {'+V' if cfg['d'] > 0 else '-V'} ({TILT_HACIA}), lado {LADO_U} (uc={cfg['uc']:.2f}), PH0={cfg['ph0']}, "
          f"hueco clip {cfg['w_in']:g} mm, radio {cfg['radio_l']:g}x{cfg['radio_w']:g}x{cfg['radio_t']:g} "
          f"({perfil['radio'].get('estado_medida')}), {np.round(out.extents, 1)} mm, {body.status()}, {digest[:16]}")
    return dst


if __name__ == "__main__":
    TILT_HACIA, LADO_U, TILT_DEG, BRIDA = _cli_args.tilt_hacia, _cli_args.lado_u, _cli_args.tilt_deg, not _cli_args.sin_brida
    out = Path(_cli_args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    keys = claves_v6() if _cli_args.variant == "todas" else [_cli_args.variant]
    for k in keys:
        if k not in claves_v6():
            sys.exit(f"variante sin STL v6: {k}")
        build_variant(_cli_args.source, out, k)
