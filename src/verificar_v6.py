#!/usr/bin/env python3
"""Verifica la v6 (radio inclinada hacia la empunadura y base de tripode reforzada); guarda resultados CAD en JSON.
Clips y radio son envolventes ESTIMADAS (ver perfiles_radio.json): no es una validacion de ajuste ni de resistencia.
    python verificar_v6.py ../stl/v6 [../docs/cad_checks_v6.json] [--tilt-hacia +V|-V] [--lado-u -U|+U] [--tilt-deg 20] [--sin-brida]
"""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent


def _parse_cli():
    parser = argparse.ArgumentParser(
        description="Comprobaciones CAD de las variantes v6; no certifican ajuste ni resistencia fisicos.",
        epilog="Ejemplo: python src/verificar_v6.py stl/v6 docs/cad_checks_v6.json",
    )
    parser.add_argument("stl_dir", help="directorio con los STL v6")
    parser.add_argument("report", nargs="?", default=str(ROOT / "docs" / "cad_checks_v6.json"),
                        help="JSON de resultados (por defecto docs/cad_checks_v6.json)")
    parser.add_argument("--tilt-hacia", choices=("+V", "-V"), default="-V")
    parser.add_argument("--lado-u", choices=("-U", "+U"), default="-U")
    parser.add_argument("--tilt-deg", type=float, default=20.0)
    parser.add_argument("--sin-brida", action="store_true")
    args = parser.parse_args()
    if not Path(args.stl_dir).is_dir():
        parser.error(f"no existe el directorio: {args.stl_dir}")
    return args


if __name__ == "__main__":
    _cli_args = _parse_cli()

import json
import numpy as np
import trimesh
import shapely.geometry as sg
from geom import to_mf, to_tm
import mango_v3 as mg
import mango_v6 as mv6
import refuerzo_base as rb
import verificar as vf

V3 = ROOT / "stl" / "mango_spacequad_v3.stl"
TOL = 0.001


def sdiff_(a, b):
    return (a - b) + (b - a)


def _json_default(o):
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


def tilt_esperado():
    """Signo en V esperado del extremo superior de la radio, calculado sin pasar por mango_v6.resolver_tilt."""
    return {"+V": 1, "-V": -1}[mv6.TILT_HACIA]


