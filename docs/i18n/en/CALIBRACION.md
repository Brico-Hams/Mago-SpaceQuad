# Anycubic Kobra S1 and Bambu Lab calibration

[Español](../es/README.md) · **English** · [Deutsch](../de/README.md) · [Français](../fr/README.md) · [Italiano](../it/README.md)

> ⚠ PENDING PHYSICAL TEST

## Printer calibration (separate from mechanical fit)

The steps here calibrate the **printer**. Assembly clearance adjustment is in `MONTAJE_ILUSTRADO.md`.

## Anycubic Kobra S1

1. Before first power-on unlock the platform/hot bed; first boot runs self-check, vibration compensation and auto-leveling (quick start guide).
2. Preheat the bed 5–10 min and wash the plate with water/detergent (first-layer guide).
3. If a «false layer» appears at a corner: turn that corner's bed screw 1/4 turn counterclockwise with an S2.0 Allen key, re-level and re-check.
4. Official data: 250³ mm volume, 0.4 nozzle, max 320 °C nozzle, 120 °C bed, ambient 8–40 °C (if <10 °C, bed ≈70 °C). Supports PLA, PETG, ABS, ASA, TPU 95A and PC/PA/CF/GF.
5. Temperature: start from the filament maker's range and the slicer preset; refine with your own towers/tests.
6. Flow: calibrate with the slicer function; Anycubic Slicer Next is based on the OrcaSlicer engine — check whether your version offers flow calibration or XY hole compensation.
7. Maintenance: Z lead screw about every 3 months (grease), Y rods monthly.

## Bambu Lab

The exact model is unknown: common steps are given plus variants supported by official documentation.

1. Auto-calibration (leveling, vibration compensation, flow dynamics) from the screen, Bambu Studio (Devices → Calibrate) or Bambu Handy.
2. Flow Dynamics (PA) is unreliable with damp/transparent filament, dirty plate, worn nozzle or TPU.
3. Flow rate: calibrate after the other calibrations.
4. XY hole/contour compensation: Process → Quality → Precision; hole diameter changes 2× the value; iterate with calipers and the same filament/profile.
5. First layer: see the series guide (X1, H2, P2S, X2D, A2L…); PETG and PETG-CF: see compatibility (CF needs a hardened nozzle).

| Series | Menu path |
|---|---|
| X1 | Control → Calibrate |
| P1 | Settings → Calibration |
| A | Settings → Maintenance → Calibration |
| H2 / P2S / X2D | Settings → Calibration → Print Calibration |

## Official sources

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
