# Variantes v6 (solo CAD)

Todo lo de este documento es geometría CAD sin imprimir ni medir. No afirma ajuste físico del clip ni resistencia de la tuerca.

## Qué cambia

1. **Inclinación de la radio.** `TILT_HACIA` (`empunadura` por defecto, o `+V` / `-V`) y `TILT_DEG` (20°). El eje largo de la radio queda inclinado `TILT_DEG` sobre la horizontal con su extremo superior (el del clip) del lado elegido. `empunadura` se resuelve como el lado V donde está el eje del trípode (y = 115,2 frente a la torre en y = 147,6): **−V**. La v3/v5 tenía el extremo superior hacia +V. El clip sigue entrando paralelo a la placa por el borde libre superior, la radio apoya sobre la cara exterior de la placa y dos cartelas de 4 mm mantienen la placa anclada en la torre. La ventana de retención opcional de 22 × 6 mm sigue cerca del fondo del hueco.
   - Interpretación adoptada: "hacia la empuñadura" = el extremo superior de la radio cae del lado V de la empuñadura. Si la pantalla debe mirar de otra forma, usar `--tilt-hacia +V` o `-V`.
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

Opciones comunes: `--tilt-hacia empunadura|+V|-V`, `--tilt-deg 20`, `--sin-brida` (pasar las mismas en los tres comandos). `verificar_v6.py` comprueba: sólido único y estanco; radio frente a mango y duplexor = 0 mm³; inclinación real del extremo superior hacia `TILT_HACIA`; barridos del clip en el hueco; pared ≥ 3 mm, piel ≥ 2,0 mm y cavidad rellena ≥ 35 mm; exterior de la empuñadura sin cambios sobre la brida. Los resultados son geométricos y no sustituyen la medición de los clips ni una prueba de carga.
