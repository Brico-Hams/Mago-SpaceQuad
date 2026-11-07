# AGENTS

- CAD en Python (`src/`), STL en `stl/`, documentación en `docs/`. Antes de dar un STL por válido ejecutar su `verificar_*.py`.
- Ninguna medida de clip de radio (UV-K5 V3, RT-950 Pro, Anytone) está confirmada físicamente; no afirmar ajuste real sin medir.
- No subir `.venv/`, el STL original de terceros ni archivos temporales. No forzar push.
- Graphify: usar `graphify-out/` para consultas de arquitectura; no indexar carpetas fuera del repo.

## Estado (integrado en main)

| Entrega | Verificación CAD | Pendiente físico |
|---|---|---|
| v5 giro radio 180° (UV-K5 V3, RT-950 Pro) | `src/verificar_v5.py` OK | medir clips; imprimir |
| Anytone genérico ajustable | `src/verificar_anytone.py` OK | medir clip y elegir calzo; imprimir |
| Refuerzo base trípode | `docs/refuerzo_base_checks.json` | prueba de carga e impresión |
