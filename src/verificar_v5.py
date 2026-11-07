#!/usr/bin/env python3
"""Verifica la v5 (radio girada 180 grados) y guarda resultados CAD en JSON.
Clips y radio son envolventes ESTIMADAS (ver perfiles_radio.json): no es una validacion de ajuste fisico.
    python verificar_v5.py ../stl/v5 [../docs/cad_checks_v5.json]
"""
import argparse
from pathlib import Path
import sys


def _parse_cli():
    parser = argparse.ArgumentParser(
        description="Comprobaciones CAD de las variantes v5; no certifican ajuste ni resistencia fisicos.",
        epilog="Ejemplo: python src/verificar_v5.py stl/v5 docs/cad_checks_v5.json",
    )
    parser.add_argument("stl_dir", help="directorio con los STL v5")
    parser.add_argument("report", nargs="?", help="JSON de resultados (opcional)")
    args = parser.parse_args()
    if not Path(args.stl_dir).is_dir():
        parser.error(f"no existe el directorio: {args.stl_dir}")
    return args


if __name__ == "__main__":
    _cli_args = _parse_cli()

import json
import numpy as np
import trimesh
from geom import *
import mango_v3 as mg
import mango_v5 as m5
import verificar as vf

ROOT = Path(__file__).resolve().parent.parent
A = np.deg2rad(mg.ANGLE)
UC = mg.PLATE_U0 + mg.PLATE_W / 2
# Marco de la placa en coordenadas del STL: s a lo largo de la placa, n normal, u transversal.
DIRS = {"s": np.array([-np.sin(A), np.cos(A), 0.0]),
        "n": np.array([-np.cos(A), -np.sin(A), 0.0]),
        "u": np.array([0.0, 0.0, 1.0])}
V_C, H_C = mg.plate_point(mg.PLATE_L / 2, 0)
CENTER = np.array([-H_C, V_C, UC])


def rot180(manifold, axis):
    """Giro de 180 grados sobre un eje de la placa por el centro de la placa."""
    d = DIRS[axis]
    R = np.eye(4)
    R[:3, :3] = 2 * np.outer(d, d) - np.eye(3)
    R[:3, 3] = CENTER - R[:3, :3] @ CENTER
    t = to_tm(manifold)
    t.apply_transform(R)
    return to_mf(t)


def assembly():
    return vf.walki() + vf.radio_clip()


