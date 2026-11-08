# Cambios

**Ayuda:** [guía del proyecto](docs/AYUDA.md) · [README](README.md) · [montaje](docs/MONTAJE.md) · [materiales](docs/MATERIALES.md).

## v6.2 limpieza
- Se conservan solo v6.2, v1 (entrada de `mango_v6.py`), v3 (generador base y referencia del Anytone) y el Anytone genérico. v2, v4 y v5 se recuperan del historial de git (commit anterior a esta limpieza).
- Eliminados: `legacy/` (v1 pinza del móvil, v2 soporte GoPro, v4 canal en V); toda la v5 (`stl/v5/`, `stl/refuerzo/`, `src/mango_v5.py`, `verificar_v5.py`, `render_v5.py`, `docs/VARIANTES_V5.md`, `docs/cad_checks_v5.json`, `docs/refuerzo_v5_*_checks.json`, `docs/img/v5_*_montaje.png`, `docs/img/guia/v5/` y `v5_refuerzo/`); `stl/mango_spacequad_v3_refuerzo.stl`; las figuras antiguas `docs/img/guia/fig*.png` y `orientaciones.json` (las vigentes están en `docs/img/guia/v6/<idioma>/`).
- Se corrigen las referencias en README, AGENTS, ayuda, montaje, materiales, refuerzo de base, `gen_docs_i18n.py` y comentarios de `mango_v3.py`/`refuerzo_base.py`; el README muestra los montajes v6.2 en lugar de `vista_uso.png`. Sin cambios de geometría ni de STL.

## v6.2 — posición D: inclinación −V y radio en el lado −U (solo CAD)
- El usuario eligió la posición D entre 4 renders: `TILT_HACIA = "-V"` por defecto (confirmado sobre la pieza real; se elimina el alias `empunadura`) y nuevo `LADO_U = "-U"` / `--lado-u` (`+U` = disposición anterior). Placa y hueco se espejan en U respecto al eje del boom (U = 15,55), y una viga empotrada 4 mm en la torre sujeta las cartelas. `verificar_v6.py` añade `radio_side_minus_u`, `radio_vs_boom_0mm3`, `bracket_anchored_in_tower` y `bracket_clear_tunnel_duplexer`; `render_v6.py` añade una vista desde atrás del operador. Sin cambios en la base de trípode, perfiles ni dimensiones del clip/radio. Pendiente: ejecutar verificación, medir clips e imprimir.

## v6.1 — corrección del sentido de la inclinación (solo CAD)
- La inclinación de la v6.0 estaba al revés: el defecto `empunadura` se resolvía a −V. Tras comprobarlo el usuario sobre una pieza impresa, el extremo superior de la radio (el del clip) debe inclinarse hacia **+V**. Ahora `TILT_HACIA = "+V"` por defecto y `empunadura` equivale a `+V`. `verificar_v6.py` espera el signo de `TILT_HACIA`; no cambia ninguna dimensión, placa, cartela, ranura ni base de trípode.

## v6 — radio inclinada y base de trípode reforzada (solo CAD)
- Nuevo `src/mango_v6.py`: la radio se inclina `TILT_DEG` (20°) con su extremo superior hacia `TILT_HACIA` (en v6.0 `empunadura` = −V, **sentido erróneo, corregido en v6.1 a +V**; alternativas `+V`/`-V`); el clip entra paralelo a la placa por el borde libre y las cartelas mantienen la placa anclada.
- Variantes distintas por radio: altura de placa calculada con la envolvente (UV-K5 V3 115×60×37,5 mm, RT-950 Pro 162×66×48 mm, ambas estimadas) y hueco del clip desde el clip estimado o un override de `perfiles_radio.json`.
- Tuerca 1/4"-20 (se rompió en una impresión real): piel 2,0 mm, bolsillo hexagonal con ≥ 3 mm de pared y esquinas redondeadas, labios de retención en el canal de entrada, cavidad maciza 36 mm con rampa cónica y brida opcional de 50 × 36 mm.
- Nuevos `src/verificar_v6.py`, `src/render_v6.py` y `docs/VARIANTES_V6.md`. Sin medidas físicas de clip ni prueba de carga; los STL se generan con los comandos de ese documento.

## Ayuda, CLI e imágenes — 2026-11-01
- Índice de ayuda en español, navegación cruzada y opciones `-h`/`--help` sin dependencias CAD.
- Renders explicativos del STL v3 actual: conjunto estimado, acceso al duplexor y detalle de placa/cartelas; sin cambios de STL ni de resultados CAD.

