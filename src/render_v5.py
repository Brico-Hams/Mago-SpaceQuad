#!/usr/bin/env python3
"""Renders de montaje v5: radio antes (v3) y despues (v5, girada 180 grados). Requiere pyvista.
Cada imagen marca el extremo A de la radio (naranja: el que en la v3 queda hacia +V) y su frente (azul).
    python render_v5.py ../stl ../docs/img
"""
import argparse
from pathlib import Path
import os


def _parse_cli():
    parser = argparse.ArgumentParser(description="Renders CAD ilustrativos de la v5; sobrescriben los PNG destino.",
                                     epilog="Ejemplo: python src/render_v5.py stl docs/img")
    parser.add_argument("stl_dir", help="directorio con stl/mango_spacequad_v3.stl y stl/v5/")
    parser.add_argument("output_dir", help="directorio de salida de los PNG")
    args = parser.parse_args()
    if not (Path(args.stl_dir) / "v5").is_dir():
        parser.error("falta el subdirectorio v5 en el directorio de STL")
    return args


if __name__ == "__main__":
    _cli_args = _parse_cli()

import numpy as np, trimesh, pyvista as pv
from geom import *
import mango_v3 as mg
import verificar as vf
import verificar_v5 as v5
import render_docs as rd
import mango_v5 as m5
pv.OFF_SCREEN = True


def pieces(after):
    uc, s1 = v5.UC, mg.PLATE_L + vf.R_ABOVE
    radio, clip = vf.walki(), vf.radio_clip()
    end_a = mg.plate_box(uc - vf.R_W/2, uc + vf.R_W/2, s1 - 10, s1, mg.PLATE_T + 0.5, mg.PLATE_T + 0.5 + vf.R_T)
    front = mg.plate_box(uc - vf.R_W/2 + 4, uc + vf.R_W/2 - 4, s1 - vf.R_L + 25, s1 - 25,
                         mg.PLATE_T + 0.5 + vf.R_T, mg.PLATE_T + 2.5 + vf.R_T)
    parts = [radio, clip, end_a, front]
    return [v5.rot180(p, "n") if after else p for p in parts]


def main(stl_dir, out, tags):
    os.makedirs(out, exist_ok=True)
    boom = rd.bx(-7.5, 7.5, 60, 300, 8, 23.1)
    dup = to_tm(vf.duplexor())
    for tag, name in tags.items():
        pl = pv.Plotter(off_screen=True, shape=(1, 2), window_size=(1800, 1000))
        c = np.array([45, 175, 0.0])
        for i, (stl, after, title) in enumerate([
                (Path(stl_dir) / "mango_spacequad_v3.stl", False, "ANTES (v3): clip entra por +V"),
                (Path(stl_dir) / "v5" / f"mango_spacequad_v5_{tag}.stl", True, "DESPUES (v5): radio girada 180 grados, clip entra por -V")]):
            pl.subplot(0, i)
            mango = trimesh.load(stl)
            radio, clip, end_a, front = [to_tm(p) for p in pieces(after)]
            for m, col, op in ((mango, '#8d9399', 1), (radio, '#2e9e5b', 0.35), (clip, '#244a85', 1),
                               (end_a, '#f39c12', 1), (front, '#3498db', 1), (boom, '#c9ced3', 1), (dup, '#c0392b', 0.7)):
                pl.add_mesh(pv.wrap(rd.rot(m)), color=col, opacity=op, smooth_shading=False)
            pl.camera_position = [tuple(c + np.array((1, -1.6, 0.55)) * 480), tuple(c), (0, 0, 1)]
            pl.camera.parallel_projection = True
            pl.camera.parallel_scale = 190
            pl.set_background('white')
            pl.add_text(title, font_size=14, position=(20, 950), color='black')
            pl.add_text(f'{name}: envolvente generica, NO el contorno real de la radio', font_size=11, position=(20, 80), color='black')
            pl.add_text('Naranja: extremo A de la radio / azul: frente / azul oscuro: clip / rojo: duplexor', font_size=11, position=(20, 55), color='black')
            pl.add_text('CAD ilustrativo: sin medidas de clip verificadas ni prueba fisica', font_size=11, position=(20, 30), color='black')
        pl.screenshot(os.path.join(out, f'v5_{tag}_montaje.png')); pl.close()


if __name__ == '__main__':
    main(_cli_args.stl_dir, _cli_args.output_dir,
         {k: v["modelo"] for k, v in m5.load_profiles().items() if v.get("stl")})
