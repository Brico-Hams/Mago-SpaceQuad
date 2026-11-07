"""Genera docs/i18n/{es,en,de,fr,it}/ desde un unico juego de cifras (coherencia entre idiomas)."""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "docs", "i18n")
LANGS = ["es", "en", "de", "fr", "it"]
NAMES = {"es": "Español", "en": "English", "de": "Deutsch", "fr": "Français", "it": "Italiano"}
IMG = "../../img/guia/"
FIGS = ["fig01a_vista_lateral", "fig01b_vista_extremo", "fig01c_planta_placa", "fig02_explosionado",
        "fig03_cortes", "fig04_orientacion_impresion", "fig05_insercion_clip"]

SRC = {
    "k_quick": "https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/quick-start-guide",
    "k_pdf": "https://wiki.anycubic.com/kobra-s1/anycubic_kobra_s1_combo_user_manual-en-v1.3.pdf",
    "k_first": "https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1/first-layer",
    "k_faq": "https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/faq",
    "k_print": "https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/printing-effect-is-not-good",
    "k_maint": "https://wiki.anycubic.com/en/fdm-3d-printer/kobra-s1-combo/maintenance-recommendations",
    "k_slicer": "https://wiki.anycubic.com/en/software-and-app/anycubicslicer",
    "b_cal": "https://wiki.bambulab.com/en/general/printer-calibration",
    "b_pa": "https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa",
    "b_flow": "https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate",
    "b_xy": "https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation",
    "b_fl": "https://wiki.bambulab.com/en/x1/troubleshooting/first-layer-printing-optimization-guide",
    "b_petg": "https://wiki.bambulab.com/en/filament/petg",
    "b_bed": "https://wiki.bambulab.com/en/x1/manual/manual-bed-leveling",
}

# Cifras comunes (mm) -> identicas en todos los idiomas
N = dict(bbox="195.2 × 95.6 × 79.0", tunel="15.5 × 15.5", pluma="15", jgo="0.25",
         af="11.4", esp="5.9", tal="6.6", piel="1.2", placa="55 × 48 × 4", ang="20°",
         gus="47", libre="7", rec="40", cupon="124 × 92 × 8")