## Revisión de placa baja v3 — 2026-11-01
- Sustituye la funda vertical por placa de 55 × 48 × 4 mm a 20°, 47 mm libres, recorrido de 40 mm, espacio de 7 mm y ventana opcional de 22 × 6 mm.
- Dos cartelas de 4 mm con pies V140..154 a H54, embebidos 4,64 mm en la torre existente; bajos abiertos, sin losa.
- Conserva empuñadura, boom y trípode. Verificación contra 35019cc, pies finitos y barridos continuos de clip y radio+clip.
- Corredores V del duplexor sin obstrucción nueva; colisión nominal heredada de v1 (462,2388 mm³) documentada, no ocultada.
- Renders CAD y resultados JSON actualizados. Dimensiones de clip/radio estimadas; sin prueba física ni certificación estructural.

## v3.1.0 — 2026-11-01 (diseño histórico, sustituido)
- En esa revisión se restaura la v3 (c77de14) como modelo activo: lengüeta del clip en la torre y tuerca única de trípode a 1,2 mm (ranura de 5,9 mm; rosca limitada por la tuerca real, 5,6 mm nominal).
- La descripción de esta versión (boca 50 mm, fondo 47 mm, 70 mm útiles y paredes en cuña) corresponde al diseño anterior; no describe el STL actual. La revisión vigente, arriba, usa una placa de 55 × 48 × 4 mm a 20°, 47 mm libres, 40 mm de inserción y dos cartelas.
  Dimensiones del clip (25–45 × 6 mm) estimadas, no verificadas; solo se conoce la separación de 26 mm entre tornillos del clip Retevis/TYT MD-380 (https://www.retevis.com/products/belt-clip-for-tyt-tytera-md-380-retevis-rt3-radio).
- La v4 (canal en V, dos tuercas) se archiva en legacy/mango_v4/.
- El verificador de aquel snapshot comparaba contra git c77de14; el script vigente compara contra 35019cc.
- Nueva imagen docs/img/clip_detalle.png.

## v4.0.0 — 2026-11-01 (diseño histórico, archivado)
- Canal universal en V para el clip del walki en la cara superior de la empuñadura (lenguas de 25 a 45 mm y hasta 6 mm de grosor).
  Labios en cola de milano a 45° (sin soportes); la lengua baja por la V hasta acuñarse. Sustituye a la lengüeta de la torre de la v3.
- Ranura del trípode para dos tuercas 1/4"-20 apiladas (rosca a 1,2 mm de la cara; 8,8 mm de rosca con un tornillo de 10 mm).
- `mango_v3.py` pasa a `mango_v4.py`; `verificar.py` comprueba el canal, los voladizos nuevos y la rosca del trípode.

## v3.0.0 — 2026-10-23
- Soporte de walki integrado: lengüeta para el clip de cinturón en el lateral de la torre (una sola pieza, sin tornillos).
  El walki queda a 28,6 mm del duplexor.
- Tuerca 1/4"-20 del trípode a 1,2 mm de la cara del culo (antes 3 mm): los tornillos cortos de las placas rápidas ya cogen rosca.
- Se retira la base GoPro con su adaptador y sus mordazas (movidos a `legacy/soporte_gopro/`; `soporte_walki.py` necesita el `mango_v2.py` de la v2.0.0).
- `mango_v2.py` pasa a `mango_v3.py`; `verificar.py` y `render_docs.py` se rehacen para la v3.

## v2.0.0 — 2026-10-11
- Soporte de walki nuevo con enganche tipo GoPro (base de 3 dedos en la cara libre de la torre). Ya no choca con el duplexor.
- Soporte **universal**: mordazas ajustables de 50 a 86 mm de ancho y hasta 54 mm de grosor.
- Se retira la función del móvil (rosca lateral 1/4" rellenada; pinza movida a `legacy/`).
- Nuevos scripts: `mango_v2.py`, `soporte_walki.py`, `verificar.py`, `render_docs.py`.
- Imágenes de la documentación actualizadas.

## v1.0.0 — 2026-09-30
- Mango nivelado sobre el eje del boom (el STL original estaba girado ~1°).
- Base plana en el culo de la empuñadura con tuerca 1/4"-20 para trípode.
- Dos roscas 1/4"-20 en la torre para brazos de rótula (walki arriba, móvil en el lateral).
- Funda para duplexor VHF/UHF entre la torre y el boom.
- Pinza de móvil imprimible (58–92 mm) con tuerca 1/4"-20.
- Scripts paramétricos de generación (`src/`).
