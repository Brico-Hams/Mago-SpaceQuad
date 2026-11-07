# Calibrazione Anycubic Kobra S1 e Bambu Lab

[Español](../es/README.md) · [English](../en/README.md) · [Deutsch](../de/README.md) · [Français](../fr/README.md) · **Italiano**

> ⚠ PROVA FISICA IN SOSPESO

## Calibrazione della stampante (separata dall'accoppiamento meccanico)

I passi qui calibrano la **stampante**. La regolazione dei giochi del montaggio è in `MONTAJE_ILUSTRADO.md`.

## Anycubic Kobra S1

1. Prima del primo avvio sbloccare piattaforma/piatto riscaldato; il primo avvio esegue autotest, compensazione vibrazioni e autolivellamento (guida rapida).
2. Preriscaldare il piatto 5–10 min e lavare la piastra con acqua/detergente (guida al primo strato).
3. Se compare un «falso strato» in un angolo: ruotare la vite del piatto di quell'angolo di 1/4 di giro in senso antiorario con chiave Allen S2.0, rilivellare e ricontrollare.
4. Dati ufficiali: volume 250³ mm, ugello 0.4, max 320 °C ugello, 120 °C piatto, ambiente 8–40 °C (se <10 °C, piatto ≈70 °C). Supporta PLA, PETG, ABS, ASA, TPU 95A e PC/PA/CF/GF.
5. Temperatura: partire dall'intervallo del produttore del filamento e dal profilo dello slicer; affinare con torri/prove proprie.
6. Flusso: calibrare con la funzione dello slicer; Anycubic Slicer Next si basa su OrcaSlicer — verificare se la vostra versione offre calibrazione del flusso o compensazione XY dei fori.
7. Manutenzione: vite di guida Z circa ogni 3 mesi (grasso), aste Y ogni mese.

## Bambu Lab

Il modello esatto è ignoto: passi comuni e varianti supportate dalla documentazione ufficiale.

1. Calibrazione automatica (livellamento, compensazione vibrazioni, flow dynamics) dallo schermo, Bambu Studio (Dispositivi → Calibra) o Bambu Handy.
2. Flow Dynamics (PA) inaffidabile con filamento umido/trasparente, piastra sporca, ugello usurato o TPU.
3. Flow rate: calibrare dopo le altre calibrazioni.
4. Compensazione XY fori/contorni: Processo → Qualità → Precisione; il diametro del foro cambia di 2× il valore; iterare con calibro e stesso filamento/profilo.
5. Primo strato: vedere la guida della serie (X1, H2, P2S, X2D, A2L…); PETG e PETG-CF: vedere compatibilità (CF richiede ugello indurito).

| Serie | Percorso menu |
|---|---|
| X1 | Control → Calibrate |
| P1 | Settings → Calibration |
| A | Settings → Maintenance → Calibration |
| H2 / P2S / X2D | Settings → Calibration → Print Calibration |

## Fonti ufficiali

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
