#!/usr/bin/env python3
"""Genera los diagramas de las guias (vistas acotadas, explosionado, cortes, orientacion de impresion).

    python src/render_guia.py stl/v6/mango_spacequad_v6_uvk5v3.stl docs/img/guia/v6

Requiere trimesh, numpy, matplotlib, pyvista y manifold3d. Las cotas del CAD salen de src/mango_v3.py y
src/mango_v6.py (posicion plana v6.4: placa en U 0..plate_w, inclinada -V; el marco de la placa sale de
mango_v6.configuracion); las medidas del STL se leen del propio modelo. La variante de radio se deduce del
nombre del STL (uvk5v3 o rt950pro) o de --radio. Las piezas comerciales (boom, tuerca, tornillo, lengua del
clip) son esquemas a escala nominal, no modelos de fabricante. Sobrescribe los PNG destino.
Sistema de coordenadas del STL: X = -H (hacia la empunadura), Y = V (a lo largo del boom), Z = U (hacia la torre)."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
import trimesh
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path as MplPath
from shapely.geometry import Polygon as ShPoly

import mango_v3 as mg
import mango_v6 as mv6
from i18n_figuras import LANGS, num, set_lang, t
from orientacion_impresion import orientaciones

# Cotas del CAD (mm), de src/mango_v3.py y src/mango_v6.py
TUNEL, BOOM = 15.5, 15.0
TUNEL_X, TUNEL_Z = 0.0, mv6.U_BOOM     # eje del tunel en el plano XZ
BUTT_X, T_YC, T_ZC = mg.BUTT_FACE, mg.T_YC, mg.T_ZC
NUT_AF, NUT_SLOT, NUT_HOLE, SKIN = mg.NUT_AF, mg.NUT_T, mg.NUT_HOLE, mv6.SKIN_V6
NUT_NOM_AF, NUT_NOM_T = 11.1, mg.NUT_T_NOMINAL
PLATE_L, PLATE_T, WALL, USABLE = mg.PLATE_L, mg.PLATE_T, mg.SIDE_T, mg.USABLE_L
GRIS, AZUL, ROJO, VERDE, NARANJA = "#b8bec6", "#1f6fb2", "#c0392b", "#2e8b57", "#e67e22"
CFG = None   # marco de la placa de la radio (mango_v6.configuracion), fijado en main()


def pt(s, n=0.0, u=None):
    """Punto del marco de la placa (s a lo largo, n normal, u transversal) en coordenadas del STL (X = -H, Y = V, Z = U)."""
    v, h = mv6.punto(CFG, s, n)
    return np.array([-h, v, CFG["uc"] if u is None else u])


def dir_s():
    return np.array([-np.sin(CFG["a"]), CFG["d"] * np.cos(CFG["a"]), 0.0])   # eje largo de la radio, hacia el borde libre


def dir_n():
    return np.array([-np.cos(CFG["a"]), -CFG["d"] * np.sin(CFG["a"]), 0.0])  # normal de la placa, hacia la radio


def cargar(ruta):
    return pv.read(str(ruta))


class Vista:
    """Camara ortografica con correspondencia mundo->pixel conocida para anotar encima."""

    def __init__(self, mallas, dir_cam, arriba, escala, centro, size=(1400, 1000)):
        self.size = size
        pl = pv.Plotter(off_screen=True, window_size=size)
        pl.set_background("white")
        for malla, kw in mallas:
            pl.add_mesh(malla, smooth_shading=False, **kw)
        d = np.asarray(dir_cam, float)
        d /= np.linalg.norm(d)
        c = np.asarray(centro, float)
        pl.camera.focal_point = c
        pl.camera.position = c + d * 2000
        pl.camera.up = arriba
        pl.camera.parallel_projection = True
        pl.camera.parallel_scale = escala
        pl.camera.clipping_range = (1, 5000)
        self.img = pl.screenshot(return_img=True)
        pl.close()
        self.k = size[1] / (2 * escala)
        self.c = c
        up = np.asarray(arriba, float)
        up = up - d * (up @ d)
        self.up = up / np.linalg.norm(up)
        self.right = np.cross(self.up, d)

    def px(self, p):
        p = np.asarray(p, float) - self.c
        return (self.size[0] / 2 + (p @ self.right) * self.k, self.size[1] / 2 - (p @ self.up) * self.k)

    def figura(self, titulo):
        fig = plt.figure(figsize=(self.size[0] / 100, self.size[1] / 100), dpi=100)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.imshow(self.img)
        ax.set_xlim(0, self.size[0])
        ax.set_ylim(self.size[1], 0)
        ax.axis("off")
        ax.text(20, 34, titulo, fontsize=16, weight="bold", va="top")
        return fig, ax


def cota(ax, v, p0, p1, texto, off=(0, 0), color=ROJO):
    a, b = v.px(p0), v.px(p1)
    a, b = (a[0] + off[0], a[1] + off[1]), (b[0] + off[0], b[1] + off[1])
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="<->", color=color, lw=1.6))
    for q, o in ((a, p0), (b, p1)):
        o_px = v.px(o)
        ax.plot([o_px[0], q[0]], [o_px[1], q[1]], color=color, lw=0.8, ls=":")
    ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 8, texto, color=color, fontsize=11, ha="center", va="bottom",
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))


def bola(ax, xy, n, color=AZUL):
    ax.add_patch(plt.Circle(xy, 20, color=color, zorder=5))
    ax.text(xy[0], xy[1], str(n), color="white", ha="center", va="center", fontsize=13, weight="bold", zorder=6)


def etiqueta(ax, xy, texto, **kw):
    ax.text(xy[0], xy[1], texto, fontsize=11, bbox=dict(fc="white", ec="#888", alpha=0.9, pad=2), **kw)


def ejes_uso(ax, v, origen_px):
    """Leyenda de ejes del STL proyectados en la vista."""
    for nombre, vec, col in ((t("ax_x"), (1, 0, 0), ROJO), (t("ax_y"), (0, 1, 0), VERDE),
                             (t("ax_z"), (0, 0, 1), AZUL)):
        vec = np.asarray(vec, float)
        dx, dy = (vec @ v.right) * 60, -(vec @ v.up) * 60
        if abs(dx) + abs(dy) < 3:
            ax.plot(*origen_px, "o", color=col, ms=9)
            ax.text(origen_px[0] + 12, origen_px[1] + 12, f"{nombre} ({t('ax_obs')})", color=col, fontsize=9)
            continue
        ax.annotate("", xy=(origen_px[0] + dx, origen_px[1] + dy), xytext=origen_px,
                    arrowprops=dict(arrowstyle="->", color=col, lw=2))
        ax.text(origen_px[0] + dx * 1.15, origen_px[1] + dy * 1.15, nombre, color=col, fontsize=9)


def fig_vistas(malla, mallas_pv, out, bb):
    ex = bb[1] - bb[0]
    c = (bb[0] + bb[1]) / 2
    kw = dict(color=GRIS, specular=0.2)
    # 1) planta lateral (mirando -Z): plano V-H con la placa a 20 grados
    v = Vista([(mallas_pv, kw)], (0, 0, 1), (-1, 0, 0), 145, c)
    fig, ax = v.figura(t("f1a"))
    cota(ax, v, (bb[0][0], bb[1][1] + 5, bb[1][2]), (bb[1][0], bb[1][1] + 5, bb[1][2]),
         t("f1a_h", v=num(ex[0])), off=(80, 0))
    cota(ax, v, (bb[0][0], bb[0][1], bb[1][2]), (bb[0][0], bb[1][1], bb[1][2]),
         t("f1a_l", v=num(ex[1])), off=(0, -45))
    # angulo de la placa (posicion D: inclinada -V, en el lado -U del boom)
    p0, p1 = pt(0, 0), pt(PLATE_L, 0)
    ax.plot(*zip(v.px(p0), v.px(p1)), color=NARANJA, lw=3)
    etiqueta(ax, (v.px(p1)[0] + 15, v.px(p1)[1] - 30), t("f1a_plate", l=f"{PLATE_L:.0f}", w=f"{CFG['plate_w']:.0f}", t=f"{PLATE_T:.0f}", a=f"{CFG['deg']:.0f}"),
             color=NARANJA)
    # envolvente estimada de la radio sobre la placa
    s_a, s_b = CFG["s1"] - CFG["radio_l"], CFG["s1"]
    n_a, n_b = mv6.RADIO_N0, mv6.RADIO_N0 + CFG["radio_t"]
    cont = [v.px(pt(s, n)) for s, n in ((s_a, n_a), (s_b, n_a), (s_b, n_b), (s_a, n_b), (s_a, n_a))]
    ax.plot(*zip(*cont), color=AZUL, lw=1.8, ls="--")
    etiqueta(ax, (cont[2][0] + 10, cont[2][1] - 10), t("f1a_radio", l=num(CFG["radio_l"], 0), t=num(CFG["radio_t"])), color=AZUL)
    # cartelas, pedestal y paredes
    g = (pt(0.5 * PLATE_L, 0.2) + np.array([-mg.ROOT_H0, (mg.ROOT_V0 + mg.ROOT_V1) / 2, CFG["uc"]])) / 2
    etiqueta(ax, (v.px(g)[0] - 250, v.px(g)[1] + 5), t("f1a_gusset", t=f"{mg.SIDE_T:.0f}"), color=ROJO)
    if mv6.LADO_U in ("-U", "plano"):
        viga = (-(mv6.PED_H0 + mg.TOWER_H) / 2, (mg.ROOT_V0 + mg.ROOT_V1) / 2, CFG["u0"])
        ax.plot(*v.px(viga), "o", color=VERDE, ms=7)
        etiqueta(ax, (v.px(viga)[0] - 270, v.px(viga)[1] + 25),
                 t("f1a_beam", w=num(mg.ROOT_V1 - mg.ROOT_V0, 0), h=num(mg.TOWER_H - mv6.PED_H0)), color=VERDE)
    ejes_uso(ax, v, (110, 900))
    fig.savefig(out / "fig01a_vista_lateral.png")
    plt.close(fig)

    # 2) vista de extremo (desde +Y): tunel del boom
    v = Vista([(mallas_pv, kw)], (0, 1, 0), (-1, 0, 0), 145, c)
    fig, ax = v.figura(t("f1b"))
    t0 = (TUNEL_X - TUNEL / 2, bb[1][1], TUNEL_Z - TUNEL / 2)
    t1 = (TUNEL_X - TUNEL / 2, bb[1][1], TUNEL_Z + TUNEL / 2)
    cota(ax, v, t0, t1, t("tunnel", v=num(TUNEL)), off=(-70, 0))
    cota(ax, v, (bb[0][0], bb[1][1], bb[0][2]), (bb[1][0], bb[1][1], bb[0][2]), num(ex[0]), off=(-110, 0))
    cota(ax, v, (bb[0][0], bb[1][1], bb[0][2]), (bb[0][0], bb[1][1], bb[1][2]), t("f1b_w", v=num(ex[2])), off=(0, -40))
    ejes_uso(ax, v, (110, 900))
    fig.savefig(out / "fig01b_vista_extremo.png")
    plt.close(fig)

    # 3) planta de la placa (desde -X): placa en el lado -U, viga hacia la torre
    v = Vista([(mallas_pv, kw)], (-1, 0, 0), (0, 1, 0), 70, (-70, 140, 15))
    fig, ax = v.figura(t("f1c"))
    v_s0 = pt(0)[1]
    v_s1 = pt(PLATE_L)[1]
    u0, u1 = CFG["u0"], CFG["u0"] + CFG["plate_w"]
    cota(ax, v, (-80, v_s0, u0), (-80, v_s0, u1), f"{CFG['plate_w']:.0f}", off=(0, -60))
    cota(ax, v, (-80, v_s1, u0 - 4), (-80, v_s0, u0 - 4),
         t("f1c_proj", v=num(abs(v_s0 - v_s1)), l=f"{PLATE_L:.0f}"), off=(-40, 0))
    if mv6.LADO_U in ("-U", "plano"):
        cota(ax, v, (-80, mg.ROOT_V1, u0), (-80, mg.ROOT_V1, mv6.TORRE_U0 + mv6.EMBED_U),
             t("f1c_beam", w=num(mg.ROOT_V1 - mg.ROOT_V0, 0), h=num(mg.TOWER_H - mv6.PED_H0), e=num(mv6.EMBED_U)),
             off=(0, -25), color=VERDE)
    etiqueta(ax, (30, 960), t("f1c_gap", g=f"{CFG['w_in']:.0f}", w=f"{WALL:.0f}"), color=AZUL)
    ejes_uso(ax, v, (1250, 900))
    fig.savefig(out / "fig01c_planta_placa.png")
    plt.close(fig)


def caja(centro, ext, **kw):
    return pv.Box(bounds=(centro[0] - ext[0] / 2, centro[0] + ext[0] / 2, centro[1] - ext[1] / 2,
                          centro[1] + ext[1] / 2, centro[2] - ext[2] / 2, centro[2] + ext[2] / 2))


def fig_explosionado(mallas_pv, out, bb):
    s_dir, n_dir = dir_s(), dir_n()
    # lengua del clip bajo la placa: s de PLATE_L-USABLE a PLATE_L, bajo la cara inferior; en la posicion D entra
    # paralela a la placa por el borde libre (extremo alto, s = PLATE_L), desplazandose hacia -s
    centro_lengua = pt(PLATE_L - USABLE / 2, -CFG["clip_t"] / 2 - 0.5)
    desp_clip = s_dir * 70
    lengua = pv.Box(bounds=(-CFG["clip_t"] / 2, CFG["clip_t"] / 2, -USABLE / 2, USABLE / 2, -CFG["clip_w"] / 2, CFG["clip_w"] / 2))
    rot = np.eye(4)
    rot[:3, :3] = np.column_stack([-n_dir, s_dir, [0, 0, CFG["d"]]])   # determinante +1 para -V y +V
    lengua.transform(rot, inplace=True)
    lengua.translate(centro_lengua + desp_clip, inplace=True)
    boom = pv.Box(bounds=(-BOOM / 2, BOOM / 2, 0, 190, -BOOM / 2, BOOM / 2))
    boom.translate((TUNEL_X, 40.0 - 130 + 80, TUNEL_Z), inplace=True)       # fuera del tunel, hacia -Y
    boom.translate((0, -75, 0), inplace=True)
    tuerca = pv.Cylinder(center=(BUTT_X - SKIN - NUT_SLOT / 2, T_YC, -45.0), direction=(1, 0, 0),
                         radius=NUT_NOM_AF / np.sqrt(3), height=NUT_NOM_T, resolution=6)
    tornillo = pv.Cylinder(center=(BUTT_X + 31, T_YC, T_ZC), direction=(1, 0, 0), radius=6.35 / 2, height=14)
    plano = pv.Box(bounds=(BUTT_X + 38, BUTT_X + 44, T_YC - 22, T_YC + 22, T_ZC - 22, T_ZC + 22))
    escena = [(mallas_pv, dict(color=GRIS, specular=0.2)),
              (boom, dict(color="#9fb4c7", opacity=0.9)), (tuerca, dict(color="#d4a017")),
              (tornillo, dict(color="#555555")), (plano, dict(color="#7f8c8d", opacity=0.9)),
              (lengua, dict(color="#2980b9", opacity=0.85))]
    c = np.array([10, 115, 5.0])
    v = Vista(escena, (-0.55, -0.62, 0.55), (-1, 0, 0), 190, c, size=(1500, 1100))
    fig, ax = v.figura(t("f2"))
    # flechas de montaje
    def flecha(p0, p1, n, col=AZUL, d=(20, -20)):
        a, b = v.px(p0), v.px(p1)
        ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2, ls="--"))
        bola(ax, ((a[0] + b[0]) / 2 + d[0], (a[1] + b[1]) / 2 + d[1]), n)
    flecha((BUTT_X - SKIN - NUT_SLOT / 2, T_YC, -45.0), (BUTT_X - SKIN - NUT_SLOT / 2, T_YC, 8.0), 1, "#d4a017")
    flecha((BUTT_X + 31, T_YC, T_ZC), (BUTT_X + 12, T_YC, T_ZC), 2, ROJO, (60, 10))
    flecha((TUNEL_X, boom.center[1] + 60, TUNEL_Z), (TUNEL_X, 110, TUNEL_Z), 3, VERDE)
    flecha(tuple(centro_lengua + desp_clip), tuple(centro_lengua), 4, NARANJA)
    etiqueta(ax, (30, 1010), t("f2_l1") + "\n" + t("f2_l2"), va="top")
    ejes_uso(ax, v, (1230, 150))
    fig.savefig(out / "fig02_explosionado.png")
    plt.close(fig)


def bucles(malla, plano_origen, plano_normal):
    s = malla.section(plane_origin=plano_origen, plane_normal=plano_normal)
    return [] if s is None else s.discrete


def rellenar(ax, lazos, cols, **kw):
    """Dibuja la seccion con huecos reales (diferencia simetrica de los lazos)."""
    g = None
    for d in lazos:
        p = ShPoly(d[:, cols]).buffer(0)
        g = p if g is None else g.symmetric_difference(p)
    for poly in ([] if g is None else (g.geoms if hasattr(g, "geoms") else [g])):
        rings = [poly.exterior] + list(poly.interiors)
        verts = np.concatenate([np.asarray(r.coords) for r in rings])
        codes = np.concatenate([[MplPath.MOVETO] + [MplPath.LINETO] * (len(r.coords) - 2) + [MplPath.CLOSEPOLY] for r in rings])
        ax.add_patch(PathPatch(MplPath(verts, codes), **kw))


def fig_cortes(malla, out):
    fig, axs = plt.subplots(1, 2, figsize=(15, 7.5), dpi=100)
    # A: corte transversal del tunel (plano y=100 -> ejes z horizontal, x vertical hacia abajo = empunadura)
    ax = axs[0]
    rellenar(ax, bucles(malla, [0, 100, 0], [0, 1, 0]), [2, 0], fc="#dfe6ee", ec="#34495e", lw=1.2)
    ax.add_patch(Rectangle((TUNEL_Z - BOOM / 2, TUNEL_X - BOOM / 2), BOOM, BOOM, fc="none", ec=VERDE, lw=2, ls="--"))
    ax.set_xlim(-6, 38)
    ax.set_ylim(-20, 20)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.set_title(t("f3a", t=num(TUNEL), b=num(BOOM)), fontsize=12, weight="bold")
    ax.annotate("", xy=(TUNEL_Z - TUNEL / 2, -12), xytext=(TUNEL_Z + TUNEL / 2, -12),
                arrowprops=dict(arrowstyle="<->", color=ROJO))
    ax.text(TUNEL_Z, -13.5, t("f3a_gap", t=num(TUNEL), g=num((TUNEL - BOOM) / 2, 2)), color=ROJO, ha="center")
    ax.set_xlabel("Z (mm)")
    ax.set_ylabel(t("f3a_ylab"))
    # B: corte longitudinal por el eje de la tuerca (plano z = T_ZC): x horizontal, y vertical
    ax = axs[1]
    rellenar(ax, bucles(malla, [0, 0, 12.0], [0, 0, 1]), [0, 1], fc="#dfe6ee", ec="#34495e", lw=1.2)
    ax.add_patch(Rectangle((BUTT_X - SKIN - NUT_SLOT, T_YC - NUT_AF / 2), NUT_SLOT, NUT_AF, fc="none", ec=NARANJA, lw=2, ls="--"))
    ax.set_xlim(70, 118)
    ax.set_ylim(T_YC - 20, T_YC + 20)
    ax.set_aspect("equal")
    ax.set_title(t("f3b"), fontsize=12, weight="bold")
    ax.annotate("", xy=(BUTT_X - SKIN - NUT_SLOT, T_YC + 9), xytext=(BUTT_X - SKIN, T_YC + 9),
                arrowprops=dict(arrowstyle="<->", color=ROJO))
    ax.text(BUTT_X - SKIN - NUT_SLOT / 2, T_YC + 10, t("slot", v=num(NUT_SLOT)), color=ROJO, ha="center")
    ax.annotate("", xy=(BUTT_X - SKIN, T_YC - 9), xytext=(BUTT_X, T_YC - 9), arrowprops=dict(arrowstyle="<->", color=ROJO))
    ax.text(BUTT_X - SKIN / 2, T_YC - 11, t("skin", v=num(SKIN)), color=ROJO, ha="center")
    ax.text(BUTT_X - SKIN - NUT_SLOT / 2, T_YC - NUT_AF / 2 - 2.5, t("af", v=num(NUT_AF), n=num(NUT_NOM_AF)),
            color=NARANJA, ha="center")
    ax.text(80, T_YC + 15, t("hole", v=num(NUT_HOLE)), color=ROJO)
    # cavidad del mango maciza FILL_L mm desde el culo y rosca engranada con la piel de 2 mm
    ax.annotate("", xy=(BUTT_X - mv6.FILL_L, T_YC - 16), xytext=(BUTT_X, T_YC - 16), arrowprops=dict(arrowstyle="<->", color=VERDE))
    ax.text(BUTT_X - mv6.FILL_L / 2, T_YC - 18.5, t("f3b_fill", v=num(mv6.FILL_L, 0)), color=VERDE, ha="center")
    ax.text(80, T_YC + 17.5, t("f3b_screw"), color=NARANJA)
    ax.set_xlabel(t("f3b_xlab"))
    ax.set_ylabel("Y (mm)")
    fig.tight_layout()
    fig.savefig(out / "fig03_cortes.png")
    plt.close(fig)


def fig_orientacion(malla, mallas_pv, out, filas):
    cands = [(t("oA"), (0, -1, 0), (-1, 0, 0), "Y−"),
             (t("oB"), (1, 0, 0), (0, 1, 0), "X+"),
             (t("oC"), (0, 0, 1), (-1, 0, 0), "Z+")]
    fig, axs = plt.subplots(1, 3, figsize=(17, 7), dpi=100)
    for ax, (tit, cama_dir, up_hint, clave) in zip(axs, cands):
        d = -np.asarray(cama_dir, float)
        # la camara mira lateralmente a la pieza, con la cama (direccion de cama_dir) abajo
        look = np.cross(d, up_hint)
        look = look / np.linalg.norm(look) if np.linalg.norm(look) > 1e-6 else np.array([0, 0, 1.0])
        v = Vista([(mallas_pv, dict(color=GRIS, specular=0.2))], look, d, 110, malla.bounds.mean(0), size=(900, 900))
        ax.imshow(v.img)
        ax.axis("off")
        base = v.px(malla.bounds.mean(0) + np.asarray(cama_dir) * (malla.extents @ np.abs(cama_dir)) / 2)[1]
        ax.axhline(base, color="k", lw=4)
        ax.text(450, base + 25, t("bed"), ha="center", va="top", fontsize=11)
        f = next(x for x in filas if x["cama"] == clave.replace("−", "-"))
        ax.set_title(tit + "\n" + t("o_met", h=f["altura_mm"], c=f["contacto_mm2"], o=f["voladizo_mm2"]), fontsize=11)
    fig.suptitle(t("f4"), fontsize=13, weight="bold")
    fig.tight_layout()
    fig.savefig(out / "fig04_orientacion_impresion.png")
    plt.close(fig)


def fig_clip(mallas_pv, out, bb):
    # el clip entra paralelo a la placa por el borde libre (extremo alto, s = PLATE_L) hacia -s
    centro = (pt(PLATE_L / 2, 0) + np.array([0, 0, 0]))
    v = Vista([(mallas_pv, dict(color=GRIS, specular=0.2))], (0, 0, 1), (-1, 0, 0), 60, centro, size=(1400, 1000))
    fig, ax = v.figura(t("f5"))
    cota(ax, v, pt(0, 0), pt(PLATE_L, 0), f"{PLATE_L:.0f}", off=(0, -70))
    etiqueta(ax, (40, 940), t("f5_gap", t=f"{PLATE_T:.0f}", g=f"{CFG['min_clear']:.0f}", c=f"{CFG['clip_t']:.0f}"), color=AZUL)
    a = v.px(pt(PLATE_L + 30, -3))
    b = v.px(pt(PLATE_L - USABLE, -3))
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=NARANJA, lw=3))
    etiqueta(ax, (a[0] - 10, a[1] + 40), t("f5_run", u=f"{USABLE:.0f}"), color=NARANJA)
    pe = v.px(pt(PLATE_L, 0))
    etiqueta(ax, (pe[0] + 15, pe[1] - 60), t("f5_edge"), color=VERDE)
    fig.savefig(out / "fig05_insercion_clip.png")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("stl", type=Path, nargs="?", default=Path("stl/v6/mango_spacequad_v6_uvk5v3.stl"),
                    help="STL v6 del mango (por defecto stl/v6/mango_spacequad_v6_uvk5v3.stl)")
    ap.add_argument("salida", type=Path, nargs="?", default=Path("docs/img/guia/v6"),
                    help="directorio base de PNG; se crea una subcarpeta por idioma")
    ap.add_argument("--radio", choices=("uvk5v3", "rt950pro"), help="variante de radio (por defecto, la del nombre del STL)")
    ap.add_argument("--langs", default=",".join(LANGS), help="idiomas separados por coma")
    a = ap.parse_args()
    global CFG
    radio = a.radio or next((k for k in ("rt950pro", "uvk5v3") if k in a.stl.name), "uvk5v3")
    CFG = mv6.configuracion(radio)
    malla = trimesh.load(a.stl)
    mpv = pv.read(str(a.stl))
    bb = malla.bounds
    filas = orientaciones(malla)
    for lang in a.langs.split(","):
        set_lang(lang)
        out = a.salida / lang
        out.mkdir(parents=True, exist_ok=True)
        (out / "orientaciones.json").write_text(json.dumps(filas, indent=1), encoding="utf-8")
        fig_vistas(malla, mpv, out, bb)
        fig_explosionado(mpv, out, bb)
        fig_cortes(malla, out)
        fig_orientacion(malla, mpv, out, filas)
        fig_clip(mpv, out, bb)
        print("OK", lang, len(list(out.glob("*.png"))))


if __name__ == "__main__":
    main()


