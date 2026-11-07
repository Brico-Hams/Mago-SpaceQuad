#!/usr/bin/env python3
"""Verifica la variante generica Anytone (mango + calzos) y guarda resultados CAD en JSON.
Clips y radio son envolventes ESTIMADAS: ninguna comprobacion demuestra ajuste fisico ni resistencia.
    python src/verificar_anytone.py stl/mango_spacequad_anytone_generico.stl stl/anytone_calzos docs/cad_checks_anytone_generico.json
"""
import argparse
import io
import json
from pathlib import Path
import subprocess
import sys


def _parse_cli():
    parser = argparse.ArgumentParser(
        description="Comprobaciones CAD de la variante generica Anytone; no certifica ajuste ni resistencia fisicos.",
        epilog="Ejemplo: python src/verificar_anytone.py stl/mango_spacequad_anytone_generico.stl "
               "stl/anytone_calzos docs/cad_checks_anytone_generico.json",
    )
    parser.add_argument("mesh", help="STL del mango generico")
    parser.add_argument("shim_dir", help="directorio con los STL de calzos")
    parser.add_argument("report", nargs="?", help="JSON de resultados (opcional)")
    args = parser.parse_args()
    for p in (args.mesh, args.shim_dir):
        if not Path(p).exists():
            parser.error(f"no existe: {p}")
    return args


if __name__ == "__main__":
    _cli_args = _parse_cli()

import numpy as np
import trimesh
from geom import *
import mango_v3 as mg
import mango_anytone_generico as ag
import verificar as base_v

ROOT = Path(__file__).resolve().parent.parent
BASE_STL = ROOT / "stl" / "mango_spacequad_v3.stl"
TOL = 0.001
DUP, R_W, R_T, R_L, R_ABOVE = base_v.DUP, base_v.R_W, base_v.R_T, base_v.R_L, base_v.R_ABOVE
use_box, sdiff = base_v.use_box, base_v.sdiff
UC = mg.PLATE_U0 + mg.PLATE_W / 2

def tongue_box(w, off, s0, s1, thick=None):
    return ag.plate_box(UC - w/2, UC + w/2, s0, s1, -(thick or mg.CLIP_T_MAX) - off, -off)

def walki(w):
    s1 = mg.PLATE_L + R_ABOVE
    return ag.plate_box(UC - w/2, UC + w/2, s1 - R_L, s1, mg.PLATE_T + 0.5, mg.PLATE_T + 0.5 + R_T)

def radio_clip(w=46.0):
    bridge = ag.plate_box(UC - w/2, UC + w/2, mg.PLATE_L, mg.PLATE_L + 2, -mg.CLIP_T_MAX - 0.5, mg.PLATE_T + 1)
    return tongue_box(w, 0.5, mg.PLATE_L - mg.USABLE_L, mg.PLATE_L) + bridge

def section_inertia(mesh, x):
    """Area y segundos momentos (respecto al centroide, ejes y/z) de la seccion x=const; huecos restan."""
    s = mesh.section(plane_origin=[x, 0, 0], plane_normal=[1, 0, 0])
    loops = [np.asarray(d)[:, 1:3] for d in s.discrete if len(d) > 3]
    def props(p):
        x_, y_ = p[:, 0], p[:, 1]; x2, y2 = np.roll(x_, -1), np.roll(y_, -1)
        c = x_ * y2 - x2 * y_
        a = c.sum() / 2
        cx = ((x_ + x2) * c).sum() / (6 * a); cy = ((y_ + y2) * c).sum() / (6 * a)
        ixx = ((y_**2 + y_*y2 + y2**2) * c).sum() / 12; iyy = ((x_**2 + x_*x2 + x2**2) * c).sum() / 12
        return abs(a), np.sign(a), cx, cy, ixx * np.sign(a), iyy * np.sign(a)
    P = [props(l) for l in loops]
    P.sort(key=lambda q: -q[0])
    outer = P[0]; area = outer[0]; ixx = abs(outer[4]); iyy = abs(outer[5])
    cx, cy = outer[2], outer[3]
    for q in P[1:]:
        area -= q[0]; ixx -= abs(q[4]); iyy -= abs(q[5])
    # inercia respecto al eje por el centroide del contorno exterior (el hueco es casi concentrico)
    ixx_c = ixx - area * cy**2 * 0; iyy_c = iyy - area * cx**2 * 0
    return dict(area_mm2=area, i_boom_axis_mm4=ixx, i_cross_axis_mm4=iyy)

