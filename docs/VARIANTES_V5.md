# Mango v5: radio girada 180°, variantes por modelo

**Ayuda:** [guía](AYUDA.md) · [montaje](MONTAJE.md) · [materiales](MATERIALES.md).

## Eje de giro

Giro de 180° sobre la **normal de la placa**, por su centro (`s → 48 − s`, `u → 2·uc − u`). No se gira el STL completo (dejaría la empuñadura boca arriba).
`verificar_v5.py` prueba los tres ejes sobre el conjunto radio + clip:

| Eje | Lengua del clip bajo la placa | Colisión con el mango | Resultado |
|---|---|---|---|
| s (largo de placa) | 0 % | 47 936 mm³ | descartado |
| u (transversal) | 0 % | 47 179 mm³ | descartado |
| **n (normal)** | **100 %** | **0 mm³** | **elegido** |

Consecuencia: el clip entra por el extremo bajo (−V) y la radio queda sobre la placa hacia +V. La placa y las cartelas son simétricas; solo cambia la ventana de retención opcional (22 × 6 mm), de s = 14–20 mm a s = 28–34 mm. El resto del STL es idéntico a la v3 (1056 mm³ de diferencia = 2 ventanas).

## Variantes

| Variante | STL | Estado |
|---|---|---|
| Quansheng UV-K5 V3 | `stl/v5/mango_spacequad_v5_uvk5v3.stl` | geometría validada; clip **sin medir** |
| Radtel RT-950 Pro | `stl/v5/mango_spacequad_v5_rt950pro.stl` | geometría validada; clip **sin medir** |
| Anytone | — | bloqueada: falta el modelo exacto |

Ambos STL son idénticos (sin medidas propias se usa la envolvente genérica de la v3). Perfiles y medidas pendientes: `src/perfiles_radio.json`.

## Dimensiones y procedencia

| Dato | Valor | Procedencia |
|---|---|---|
| Placa | 55 × 48 × 4 mm a 20° | v3 (CAD propio) |
| Ancho libre entre cartelas | 47 mm | v3 (CAD propio) |
| Hueco bajo placa | 7 mm | v3 (CAD propio) |
| Entrada máxima | 40 mm | v3 (estimada) |
| Holgura lateral / grueso (clip 45 × 6 mm) | 2 mm total / 1 mm | cálculo CAD sobre la envolvente |
| Ancho, grueso, saliente y longitud del clip UV-K5 V3 | **sin dato** | no hay cota verificable |
| Ancho, grueso, saliente y longitud del clip RT-950 Pro | **sin dato** | radtels.com solo indica «1x Belt clip» |
| Envolvente de radio 62 × 40 × 130 mm | estimada | v3; no es la radio real |

## Medidas necesarias (por modelo)

1. Ancho de la lengua del clip (calibre).
2. Grueso máximo incluido el saliente de retención.
3. Longitud de lengua que entra bajo la placa.
4. Separación lengua–dorso de la radio.
5. Posición y tamaño del saliente, desde el borde libre de la lengua.
6. Ancho × grueso × largo de la radio con batería y clip.
7. Distancia del clip al extremo de la antena.

Anytone: además, el modelo exacto.

## Verificación

`python src/verificar_v5.py stl/v5 docs/cad_checks_v5.json`: malla estanca y de un solo sólido, solo se mueve la ventana respecto a la v3, barridos de inserción de clips de 25–45 mm, radios de 50/62/70 mm, corredores del duplexor y holguras de impresión. No certifica ajuste ni resistencia. Renders: `docs/img/v5_*_montaje.png` (`python src/render_v5.py stl docs/img`).