L = {}
L["es"] = dict(
    title="Mango SpaceQuad v5 — Guía de montaje ilustrada",
    idx_title="Guías SpaceQuad (multiidioma)", idx_intro="Documentación coherente en 5 idiomas. Todos los perfiles de impresión y pruebas de carga son **valores iniciales PENDIENTES DE PRUEBA FÍSICA**.",
    d_mont="Montaje ilustrado, BOM, holguras y pruebas de carga", d_imp="Material, orientación y perfiles iniciales de impresión", d_cal="Calibración Anycubic Kobra S1 y Bambu Lab",
    pend="⚠ PENDIENTE DE PRUEBA FÍSICA", geo="Basado en la geometría de `feat/v5-radio-180` (2497ad7). Si cambia la geometría, regenerar con `src/render_guia.py`. Las dimensiones del clip son estimadas, no medidas.",
    figs=["Vista lateral con cotas (X apunta al agarre)", "Vista de extremo (culata)", "Planta de la placa del clip: %s mm a %s" % (N["placa"], N["ang"]),
          "Explosionado y pasos numerados ①–④ (la tuerca entra desde Z−)", "Cortes A-A (túnel) y B-B (alojamiento de tuerca)", "Orientaciones de impresión comparadas", "Inserción del clip (v3 entra por +V; v5 por −V)"],
    h_fig="Gráficos", h_bom="Lista de materiales (BOM)", bom_h=["Nº", "Cant.", "Elemento", "Medida / especificación", "Nota"],
    bom=[("1", "1", "Mango impreso v5 (`stl/v5/*uvk5v3.stl`)", "Envolvente %s mm" % N["bbox"], "PETG recomendado"),
         ("2", "1", "Tuerca hexagonal 1/4\"-20 UNC", "Entre caras 11.1 mm, espesor 5.6 mm", "Alojamiento AF %s × %s mm" % (N["af"], N["esp"])),
         ("3", "1", "Pluma / boom (no incluida)", "Ø%s mm, túnel %s mm (juego nominal %s mm por lado)" % (N["pluma"], N["tunel"], N["jgo"]), "Medir la pluma real"),
         ("4", "0–1", "Placa/tornillo de zapata de trípode (opcional)", "1/4\"-20", "Según uso"),
         ("5", "0–1", "Duplexor y tira EVA (opcionales)", "—", "Según radio")],
    nobear="Este diseño **no lleva rodamientos ni ejes**; la única tornillería es la tuerca 1/4\"-20.",
    h_ord="Orden de montaje", steps=["Verificar la pieza: limpiar rebabas del túnel y del alojamiento hexagonal.", "Insertar la tuerca por el lado Z− en el alojamiento (piel de %s mm hacia la culata)." % N["piel"], "Deslizar la pluma Ø%s mm por el túnel de %s mm." % (N["pluma"], N["tunel"]), "Montar el clip en la placa (%s a %s) y fijar la radio." % (N["placa"], N["ang"])],
    h_hol="Medir y ajustar holguras (ajuste mecánico)", hol=[
        "Imprimir `stl/calibracion/prueba_holguras.stl` (%s mm) con el perfil FINAL y el mismo filamento." % N["cupon"],
        "Fila 1: agujeros cuadrados 15.1–15.9 mm para la pluma. Fila 2: hexágonos AF 11.1–11.9 mm. Fila 3: ranuras 6.0–8.0 mm. Los hoyuelos 1–5 indican el tamaño.",
        "Medir con calibre (0.02 mm) tras enfriar 24 h; probar la pluma y la tuerca reales.",
        "Elegir el agujero que desliza con presión de dedo y sin juego visible (objetivo inicial 0.2–0.3 mm por lado, pendiente de prueba).",
        "Corregir con la compensación XY de agujeros del slicer (si existe) o con el modelo; no tocar el flujo para ajustar encaje."],
    h_car="Verificación de resistencia (pruebas prudentes)", car=[
        "Pesar la radio con accesorios montados: masa real M (no se conoce a priori).",
        "Carga de prueba = 2 × M, aplicada en escalones del 25 %, 50 % y 100 % de esa carga, 60 s cada uno, con lastre sobre superficie baja y protegido.",
        "Inspeccionar tras cada escalón; detener si hay grietas, blanqueo o deformación > 0.3 mm.",
        "Es un procedimiento práctico, no una certificación. Con cargas justificadas por M, nunca con la radio sobre una persona o equipo valioso."],
    h_mat="Material y orientación", mat_h=["Opción", "Cuándo", "Estado"],
    mat=[("PETG (recomendado)", "Uso general, tenacidad; muy buena capa-capa", "inicial, pendiente de prueba"),
         ("ASA", "Exterior prolongado/UV; requiere ventilación y cerramiento", "inicial, pendiente de prueba"),
         ("PLA", "No recomendado: fluencia/deformación con calor", "—")],
    ori_h=["Cara en cama", "Altura", "Contacto", "Voladizo >45°", "Comentario"],
    ori_c=["Recomendada: túnel vertical; capas en aros alrededor de la pluma; carga de tuerca en el plano de capa; usar brim", "Eje de tuerca vertical: tracción perpendicular a capas (débil)", "Alternativa"],
    h_prof="Perfiles iniciales", prof_h=["Parámetro", "Valor inicial"], prof=[("Altura de capa", "0.20 mm"), ("Perímetros", "4"), ("Relleno", "gyroid 40 %"), ("Brim", "5 mm (opción A)"), ("Ajuste dimensional", "0 hasta medir el cupón")],
    prof_note="Todos son valores iniciales **pendientes de prueba física**; sin parámetros universales: usar el rango de temperatura impreso en la bobina.",
    h_sep="Calibración de impresora (separada del ajuste mecánico)", sep="Los pasos de esta guía calibran la **impresora**. El ajuste de holguras del montaje está en `MONTAJE_ILUSTRADO.md`.",
    h_k="Anycubic Kobra S1", k=[
        "Antes del primer encendido desbloquear plataforma/cama; el primer arranque ejecuta autoverificación, compensación de vibración y autonivelado (guía rápida).",
        "Precalentar la cama 5–10 min y lavar la placa con agua/detergente (guía de primera capa).",
        "Si hay «capa falsa» en una esquina: girar el tornillo de la cama de esa esquina 1/4 de vuelta en sentido antihorario con llave Allen S2.0, volver a nivelar y reevaluar.",
        "Datos oficiales: volumen 250³ mm, boquilla 0.4, máx. 320 °C boquilla, 120 °C cama, ambiente 8–40 °C (si <10 °C, cama ≈70 °C). Soporta PLA, PETG, ABS, ASA, TPU 95A y PC/PA/CF/GF.",
        "Temperatura: usar el rango del fabricante del filamento y el perfil del slicer como punto de partida; ajustar con torres/ensayos propios.",
        "Flujo: calibrar con la función del slicer; Anycubic Slicer Next se basa en el motor OrcaSlicer — comprobar en su versión si ofrece calibración de flujo o compensación XY de agujeros.",
        "Mantenimiento: husillo Z cada ~3 meses (grasa), varillas Y mensualmente."],
    h_b="Bambu Lab", b0="El modelo exacto es desconocido: se dan pasos comunes y las variantes que respalda la documentación oficial.",
    b=["Calibración automática (nivelado, compensación de vibración, flujo dinámico) desde pantalla, Bambu Studio (Dispositivos → Calibrar) o Bambu Handy.",
       "Flow Dynamics (PA) poco fiable con filamento húmedo/transparente, placa sucia, boquilla desgastada o TPU.",
       "Flow rate: calibrar después de las demás calibraciones.",
       "Compensación XY de agujeros/contorno: Proceso → Calidad → Precisión; el diámetro del agujero cambia 2× el valor; iterar con calibre y mismo filamento/perfil.",
       "Primera capa: ver guía de la serie (X1, H2, P2S, X2D, A2L…); PETG y PETG-CF: ver compatibilidad (CF requiere boquilla endurecida)."],
    bser_h=["Serie", "Ruta de menú"], bser=[("X1", "Control → Calibrate"), ("P1", "Settings → Calibration"), ("A", "Settings → Maintenance → Calibration"), ("H2 / P2S / X2D", "Settings → Calibration → Print Calibration")],
    h_src="Fuentes oficiales", h_lic="Licencia y atribución", lic="Licencia CC del repositorio (`LICENSE`, Bricohams). La rebobinadora Pastamatic mantiene su autoría original; su licencia no está verificada y no se publica aquí.",
)

