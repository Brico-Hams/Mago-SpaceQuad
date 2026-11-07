#!/usr/bin/env python3
"""
Repara la malla de un STL del mango sin cambiar su geometria funcional.

    python reparar_malla.py entrada.stl [salida.stl]      (sin salida: sobrescribe la entrada)

Soldadura de vertices + reconstruccion con manifold3d (elimina la arista no-manifold de 4 caras heredada del
STL original) y simplify(1e-5 mm) para colapsar las caras degeneradas. Se aborta si cambia el volumen
(> 0,01 %) o la caja envolvente (> 1e-3 mm). No es una comprobacion fisica.
"""
import sys
from collections import Counter
from pathlib import Path

import manifold3d as mf
import numpy as np
import trimesh

TOL = 1e-5
AREA_MIN = 1e-9


def health(m):
    c = Counter(map(tuple, np.sort(m.edges, axis=1)))
    return {
        "faces": int(len(m.faces)),
        "non_manifold_edges": sum(v > 2 for v in c.values()),
        "open_edges": sum(v == 1 for v in c.values()),
        "degenerate_faces": int((m.area_faces < AREA_MIN).sum()),
        "watertight": bool(m.is_watertight),
        "volume_mm3": round(float(m.volume), 2),
    }


def repair(src, dst):
    m = trimesh.load(src, process=False)
    m.merge_vertices()
    before = health(m)
    M = mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32),
                            tri_verts=np.asarray(m.faces, np.uint32)))
    if M.status() != mf.Error.NoError:
        raise SystemExit(f"{src}: no convertible a solido ({M.status()})")
    g = M.simplify(TOL).to_mesh()
    r = trimesh.Trimesh(g.vert_properties[:, :3].copy(), g.tri_verts.copy(), process=False)
    after = health(r)
    dv = abs(after["volume_mm3"] - before["volume_mm3"]) / before["volume_mm3"]
    db = float(np.abs(r.bounds - m.bounds).max())
    if dv > 1e-4 or db > 1e-3 or not after["watertight"]:
        raise SystemExit(f"{src}: reparacion rechazada (dV={dv:.2e}, dBounds={db:.4f}, {after})")
    r.export(dst)
    return {"file": Path(dst).name, "before": before, "after": after, "delta_volume_rel": dv, "delta_bounds_mm": db}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    s = sys.argv[1]
    print(repair(s, sys.argv[2] if len(sys.argv) > 2 else s))
