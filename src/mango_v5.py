#!/usr/bin/env python3
"""
Mango SpaceQuad v5 (Bricohams): v3 con la radio girada 180 grados sobre el enganche superior.

    python mango_v5.py ../stl/mango_spacequad_tripode.stl ../stl/v5 [uvk5v3|rt950pro|todas]

Eje de giro: la NORMAL de la placa (n) por el centro de la placa, no un giro del STL completo (eso
dejaria la empunadura boca arriba). Los giros alrededor de s (eje largo) o de u (transversal) dejan la
radio bajo la placa o contra la torre: se descartan con verificar_v5.py.
Efecto: s -> PLATE_L - s, u -> 2*uc - u. El clip entra por el extremo bajo (-V, s=0) y la radio queda
sobre la placa hacia +V. La placa y las cartelas son simetricas, asi que solo cambia la ventana de
retencion opcional (22 x 6 mm), que pasa de s=14..20 a s=28..34. El resto del mango es identico a la v3.

Las medidas del clip por modelo se leen de perfiles_radio.json. Sin medida verificada se usa la
envolvente generica de la v3 y la variante queda marcada como provisional.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def _parse_cli():
    parser = argparse.ArgumentParser(
        description="Genera las variantes v5 (radio girada 180 grados) desde el STL v1.",
        epilog="Ejemplo: python src/mango_v5.py stl/mango_spacequad_tripode.stl stl/v5 todas",
    )
    parser.add_argument("source", help="STL v1 de entrada")
    parser.add_argument("out_dir", help="directorio de salida")
    parser.add_argument("variant", nargs="?", default="todas")
    args = parser.parse_args()
    if not Path(args.source).is_file():
        parser.error(f"no existe el STL de entrada: {args.source}")
    return args


if __name__ == "__main__":
    _cli_args = _parse_cli()

import numpy as np
import mango_v3 as mg

FLIP_S = lambda s: mg.PLATE_L - s          # imagen de s al girar 180 grados sobre n
WIN_S_V5 = FLIP_S(mg.WIN_S + mg.WIN_H)     # ventana: 28..34 mm


def load_profiles():
    return json.loads((HERE / "perfiles_radio.json").read_text(encoding="utf-8"))


def clip_holder():
    """Misma placa y cartelas que la v3; ventana de retencion en la posicion girada."""
    plate = mg.plate_box(mg.PLATE_U0, mg.PLATE_U0 + mg.PLATE_W, 0, mg.PLATE_L, 0, mg.PLATE_T)
    if mg.HOOK_WINDOW:
        uc = mg.PLATE_U0 + mg.PLATE_W / 2
        plate -= mg.plate_box(uc - mg.WIN_W/2, uc + mg.WIN_W/2, WIN_S_V5, WIN_S_V5 + mg.WIN_H, -1, mg.PLATE_T + 1)
    gusset = [mg.plate_point(0, 0.2), mg.plate_point(mg.PLATE_L, 0.2),
              (mg.ROOT_V1, mg.ROOT_H0), (mg.ROOT_V0, mg.ROOT_H0)]
    for u in (mg.PLATE_U0, mg.PLATE_U0 + mg.PLATE_W - mg.SIDE_T):
        plate += mg.use_prism(gusset, u, u + mg.SIDE_T)
    return plate


def build_variant(src, out_dir, key):
    profile = load_profiles()[key]
    dst = Path(out_dir) / profile["stl"]
    mg.clip_holder = clip_holder          # build() de la v3 resuelve el nombre en tiempo de ejecucion
    mg.build(src, str(dst))
    digest = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(key, profile["estado"], digest[:16])
    return dst


if __name__ == "__main__":
    out = Path(_cli_args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    keys = [k for k, v in load_profiles().items() if v.get("stl")] if _cli_args.variant == "todas" else [_cli_args.variant]
    for k in keys:
        build_variant(_cli_args.source, out, k)
