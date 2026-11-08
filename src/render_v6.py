#!/usr/bin/env python3
"""Renders de montaje v6: radio inclinada (envolvente estimada), duplexor, boom y detalle del culo reforzado. Requiere pyvista.
Escribe docs/img/v6_<variante>_montaje.png. Solo CAD ilustrativo.
    python render_v6.py ../stl ../docs/img [--tilt-hacia +V|-V] [--lado-u plano|-U|+U] [--tilt-deg 20] [--sin-brida]
"""
import argparse
from pathlib import Path
import os


def _parse_cli():
    parser = argparse.ArgumentParser(description="Renders CAD ilustrativos de la v6; sobrescriben los PNG destino.",
                                     epilog="Ejemplo: python src/render_v6.py stl docs/img")
    parser.add_argument("stl_dir", help="directorio con el subdirectorio v6/")
    parser.add_argument("output_dir", help="directorio de salida de los PNG")
    parser.add_argument("--tilt-hacia", choices=("+V", "-V"), default="-V")
    parser.add_argument("--lado-u", choices=("plano", "-U", "+U"), default="plano")
    parser.add_argument("--tilt-deg", type=float, default=20.0)
    parser.add_argument("--sin-brida", action="store_true")
    args = parser.parse_args()
    if not (Path(args.stl_dir) / "v6").is_dir():
        parser.error("falta el subdirectorio v6 en el directorio de STL")
    return args


if __name__ == "__main__":
    _cli_args = _parse_cli()

import numpy as np, trimesh, pyvista as pv
from geom import to_tm
import mango_v3 as mg
import mango_v6 as mv6
import verificar as vf
import render_docs as rd
pv.OFF_SCREEN = True


def contorno_corte(mesh, z):
    """Lineas de la seccion del mango por el plano z=z (eje de la tuerca), en coordenadas de render."""
    sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if sec is None:
        return None
    pts, lines = [], []
    for seg in sec.discrete:
        seg = np.asarray(seg)
        base = sum(len(p) for p in pts)
        pts.append(np.c_[seg[:, 2], seg[:, 1], -seg[:, 0]])
        lines.append(np.r_[len(seg), np.arange(base, base + len(seg))])
    poly = pv.PolyData(np.vstack(pts))
    poly.lines = np.hstack(lines)
    return poly