def main(stl_dir, report=None):
    root = Path(stl_dir)
    v1_mesh = trimesh.load(vf.V1)
    v1 = to_mf(v1_mesh)
    v3_mesh = trimesh.load(V3)
    v3 = to_mf(v3_mesh)
    dup = vf.duplexor()
    boom = vf.use_box(mv6.U_BOOM - 7.5, mv6.U_BOOM + 7.5, -100, 400, -7.5, 7.5)   # barra 15 x 15 mm extendida en V
    z_ext = mv6.z_exterior(v1_mesh.vertices)
    results = []

    def check(name, passed, **values):
        results.append(dict(name=name, passed=bool(passed), **values))
        print(f"[{'OK' if passed else 'FALLO'}] {name} {values}", flush=True)

    perfiles = mv6.cargar_perfiles()
    cfgs = {}
    for key in mv6.claves_v6():
        path = root / perfiles[key]["stl_v6"]
        if not path.is_file():
            check(f"{key}:stl_present", False, path=str(path))
            continue
        cfg = mv6.configuracion(key)
        cfgs[key] = cfg
        mesh = trimesh.load(path)
        mango = to_mf(mesh)
        canonical = to_tm(mango)
        check(f"{key}:manifold", mango.status().name == "NoError" and canonical.is_watertight
              and canonical.is_winding_consistent, status=mango.status().name)
        check(f"{key}:one_solid", sum(c.volume() > 0 for c in mango.decompose()) == 1, volume_mm3=mango.volume())

        # --- inclinacion: centro superior frente a centro inferior de la radio, a lo largo del eje esperado
        radio = mv6.envolvente_radio(cfg)
        rt = to_tm(radio)
        eje = mv6.eje_radio(cfg)
        proy = rt.vertices @ eje
        top = rt.vertices[proy > proy.max() - 1e-3].mean(axis=0)
        bot = rt.vertices[proy < proy.min() + 1e-3].mean(axis=0)
        dv, dh = float(top[1] - bot[1]), float(-(top[0] - bot[0]))
        ang = float(np.degrees(np.arctan2(dh, abs(dv))))
        esp = tilt_esperado()
        check(f"{key}:radio_tilt_toward_{mv6.TILT_HACIA}", dv * esp > 0 and dh > 0 and abs(ang - mv6.TILT_DEG) < 0.5,
              top_centre_stl=np.round(top, 2), bottom_centre_stl=np.round(bot, 2), delta_v_mm=dv, delta_h_mm=dh,
              expected_sign_v=esp, tilt_deg_measured=ang)
        check(f"{key}:radio_tilt_config_sign_matches_{mv6.TILT_HACIA}", cfg["d"] == esp,
              config_sign=cfg["d"], expected_sign=esp)

        # --- radio y clip contra mango, duplexor y corredor del duplexor
        conj = radio + mv6.clip_radio(cfg)
        check(f"{key}:assembly_connected", sum(c.volume() > 0 for c in conj.decompose()) == 1)
        cen_u = float(rt.vertices[:, 2].mean())
        check(f"{key}:radio_side_minus_u" if mv6.LADO_U == "-U" else f"{key}:radio_side_plus_u",
              (cen_u < mv6.U_BOOM - 20) if mv6.LADO_U == "-U" else (cen_u > mv6.U_BOOM + 20),
              radio_centroid_u=cen_u, plate_centre_u=cfg["uc"], boom_axis_u=mv6.U_BOOM)
        for nombre, otro in (("mango", mango), ("duplexor", dup), ("boom", boom)):
            check(f"{key}:radio_vs_{nombre}_0mm3", (radio ^ otro).volume() < TOL and (conj ^ otro).volume() < TOL,
                  collision_mm3=(conj ^ otro).volume())
        for direction, v0, v2 in (("minus_v", -100, 177), ("plus_v", 118, 400)):
            corridor = vf.use_box(28, 59.5, v0, v2, 17.9, 33.4)
            added = ((mango - v1) ^ corridor).volume()
            check(f"{key}:duplexor_corridor_{direction}", added < TOL and (conj ^ corridor).volume() < TOL,
                  added_collision_mm3=added)
        barrido = mv6.envolvente_radio(cfg, extra_s=mg.USABLE_L) + mv6.caja(
            cfg, cfg["uc"] - cfg["clip_w"] / 2, cfg["uc"] + cfg["clip_w"] / 2, mg.PLATE_L, mg.PLATE_L + 2 + mg.USABLE_L,
            -cfg["clip_t"] - 0.5, mg.PLATE_T + 1)
        check(f"{key}:insertion_sweep_clear", (barrido ^ mango).volume() < TOL and (barrido ^ dup).volume() < TOL
              and (barrido ^ boom).volume() < TOL,
              sweep_mm=mg.USABLE_L, mango_collision_mm3=(barrido ^ mango).volume(),
              boom_collision_mm3=(barrido ^ boom).volume())
        # la viga no puede entrar en el tunel del boom (15,5 mm + 0,5 mm de holgura) ni en el duplexor
        tunel = vf.use_box(mv6.U_BOOM - 8.25, mv6.U_BOOM + 8.25, -100, 400, -8.25, 8.25)
        soporte = mv6.soporte(cfg)
        check(f"{key}:bracket_clear_tunnel_duplexer",
              (soporte ^ tunel).volume() < TOL and (soporte ^ dup).volume() < TOL
              and ((mango - v1) ^ tunel).volume() < TOL,
              bracket_tunnel_mm3=(soporte ^ tunel).volume(), bracket_duplexer_mm3=(soporte ^ dup).volume())
        solape = to_tm(soporte ^ v1)
        if solape.vertices.shape[0]:
            ext = solape.bounds[1] - solape.bounds[0]
            prof_u, prof_h = float(ext[2]), float(ext[0])
        else:
            prof_u = prof_h = 0.0
        check(f"{key}:bracket_anchored_in_tower", prof_u >= 2.0 and prof_h >= 2.0,
              overlap_depth_u_mm=prof_u, overlap_depth_h_mm=prof_h, overlap_volume_mm3=(soporte ^ v1).volume(),
              wall_mm=mg.SIDE_T)
        check(f"{key}:clearance_above_tower", cfg["radio_h_min"] >= mg.TOWER_H + 3 and cfg["hueco_h_min"] >= mg.TOWER_H + 3,
              radio_h_min=cfg["radio_h_min"], slot_h_min=cfg["hueco_h_min"], tower_top_h=mg.TOWER_H, ph0=cfg["ph0"])

        # --- hueco del clip: ancho segun el clip estimado de cada radio
        uc = cfg["uc"]
        anchos = sorted({mg.CLIP_W_MIN, 30.0, 35.0, 40.0, cfg["clip_w"]})
        peor = 0.0
        for w in anchos:
            for off in (0.05, 0.5, 0.95):
                sw = mv6.caja(cfg, uc - w / 2, uc + w / 2, mg.PLATE_L - mg.USABLE_L, mg.PLATE_L + mg.USABLE_L,
                              -cfg["clip_t"] - off, -off)
                peor = max(peor, (sw ^ mango).volume() + (sw ^ dup).volume())
        check(f"{key}:clip_sweeps_clear", peor < TOL, widths_mm=anchos, worst_collision_mm3=peor)
        hueco = mv6.caja(cfg, uc - cfg["w_in"] / 2, uc + cfg["w_in"] / 2, mg.PLATE_L - mg.USABLE_L, mg.PLATE_L,
                         -cfg["min_clear"], -0.001)
        pared = mv6.caja(cfg, uc - cfg["w_in"] / 2 - 0.5, uc - cfg["w_in"] / 2 - 0.01, 12, 40,
                         -cfg["min_clear"] + 1, -1)
        check(f"{key}:slot_width_from_clip", (hueco ^ mango).volume() < TOL and (pared - mango).volume() < TOL
              and cfg["w_in"] - cfg["clip_w"] >= 2.0 - 1e-9 and cfg["min_clear"] - cfg["clip_t"] >= 1.0 - 1e-9,
              slot_width_mm=cfg["w_in"], clip_width_mm=cfg["clip_w"], slot_depth_mm=cfg["min_clear"],
              clip_thickness_mm=cfg["clip_t"], plate_width_mm=cfg["plate_w"])
        ventana = mv6.caja(cfg, uc - mg.WIN_W / 2 + 0.1, uc + mg.WIN_W / 2 - 0.1, mg.WIN_S + 0.1,
                           mg.WIN_S + mg.WIN_H - 0.1, 0.1, mg.PLATE_T - 0.1)
        check(f"{key}:optional_hook_window", (ventana ^ mango).volume() < TOL if mg.HOOK_WINDOW
              else (ventana ^ mango).volume() > 1)
        muestra = mv6.caja(cfg, uc + mg.WIN_W / 2 + 1, uc + mg.WIN_W / 2 + 2, 14, 15, 0.1, mg.PLATE_T - 0.1)
        check(f"{key}:plate_solid_four_mm", (muestra - mango).volume() < TOL)

        # --- placa enraizada en la torre con cartelas
        cart = mv6.cartelas(cfg)
        for i, u in enumerate((cfg["u0"], cfg["u0"] + cfg["plate_w"] - mg.SIDE_T)):
            pie = vf.use_box(u + 0.5, min(u + mg.SIDE_T - 0.5, 77.8), mg.ROOT_V0 + 2, mg.ROOT_V1 - 2,
                             mg.ROOT_H0 + 0.5, mg.ROOT_H0 + 3.5)
            falta = (pie - mango).volume() + (pie - cart).volume()
            check(f"{key}:gusset_{i + 1}_anchored", falta < TOL, missing_foot_mm3=falta,
                  overlap_with_v1_mm3=(cart ^ v1).volume(), gusset_height_mm=cfg["ph0"] - mg.ROOT_H0)

        # --- cambios respecto a la v3: solo placa/cartelas/viga y zona de cavidad y culo
        zona_placa = vf.use_box(-80, 100, 0, 300, 50, 230)
        zona_base = vf.use_box(-20, 100, 0, 300, -112, -39)
        fuera = abs((sdiff_(mango, v3) - zona_placa - zona_base).volume())
        check(f"{key}:changes_localized", fuera < 0.01, outside_mm3=fuera)

        # --- tripode
        tm = to_tm(mango)
        vacios = [p for p in tm.split(only_watertight=False) if p.volume < 0]
        x_vacio = max((float(p.bounds[1][0]) for p in vacios), default=float("-inf"))
        check(f"{key}:tripod_cavity_filled_35mm", x_vacio <= mg.BUTT_FACE - 35.0,
              filled_from_butt_mm=mg.BUTT_FACE - x_vacio if vacios else None, last_void_x=x_vacio, voids=len(vacios))
        huecos = []
        for x in np.arange(mv6.X_SOLIDO0 + 1, mv6.X_P0 - mv6.RELIEF - 1, 3.0):
            try:
                p = rb.main_poly(tm, float(x))
                huecos.append(abs(p.area - sg.Polygon(p.exterior).area))
            except Exception as e:   # sin seccion util: cuenta como fallo
                huecos.append(float("inf"))
        check(f"{key}:tripod_sections_solid", max(huecos) < 0.5, max_hole_area_mm2=max(huecos), samples=len(huecos))
        bol = mv6.bolsillo_2d(z_ext)
        semiplano = sg.box(-1e3, z_ext, 1e3, 1e3)
        hex_libre = mv6.prisma_x(mv6.hex_poly().buffer(-0.3), mv6.X_P0 + 0.001, mv6.X_P1 - 0.001)
        check(f"{key}:nut_pocket_open", (hex_libre ^ mango).volume() < TOL, nut_af_mm=mg.NUT_AF, depth_mm=mg.NUT_T)
        anillo = bol.buffer(mv6.PARED_MIN, join_style=2).difference(bol).intersection(semiplano)
        lateral = mv6.prisma_x(anillo, mv6.X_P0 + 0.001, mv6.X_P1 - 0.001)
        falta_lat = (lateral - mango).volume()
        agujero = sg.Point(mg.T_YC, mg.T_ZC).buffer(mg.NUT_HOLE / 2 + 0.05, 48)
        trasera = mv6.hex_poly().buffer(mv6.PARED_MIN, join_style=2).difference(agujero)
        falta_tras = (mv6.prisma_x(trasera, mv6.X_P0 - mv6.PARED_MIN, mv6.X_P0 - 0.001) - mango).volume()
        piel = bol.buffer(mv6.PARED_MIN, join_style=2).intersection(semiplano).difference(agujero)
        falta_piel = (mv6.prisma_x(piel, mv6.X_P1 + 0.001, mg.BUTT_FACE - 0.001) - mango).volume()
        check(f"{key}:tripod_wall_ge_3mm", falta_lat < 0.01 and falta_tras < 0.01,
              required_mm=mv6.PARED_MIN, missing_side_mm3=falta_lat, missing_back_mm3=falta_tras,
              note="el canal de entrada lateral queda cerrado por los labios y se excluye; el taladro de la rosca no cuenta como pared")
        check(f"{key}:tripod_face_skin_ge_2mm", mg.BUTT_FACE - mv6.X_P1 >= 2.0 - 1e-9 and falta_piel < 0.01,
              skin_mm=mg.BUTT_FACE - mv6.X_P1, missing_mm3=falta_piel,
              screw_engagement_note="tornillo de 6+ mm: ~4 mm de rosca de tuerca engranada")
        lab = mv6.prisma_x(sg.box(mg.T_YC - mg.NUT_AF / 2 + 0.05, z_ext + 0.1, mg.T_YC - mg.NUT_AF / 2 + mv6.LABIO - 0.05,
                                  z_ext + mv6.LABIO_L - 0.1), mv6.X_P0 + 0.1, mv6.X_P1 - 0.1)
        check(f"{key}:nut_retention_lips", (lab - mango).volume() < TOL,
              opening_mm=mg.NUT_AF - 2 * mv6.LABIO, nut_af_nominal_mm=11.1)
        cara = (tm.face_normals[:, 0] > 0.999) & (np.abs(tm.triangles_center[:, 0] - mg.BUTT_FACE) < TOL)
        check(f"{key}:butt_face_flat", abs(float(tm.bounds[1][0]) - mg.BUTT_FACE) < TOL and tm.area_faces[cara].sum() > 500,
              flat_area_mm2=float(tm.area_faces[cara].sum()), max_x=float(tm.bounds[1][0]))
        zona_ext = []
        for x in np.arange(40.0, mv6.X_BRIDA0 - mv6.BRIDA_CH - 0.5, 4.0):
            a, b = rb.section_props(v3_mesh, float(x)), rb.section_props(mesh, float(x))
            zona_ext.append(abs(a["outer_area"] - b["outer_area"]))
        check(f"{key}:grip_outside_unchanged_above_flange", max(zona_ext) < 0.5,
              max_outer_area_diff_mm2=max(zona_ext), checked_up_to_x=mv6.X_BRIDA0 - mv6.BRIDA_CH - 0.5)
        if mv6.BRIDA:
            check(f"{key}:flange_within_60x40", mv6.BRIDA_Y <= 60 and mv6.BRIDA_Z <= 40,
                  flange_y_mm=mv6.BRIDA_Y, flange_z_mm=mv6.BRIDA_Z, flange_thickness_mm=mv6.BRIDA_T)

    # --- las variantes deben ser realmente distintas
    if len(cfgs) > 1:
        a, b = (mv6.clip_holder(c) for c in cfgs.values())
        check("variants_differ", abs(sdiff_(a, b).volume()) > 1.0 and len({c["ph0"] for c in cfgs.values()}) == len(cfgs),
              plate_h0_mm={k: c["ph0"] for k, c in cfgs.items()}, radio_envelope_mm={
                  k: [c["radio_l"], c["radio_w"], c["radio_t"]] for k, c in cfgs.items()})
    passed = all(r["passed"] for r in results) and len(cfgs) == len(mv6.claves_v6())
    data = dict(passed=passed, parametros=dict(tilt_hacia=mv6.TILT_HACIA, lado_u=mv6.LADO_U, tilt_deg=mv6.TILT_DEG, brida=mv6.BRIDA,
                                              pared_min_mm=mv6.PARED_MIN, piel_mm=mv6.SKIN_V6, relleno_mm=mv6.FILL_L),
                variantes={k: dict(ph0_mm=c["ph0"], hueco_clip_mm=c["w_in"], placa_ancho_mm=c["plate_w"],
                                   radio_estado=c["perfil"]["radio"].get("estado_medida"),
                                   radio_largo_ancho_grueso_mm=[c["radio_l"], c["radio_w"], c["radio_t"]],
                                   clip_ancho_mm=c["clip_w"], clip_grueso_mm=c["clip_t"]) for k, c in cfgs.items()},
                checks=results,
                limitations=["Solo CAD: ninguna medida de clip UV-K5 V3 / RT-950 Pro esta confirmada fisicamente.",
                             "Dimensiones de radio estimadas de fuentes de terceros (UV-K5 V3) y copias no oficiales del manual (RT-950 Pro).",
                             "La radio y el clip son envolventes de caja, no el contorno real; se prueban solo contra el STL del mango y la caja nominal del duplexor.",
                             "El 'grosor de material' del tripode es geometrico; no es una prueba de carga ni garantiza que no se rompa.",
                             "La interferencia de los labios con la tuerca (~0,25 mm por lado) y el ajuste real de la tuerca no estan probados.",
                             "Anytone: sin modelo exacto, sin STL."])
    if report:
        Path(report).write_text(json.dumps(data, indent=2, ensure_ascii=False, default=_json_default) + "\n", encoding="utf-8")
    return passed


if __name__ == "__main__":
    mv6.TILT_HACIA, mv6.LADO_U, mv6.TILT_DEG, mv6.BRIDA = _cli_args.tilt_hacia, _cli_args.lado_u, _cli_args.tilt_deg, not _cli_args.sin_brida
    sys.exit(0 if main(_cli_args.stl_dir, _cli_args.report) else 1)