L["en"] = dict(
    title="SpaceQuad v5 handle — Illustrated assembly guide",
    idx_title="SpaceQuad guides (multilingual)", idx_intro="Consistent documentation in 5 languages. All print profiles and load tests are **initial values PENDING PHYSICAL TESTING**.",
    d_mont="Illustrated assembly, BOM, clearances and load tests", d_imp="Material, orientation and initial print profiles", d_cal="Anycubic Kobra S1 and Bambu Lab calibration",
    pend="⚠ PENDING PHYSICAL TEST", geo="Based on the geometry of `feat/v5-radio-180` (2497ad7). If geometry changes, regenerate with `src/render_guia.py`. Clip dimensions are estimated, not measured.",
    figs=["Side view with dimensions (X points to the grip)", "End view (butt face)", "Clip plate plan: %s mm at %s" % (N["placa"], N["ang"]),
          "Exploded view and numbered steps ①–④ (nut enters from Z−)", "Sections A-A (tunnel) and B-B (nut slot)", "Print orientations compared", "Clip insertion (v3 enters from +V; v5 from −V)"],
    h_fig="Graphics", h_bom="Bill of materials (BOM)", bom_h=["No.", "Qty", "Item", "Size / specification", "Note"],
    bom=[("1", "1", "Printed handle v5 (`stl/v5/*uvk5v3.stl`)", "Envelope %s mm" % N["bbox"], "PETG recommended"),
         ("2", "1", "Hex nut 1/4\"-20 UNC", "Across flats 11.1 mm, thickness 5.6 mm", "Pocket AF %s × %s mm" % (N["af"], N["esp"])),
         ("3", "1", "Boom (not included)", "Ø%s mm, tunnel %s mm (nominal clearance %s mm per side)" % (N["pluma"], N["tunel"], N["jgo"]), "Measure the real boom"),
         ("4", "0–1", "Tripod quick-release plate/screw (optional)", "1/4\"-20", "As needed"),
         ("5", "0–1", "Duplexer and EVA strip (optional)", "—", "Per radio")],
    nobear="This design has **no bearings or shafts**; the only hardware is the 1/4\"-20 nut.",
    h_ord="Assembly order", steps=["Check the part: remove burrs from the tunnel and hex pocket.", "Insert the nut from the Z− side into the pocket (%s mm skin toward the butt face)." % N["piel"], "Slide the Ø%s mm boom through the %s mm tunnel." % (N["pluma"], N["tunel"]), "Mount the clip on the plate (%s at %s) and secure the radio." % (N["placa"], N["ang"])],
    h_hol="Measure and adjust clearances (mechanical fit)", hol=[
        "Print `stl/calibracion/prueba_holguras.stl` (%s mm) with the FINAL profile and same filament." % N["cupon"],
        "Row 1: square holes 15.1–15.9 mm for the boom. Row 2: hex pockets AF 11.1–11.9 mm. Row 3: slots 6.0–8.0 mm. Dimples 1–5 mark the size.",
        "Measure with calipers (0.02 mm) after 24 h cooling; test with the real boom and nut.",
        "Pick the hole that slides with finger pressure and no visible play (initial target 0.2–0.3 mm per side, pending test).",
        "Correct with the slicer's XY hole compensation (if available) or the model; do not use flow to tune fit."],
    h_car="Strength verification (prudent tests)", car=[
        "Weigh the radio with accessories: real mass M (not known a priori).",
        "Proof load = 2 × M, applied in steps of 25 %, 50 % and 100 % of that load, 60 s each, ballast over a low, protected surface.",
        "Inspect after each step; stop on cracks, whitening or deformation > 0.3 mm.",
        "A practical procedure, not a certification. Loads justified by M; never over a person or valuable equipment."],
    h_mat="Material and orientation", mat_h=["Option", "When", "Status"],
    mat=[("PETG (recommended)", "General use, toughness; good layer adhesion", "initial, pending test"),
         ("ASA", "Prolonged outdoor/UV; needs ventilation and enclosure", "initial, pending test"),
         ("PLA", "Not recommended: creep/deformation with heat", "—")],
    ori_h=["Bed face", "Height", "Contact", "Overhang >45°", "Comment"],
    ori_c=["Recommended: vertical tunnel; layers as hoops around the boom; nut load in the layer plane; use brim", "Vertical nut axis: tension perpendicular to layers (weak)", "Alternative"],
    h_prof="Initial profiles", prof_h=["Parameter", "Initial value"], prof=[("Layer height", "0.20 mm"), ("Perimeters", "4"), ("Infill", "gyroid 40 %"), ("Brim", "5 mm (option A)"), ("Dimensional adjustment", "0 until the coupon is measured")],
    prof_note="All are initial values **pending physical testing**; no universal parameters: use the temperature range printed on the spool.",
    h_sep="Printer calibration (separate from mechanical fit)", sep="The steps here calibrate the **printer**. Assembly clearance adjustment is in `MONTAJE_ILUSTRADO.md`.",
    h_k="Anycubic Kobra S1", k=[
        "Before first power-on unlock the platform/hot bed; first boot runs self-check, vibration compensation and auto-leveling (quick start guide).",
        "Preheat the bed 5–10 min and wash the plate with water/detergent (first-layer guide).",
        "If a «false layer» appears at a corner: turn that corner's bed screw 1/4 turn counterclockwise with an S2.0 Allen key, re-level and re-check.",
        "Official data: 250³ mm volume, 0.4 nozzle, max 320 °C nozzle, 120 °C bed, ambient 8–40 °C (if <10 °C, bed ≈70 °C). Supports PLA, PETG, ABS, ASA, TPU 95A and PC/PA/CF/GF.",
        "Temperature: start from the filament maker's range and the slicer preset; refine with your own towers/tests.",
        "Flow: calibrate with the slicer function; Anycubic Slicer Next is based on the OrcaSlicer engine — check whether your version offers flow calibration or XY hole compensation.",
        "Maintenance: Z lead screw about every 3 months (grease), Y rods monthly."],
    h_b="Bambu Lab", b0="The exact model is unknown: common steps are given plus variants supported by official documentation.",
    b=["Auto-calibration (leveling, vibration compensation, flow dynamics) from the screen, Bambu Studio (Devices → Calibrate) or Bambu Handy.",
       "Flow Dynamics (PA) is unreliable with damp/transparent filament, dirty plate, worn nozzle or TPU.",
       "Flow rate: calibrate after the other calibrations.",
       "XY hole/contour compensation: Process → Quality → Precision; hole diameter changes 2× the value; iterate with calipers and the same filament/profile.",
       "First layer: see the series guide (X1, H2, P2S, X2D, A2L…); PETG and PETG-CF: see compatibility (CF needs a hardened nozzle)."],
    bser_h=["Series", "Menu path"], bser=[("X1", "Control → Calibrate"), ("P1", "Settings → Calibration"), ("A", "Settings → Maintenance → Calibration"), ("H2 / P2S / X2D", "Settings → Calibration → Print Calibration")],
    h_src="Official sources", h_lic="License and attribution", lic="Repository CC license (`LICENSE`, Bricohams). The Pastamatic rewinder keeps its original authorship; its license is unverified and it is not published here.",
)

