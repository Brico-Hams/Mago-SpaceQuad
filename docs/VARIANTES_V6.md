# Variantes v6 (solo CAD)

Todo lo de este documento es geometría CAD sin imprimir ni medir. No afirma ajuste físico del clip ni resistencia de la tuerca.

## Qué cambia

1. **Posición D (v6.2): inclinación −V y radio en el lado −U.** Elegida por el usuario entre 4 opciones renderizadas. `TILT_HACIA` = `-V` por defecto (sentido confirmado por el usuario sobre la pieza real; ya no existe el alias `empunadura`), `LADO_U` = `-U` por defecto (`+U` = disposición anterior) y `TILT_DEG` (20°). El eje largo de la radio queda inclinado `TILT_DEG` sobre la horizontal con su extremo superior (el del clip) hacia −V. La placa y el hueco se espejan en U respecto al eje del boom (U = 15,55): la placa pasa de U 24…79 a U ≈ −48…7 y la radio queda en el lado −U, lejos del duplexor. Como ahí no hay torre, con `-U` una viga de 14 × 7,5 mm (V 140…154, H 50,5…58) une las dos cartelas de 4 mm con la torre y entra 4 mm en U dentro de ella (supuesto: torre en U ≈ 8…78); no toca el túnel del boom (15,5 mm + 0,5 mm de holgura) ni el duplexor. El hueco bajo la placa queda abierto. El clip entra paralelo a la placa por el borde libre superior y la ventana de retención de 22 × 6 mm sigue cerca del fondo del hueco.
   - Historial: v6.0 usó −V; v6.1 pasó a +V; v6.2 vuelve a −V tras confirmarlo sobre la pieza real. Para la disposición anterior: `--tilt-hacia +V --lado-u +U`.
2. **Variantes reales.** La altura de la placa (`PH0`) se calcula para que el punto más bajo de la envolvente de cada radio y el hueco del clip queden ≥ 3,4 mm sobre la cara de la torre (H = 62). Resultado nominal con 20°: UV-K5 V3 `PH0` = 72,5 mm; RT-950 Pro `PH0` = 88,5 mm (cartelas más altas). El ancho del hueco sale del clip de cada radio (`clip.ancho_mm`, o 45 mm si es `null`) más 1 mm por lado; el grueso del hueco, `clip.grueso_max_mm` (o 6 mm) + 1 mm.
3. **Base del trípode (la tuerca se rompió en una impresión real).**
   - Piel de la cara del culo de 2,0 mm (v3: 1,2 mm). Un tornillo de trípode de 6 mm o más engrana unos 4 mm de la tuerca (nominal 5,6 mm).
   - Bolsillo hexagonal (AF 11,4 mm, fondo 5,9 mm) con las esquinas redondeadas (r = 0,8 mm) y ≥ 3 mm de material en el fondo y en los lados. Taladro Ø6,6 mm con alivio de 4 mm tras la tuerca para la punta del tornillo.
   - El canal lateral de entrada se cierra con dos labios de 0,4 mm por lado (apertura 10,6 mm frente a 11,1 mm nominales de la tuerca): la tuerca entra a presión. La interferencia es teórica y no está probada; el canal queda fuera de la regla de 3 mm.
   - Cavidad del mango maciza 36 mm desde el culo, con rampa cónica de 30 mm antes (lógica de `refuerzo_base.py`).
   - Brida opcional en el culo de 50 × 36 mm (límite 60 × 40), 12 mm de grueso y chaflán de 5 mm; cara del culo plana. Se desactiva con `--sin-brida`. El exterior de la empuñadura por encima de la brida no cambia.

## Fuentes y estado de cada dimensión

| Dato | Valor | Fuente | Estado |
|---|---|---|---|
| UV-K5 V3 cuerpo | 115 × 60 × 37,5 mm, ~234 g | onesdr.com y newegg; hamradio.my da 110 × 58 × 32 mm | estimada, fuentes de terceros |
| RT-950 Pro cuerpo | ~162 × 66 × 48 mm, ~0,66 kg | copias de manuals.plus del manual de Radtel (no oficiales); el alto probablemente incluye botones | estimada |
| Lengüeta del clip | 25–45 mm de ancho, hasta 6 mm de grueso | envolvente de ingeniería de la v3; solo la separación de 26 mm entre tornillos del clip Retevis/TYT MD-380 está verificada | estimada; sin medir en ninguna radio |
| Distancia clip–extremo superior | 25 mm | valor de la v3 (`R_ABOVE`) | estimada |
| Tuerca, taladro, posición del trípode | 1/4"-20, AF 11,4 mm, Ø6,6 mm, y = 115,2, z = 15,7 | medidas sobre el STL v1 (v3) | del CAD, no del objeto físico |
| Duplexor | caja x −33,4…−17,9, y 118…177, z 28…59,5 | `verificar.py` | nominal |

`perfiles_radio.json` admite un override por radio: poner valores en `clip.ancho_mm`, `clip.grueso_max_mm` y `radio.pos_clip_desde_extremo_A_mm` (`null` = usar la estimación). Anytone sigue bloqueado: sin modelo exacto, sin STL.

## Regenerar

```powershell
python src/mango_v6.py stl/mango_spacequad_tripode.stl stl/v6 todas
python src/verificar_v6.py stl/v6 docs/cad_checks_v6.json
python src/render_v6.py stl docs/img
```

Opciones comunes: `--tilt-hacia +V|-V`, `--lado-u -U|+U`, `--tilt-deg 20`, `--sin-brida` (pasar las mismas en los tres comandos). `verificar_v6.py` comprueba: sólido único y estanco; radio frente a mango, duplexor y barra del boom (15 × 15 mm, V −100…400) = 0 mm³; radio en el lado −U (`radio_side_minus_u`); inclinación real del extremo superior hacia `TILT_HACIA`; viga y cartelas fuera del túnel del boom y del duplexor; soporte empotrado ≥ 2 mm en la torre (`bracket_anchored_in_tower`); barridos del clip en el hueco; pared ≥ 3 mm, piel ≥ 2,0 mm y cavidad rellena ≥ 35 mm; exterior de la empuñadura sin cambios sobre la brida. `render_v6.py` añade un tercer panel visto desde atrás del operador (extremo −V, arriba y de lado). Los resultados son geométricos y no sustituyen la medición de los clips ni una prueba de carga.