def baseline():
    return trimesh.load(BASE_STL)

def main(path, shim_dir, report=None):
    mesh, base_mesh = trimesh.load(path), baseline()
    mango, base, v1 = to_mf(mesh), to_mf(base_mesh), to_mf(trimesh.load(base_v.V1))
    mount, dup = ag.clip_holder(), base_v.duplexor()
    results = []
    def check(name, passed, **values):
        results.append(dict(name=name, passed=bool(passed), **values))
        print(f"[{'OK' if passed else 'FALLO'}] {name} {values}", flush=True)
    canonical = to_tm(mango)
    check("manifold", mango.status().name == "NoError" and canonical.is_watertight and canonical.is_winding_consistent,
          canonical_watertight=canonical.is_watertight, raw_trimesh_watertight=mesh.is_watertight,
          baseline_raw_trimesh_watertight=base_mesh.is_watertight, status=mango.status().name)
    positive = [c for c in mango.decompose() if c.volume() > 0]
    check("one_solid", len(positive) == 1, solids=len(positive), volume_mm3=mango.volume())
    cavities = lambda m: sorted(round(c.volume(), 1) for c in m.decompose() if c.volume() < -1.0)
    cv_new, cv_old = cavities(mango), cavities(base)
    check("grip_cavity_reduced_not_opened", len(cv_new) == 1 and abs(cv_new[0]) < abs(cv_old[0]),
          cavity_before_mm3=cv_old, cavity_after_mm3=cv_new)
    old_env = use_box(23, 80, 128, 176, 53, 87)
    new_env = use_box(23, 80, 116, 168, 53, 87)
    reinf_env = to_mf(trimesh.creation.box(bounds=[[ag.RIB_X0 - 0.01, 85, 3], [97.5, 141, 28]]))
    difference = sdiff(mango, base)
    outside = abs((difference - old_env - new_env - reinf_env).volume())
    check("changes_localized", outside < TOL and difference.volume() > 100, outside_mm3=outside,
          changed_mm3=difference.volume(), baseline="HEAD stl/mango_spacequad_v3.stl")
    tripod_zone = to_mf(trimesh.creation.box(bounds=[[97.5, 70, -1], [112, 180, 40]]))
    check("tripod_nut_and_face_exact", abs((difference ^ tripod_zone).volume()) < TOL,
          symmetric_difference_mm3=abs((difference ^ tripod_zone).volume()))
    boom = use_box(-1, 28, 70, 180, -1, 34)
    check("boom_exact", (difference ^ boom).volume() < TOL, intersection_mm3=(difference ^ boom).volume())    # El refuerzo solo anade material (nunca resta) en la zona del hueco; el mango exterior de v3 se mantiene.
    removed = (base - mango) ^ reinf_env
    check("reinforcement_adds_only", removed.volume() < TOL, removed_in_zone_mm3=removed.volume(),
          added_mm3=(difference ^ reinf_env).volume())
    void_pos = None
    for c in base.decompose():
        if c.volume() < 0:
            vm = to_tm(c); vm.invert(); void_pos = to_mf(vm)
    outside_void = ((mango - base) - void_pos) - mount - ag.shim_in_mango(ag.SHIM_D[0])
    check("reinforcement_inside_original_void", outside_void.volume() < 1.0,           outside_void_mm3=outside_void.volume(),
          note="el casco convexo rellena un bolsillo contiguo de ~0,4 mm3; se tolera < 1 mm3")
    # Geometria de seccion: relleno macizo + nervios
    sect = {}
    for x in (80.0, 70.0, 52.0):
        a, b = section_inertia(base_mesh, x), section_inertia(mesh, x)
        sect[f"x={x:g}"] = dict(before=a, after=b, area_ratio=b["area_mm2"] / a["area_mm2"],
                                inertia_ratio_boom=b["i_boom_axis_mm4"] / a["i_boom_axis_mm4"],
                                inertia_ratio_cross=b["i_cross_axis_mm4"] / a["i_cross_axis_mm4"])
    check("section_stiffer_near_base", all(v["area_ratio"] > 1.2 for v in sect.values()), sections=sect)
    # --- placa girada 180 grados
    old_high = mg.plate_point(mg.PLATE_L, 0)[0]
    new_high = ag.mirror_point(mg.PLATE_L, 0)[0]
    check("holder_rotated_180", abs((old_high - ag.V_PIV) + (new_high - ag.V_PIV)) < 1e-9 and new_high < ag.V_PIV < old_high,
          old_entry_v=old_high, new_entry_v=new_high, pivot_v=ag.V_PIV,
          radio_centroid_v_new=float(to_tm(walki(R_W)).centroid[1]),
          radio_centroid_v_old=float(to_tm(base_v.walki(R_W)).centroid[1]))
    check("plate_above_duplexor", mg.PLATE_H0 >= 65, underside_min_h=mg.PLATE_H0)
    for i, u in enumerate((mg.PLATE_U0, mg.PLATE_U0 + mg.PLATE_W - mg.SIDE_T)):
        foot = use_box(u + 0.5, min(u + mg.SIDE_T - 0.5, 77.8), mg.ROOT_V0 + 2, mg.ROOT_V1 - 2, mg.ROOT_H0 + 0.5, mg.ROOT_H0 + 3.5)
        missing = (foot - base).volume() + (foot - mount).volume()
        check(f"gusset_{i+1}_anchored", (mount ^ base ^ use_box(u, u + mg.SIDE_T, 136, 159, mg.ROOT_H0, mg.TOWER_H)).volume() > 100
              and missing < TOL, missing_foot_mm3=missing, embed_mm=mg.TOWER_H - mg.ROOT_H0)
    # --- slots y ventana
    for k, (u0, u1) in enumerate(ag.slot_us()):
        for s in ag.SLOT_S:
            probe = ag.plate_box(u0 + 0.1, u1 - 0.1, s + 0.1, s + ag.SLOT_L - 0.1, 0.1, mg.PLATE_T - 0.1)
            check(f"slot_{k}_{s:g}_open", (probe ^ mango).volume() < TOL, solid_in_slot_mm3=(probe ^ mango).volume())
    # --- calzos: geometria propia + montaje sin colision
    shims = {}
    for d in ag.SHIM_D:
        fs = sorted(Path(shim_dir).glob(f"calzos_d{d:02d}_*.stl"))
        pair = trimesh.load(fs[0]) if fs else None
        ok = pair is not None and pair.is_watertight and pair.is_winding_consistent and pair.volume > 0
        n = len(pair.split(only_watertight=False)) if pair is not None else 0
        check(f"shim_d{d:02d}_mesh", ok and n == 2, file=fs[0].name if fs else None,
              watertight=bool(pair is not None and pair.is_watertight), bodies=n,
              extents_mm=np.round(pair.extents, 1).tolist() if pair is not None else None)
        sm = ag.shim_in_mango(d)
        shims[d] = sm
        coll = (sm ^ mango).volume()
        check(f"shim_d{d:02d}_assembly_no_collision", coll < TOL, collision_mm3=coll, shim_volume_mm3=sm.volume())    # tabs: todo el volumen por encima de la cara inferior de la placa debe estar dentro de una ranura
    for d, sm in shims.items():
        above = sm ^ ag.plate_box(UC - 30, UC + 30, 0, mg.PLATE_L + 5, 0, mg.PLATE_T + 1)
        slots = None
        for u0, u1 in ag.slot_us():
            for s in ag.SLOT_S:
                b = ag.plate_box(u0, u1, s, s + ag.SLOT_L, -1, mg.PLATE_T + 1)
                slots = b if slots is None else slots + b
        outside_slots = (above - slots).volume()
        check(f"shim_d{d:02d}_tabs_only_in_slots", outside_slots < TOL and above.volume() > 1,
              tab_volume_mm3=above.volume(), outside_slots_mm3=outside_slots)
    # --- barridos continuos de la lengua en cada juego, a lo largo de TODO el rango
    ranges = {0: ag.tongue_range(0)}
    for d in ag.SHIM_D:
        ranges[d] = ag.tongue_range(d)
    sets = [0] + list(ag.SHIM_D)
    for d in sets:
        lo, hi = ranges[d]
        env = mango + shims[d] if d else mango
        for w in (lo, (lo + hi) / 2, hi):
            for off in (0.05, 0.5, 0.95):
                sweep = tongue_box(w, off, mg.PLATE_L - mg.USABLE_L, mg.PLATE_L + mg.USABLE_L)
                col = (sweep ^ env).volume()
                check(f"sweep_set{d:02d}_w{w:.1f}_off{off:g}", col < TOL, tongue_w_mm=round(w, 2), collision_mm3=col)
        # limite superior real: una lengua 0,3 mm mas ancha que (hueco - 0,6) debe chocar si hay calzos.
        too_wide = tongue_box(clear_w := ag.clear_width(d) + 0.2, 0.5, mg.PLATE_L - mg.USABLE_L, mg.PLATE_L)
        check(f"overwide_set{d:02d}_collides", (too_wide ^ env).volume() > 1, width_mm=round(clear_w, 2),
              collision_mm3=(too_wide ^ env).volume())
    gaps = [(sets[i], ranges[sets[i]][0], ranges[sets[i + 1]][1]) for i in range(len(sets) - 1)]
    check("ranges_contiguous", all(ranges[a][0] <= ranges[b][1] for a, b in zip(sets[1:], sets[:-1])) and
          abs(ag.RANGE_W[0] - ranges[sets[-1]][0]) < 1e-9,
          width_range_mm=[round(ag.RANGE_W[0], 2), round(ag.RANGE_W[1], 2)],
          per_set={f"d{d}": [round(ranges[d][0], 2), round(ranges[d][1], 2)] for d in sets})
    # --- espacio de 7 mm entre placa y nada (tambien con los calzos montados)
    gap = ag.plate_box(UC - 20, UC + 20, mg.PLATE_L - mg.USABLE_L, mg.PLATE_L, -mg.MIN_CLEAR, -0.001)
    check("seven_mm_gap", (gap ^ mango).volume() < TOL, collision_mm3=(gap ^ mango).volume())
    open_under = ag.plate_box(UC - 10, UC + 10, 8, 40, -mg.MIN_CLEAR, -0.5)
    check("open_underside", (open_under ^ mount).volume() < TOL)
    # --- radio y duplexor (mismas envolventes estimadas que verificar.py, ahora con la placa girada)
    check("duplexor_no_new_collision", (mount ^ dup).volume() < TOL, new_collision_mm3=(mount ^ dup).volume(),
          inherited_v1_collision_mm3=(v1 ^ dup).volume())
    for direction, v0, v2 in (("minus_v", -100, 177), ("plus_v", 118, 400)):
        corridor = use_box(28, 59.5, v0, v2, 17.9, 33.4)
        added = ((mango - v1) ^ corridor).volume()
        check(f"duplexor_corridor_{direction}", added < TOL, added_collision_mm3=added)
        check(f"radio_clear_of_{direction}_corridor", ((walki(R_W) + radio_clip()) ^ corridor).volume() < TOL)
    clip = radio_clip()
    for w in (50.0, R_W, 70.0):
        radio = walki(w)
        check(f"radio_{w:g}_clear", (radio ^ mango).volume() < TOL and (radio ^ dup).volume() < TOL,
              mango_collision_mm3=(radio ^ mango).volume(), duplexor_collision_mm3=(radio ^ dup).volume())
    s1 = mg.PLATE_L + R_ABOVE
    assembly = ag.plate_box(UC - R_W/2, UC + R_W/2, s1 - R_L, s1 + mg.USABLE_L, mg.PLATE_T + 0.5, mg.PLATE_T + 0.5 + R_T) + \
        tongue_box(46.0, 0.5, mg.PLATE_L - mg.USABLE_L, mg.PLATE_L + mg.USABLE_L)
    check("continuous_full_assembly_sweep", (assembly ^ mango).volume() < TOL and (assembly ^ dup).volume() < TOL,
          mango_collision_mm3=(assembly ^ mango).volume(), duplexor_collision_mm3=(assembly ^ dup).volume())
    passed = all(r["passed"] for r in results)
    data = dict(passed=passed, width_range_mm=list(map(float, ag.RANGE_W)), max_tongue_thickness_mm=mg.CLIP_T_MAX,
                min_insertion_mm=mg.USABLE_L, checks=results,
                limitations=["Clips y radio estimados; ningun clip Anytone medido ni probado impreso.",
                             "La caja nominal del duplexor intersecta la funda v1 (heredado); solo se exige no empeorar.",
                             "Retencion de calzos por ranura/lengueta: sin prueba de impresion ni de desgaste.",
                             "Relleno y nervios de la base: mejora geometrica de seccion, no certificacion de resistencia.",
                             "El giro de 180 grados es un espejo en V respecto a la torre; falta confirmarlo con la sesion de giro."])
    if report:
        Path(report).write_text(json.dumps(data, indent=2, default=float) + "\n", encoding="utf-8")
    return passed

if __name__ == "__main__":
    sys.exit(0 if main(_cli_args.mesh, _cli_args.shim_dir, _cli_args.report) else 1)