L["de"] = dict(
    title="SpaceQuad-Griff v5 — Bebilderte Montageanleitung",
    idx_title="SpaceQuad-Anleitungen (mehrsprachig)", idx_intro="Konsistente Dokumentation in 5 Sprachen. Alle Druckprofile und Belastungstests sind **Startwerte, DIE NOCH PHYSISCH ZU PRÜFEN SIND**.",
    d_mont="Bebilderte Montage, Stückliste, Spiel und Belastungstests", d_imp="Material, Ausrichtung und anfängliche Druckprofile", d_cal="Kalibrierung Anycubic Kobra S1 und Bambu Lab",
    pend="⚠ PHYSISCHE PRÜFUNG AUSSTEHEND", geo="Basiert auf der Geometrie von `feat/v5-radio-180` (2497ad7). Bei Geometrieänderung mit `src/render_guia.py` neu erzeugen. Die Clip-Maße sind geschätzt, nicht gemessen.",
    figs=["Seitenansicht mit Maßen (X zeigt zum Griff)", "Stirnansicht (Griffende)", "Draufsicht der Clip-Platte: %s mm bei %s" % (N["placa"], N["ang"]),
          "Explosionsansicht und nummerierte Schritte ①–④ (Mutter von Z− einsetzen)", "Schnitte A-A (Tunnel) und B-B (Mutterntasche)", "Druckausrichtungen im Vergleich", "Clip-Einschub (v3 von +V; v5 von −V)"],
    h_fig="Grafiken", h_bom="Stückliste (BOM)", bom_h=["Nr.", "Menge", "Teil", "Maß / Spezifikation", "Hinweis"],
    bom=[("1", "1", "Gedruckter Griff v5 (`stl/v5/*uvk5v3.stl`)", "Hüllmaß %s mm" % N["bbox"], "PETG empfohlen"),
         ("2", "1", "Sechskantmutter 1/4\"-20 UNC", "Schlüsselweite 11.1 mm, Dicke 5.6 mm", "Tasche SW %s × %s mm" % (N["af"], N["esp"])),
         ("3", "1", "Ausleger (nicht enthalten)", "Ø%s mm, Tunnel %s mm (Nennspiel %s mm je Seite)" % (N["pluma"], N["tunel"], N["jgo"]), "Echten Ausleger messen"),
         ("4", "0–1", "Stativ-Schnellwechselplatte/-schraube (optional)", "1/4\"-20", "Nach Bedarf"),
         ("5", "0–1", "Duplexer und EVA-Streifen (optional)", "—", "Je nach Funkgerät")],
    nobear="Dieses Design hat **keine Lager oder Wellen**; einziges Beschlagteil ist die 1/4\"-20-Mutter.",
    h_ord="Montagereihenfolge", steps=["Teil prüfen: Grate in Tunnel und Sechskanttasche entfernen.", "Mutter von der Z−-Seite in die Tasche einsetzen (%s mm Haut zum Griffende)." % N["piel"], "Ausleger Ø%s mm durch den %s-mm-Tunnel schieben." % (N["pluma"], N["tunel"]), "Clip auf der Platte (%s bei %s) montieren und Funkgerät sichern." % (N["placa"], N["ang"])],
    h_hol="Spiel messen und anpassen (mechanische Passung)", hol=[
        "`stl/calibracion/prueba_holguras.stl` (%s mm) mit dem ENDGÜLTIGEN Profil und demselben Filament drucken." % N["cupon"],
        "Reihe 1: Vierkantlöcher 15.1–15.9 mm für den Ausleger. Reihe 2: Sechskanttaschen SW 11.1–11.9 mm. Reihe 3: Schlitze 6.0–8.0 mm. Punkte 1–5 kennzeichnen die Größe.",
        "Mit Messschieber (0.02 mm) nach 24 h Abkühlen messen; mit echtem Ausleger und echter Mutter testen.",
        "Das Loch wählen, das mit Fingerdruck ohne sichtbares Spiel gleitet (Startziel 0.2–0.3 mm je Seite, Test ausstehend).",
        "Mit XY-Lochkompensation des Slicers (falls vorhanden) oder dem Modell korrigieren; nicht über den Fluss anpassen."],
    h_car="Festigkeitsprüfung (vorsichtige Tests)", car=[
        "Funkgerät mit Zubehör wiegen: reale Masse M (vorab unbekannt).",
        "Prüflast = 2 × M, in Stufen von 25 %, 50 % und 100 % dieser Last, je 60 s, Ballast über niedriger, geschützter Fläche.",
        "Nach jeder Stufe prüfen; bei Rissen, Weißbruch oder Verformung > 0.3 mm abbrechen.",
        "Praktisches Verfahren, keine Zertifizierung. Lasten durch M begründet; nie über Personen oder wertvollen Geräten."],
    h_mat="Material und Ausrichtung", mat_h=["Option", "Wann", "Status"],
    mat=[("PETG (empfohlen)", "Allgemein, zäh; gute Schichthaftung", "Startwert, Test ausstehend"),
         ("ASA", "Längerer Außeneinsatz/UV; Belüftung und Einhausung nötig", "Startwert, Test ausstehend"),
         ("PLA", "Nicht empfohlen: Kriechen/Verformung bei Wärme", "—")],
    ori_h=["Bettfläche", "Höhe", "Kontakt", "Überhang >45°", "Kommentar"],
    ori_c=["Empfohlen: Tunnel vertikal; Schichten als Ringe um den Ausleger; Mutterlast in Schichtebene; Brim nutzen", "Vertikale Mutterachse: Zug quer zu den Schichten (schwach)", "Alternative"],
    h_prof="Anfängliche Profile", prof_h=["Parameter", "Startwert"], prof=[("Schichthöhe", "0.20 mm"), ("Perimeter", "4"), ("Füllung", "Gyroid 40 %"), ("Brim", "5 mm (Option A)"), ("Maßkorrektur", "0 bis zur Messung des Prüfkörpers")],
    prof_note="Alles sind Startwerte, **physische Prüfung ausstehend**; keine universellen Parameter: den auf der Spule angegebenen Temperaturbereich verwenden.",
    h_sep="Druckerkalibrierung (getrennt von mechanischer Passung)", sep="Die Schritte hier kalibrieren den **Drucker**. Die Spielanpassung der Montage steht in `MONTAJE_ILUSTRADO.md`.",
    h_k="Anycubic Kobra S1", k=[
        "Vor dem ersten Einschalten Plattform/Heizbett entriegeln; der erste Start führt Selbsttest, Vibrationskompensation und Auto-Leveling aus (Schnellstartanleitung).",
        "Bett 5–10 min vorheizen und Platte mit Wasser/Spülmittel reinigen (Erste-Schicht-Anleitung).",
        "Bei «falscher Schicht» an einer Ecke: Bettschraube dieser Ecke 1/4 Umdrehung gegen den Uhrzeigersinn mit S2.0-Inbusschlüssel drehen, neu leveln und prüfen.",
        "Offizielle Daten: Bauraum 250³ mm, Düse 0.4, max. 320 °C Düse, 120 °C Bett, Umgebung 8–40 °C (bei <10 °C Bett ≈70 °C). Unterstützt PLA, PETG, ABS, ASA, TPU 95A und PC/PA/CF/GF.",
        "Temperatur: vom Bereich des Filamentherstellers und Slicer-Profil ausgehen; mit eigenen Türmen/Tests verfeinern.",
        "Fluss: mit der Slicer-Funktion kalibrieren; Anycubic Slicer Next basiert auf OrcaSlicer — prüfen, ob Ihre Version Fluss-Kalibrierung oder XY-Lochkompensation bietet.",
        "Wartung: Z-Spindel etwa alle 3 Monate (Fett), Y-Stangen monatlich."],
    h_b="Bambu Lab", b0="Das genaue Modell ist unbekannt: gemeinsame Schritte plus Varianten, die die offizielle Dokumentation stützt.",
    b=["Automatische Kalibrierung (Leveling, Vibrationskompensation, Flow Dynamics) am Display, in Bambu Studio (Geräte → Kalibrieren) oder Bambu Handy.",
       "Flow Dynamics (PA) unzuverlässig bei feuchtem/transparentem Filament, schmutziger Platte, verschlissener Düse oder TPU.",
       "Flussrate: nach den anderen Kalibrierungen kalibrieren.",
       "XY-Loch-/Konturkompensation: Prozess → Qualität → Präzision; Lochdurchmesser ändert sich um das 2-Fache des Wertes; mit Messschieber und gleichem Filament/Profil iterieren.",
       "Erste Schicht: Anleitung der Serie (X1, H2, P2S, X2D, A2L…); PETG und PETG-CF: Kompatibilität beachten (CF braucht gehärtete Düse)."],
    bser_h=["Serie", "Menüpfad"], bser=[("X1", "Control → Calibrate"), ("P1", "Settings → Calibration"), ("A", "Settings → Maintenance → Calibration"), ("H2 / P2S / X2D", "Settings → Calibration → Print Calibration")],
    h_src="Offizielle Quellen", h_lic="Lizenz und Namensnennung", lic="CC-Lizenz des Repositories (`LICENSE`, Bricohams). Der Pastamatic-Umspuler behält seine ursprüngliche Urheberschaft; seine Lizenz ist nicht verifiziert und wird hier nicht veröffentlicht.",
)