def main(stl_dir, report=None):
    root = Path(stl_dir)
    v3 = to_mf(trimesh.load(ROOT / "stl" / "mango_spacequad_v3.stl"))
    dup = vf.duplexor()
    results = []

    def check(name, passed, **values):
        results.append(dict(name=name, passed=bool(passed), **values))
        print(f"[{'OK' if passed else 'FALLO'}] {name} {values}", flush=True)

    # --- 1) eleccion del eje: solo n deja el clip bajo la placa y la radio libre
    ref_mango = to_mf(trimesh.load(next(root.glob("*.stl"))))
    slot = mg.plate_box(UC - mg.W_IN/2, UC + mg.W_IN/2, 0, mg.PLATE_L, -mg.MIN_CLEAR, -0.001)
    tongue0 = vf.tongue(45.0, mg.USABLE_L)
    for axis in ("s", "u", "n"):
        radio = rot180(vf.walki(), axis)
        tongue = rot180(tongue0, axis)
        in_slot = (tongue ^ slot).volume() / tongue.volume()
        hit = (radio ^ ref_mango).volume() + (tongue ^ ref_mango).volume()
        ok = in_slot > 0.999 and hit < 0.001
        check(f"axis_{axis}_candidate", ok == (axis == "n"), tongue_in_slot_fraction=in_slot,
              collision_mm3=hit, feasible=ok)
    # El giro sobre n coincide con la imagen s -> L-s, u -> 2uc-u de la placa simetrica.
    mirrored_tongue = mg.plate_box(UC - 22.5, UC + 22.5, 0, mg.USABLE_L, -mg.CLIP_T_MAX - 0.5, -0.5)
    check("rotation_equals_s_mirror", (rot180(tongue0, "n") ^ mirrored_tongue).volume() > 0.999 * tongue0.volume()
          and abs(rot180(tongue0, "n").volume() - tongue0.volume()) < 0.01)

    for path in sorted(root.glob("*.stl")):
        tag = path.stem.replace("mango_spacequad_v5_", "")
        mesh = trimesh.load(path)
        mango = to_mf(mesh)
        canonical = to_tm(mango)
        check(f"{tag}:manifold", mango.status().name == "NoError" and canonical.is_watertight
              and canonical.is_winding_consistent, status=mango.status().name)
        check(f"{tag}:one_solid", sum(c.volume() > 0 for c in mango.decompose()) == 1, volume_mm3=mango.volume())
        # Unica diferencia con la v3: ventana de retencion movida; empunadura, boom y tripode intactos.
        diff = sdiff_(mango, v3)
        win_old = mg.plate_box(UC - mg.WIN_W/2, UC + mg.WIN_W/2, mg.WIN_S, mg.WIN_S + mg.WIN_H, -0.001, mg.PLATE_T + 0.001)
        win_new = mg.plate_box(UC - mg.WIN_W/2, UC + mg.WIN_W/2, m5.WIN_S_V5, m5.WIN_S_V5 + mg.WIN_H, -0.001, mg.PLATE_T + 0.001)
        outside = abs((diff - win_old - win_new).volume())
        expected = 2 * mg.WIN_W * mg.WIN_H * mg.PLATE_T
        check(f"{tag}:only_window_moved", outside < 0.01 and abs(diff.volume() - expected) < 1,
              outside_mm3=outside, changed_mm3=diff.volume(), expected_mm3=expected)
        wnd = mg.plate_box(UC - mg.WIN_W/2 + 0.1, UC + mg.WIN_W/2 - 0.1, m5.WIN_S_V5 + 0.1,
                           m5.WIN_S_V5 + mg.WIN_H - 0.1, 0.1, mg.PLATE_T - 0.1)
        check(f"{tag}:mirrored_window_open", (wnd ^ mango).volume() < 0.001)
        # Barridos de insercion por el extremo -s con la misma transformacion que el montaje.
        worst = 0.0
        for w in vf.CLIPS:
            for off in (0.05, 0.5, 0.95):
                sweep = rot180(mg.plate_box(UC-w/2, UC+w/2, mg.PLATE_L-mg.USABLE_L, mg.PLATE_L+mg.USABLE_L,
                                            -mg.CLIP_T_MAX-off, -off), "n")
                worst = max(worst, (sweep ^ mango).volume() + (sweep ^ dup).volume())
        check(f"{tag}:clip_sweeps_25_45_clear", worst < 0.001, worst_collision_mm3=worst, entry="-s (extremo -V)")
        gap = rot180(mg.plate_box(UC-mg.W_IN/2, UC+mg.W_IN/2, mg.PLATE_L-mg.USABLE_L, mg.PLATE_L,
                                  -mg.MIN_CLEAR, -0.001), "n")
        check(f"{tag}:seven_mm_gap", (gap ^ mango).volume() < 0.001)
        check(f"{tag}:print_clearance", mg.W_IN - mg.CLIP_W_MAX >= 1.0 and mg.MIN_CLEAR - mg.CLIP_T_MAX >= 1.0,
              side_gap_total_mm=mg.W_IN - mg.CLIP_W_MAX, thickness_gap_mm=mg.MIN_CLEAR - mg.CLIP_T_MAX)
        for w in (50.0, vf.R_W, 70.0):
            radio = rot180(vf.walki(w), "n")
            sw = rot180(mg.plate_box(UC-w/2, UC+w/2, mg.PLATE_L + vf.R_ABOVE - vf.R_L,
                                     mg.PLATE_L + vf.R_ABOVE + mg.USABLE_L, mg.PLATE_T+0.5,
                                     mg.PLATE_T+0.5+vf.R_T), "n")
            check(f"{tag}:radio_{w:g}_clear", (sw ^ mango).volume() < 0.001 and (sw ^ dup).volume() < 0.001
                  and (radio ^ mango).volume() < 0.001, mango_collision_mm3=(sw ^ mango).volume(),
                  duplexor_collision_mm3=(sw ^ dup).volume())
        full = rot180(assembly(), "n")
        check(f"{tag}:assembly_connected", sum(c.volume() > 0 for c in full.decompose()) == 1)
        for direction, v0, v2 in (("minus_v", -100, 177), ("plus_v", 118, 400)):
            corridor = vf.use_box(28, 59.5, v0, v2, 17.9, 33.4)
            added = ((mango - to_mf(trimesh.load(vf.V1))) ^ corridor).volume()
            check(f"{tag}:duplexor_corridor_{direction}", added < 0.001 and (full ^ corridor).volume() < 0.001,
                  added_collision_mm3=added)
    passed = all(r["passed"] for r in results)
    data = dict(passed=passed, checks=results,
                limitations=["Clip y radio son envolventes genericas estimadas; ninguna medida de clip UV-K5 V3 / RT-950 Pro verificada.",
                             "Anytone: sin modelo exacto, sin STL.",
                             "La caja nominal del duplexor ya roza la funda v1 (heredado).",
                             "El conjunto radio+clip se prueba solo contra el STL del mango, no contra la antena completa.",
                             "No es certificacion de ajuste ni de resistencia."])
    if report:
        Path(report).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return passed


def sdiff_(a, b):
    return (a - b) + (b - a)


if __name__ == "__main__":
    sys.exit(0 if main(_cli_args.stl_dir, _cli_args.report) else 1)