def main(stl_dir, out):
    os.makedirs(out, exist_ok=True)
    boom = rd.bx(-7.5, 7.5, 60, 300, 8, 23.1)
    dup = to_tm(vf.duplexor())
    for key in mv6.claves_v6():
        perfil = mv6.cargar_perfiles()[key]
        cfg = mv6.configuracion(key)
        mango = trimesh.load(Path(stl_dir) / "v6" / perfil["stl_v6"])
        radio = to_tm(mv6.envolvente_radio(cfg))
        clip = to_tm(mv6.clip_radio(cfg))
        v = radio.vertices @ mv6.eje_radio(cfg)
        top, bot = radio.vertices[v > v.max() - 1e-3].mean(axis=0), radio.vertices[v < v.min() + 1e-3].mean(axis=0)
        pl = pv.Plotter(off_screen=True, shape=(1, 3), window_size=(3000, 1000))
        lado = "+V" if cfg["d"] > 0 else "-V"
        lado_u = mv6.LADO_U
        su = -1 if lado_u == "-U" else 1   # signo de U del lado de la radio ("plano" y "+U": +1)

        pl.subplot(0, 0)
        for m, col, op in ((mango, '#8d9399', 1), (radio, '#2e9e5b', 0.35), (clip, '#244a85', 1),
                           (boom, '#c9ced3', 1), (dup, '#c0392b', 0.7)):
            pl.add_mesh(pv.wrap(rd.rot(m)), color=col, opacity=op, smooth_shading=False)
        t, b = (np.array([p[2], p[1], -p[0]]) for p in (top, bot))   # misma transformacion que rd.rot
        pl.add_mesh(pv.Line(b, t), color='#f39c12', line_width=6)
        pl.add_mesh(pv.Sphere(radius=4, center=t), color='#f39c12')
        pl.add_mesh(pv.Sphere(radius=4, center=b), color='#3498db')
        c = np.array([45, 150, 20.0])
        pl.camera_position = [tuple(c + np.array((su, -0.45, 0.25)) * 520), tuple(c), (0, 0, 1)]
        pl.camera.parallel_projection = True
        pl.camera.parallel_scale = 150
        pl.set_background('white')
        titulo = (f"v6.4 pieza plana {perfil['modelo']}" if lado_u == "plano" else f"v6.2 posicion D {perfil['modelo']}")
        pl.add_text(f"{titulo}: radio en {lado_u}, extremo superior hacia {lado}, {cfg['deg']:g} grados",
                    font_size=12, position=(20, 950), color='black')
        pl.add_text(f"Envolvente {cfg['radio_l']:g} x {cfg['radio_w']:g} x {cfg['radio_t']:g} mm ({perfil['radio'].get('estado_medida')}), NO el contorno real",
                    font_size=10, position=(20, 80), color='black')
        pl.add_text('Naranja: extremo superior / azul claro: inferior / azul oscuro: clip / rojo: duplexor / gris claro: boom',
                    font_size=10, position=(20, 55), color='black')
        pl.add_text('CAD ilustrativo: sin medidas de clip verificadas ni prueba fisica', font_size=10, position=(20, 30), color='black')

        pl.subplot(0, 1)
        pl.add_mesh(pv.wrap(rd.rot(mango)), color='#8d9399', opacity=0.18, smooth_shading=False)
        corte = contorno_corte(mango, mg.T_ZC)
        if corte is not None:
            pl.add_mesh(corte, color='#c0392b', line_width=3)
        c2 = np.array([mg.T_ZC, mg.T_YC, -(mv6.X_SOLIDO0 + mv6.FILL_L / 2)])
        pl.camera_position = [tuple(c2 + np.array((-1, 0, 0)) * 400), tuple(c2), (0, 0, 1)]
        pl.camera.parallel_projection = True
        pl.camera.parallel_scale = 30
        pl.set_background('white')
        pl.add_text('Detalle del culo reforzado: corte por el eje de la tuerca (rojo)', font_size=12, position=(20, 950), color='black')
        pl.add_text(f"Piel {mv6.SKIN_V6:g} mm, pared >= {mv6.PARED_MIN:g} mm, cavidad maciza {mv6.FILL_L:g} mm con rampa, brida {'si' if mv6.BRIDA else 'no'}",
                    font_size=10, position=(20, 55), color='black')
        pl.add_text('CAD ilustrativo: sin prueba de carga ni de impresion', font_size=10, position=(20, 30), color='black')

        pl.subplot(0, 2)
        for m, col, op in ((mango, '#8d9399', 1), (radio, '#2e9e5b', 0.35), (clip, '#244a85', 1),
                           (boom, '#c9ced3', 1), (dup, '#c0392b', 0.7)):
            pl.add_mesh(pv.wrap(rd.rot(m)), color=col, opacity=op, smooth_shading=False)
        pl.add_mesh(pv.Line(b, t), color='#f39c12', line_width=6)
        pl.add_mesh(pv.Sphere(radius=4, center=t), color='#f39c12')
        pl.camera_position = [tuple(c + np.array((0.45 * su, -1, 0.45)) * 520), tuple(c), (0, 0, 1)]   # desde el extremo -V, arriba y de lado
        pl.camera.parallel_projection = True
        pl.camera.parallel_scale = 150
        pl.set_background('white')
        pl.add_text(f"Vista desde atras del operador (extremo -V, empunadura abajo): radio en {lado_u}, tilt {lado}",
                    font_size=12, position=(20, 950), color='black')
        pl.add_text('CAD ilustrativo: sin medidas de clip verificadas ni prueba fisica', font_size=10, position=(20, 30), color='black')
        pl.screenshot(os.path.join(out, f'v6_{key}_montaje.png'))
        pl.close()

        # vista de impresion: marco del STL sin rotar (Z arriba), cama gris clara en z = 0
        pi = pv.Plotter(off_screen=True, window_size=(1800, 1000))
        pi.add_mesh(pv.wrap(mango), color='#8d9399', smooth_shading=False)
        ctr = mango.bounds.mean(axis=0)
        ext = float(np.max(mango.extents))
        cama = pv.Plane(center=(ctr[0], ctr[1], 0), direction=(0, 0, 1), i_size=1.4 * ext, j_size=1.4 * ext)
        pi.add_mesh(cama, color='#d9d9d9', opacity=0.6)
        pi.camera_position = [tuple(ctr + np.array((0.25, -1, 0.12)) * 1.6 * ext), tuple(ctr), (0, 0, 1)]
        pi.set_background('white')
        pi.add_text(f"{'v6.4 pieza plana' if lado_u == 'plano' else 'v6 ' + lado_u} {perfil['modelo']}: como se imprime (Z arriba, cama gris en z = 0)",
                    font_size=12, position=(20, 950), color='black')
        pi.add_text(f"z minimo del STL: {mango.bounds[0][2]:.2f} mm", font_size=10, position=(20, 55), color='black')
        pi.add_text('CAD ilustrativo: sin prueba de impresion ni de resistencia', font_size=10, position=(20, 30), color='black')
        pi.screenshot(os.path.join(out, f'v6_{key}_impresion.png'))
        pi.close()


if __name__ == '__main__':
    mv6.TILT_HACIA, mv6.LADO_U, mv6.TILT_DEG, mv6.BRIDA = _cli_args.tilt_hacia, _cli_args.lado_u, _cli_args.tilt_deg, not _cli_args.sin_brida
    main(_cli_args.stl_dir, _cli_args.output_dir)