L["fr"] = dict(
    title="Poignée SpaceQuad v5 — Guide de montage illustré",
    idx_title="Guides SpaceQuad (multilingue)", idx_intro="Documentation cohérente en 5 langues. Tous les profils d'impression et essais de charge sont des **valeurs initiales EN ATTENTE D'ESSAI PHYSIQUE**.",
    d_mont="Montage illustré, nomenclature, jeux et essais de charge", d_imp="Matériau, orientation et profils d'impression initiaux", d_cal="Calibration Anycubic Kobra S1 et Bambu Lab",
    pend="⚠ ESSAI PHYSIQUE EN ATTENTE", geo="Basé sur la géométrie de `feat/v5-radio-180` (2497ad7). Si la géométrie change, régénérer avec `src/render_guia.py`. Les dimensions du clip sont estimées, non mesurées.",
    figs=["Vue latérale cotée (X pointe vers la prise)", "Vue de bout (culasse)", "Plan de la plaque du clip : %s mm à %s" % (N["placa"], N["ang"]),
          "Vue éclatée et étapes numérotées ①–④ (l'écrou entre par Z−)", "Coupes A-A (tunnel) et B-B (logement d'écrou)", "Orientations d'impression comparées", "Insertion du clip (v3 par +V ; v5 par −V)"],
    h_fig="Graphiques", h_bom="Nomenclature (BOM)", bom_h=["N°", "Qté", "Élément", "Dimension / spécification", "Remarque"],
    bom=[("1", "1", "Poignée imprimée v5 (`stl/v5/*uvk5v3.stl`)", "Encombrement %s mm" % N["bbox"], "PETG recommandé"),
         ("2", "1", "Écrou hexagonal 1/4\"-20 UNC", "Sur plats 11.1 mm, épaisseur 5.6 mm", "Logement SP %s × %s mm" % (N["af"], N["esp"])),
         ("3", "1", "Mât / boom (non inclus)", "Ø%s mm, tunnel %s mm (jeu nominal %s mm par côté)" % (N["pluma"], N["tunel"], N["jgo"]), "Mesurer le mât réel"),
         ("4", "0–1", "Plaque/vis de déclenchement rapide trépied (option)", "1/4\"-20", "Selon usage"),
         ("5", "0–1", "Duplexeur et bande EVA (options)", "—", "Selon la radio")],
    nobear="Cette conception **n'a ni roulements ni arbres** ; la seule visserie est l'écrou 1/4\"-20.",
    h_ord="Ordre de montage", steps=["Vérifier la pièce : ébavurer le tunnel et le logement hexagonal.", "Insérer l'écrou côté Z− dans le logement (peau de %s mm vers la culasse)." % N["piel"], "Faire glisser le mât Ø%s mm dans le tunnel de %s mm." % (N["pluma"], N["tunel"]), "Monter le clip sur la plaque (%s à %s) et fixer la radio." % (N["placa"], N["ang"])],
    h_hol="Mesurer et ajuster les jeux (ajustement mécanique)", hol=[
        "Imprimer `stl/calibracion/prueba_holguras.stl` (%s mm) avec le profil FINAL et le même filament." % N["cupon"],
        "Rangée 1 : trous carrés 15.1–15.9 mm pour le mât. Rangée 2 : logements hexagonaux SP 11.1–11.9 mm. Rangée 3 : fentes 6.0–8.0 mm. Les alvéoles 1–5 indiquent la taille.",
        "Mesurer au pied à coulisse (0.02 mm) après 24 h de refroidissement ; essayer avec le vrai mât et le vrai écrou.",
        "Choisir le trou qui glisse à la pression du doigt sans jeu visible (objectif initial 0.2–0.3 mm par côté, à valider).",
        "Corriger via la compensation XY des trous du slicer (si disponible) ou le modèle ; ne pas régler l'ajustement avec le débit."],
    h_car="Vérification de résistance (essais prudents)", car=[
        "Peser la radio avec accessoires : masse réelle M (inconnue a priori).",
        "Charge d'épreuve = 2 × M, appliquée par paliers de 25 %, 50 % et 100 % de cette charge, 60 s chacun, lest au-dessus d'une surface basse et protégée.",
        "Inspecter après chaque palier ; arrêter en cas de fissures, blanchiment ou déformation > 0.3 mm.",
        "Procédure pratique, pas une certification. Charges justifiées par M ; jamais au-dessus d'une personne ou d'un matériel de valeur."],
    h_mat="Matériau et orientation", mat_h=["Option", "Quand", "Statut"],
    mat=[("PETG (recommandé)", "Usage général, ténacité ; bonne adhérence entre couches", "initial, essai en attente"),
         ("ASA", "Extérieur prolongé/UV ; ventilation et caisson requis", "initial, essai en attente"),
         ("PLA", "Non recommandé : fluage/déformation à la chaleur", "—")],
    ori_h=["Face sur le plateau", "Hauteur", "Contact", "Surplomb >45°", "Commentaire"],
    ori_c=["Recommandée : tunnel vertical ; couches en cerceaux autour du mât ; charge de l'écrou dans le plan des couches ; utiliser un brim", "Axe d'écrou vertical : traction perpendiculaire aux couches (faible)", "Alternative"],
    h_prof="Profils initiaux", prof_h=["Paramètre", "Valeur initiale"], prof=[("Hauteur de couche", "0.20 mm"), ("Périmètres", "4"), ("Remplissage", "gyroïde 40 %"), ("Brim", "5 mm (option A)"), ("Ajustement dimensionnel", "0 jusqu'à mesure de l'éprouvette")],
    prof_note="Toutes sont des valeurs initiales **en attente d'essai physique** ; pas de paramètres universels : utiliser la plage de température imprimée sur la bobine.",
    h_sep="Calibration de l'imprimante (séparée de l'ajustement mécanique)", sep="Les étapes ici calibrent l'**imprimante**. L'ajustement des jeux du montage est dans `MONTAJE_ILUSTRADO.md`.",
    h_k="Anycubic Kobra S1", k=[
        "Avant la première mise sous tension, déverrouiller la plateforme/le plateau chauffant ; le premier démarrage lance auto-test, compensation des vibrations et nivellement auto (guide de démarrage rapide).",
        "Préchauffer le plateau 5–10 min et laver la plaque à l'eau/détergent (guide de première couche).",
        "En cas de « fausse couche » dans un coin : tourner la vis du plateau de ce coin d'un quart de tour dans le sens antihoraire avec une clé Allen S2.0, renivelez et revérifier.",
        "Données officielles : volume 250³ mm, buse 0.4, max 320 °C buse, 120 °C plateau, ambiance 8–40 °C (si <10 °C, plateau ≈70 °C). Prend en charge PLA, PETG, ABS, ASA, TPU 95A et PC/PA/CF/GF.",
        "Température : partir de la plage du fabricant du filament et du profil du slicer ; affiner par vos propres tours/essais.",
        "Débit : calibrer avec la fonction du slicer ; Anycubic Slicer Next repose sur OrcaSlicer — vérifier si votre version propose calibration du débit ou compensation XY des trous.",
        "Entretien : vis-mère Z environ tous les 3 mois (graisse), tiges Y chaque mois."],
    h_b="Bambu Lab", b0="Le modèle exact est inconnu : étapes communes et variantes appuyées par la documentation officielle.",
    b=["Calibration automatique (nivellement, compensation des vibrations, dynamique du flux) depuis l'écran, Bambu Studio (Appareils → Calibrer) ou Bambu Handy.",
       "Flow Dynamics (PA) peu fiable avec filament humide/transparent, plaque sale, buse usée ou TPU.",
       "Débit : calibrer après les autres calibrations.",
       "Compensation XY des trous/contours : Processus → Qualité → Précision ; le diamètre du trou change de 2× la valeur ; itérer au pied à coulisse avec le même filament/profil.",
       "Première couche : voir le guide de la série (X1, H2, P2S, X2D, A2L…) ; PETG et PETG-CF : voir compatibilité (CF exige une buse durcie)."],
    bser_h=["Série", "Chemin de menu"], bser=[("X1", "Control → Calibrate"), ("P1", "Settings → Calibration"), ("A", "Settings → Maintenance → Calibration"), ("H2 / P2S / X2D", "Settings → Calibration → Print Calibration")],
    h_src="Sources officielles", h_lic="Licence et attribution", lic="Licence CC du dépôt (`LICENSE`, Bricohams). Le rebobineur Pastamatic conserve sa paternité d'origine ; sa licence n'est pas vérifiée et il n'est pas publié ici.",
)

