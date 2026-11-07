"""Metricas de orientacion de impresion (compartido por render_guia.py y las guias)."""
import numpy as np

EJES = {"X": 0, "Y": 1, "Z": 2}


def orientaciones(m, angulo_voladizo=45.0):
    """Para cada cara axial apoyada en la cama: altura, contacto y area en voladizo (>angulo desde la vertical)."""
    n, a, c = m.face_normals, m.area_faces, m.triangles_center
    filas = []
    for nombre, ax in EJES.items():
        for sg in (1, -1):
            arriba = np.zeros(3)
            arriba[ax] = sg
            d = n @ arriba
            pos = c[:, ax] * sg
            cama = pos < pos.min() + 0.3
            contacto = a[(d < -0.99) & cama].sum()
            volad = a[(d < -np.cos(np.deg2rad(angulo_voladizo))) & ~cama].sum()
            filas.append({"arriba": f"{nombre}{'+' if sg > 0 else '-'}", "cama": f"{nombre}{'-' if sg > 0 else '+'}",
                          "altura_mm": round(float(m.extents[ax]), 1), "contacto_mm2": round(float(contacto)),
                          "voladizo_mm2": round(float(volad))})
    return filas


if __name__ == "__main__":
    import sys, trimesh
    m = trimesh.load(sys.argv[1])
    for f in orientaciones(m):
        print(f)
