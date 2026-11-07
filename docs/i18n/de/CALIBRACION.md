# Kalibrierung Anycubic Kobra S1 und Bambu Lab

[Español](../es/README.md) · [English](../en/README.md) · **Deutsch** · [Français](../fr/README.md) · [Italiano](../it/README.md)

> ⚠ PHYSISCHE PRÜFUNG AUSSTEHEND

## Druckerkalibrierung (getrennt von mechanischer Passung)

Die Schritte hier kalibrieren den **Drucker**. Die Spielanpassung der Montage steht in `MONTAJE_ILUSTRADO.md`.

## Anycubic Kobra S1

1. Vor dem ersten Einschalten Plattform/Heizbett entriegeln; der erste Start führt Selbsttest, Vibrationskompensation und Auto-Leveling aus (Schnellstartanleitung).
2. Bett 5–10 min vorheizen und Platte mit Wasser/Spülmittel reinigen (Erste-Schicht-Anleitung).
3. Bei «falscher Schicht» an einer Ecke: Bettschraube dieser Ecke 1/4 Umdrehung gegen den Uhrzeigersinn mit S2.0-Inbusschlüssel drehen, neu leveln und prüfen.
4. Offizielle Daten: Bauraum 250³ mm, Düse 0.4, max. 320 °C Düse, 120 °C Bett, Umgebung 8–40 °C (bei <10 °C Bett ≈70 °C). Unterstützt PLA, PETG, ABS, ASA, TPU 95A und PC/PA/CF/GF.
5. Temperatur: vom Bereich des Filamentherstellers und Slicer-Profil ausgehen; mit eigenen Türmen/Tests verfeinern.
6. Fluss: mit der Slicer-Funktion kalibrieren; Anycubic Slicer Next basiert auf OrcaSlicer — prüfen, ob Ihre Version Fluss-Kalibrierung oder XY-Lochkompensation bietet.
7. Wartung: Z-Spindel etwa alle 3 Monate (Fett), Y-Stangen monatlich.

## Bambu Lab

Das genaue Modell ist unbekannt: gemeinsame Schritte plus Varianten, die die offizielle Dokumentation stützt.

1. Automatische Kalibrierung (Leveling, Vibrationskompensation, Flow Dynamics) am Display, in Bambu Studio (Geräte → Kalibrieren) oder Bambu Handy.
2. Flow Dynamics (PA) unzuverlässig bei feuchtem/transparentem Filament, schmutziger Platte, verschlissener Düse oder TPU.
3. Flussrate: nach den anderen Kalibrierungen kalibrieren.
4. XY-Loch-/Konturkompensation: Prozess → Qualität → Präzision; Lochdurchmesser ändert sich um das 2-Fache des Wertes; mit Messschieber und gleichem Filament/Profil iterieren.
5. Erste Schicht: Anleitung der Serie (X1, H2, P2S, X2D, A2L…); PETG und PETG-CF: Kompatibilität beachten (CF braucht gehärtete Düse).

| Serie | Menüpfad |
|---|---|
| X1 | Control → Calibrate |
| P1 | Settings → Calibration |
| A | Settings → Maintenance → Calibration |
| H2 / P2S / X2D | Settings → Calibration → Print Calibration |

## Offizielle Quellen

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