L["it"] = dict(
    title="Impugnatura SpaceQuad v5 — Guida di montaggio illustrata",
    idx_title="Guide SpaceQuad (multilingue)", idx_intro="Documentazione coerente in 5 lingue. Tutti i profili di stampa e le prove di carico sono **valori iniziali IN ATTESA DI PROVA FISICA**.",
    d_mont="Montaggio illustrato, distinta, giochi e prove di carico", d_imp="Materiale, orientamento e profili di stampa iniziali", d_cal="Calibrazione Anycubic Kobra S1 e Bambu Lab",
    pend="⚠ PROVA FISICA IN SOSPESO", geo="Basato sulla geometria di `feat/v5-radio-180` (2497ad7). Se la geometria cambia, rigenerare con `src/render_guia.py`. Le dimensioni della clip sono stimate, non misurate.",
    figs=["Vista laterale quotata (X punta verso l'impugnatura)", "Vista di testa (culatta)", "Pianta della piastra della clip: %s mm a %s" % (N["placa"], N["ang"]),
          "Vista esplosa e passi numerati ①–④ (il dado entra da Z−)", "Sezioni A-A (tunnel) e B-B (sede del dado)", "Orientamenti di stampa a confronto", "Inserimento della clip (v3 da +V; v5 da −V)"],
    h_fig="Grafici", h_bom="Distinta base (BOM)", bom_h=["N.", "Q.tà", "Elemento", "Misura / specifica", "Nota"],
    bom=[("1", "1", "Impugnatura stampata v5 (`stl/v5/*uvk5v3.stl`)", "Ingombro %s mm" % N["bbox"], "PETG consigliato"),
         ("2", "1", "Dado esagonale 1/4\"-20 UNC", "Chiave 11.1 mm, spessore 5.6 mm", "Sede CH %s × %s mm" % (N["af"], N["esp"])),
         ("3", "1", "Asta / boom (non inclusa)", "Ø%s mm, tunnel %s mm (gioco nominale %s mm per lato)" % (N["pluma"], N["tunel"], N["jgo"]), "Misurare l'asta reale"),
         ("4", "0–1", "Piastra/vite a sgancio rapido per treppiede (opzionale)", "1/4\"-20", "Secondo l'uso"),
         ("5", "0–1", "Duplexer e striscia EVA (opzionali)", "—", "Secondo la radio")],
    nobear="Questo progetto **non ha cuscinetti né alberi**; l'unica minuteria è il dado 1/4\"-20.",
    h_ord="Ordine di montaggio", steps=["Controllare il pezzo: sbavare tunnel e sede esagonale.", "Inserire il dado dal lato Z− nella sede (pelle di %s mm verso la culatta)." % N["piel"], "Far scorrere l'asta Ø%s mm nel tunnel di %s mm." % (N["pluma"], N["tunel"]), "Montare la clip sulla piastra (%s a %s) e fissare la radio." % (N["placa"], N["ang"])],
    h_hol="Misurare e regolare i giochi (accoppiamento meccanico)", hol=[
        "Stampare `stl/calibracion/prueba_holguras.stl` (%s mm) con il profilo FINALE e lo stesso filamento." % N["cupon"],
        "Fila 1: fori quadrati 15.1–15.9 mm per l'asta. Fila 2: sedi esagonali CH 11.1–11.9 mm. Fila 3: asole 6.0–8.0 mm. Le fossette 1–5 indicano la misura.",
        "Misurare con calibro (0.02 mm) dopo 24 h di raffreddamento; provare con asta e dado reali.",
        "Scegliere il foro che scorre con pressione delle dita senza gioco visibile (obiettivo iniziale 0.2–0.3 mm per lato, da verificare).",
        "Correggere con la compensazione XY dei fori dello slicer (se presente) o col modello; non regolare l'accoppiamento col flusso."],
    h_car="Verifica di resistenza (prove prudenti)", car=[
        "Pesare la radio con accessori: massa reale M (non nota a priori).",
        "Carico di prova = 2 × M, applicato a gradini del 25 %, 50 % e 100 % di tale carico, 60 s ciascuno, zavorra su superficie bassa e protetta.",
        "Ispezionare dopo ogni gradino; fermarsi con crepe, sbiancamento o deformazione > 0.3 mm.",
        "Procedura pratica, non una certificazione. Carichi giustificati da M; mai sopra persone o apparecchi di valore."],
    h_mat="Materiale e orientamento", mat_h=["Opzione", "Quando", "Stato"],
    mat=[("PETG (consigliato)", "Uso generale, tenacità; buona adesione tra strati", "iniziale, prova in sospeso"),
         ("ASA", "Esterno prolungato/UV; servono ventilazione e camera chiusa", "iniziale, prova in sospeso"),
         ("PLA", "Sconsigliato: scorrimento/deformazione col calore", "—")],
    ori_h=["Faccia sul piatto", "Altezza", "Contatto", "Sporgenza >45°", "Commento"],
    ori_c=["Consigliata: tunnel verticale; strati ad anello attorno all'asta; carico del dado nel piano degli strati; usare brim", "Asse del dado verticale: trazione perpendicolare agli strati (debole)", "Alternativa"],
    h_prof="Profili iniziali", prof_h=["Parametro", "Valore iniziale"], prof=[("Altezza strato", "0.20 mm"), ("Perimetri", "4"), ("Riempimento", "gyroid 40 %"), ("Brim", "5 mm (opzione A)"), ("Correzione dimensionale", "0 fino alla misura del provino")],
    prof_note="Sono tutti valori iniziali **in attesa di prova fisica**; nessun parametro universale: usare l'intervallo di temperatura stampato sulla bobina.",
    h_sep="Calibrazione della stampante (separata dall'accoppiamento meccanico)", sep="I passi qui calibrano la **stampante**. La regolazione dei giochi del montaggio è in `MONTAJE_ILUSTRADO.md`.",
    h_k="Anycubic Kobra S1", k=[
        "Prima del primo avvio sbloccare piattaforma/piatto riscaldato; il primo avvio esegue autotest, compensazione vibrazioni e autolivellamento (guida rapida).",
        "Preriscaldare il piatto 5–10 min e lavare la piastra con acqua/detergente (guida al primo strato).",
        "Se compare un «falso strato» in un angolo: ruotare la vite del piatto di quell'angolo di 1/4 di giro in senso antiorario con chiave Allen S2.0, rilivellare e ricontrollare.",
        "Dati ufficiali: volume 250³ mm, ugello 0.4, max 320 °C ugello, 120 °C piatto, ambiente 8–40 °C (se <10 °C, piatto ≈70 °C). Supporta PLA, PETG, ABS, ASA, TPU 95A e PC/PA/CF/GF.",
        "Temperatura: partire dall'intervallo del produttore del filamento e dal profilo dello slicer; affinare con torri/prove proprie.",
        "Flusso: calibrare con la funzione dello slicer; Anycubic Slicer Next si basa su OrcaSlicer — verificare se la vostra versione offre calibrazione del flusso o compensazione XY dei fori.",
        "Manutenzione: vite di guida Z circa ogni 3 mesi (grasso), aste Y ogni mese."],
    h_b="Bambu Lab", b0="Il modello esatto è ignoto: passi comuni e varianti supportate dalla documentazione ufficiale.",
    b=["Calibrazione automatica (livellamento, compensazione vibrazioni, flow dynamics) dallo schermo, Bambu Studio (Dispositivi → Calibra) o Bambu Handy.",
       "Flow Dynamics (PA) inaffidabile con filamento umido/trasparente, piastra sporca, ugello usurato o TPU.",
       "Flow rate: calibrare dopo le altre calibrazioni.",
       "Compensazione XY fori/contorni: Processo → Qualità → Precisione; il diametro del foro cambia di 2× il valore; iterare con calibro e stesso filamento/profilo.",
       "Primo strato: vedere la guida della serie (X1, H2, P2S, X2D, A2L…); PETG e PETG-CF: vedere compatibilità (CF richiede ugello indurito)."],
    bser_h=["Serie", "Percorso menu"], bser=[("X1", "Control → Calibrate"), ("P1", "Settings → Calibration"), ("A", "Settings → Maintenance → Calibration"), ("H2 / P2S / X2D", "Settings → Calibration → Print Calibration")],
    h_src="Fonti ufficiali", h_lic="Licenza e attribuzione", lic="Licenza CC del repository (`LICENSE`, Bricohams). Il riavvolgitore Pastamatic mantiene la paternità originale; la sua licenza non è verificata e non è pubblicato qui.",
)


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def nav(lang):
    return " · ".join("**%s**" % NAMES[l] if l == lang else "[%s](../%s/README.md)" % (NAMES[l], l) for l in LANGS)


