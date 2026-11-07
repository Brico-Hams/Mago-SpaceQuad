#!/usr/bin/env python3
"""Genera los diagramas de las guias (vistas acotadas, explosionado, cortes, orientacion de impresion).

    python src/render_guia.py stl/v5/mango_spacequad_v5_uvk5v3.stl docs/img/guia

Requiere trimesh, numpy, matplotlib y pyvista. Las cotas del CAD salen de src/mango_v3.py; las medidas del
STL se leen del propio modelo. Las piezas comerciales (boom, tuerca, tornillo, lengua del clip) son esquemas
a escala nominal, no modelos de fabricante. Sobrescribe los PNG destino.
Sistema de coordenadas del STL: X hacia la empunadura, Y a lo largo del boom, Z hacia la torre."""
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

from i18n_figuras import LANGS, num, set_lang, t
from orientacion_impresion import orientaciones

# Cotas de src/mango_v3.py (mm)
TUNEL, BOOM = 15.5, 15.0
TUNEL_X, TUNEL_Z = 0.0, 15.55          # eje del tunel en el plano XZ (medido en el STL)
BUTT_X, T_YC, T_ZC = 110.0, 115.2, 15.7
NUT_AF, NUT_SLOT, NUT_HOLE, SKIN = 11.4, 5.9, 6.6, 1.2
NUT_NOM_AF, NUT_NOM_T = 11.1, 5.6
PLATE_W, PLATE_L, PLATE_T, ANGLE, WALL = 55.0, 48.0, 4.0, 20.0, 4.0
PLATE_U0, PLATE_V0, PLATE_H0 = 24.0, 130.0, 65.0
CLIP_W, CLIP_T, USABLE = 45.0, 6.0, 40.0
GRIS, AZUL, ROJO, VERDE, NARANJA = "#b8bec6", "#1f6fb2", "#c0392b", "#2e8b57", "#e67e22"


def cargar(ruta):
    return pv.wrap(trimesh.load(ruta)) if False else pv.read(str(ruta))


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
    # angulo de la placa
    p0 = np.array([-(PLATE_H0), PLATE_V0, 79.0])
    a = np.deg2rad(ANGLE)
    p1 = p0 + PLATE_L * np.array([-np.sin(a), np.cos(a), 0])
    ax.plot(*zip(v.px(p0), v.px(p1)), color=NARANJA, lw=3)
    etiqueta(ax, (v.px(p1)[0] + 15, v.px(p1)[1] - 30), t("f1a_plate", l=f"{PLATE_L:.0f}", w=f"{PLATE_W:.0f}", t=f"{PLATE_T:.0f}", a=f"{ANGLE:.0f}"),
             color=NARANJA)
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

    # 3) planta de la placa (desde -X)
    v = Vista([(mallas_pv, kw)], (-1, 0, 0), (0, 1, 0), 70, (-70, 140, 52))
    fig, ax = v.figura(t("f1c"))
    zc = PLATE_U0
    cota(ax, v, (-80, PLATE_V0, zc), (-80, PLATE_V0, zc + PLATE_W), f"{PLATE_W:.0f}", off=(0, -60))
    cota(ax, v, (-80, PLATE_V0, 5), (-80, PLATE_V0 + PLATE_L * np.cos(np.deg2rad(ANGLE)), 5),
         t("f1c_proj", v=num(PLATE_L * np.cos(np.deg2rad(ANGLE))), l=f"{PLATE_L:.0f}"), off=(-40, 0))
    etiqueta(ax, (30, 960), t("f1c_gap", g=f"{PLATE_W - 2 * WALL:.0f}", w=f"{WALL:.0f}"), color=AZUL)
    ejes_uso(ax, v, (1250, 900))
    fig.savefig(out / "fig01c_planta_placa.png")
    plt.close(fig)


def caja(centro, ext, **kw):
    return pv.Box(bounds=(centro[0] - ext[0] / 2, centro[0] + ext[0] / 2, centro[1] - ext[1] / 2,
                          centro[1] + ext[1] / 2, centro[2] - ext[2] / 2, centro[2] + ext[2] / 2))


def fig_explosionado(mallas_pv, out, bb):
    ang = np.deg2rad(ANGLE)
    s_dir = np.array([-np.sin(ang), np.cos(ang), 0])       # a lo largo de la placa (hacia +V)
    n_dir = np.array([-np.cos(ang), -np.sin(ang), 0])      # normal de la placa (hacia fuera)
    origen_placa = np.array([-PLATE_H0, PLATE_V0, 0.0])
    uc = PLATE_U0 + PLATE_W / 2
    # lengua del clip bajo la placa: s 0..USABLE, n de -CLIP_T a 0 (v5: entra por el extremo bajo, -V)
    centro_lengua = origen_placa + s_dir * (USABLE / 2) - n_dir * (CLIP_T / 2 + 0.5)
    centro_lengua[2] = uc
    desp_clip = -s_dir * 70
    lengua = pv.Box(bounds=(-CLIP_T / 2, CLIP_T / 2, -USABLE / 2, USABLE / 2, -CLIP_W / 2, CLIP_W / 2))
    rot = np.eye(4)
    rot[:3, :3] = np.column_stack([-n_dir, s_dir, [0, 0, 1]])
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
    c = np.array([15, 120, 40.0])
    v = Vista(escena, (-0.55, -0.62, 0.55), (-1, 0, 0), 175, c, size=(1500, 1100))
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
    v = Vista([(mallas_pv, dict(color=GRIS, specular=0.2))], (0, 0, 1), (-1, 0, 0), 60, (-58, 147, 50), size=(1400, 1000))
    fig, ax = v.figura(t("f5"))
    ang = np.deg2rad(ANGLE)
    s = np.array([-np.sin(ang), np.cos(ang), 0])
    n = np.array([-np.cos(ang), -np.sin(ang), 0])
    o = np.array([-PLATE_H0, PLATE_V0, 79.0])
    cota(ax, v, o, o + s * PLATE_L, f"{PLATE_L:.0f}", off=(0, -70))
    etiqueta(ax, (40, 940), t("f5_gap", t=f"{PLATE_T:.0f}", c=f"{CLIP_T:.0f}"), color=AZUL)
    a = v.px(o + s * 0 - n * 3 - s * 30)
    b = v.px(o + s * USABLE - n * 3)
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=NARANJA, lw=3))
    etiqueta(ax, (a[0] - 10, a[1] + 40), t("f5_run", u=f"{USABLE:.0f}"), color=NARANJA)
    fig.savefig(out / "fig05_insercion_clip.png")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("stl", type=Path, help="STL del mango (p. ej. stl/v5/mango_spacequad_v5_uvk5v3.stl)")
    ap.add_argument("salida", type=Path, help="directorio base de PNG; se crea una subcarpeta por idioma")
    ap.add_argument("--langs", default=",".join(LANGS), help="idiomas separados por coma")
    a = ap.parse_args()
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


