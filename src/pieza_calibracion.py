#!/usr/bin/env python3
"""Genera la pieza de prueba de holguras (cupon) para calibrar la impresora antes de imprimir el mango.

    python src/pieza_calibracion.py stl/calibracion/prueba_holguras.stl

Tres filas, de 1 a 5 marcas (puntos) por hueco, de menor a mayor medida:
  fila 1: huecos cuadrados pasantes para el boom de 15 mm (15,1 / 15,3 / 15,5 / 15,7 / 15,9);
  fila 2: bolsillos hexagonales para la tuerca 1/4"-20 (AF 11,1 / 11,3 / 11,5 / 11,7 / 11,9; 6,5 mm de fondo);
  fila 3: ranuras para la lengua del clip (6,0 / 6,5 / 7,0 / 7,5 / 8,0 de ancho, 22 de largo).
Marcas de la dimension de diseno: 15,5 (3 puntos), tuerca 11,4 se prueba entre 11,3 y 11,5, ranura de 7 (3 puntos).
Es una herramienta de calibracion de la impresora, no parte del mango. Sobrescribe el STL destino."""
import argparse
from pathlib import Path

import manifold3d as mf
import numpy as np
import trimesh

ESPESOR, PASO, ANCHO, FONDO_HEX = 8.0, 24.0, 124.0, 6.5
CUADRADOS = [15.1, 15.3, 15.5, 15.7, 15.9]
HEXAGONOS = [11.1, 11.3, 11.5, 11.7, 11.9]
RANURAS = [6.0, 6.5, 7.0, 7.5, 8.0]


def to_mf(m):
    return mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32), tri_verts=np.asarray(m.faces, np.uint32)))


def caja(cx, cy, z0, z1, w, h):
    return to_mf(trimesh.creation.box(bounds=[[cx - w / 2, cy - h / 2, z0], [cx + w / 2, cy + h / 2, z1]]))


def construir():
    alto = 92.0
    cuerpo = caja(ANCHO / 2, alto / 2, 0, ESPESOR, ANCHO, alto)
    x0 = ANCHO / 2 - 2 * PASO
    for fila, (valores, y) in enumerate(zip((CUADRADOS, HEXAGONOS, RANURAS), (74.0, 46.0, 17.0))):
        for i, v in enumerate(valores):
            x = x0 + i * PASO
            if fila == 0:
                corte = caja(x, y, -1, ESPESOR + 1, v, v)
            elif fila == 1:
                hexa = trimesh.creation.cylinder(radius=v / np.sqrt(3), height=FONDO_HEX + 1, sections=6)
                hexa.apply_translation([x, y, ESPESOR - FONDO_HEX / 2 + 0.5])
                corte = to_mf(hexa)
            else:
                corte = caja(x, y, -1, ESPESOR + 1, v, 22.0)
            cuerpo = cuerpo - corte
            for k in range(i + 1):   # i + 1 marcas hundidas de 0,6 mm de fondo
                pt = trimesh.creation.cylinder(radius=0.9, height=1.2, sections=16)
                pt.apply_translation([x + (k - i / 2) * 3.0, y - 14.0 if fila == 2 else y - v / 2 - 3.5, ESPESOR])
                cuerpo = cuerpo - to_mf(pt)
    g = cuerpo.to_mesh()
    m = trimesh.Trimesh(g.vert_properties[:, :3].copy(), g.tri_verts.copy(), process=True)
    return m


def main():
    ap = argparse.ArgumentParser(description="Genera el cupon de holguras para calibrar la impresora.")
    ap.add_argument("destino", type=Path, help="STL de salida")
    a = ap.parse_args()
    a.destino.parent.mkdir(parents=True, exist_ok=True)
    m = construir()
    m.export(a.destino)
    print("OK", a.destino, m.extents.round(1), "watertight", m.is_watertight)


if __name__ == "__main__":
    main()

