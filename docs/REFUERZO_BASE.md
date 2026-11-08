# Refuerzo de la base de trípode

El refuerzo ahora vive dentro de `src/mango_v6.py`, que reutiliza `src/refuerzo_base.py` (fuente editable); `docs/refuerzo_base_checks.json` guarda las comprobaciones.
`refuerzo_base.py` es un **post-proceso del STL**: no modifica `mango_v3.py`, y se aplica a cualquier STL de la familia v3 que conserve la empuñadura y la base de trípode de v3.
El STL `stl/mango_spacequad_v3_refuerzo.stl` se eliminó; se regenera con:

    python src/refuerzo_base.py stl/mango_spacequad_v3.stl <salida.stl> docs/refuerzo_base_checks.json

## Origen medido del punto débil

Todo sale de secciones del STL v3 perpendiculares a la empuñadura (eje X); **no se han supuesto cargas**.

- La empuñadura es una cáscara con una cavidad cerrada de ~790 mm² (X 34..88). Termina en un tapón macizo con **escalón plano en X ≈ 88**:
  la sección pasa de **~600 mm² a ~1390 mm²** y el módulo resistente débil (flexión en el plano X-Z, canto de 31 mm) de **~4430 a ~6050 mm³** en menos de 0,5 mm.
  Ese salto brusco (gradiente 3376 mm³/mm) es un concentrador de tensión justo junto a la base, donde el momento de flexión de la antena sobre el trípode es mayor.
- Tras el escalón la cavidad sigue como rendijas finas hasta X ≈ 96,4 (≈ 32 mm³): grietas internas dentro del tapón.
- La ranura de tuerca reduce el módulo débil de 6760 a 5420 mm³ (X 103..109), pero sigue por encima del tramo hueco; la piel de 1,2 mm delante de la tuerca trabaja a compresión
  entre la placa del trípode y la tuerca. Se deja tal cual para conservar el enganche de rosca.

## Cambio

- La cavidad se rellena en **rampa cónica de 30 mm** (X 58..88): la pared interior engrosa linealmente hasta cerrar la cavidad en el escalón (radio inscrito 10,09 mm).
- Se rellenan las rendijas finas tras el escalón (X 88..96,4).
- Volumen añadido: **13,2 cm³** (191,95 → 205,17 cm³). No hay nervios ni radios externos: no hacían falta.

## Comprobaciones (CAD, no ensayo físico)

| Prueba | Resultado |
|---|---|
| Contorno exterior (todas las secciones X 40..109) | idéntico; bounding box idéntico |
| Material eliminado respecto al v3 | 0 mm³ |
| Interferencia con ranura de tuerca, taladro Ø6,6 y cilindro de acceso del tornillo/placa | 0 mm³ |
| Zona modificada | X 57,7..96,4, solo dentro de la cavidad |
| Salto en el escalón (área / Z débil) | 600→1390 mm² / 4430→6050 mm³; ahora 1393→1389 mm² / 6092→6057 mm³ |
| Gradiente máximo de Z débil | 3376 → 669 mm³/mm |
| Z débil en X=64 / 72 / 80 | 3635→4321 / 3941→5169 / 4163→5673 mm³ |
| Malla | mismas 2 piezas (cuerpo + cavidad), sin aristas abiertas; se conservan los defectos previos del v3 (1 arista no-manifold, 41 caras degeneradas) |

La sección débil mínima del mango (≈3040 mm³ en X≈44, cáscara hueca) **no se ha modificado**: está lejos de la base. Si la rotura real ocurre ahí, hay que ampliar la rampa.

## Orientación de impresión

Imprime **en la orientación del STL** (empuñadura horizontal, cama en Z=0). Las capas quedan paralelas al eje de la empuñadura y el plano de rotura (X≈88) corta
las capas, no coincide con una interfaz entre ellas. **No imprimas el mango de pie sobre el culo**: las capas coincidirían con el plano de rotura y la unión entre capas
trabajaría a tracción justo en el escalón y en la ranura de tuerca. La ranura de tuerca sigue abierta hacia la cama (Z=0). Sugerencia sin validar: 5–6 perímetros y relleno ≥ 50 % en X 58..110.

## Pendiente

Sin ensayo de carga ni validación física. `mango_v6.py` ya aplica el refuerzo; para otros STL basta ejecutar el script sobre cada uno.
