# Lista de materiales

**Ayuda:** [guía del proyecto](AYUDA.md) · [montaje](MONTAJE.md) · [README](../README.md).

## Piezas impresas

| Archivo | Cantidad | Volumen aprox. | Notas |
|---|---|---|---|
| `stl/v6/mango_spacequad_v6_uvk5v3.stl` | 1 (según tu radio) | ver laminador | **v6.2 recomendada** para UV-K5 V3. Soportes bajo placa y viga; relleno alto o paredes extra en viga y trípode. PETG o ASA |
| `stl/v6/mango_spacequad_v6_rt950pro.stl` | 1 (según tu radio) | ver laminador | **v6.2 recomendada** para RT-950 Pro. Mismas indicaciones |

Imprime solo el STL de tu radio. El volumen real lo da el laminador (consumo con relleno y soportes); el volumen macizo de cada STL se calcula en `docs/cad_checks_v6.json`.
**Haz una prueba de carga antes de fiarte de la pieza**: ni la viga ni la tuerca reforzada se han probado físicamente.

## Tornillería

| Cantidad | Pieza | Dónde va |
|---|---|---|
| 1 | Tuerca hexagonal 1/4"-20 UNC (11,1 mm e/c, 5,6 mm de grosor nominal) | Culo de la empuñadura (trípode), a presión pasando los labios; piel de 2 mm. Opcional |
| 1 | Tornillo de trípode 1/4"-20 de 6 mm o más | Engrana unos 4 mm de la tuerca |

## Accesorios comerciales

| Cantidad | Pieza | Notas |
|---|---|---|
| 1 | Trípode con rótula y placa de liberación rápida de 1/4" | Opcional |
| 1 | Duplexor VHF/UHF de hasta 16 × 32 mm de sección | Por ejemplo, un duplexor casero en perfil de aluminio |
| 1 | Tira fina de goma EVA | Opcional, si el clip queda flojo |

## Capacidad del soporte (v6.2, estimada)

| Dato | Valor |
|---|---|
| Ancho de la lengua del clip (estimado, no medido) | de 25 a 45 mm; 47 mm libres |
| Grosor de la lengua del clip (estimado) | hasta 6 mm (holgura mínima 7 mm) |
| Recorrido útil (estimado) | 40 mm, paralelo a placa de 55 × 48 × 4 mm a 20°, entrando por su borde libre alto |
| Envolvente UV-K5 V3 / RT-950 Pro (estimada, terceros) | 115 × 60 × 37,5 mm / 162 × 66 × 48 mm |
| Walki | clips de cinturón de Baofeng, Radtel, Anytone, Quansheng, Retevis RT3S: no medidos, sin garantía de ajuste universal |

## Versiones anteriores

Solo siguen v1 (entrada), v3 (generador base y referencia del Anytone, `stl/mango_spacequad_v3.stl`) y el Anytone genérico
(`stl/mango_spacequad_anytone_generico.stl` con `stl/anytone_calzos/`). v2, v4 y v5 se eliminaron; se recuperan del historial de git (commit anterior a la limpieza).
Usan la misma tuerca 1/4"-20, pero la v6.2 es la pieza recomendada.
