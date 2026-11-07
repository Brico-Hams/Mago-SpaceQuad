# SpaceQuad-Griff v5 — Bebilderte Montageanleitung

[Español](../es/README.md) · [English](../en/README.md) · **Deutsch** · [Français](../fr/README.md) · [Italiano](../it/README.md)

> Basiert auf der Geometrie von `feat/v5-radio-180` (2497ad7). Bei Geometrieänderung mit `src/render_guia.py` neu erzeugen. Die Clip-Maße sind geschätzt, nicht gemessen.

## Grafiken

![Seitenansicht mit Maßen (X zeigt zum Griff)](../../img/guia/fig01a_vista_lateral.png)
*Seitenansicht mit Maßen (X zeigt zum Griff)*

![Stirnansicht (Griffende)](../../img/guia/fig01b_vista_extremo.png)
*Stirnansicht (Griffende)*

![Draufsicht der Clip-Platte: 55 × 48 × 4 mm bei 20°](../../img/guia/fig01c_planta_placa.png)
*Draufsicht der Clip-Platte: 55 × 48 × 4 mm bei 20°*

![Explosionsansicht und nummerierte Schritte ①–④ (Mutter von Z− einsetzen)](../../img/guia/fig02_explosionado.png)
*Explosionsansicht und nummerierte Schritte ①–④ (Mutter von Z− einsetzen)*

![Schnitte A-A (Tunnel) und B-B (Mutterntasche)](../../img/guia/fig03_cortes.png)
*Schnitte A-A (Tunnel) und B-B (Mutterntasche)*

![Druckausrichtungen im Vergleich](../../img/guia/fig04_orientacion_impresion.png)
*Druckausrichtungen im Vergleich*

![Clip-Einschub (v3 von +V; v5 von −V)](../../img/guia/fig05_insercion_clip.png)
*Clip-Einschub (v3 von +V; v5 von −V)*

## Stückliste (BOM)

| Nr. | Menge | Teil | Maß / Spezifikation | Hinweis |
|---|---|---|---|---|
| 1 | 1 | Gedruckter Griff v5 (`stl/v5/*uvk5v3.stl`) | Hüllmaß 195.2 × 95.6 × 79.0 mm | PETG empfohlen |
| 2 | 1 | Sechskantmutter 1/4"-20 UNC | Schlüsselweite 11.1 mm, Dicke 5.6 mm | Tasche SW 11.4 × 5.9 mm |
| 3 | 1 | Ausleger (nicht enthalten) | Ø15 mm, Tunnel 15.5 × 15.5 mm (Nennspiel 0.25 mm je Seite) | Echten Ausleger messen |
| 4 | 0–1 | Stativ-Schnellwechselplatte/-schraube (optional) | 1/4"-20 | Nach Bedarf |
| 5 | 0–1 | Duplexer und EVA-Streifen (optional) | — | Je nach Funkgerät |

Dieses Design hat **keine Lager oder Wellen**; einziges Beschlagteil ist die 1/4"-20-Mutter.

## Montagereihenfolge

1. Teil prüfen: Grate in Tunnel und Sechskanttasche entfernen.
2. Mutter von der Z−-Seite in die Tasche einsetzen (1.2 mm Haut zum Griffende).
3. Ausleger Ø15 mm durch den 15.5 × 15.5-mm-Tunnel schieben.
4. Clip auf der Platte (55 × 48 × 4 bei 20°) montieren und Funkgerät sichern.

## Spiel messen und anpassen (mechanische Passung)

> ⚠ PHYSISCHE PRÜFUNG AUSSTEHEND

1. `stl/calibracion/prueba_holguras.stl` (124 × 92 × 8 mm) mit dem ENDGÜLTIGEN Profil und demselben Filament drucken.
2. Reihe 1: Vierkantlöcher 15.1–15.9 mm für den Ausleger. Reihe 2: Sechskanttaschen SW 11.1–11.9 mm. Reihe 3: Schlitze 6.0–8.0 mm. Punkte 1–5 kennzeichnen die Größe.
3. Mit Messschieber (0.02 mm) nach 24 h Abkühlen messen; mit echtem Ausleger und echter Mutter testen.
4. Das Loch wählen, das mit Fingerdruck ohne sichtbares Spiel gleitet (Startziel 0.2–0.3 mm je Seite, Test ausstehend).
5. Mit XY-Lochkompensation des Slicers (falls vorhanden) oder dem Modell korrigieren; nicht über den Fluss anpassen.

## Festigkeitsprüfung (vorsichtige Tests)

> ⚠ PHYSISCHE PRÜFUNG AUSSTEHEND

1. Funkgerät mit Zubehör wiegen: reale Masse M (vorab unbekannt).
2. Prüflast = 2 × M, in Stufen von 25 %, 50 % und 100 % dieser Last, je 60 s, Ballast über niedriger, geschützter Fläche.
3. Nach jeder Stufe prüfen; bei Rissen, Weißbruch oder Verformung > 0.3 mm abbrechen.
4. Praktisches Verfahren, keine Zertifizierung. Lasten durch M begründet; nie über Personen oder wertvollen Geräten.

## Lizenz und Namensnennung

CC-Lizenz des Repositories (`LICENSE`, Bricohams). Der Pastamatic-Umspuler behält seine ursprüngliche Urheberschaft; seine Lizenz ist nicht verifiziert und wird hier nicht veröffentlicht.