def doc_mont(lang, t):
    o = ["# " + t["title"], "", nav(lang), "", "> " + t["geo"], "", "## " + t["h_fig"], ""]
    for f, c in zip(FIGS, t["figs"]):
        o += ["![%s](%s%s.png)" % (c, IMG, f), "*%s*" % c, ""]
    o += ["## " + t["h_bom"], "", table(t["bom_h"], [list(r) for r in t["bom"]]), "", t["nobear"], "",
          "## " + t["h_ord"], ""] + ["%d. %s" % (i + 1, s) for i, s in enumerate(t["steps"])]
    o += ["", "## " + t["h_hol"], "", "> " + t["pend"], ""] + ["%d. %s" % (i + 1, s) for i, s in enumerate(t["hol"])]
    o += ["", "## " + t["h_car"], "", "> " + t["pend"], ""] + ["%d. %s" % (i + 1, s) for i, s in enumerate(t["car"])]
    o += ["", "## " + t["h_lic"], "", t["lic"], ""]
    return "\n".join(o)


def doc_imp(lang, t):
    import json
    ori = json.load(open(os.path.join(ROOT, "docs", "img", "guia", "orientaciones.json"), encoding="utf-8"))
    rows = ori if isinstance(ori, list) else ori.get("orientaciones", ori)
    metr = [("Y−", "95.6", "355", "7688"), ("X+", "195.2", "1284", "10144"), ("Z+", "79.0", "711", "11941")]
    o = ["# " + t["h_mat"] + " — SpaceQuad v5", "", nav(lang), "", "> " + t["pend"], "", "## " + t["h_mat"], "",
         table(t["mat_h"], [list(r) for r in t["mat"]]), "",
         table(t["ori_h"], [[m[0], m[1] + " mm", m[2] + " mm²", m[3] + " mm²", c] for m, c in zip(metr, t["ori_c"])]), "",
         "![%s](%sfig04_orientacion_impresion.png)" % (t["figs"][5], IMG), "",
         "## " + t["h_prof"], "", table(t["prof_h"], [list(r) for r in t["prof"]]), "", t["prof_note"], "",
         "- " + SRC["b_petg"], ""]
    return "\n".join(o)


