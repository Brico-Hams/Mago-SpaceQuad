# Variante genérica para clips de cinturón (Anytone y similares)

**Ayuda:** [README](../README.md) · [montaje](MONTAJE.md) · [guía](AYUDA.md) · resultados: [cad_checks_anytone_generico.json](cad_checks_anytone_generico.json).

Soporte **ajustable y genérico**, no una pieza «para todos los Anytone»: no hay medidas de ningún clip Anytone.
Sirve para cualquier clip de cinturón cuya **lengua** (la parte que se desliza bajo la placa) entre en el rango de abajo.
**Mídela antes de imprimir.** Ni el mango ni los calzos se han probado impresos.

## Rango de ajuste (verificado en CAD con envolventes, no con clips reales)

| Dato de la lengua del clip | Rango admitido |
|---|---|
| Ancho | **21,6 a 46,4 mm** (cinco juegos de calzos + sin calzos) |
| Grosor (incluido el saliente que roza la placa) | hasta **6,0 mm**; hueco libre de 7,0 mm |
| Recorrido de inserción | 40 mm |

| Juego | Calzo (mm) | Ancho libre | Ancho de lengua que admite |
|---|---|---|---|
| Sin calzos | 0 | 47,0 | 42,0 – 46,4 |
| `calzos_d02` | 2 | 42,6 | 37,6 – 42,0 |
| `calzos_d04` | 4 | 38,6 | 33,6 – 38,0 |
| `calzos_d06` | 6 | 34,6 | 29,6 – 34,0 |
| `calzos_d08` | 8 | 30,6 | 25,6 – 30,0 |
| `calzos_d10` | 10 | 26,6 | 21,6 – 26,0 |

Regla: lengua = ancho libre − 0,6 mm (holgura mínima) … − 5,0 mm (holgura máxima). Los rangos se solapan, así que no hay huecos.
Elige el juego más estrecho en el que tu lengua entre.

### Cómo medir tu clip (calibre)
1. Ancho de la lengua en su parte más ancha (sin contar tornillos). 2. Grosor total de la lengua en su punto más grueso (con el diente/saliente).
3. Longitud de lengua que desliza (debe ser ≥ 40 mm para usar todo el recorrido; menos longitud queda sujeta solo por el muelle del clip).
Si algo queda fuera de rango, **no es compatible** sin modificar los parámetros de `src/mango_anytone_generico.py`.

## Qué cambia respecto a la v3 actual
- **Radio girada 180°:** la placa y sus cartelas se reflejan en V respecto al centro de las raíces de las cartelas (V = 147 mm), equivalente a girar 180° alrededor del eje vertical de uso. El clip entra ahora desde el extremo −V y el centroide de la radio estimada pasa de V = 129 a V = 165 mm. **Pendiente de confirmar** con la sesión que corrige la orientación del clip, que trabaja de forma independiente.
- **Calzos laterales imprimibles:** dos ranuras de 1,8 × 8 mm por lado en la placa y lengüetas en el calzo; sin tornillos. Cada pareja se imprime plana (STL en `stl/anytone_calzos/`), con entrada achaflanada.
- **Base reforzada:** el hueco interior del mango (32 021 mm³) se rellena desde x = 62 hasta su cierre en la base, y dos nervios en cruz de 3 mm lo continúan hasta x = 44 (hueco restante 10 643 mm³). Sección a x = 70: área ×2,2 y momento de inercia ×2,0–2,2; a x = 52: ×1,2–1,3.
  Tuerca 1/4"-20, piel de 1,2 mm y cara de apoyo **no cambian** (verificado: diferencia 0 en x > 97,5). Si la rotura es por arrancamiento de la piel de 1,2 mm, esto no la resuelve: habría que aumentar `TRIPOD_SKIN` (menos rosca útil).

## Montaje
1. Imprime el mango (PETG/ASA, 4 perímetros, 30–40 % de relleno; soportes bajo la placa y las cartelas) y la pareja de calzos que corresponda, planos y con la lengüeta hacia arriba.
2. Mete cada calzo desde abajo, con las lengüetas en las ranuras de la placa, pegado a la cara interior de cada cartela. Si no necesitas calzos, no pongas ninguno.
3. Desliza la lengua del clip bajo la placa desde el extremo −V; la radio queda encima, girada 180° respecto a la v3.
4. Comprueba que el walki no toque rótula, duplexor ni elementos de la antena.

## Regenerar y verificar
```bash
python src/mango_anytone_generico.py stl/mango_spacequad_tripode.stl stl/mango_spacequad_anytone_generico.stl stl/anytone_calzos
python src/verificar_anytone.py stl/mango_spacequad_anytone_generico.stl stl/anytone_calzos docs/cad_checks_anytone_generico.json
```

## Verificación de malla (104 comprobaciones, todas correctas)
Mango: variedad válida y estanca (`manifold`), un solo sólido, un único hueco interior, cambios solo en la placa y el hueco respecto a `stl/mango_spacequad_v3.stl`, boom y trípode idénticos.
Calzos: cada STL estanco con 2 cuerpos; montados sin colisión (0 mm³) y con las lengüetas solo dentro de las ranuras.
Barridos continuos de la lengua (anchos mínimo, medio y máximo de cada juego, tres posiciones verticales) sin colisión, y una lengua 0,2 mm más ancha que el hueco choca (el límite superior es real).
Radio estimada (50, 62 y 70 mm) y duplexor sin colisiones nuevas.

## Límites pendientes de prueba impresa
- Ningún clip Anytone medido: la compatibilidad solo vale para lenguas dentro del rango, no por modelo.
- Ajuste y retención de calzos (lengüeta de 1,4 mm, holguras de 0,1–0,2 mm), desgaste y deformación del clip bajo carga.
- Resistencia de la base reforzada: mejora geométrica de la sección, sin cálculo ni ensayo de carga; revisar el laminador y probar con lastre.
- Giro de 180° y refuerzo de base calculados aquí de forma independiente: reconciliar con las sesiones de clip y de base antes de fusionar.
- El grosor de 6,0 mm incluye solo la lengua; un saliente mayor no cabe en el hueco de 7 mm.
