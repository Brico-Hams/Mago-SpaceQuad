# Calibration Anycubic Kobra S1 et Bambu Lab

[Español](../es/README.md) · [English](../en/README.md) · [Deutsch](../de/README.md) · **Français** · [Italiano](../it/README.md)

> ⚠ ESSAI PHYSIQUE EN ATTENTE

## Calibration de l'imprimante (séparée de l'ajustement mécanique)

Les étapes ici calibrent l'**imprimante**. L'ajustement des jeux du montage est dans `MONTAJE_ILUSTRADO.md`.

## Anycubic Kobra S1

1. Avant la première mise sous tension, déverrouiller la plateforme/le plateau chauffant ; le premier démarrage lance auto-test, compensation des vibrations et nivellement auto (guide de démarrage rapide).
2. Préchauffer le plateau 5–10 min et laver la plaque à l'eau/détergent (guide de première couche).
3. En cas de « fausse couche » dans un coin : tourner la vis du plateau de ce coin d'un quart de tour dans le sens antihoraire avec une clé Allen S2.0, renivelez et revérifier.
4. Données officielles : volume 250³ mm, buse 0.4, max 320 °C buse, 120 °C plateau, ambiance 8–40 °C (si <10 °C, plateau ≈70 °C). Prend en charge PLA, PETG, ABS, ASA, TPU 95A et PC/PA/CF/GF.
5. Température : partir de la plage du fabricant du filament et du profil du slicer ; affiner par vos propres tours/essais.
6. Débit : calibrer avec la fonction du slicer ; Anycubic Slicer Next repose sur OrcaSlicer — vérifier si votre version propose calibration du débit ou compensation XY des trous.
7. Entretien : vis-mère Z environ tous les 3 mois (graisse), tiges Y chaque mois.

## Bambu Lab

Le modèle exact est inconnu : étapes communes et variantes appuyées par la documentation officielle.

1. Calibration automatique (nivellement, compensation des vibrations, dynamique du flux) depuis l'écran, Bambu Studio (Appareils → Calibrer) ou Bambu Handy.
2. Flow Dynamics (PA) peu fiable avec filament humide/transparent, plaque sale, buse usée ou TPU.
3. Débit : calibrer après les autres calibrations.
4. Compensation XY des trous/contours : Processus → Qualité → Précision ; le diamètre du trou change de 2× la valeur ; itérer au pied à coulisse avec le même filament/profil.
5. Première couche : voir le guide de la série (X1, H2, P2S, X2D, A2L…) ; PETG et PETG-CF : voir compatibilité (CF exige une buse durcie).

| Série | Chemin de menu |
|---|---|
| X1 | Control → Calibrate |
| P1 | Settings → Calibration |
| A | Settings → Maintenance → Calibration |
| H2 / P2S / X2D | Settings → Calibration → Print Calibration |

## Sources officielles

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