def doc_cal(lang, t):
    o = ["# " + t["d_cal"], "", nav(lang), "", "> " + t["pend"], "", "## " + t["h_sep"], "", t["sep"], "",
         "## " + t["h_k"], ""] + ["%d. %s" % (i + 1, s) for i, s in enumerate(t["k"])]
    o += ["", "## " + t["h_b"], "", t["b0"], ""] + ["%d. %s" % (i + 1, s) for i, s in enumerate(t["b"])]
    o += ["", table(t["bser_h"], [list(r) for r in t["bser"]]), "", "## " + t["h_src"], ""]
    o += ["- <%s>" % u for u in SRC.values()]
    o += [""]
    return "\n".join(o)


def doc_idx(lang, t):
    o = ["# " + t["idx_title"], "", nav(lang), "", t["idx_intro"], "",
         "- [MONTAJE_ILUSTRADO.md](MONTAJE_ILUSTRADO.md) — " + t["d_mont"],
         "- [IMPRESION.md](IMPRESION.md) — " + t["d_imp"],
         "- [CALIBRACION.md](CALIBRACION.md) — " + t["d_cal"], ""]
    return "\n".join(o)


def main():
    for lang in LANGS:
        t = L[lang]
        d = os.path.join(OUT, lang)
        os.makedirs(d, exist_ok=True)
        for name, fn in (("README.md", doc_idx), ("MONTAJE_ILUSTRADO.md", doc_mont), ("IMPRESION.md", doc_imp), ("CALIBRACION.md", doc_cal)):
            with open(os.path.join(d, name), "w", encoding="utf-8", newline="\n") as f:
                f.write(fn(lang, t))
    print("ok", len(LANGS) * 4)


if __name__ == "__main__":
    main()
