# Calibración Anycubic Kobra S1 y Bambu Lab

**Español** · [English](../en/README.md) · [Deutsch](../de/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md)

> ⚠ PENDIENTE DE PRUEBA FÍSICA

## Calibración de impresora (separada del ajuste mecánico)

Los pasos de esta guía calibran la **impresora**. El ajuste de holguras del montaje está en `MONTAJE_ILUSTRADO.md`.

## Anycubic Kobra S1

1. Antes del primer encendido desbloquear plataforma/cama; el primer arranque ejecuta autoverificación, compensación de vibración y autonivelado (guía rápida).
2. Precalentar la cama 5–10 min y lavar la placa con agua/detergente (guía de primera capa).
3. Si hay «capa falsa» en una esquina: girar el tornillo de la cama de esa esquina 1/4 de vuelta en sentido antihorario con llave Allen S2.0, volver a nivelar y reevaluar.
4. Datos oficiales: volumen 250³ mm, boquilla 0.4, máx. 320 °C boquilla, 120 °C cama, ambiente 8–40 °C (si <10 °C, cama ≈70 °C). Soporta PLA, PETG, ABS, ASA, TPU 95A y PC/PA/CF/GF.
5. Temperatura: usar el rango del fabricante del filamento y el perfil del slicer como punto de partida; ajustar con torres/ensayos propios.
6. Flujo: calibrar con la función del slicer; Anycubic Slicer Next se basa en el motor OrcaSlicer — comprobar en su versión si ofrece calibración de flujo o compensación XY de agujeros.
7. Mantenimiento: husillo Z cada ~3 meses (grasa), varillas Y mensualmente.

## Bambu Lab

El modelo exacto es desconocido: se dan pasos comunes y las variantes que respalda la documentación oficial.

1. Calibración automática (nivelado, compensación de vibración, flujo dinámico) desde pantalla, Bambu Studio (Dispositivos → Calibrar) o Bambu Handy.
2. Flow Dynamics (PA) poco fiable con filamento húmedo/transparente, placa sucia, boquilla desgastada o TPU.
3. Flow rate: calibrar después de las demás calibraciones.
4. Compensación XY de agujeros/contorno: Proceso → Calidad → Precisión; el diámetro del agujero cambia 2× el valor; iterar con calibre y mismo filamento/perfil.
5. Primera capa: ver guía de la serie (X1, H2, P2S, X2D, A2L…); PETG y PETG-CF: ver compatibilidad (CF requiere boquilla endurecida).

| Serie | Ruta de menú |
|---|---|
| X1 | Control → Calibrate |
| P1 | Settings → Calibration |
| A | Settings → Maintenance → Calibration |
| H2 / P2S / X2D | Settings → Calibration → Print Calibration |

## Fuentes oficiales

- <https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/quick-start-guide>
- <https://wiki.anycubic.com/kobra-s1/anycubic_kobra_s1_combo_user_manual-en-v1.3.pdf>
- <https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/first-layer>
- <https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/faq>
- <https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/printing-effect-is-not-good>
- <https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/maintenance-recommendations>
- <https://wiki.anycubic.com/en/software-and-app/anycubicslicer>
- <https://wiki.bambulab.com/en/general/printer-calibration>
- <https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa>
- <https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate>
- <https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation>
- <https://wiki.bambulab.com/en/x1/troubleshooting/first-layer-printing-optimization-guide>
- <https://wiki.bambulab.com/en/filament/petg>
- <https://wiki.bambulab.com/en/x1/manual/manual-bed-leveling>
