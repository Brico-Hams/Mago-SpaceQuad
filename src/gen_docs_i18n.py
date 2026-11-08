"""Genera docs/i18n/{es,en,de,fr,it}/ desde un unico juego de cifras (coherencia entre idiomas)."""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "docs", "i18n")
LANGS = ["es", "en", "de", "fr", "it"]
NAMES = {"es": "Español", "en": "English", "de": "Deutsch", "fr": "Français", "it": "Italiano"}
IMG = "../../img/guia/v6/"
FIGS = ["fig01a_vista_lateral", "fig01b_vista_extremo", "fig01c_planta_placa", "fig02_explosionado",
        "fig03_cortes", "fig04_orientacion_impresion", "fig05_insercion_clip"]
V6_STL = {"uvk5v3": "stl/v6/mango_spacequad_v6_uvk5v3.stl", "rt950pro": "stl/v6/mango_spacequad_v6_rt950pro.stl"}


def medidas_stl(ruta):
    """Envolvente (mm) y volumen (mm³) del STL v6 si existe; '—' si aún no se ha generado."""
    p = os.path.join(ROOT, ruta)
    if not os.path.isfile(p):
        return "—", "—"
    import trimesh
    m = trimesh.load(p)
    return " × ".join("%.1f" % e for e in m.extents), "%d" % round(abs(m.volume))


BBOX_UV = medidas_stl(V6_STL["uvk5v3"])[0]

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
N = dict(bbox=BBOX_UV, tunel="15.5 × 15.5", pluma="15", jgo="0.25",
         af="11.4", esp="5.9", tal="6.6", piel="2.0", placa="55 × 48 × 4", ang="20°",
         gus="47", libre="7", rec="40", cupon="124 × 92 × 8", viga="14 × 7.5", rampa="36")

L = {}
L["es"] = dict(
    title="Mango SpaceQuad v6.2 — Guía de montaje ilustrada",
    idx_title="Guías SpaceQuad (multiidioma)", idx_intro="Documentación coherente en 5 idiomas. Todos los perfiles de impresión y pruebas de carga son **valores iniciales PENDIENTES DE PRUEBA FÍSICA**.",
    d_mont="Montaje ilustrado, BOM, holguras y pruebas de carga", d_imp="Material, orientación y perfiles iniciales de impresión", d_cal="Calibración Anycubic Kobra S1 y Bambu Lab",
    pend="⚠ PENDIENTE DE PRUEBA FÍSICA",     geo="Basado en la geometría v6.2 (posición D) de `stl/v6/`. Si cambia la geometría, regenerar con `src/render_guia.py`. Solo CAD: las dimensiones del clip y de cada radio son estimadas, no medidas, y no hay prueba de carga.",
        figs=["Vista lateral con cotas (X apunta al agarre; radio en el lado −U)", "Vista de extremo (culata)", "Planta de la placa del clip y de la viga: %s mm a %s" % (N["placa"], N["ang"]),
              "Explosionado y pasos numerados ①–④ (la tuerca entra a presión desde Z−)", "Cortes A-A (túnel) y B-B (alojamiento de tuerca, piel de 2 mm)", "Orientaciones de impresión comparadas", "Inserción del clip (posición D: por el borde libre alto, paralelo a la placa)"],
    h_fig="Gráficos", h_bom="Lista de materiales (BOM)", bom_h=["Nº", "Cant.", "Elemento", "Medida / especificación", "Nota"],
    bom=[("1", "1", "Mango impreso v6.2 (`stl/v6/*_v6_uvk5v3.stl` o `*_v6_rt950pro.stl`)", "Envolvente %s mm (UV-K5 V3)" % N["bbox"], "PETG recomendado"),
         ("2", "1", "Tuerca hexagonal 1/4\"-20 UNC", "Entre caras 11.1 mm, espesor 5.6 mm", "Alojamiento AF %s × %s mm" % (N["af"], N["esp"])),
         ("3", "1", "Pluma / boom (no incluida)", "Ø%s mm, túnel %s mm (juego nominal %s mm por lado)" % (N["pluma"], N["tunel"], N["jgo"]), "Medir la pluma real"),
         ("4", "0–1", "Placa/tornillo de zapata de trípode (opcional)", "1/4\"-20", "Según uso"),
         ("5", "0–1", "Duplexor y tira EVA (opcionales)", "—", "Según radio")],
    nobear="Este diseño **no lleva rodamientos ni ejes**; la única tornillería es la tuerca 1/4\"-20.",
    h_ord="Orden de montaje", steps=["Verificar la pieza: limpiar rebabas del túnel y del alojamiento hexagonal.", "Insertar la tuerca a presión por el canal lateral del lado Z−, pasando los labios de retención (piel de %s mm hacia la culata; un tornillo de 6 mm o más engrana unos 4 mm)." % N["piel"], "Deslizar la pluma Ø%s mm por el túnel de %s mm." % (N["pluma"], N["tunel"]), "Introducir la lengua del clip por el borde libre alto de la placa (%s a %s), paralela a ella, y fijar la radio en el lado −U." % (N["placa"], N["ang"])],
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
    h_prof="Perfiles iniciales", prof_h=["Parámetro", "Valor inicial"], prof=[("Altura de capa", "0.20 mm"), ("Perímetros", "4"), ("Relleno", "gyroid 40 % (60–100 % o paredes extra en la viga y la zona del trípode)"), ("Brim", "5 mm (opción A)"), ("Soportes", "bajo la placa y la viga"), ("Ajuste dimensional", "0 hasta medir el cupón")],
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
    title="SpaceQuad v6.2 handle — Illustrated assembly guide",
    idx_title="SpaceQuad guides (multilingual)", idx_intro="Consistent documentation in 5 languages. All print profiles and load tests are **initial values PENDING PHYSICAL TESTING**.",
    d_mont="Illustrated assembly, BOM, clearances and load tests", d_imp="Material, orientation and initial print profiles", d_cal="Anycubic Kobra S1 and Bambu Lab calibration",
    pend="⚠ PENDING PHYSICAL TEST",     geo="Based on the v6.2 geometry (position D) in `stl/v6/`. If geometry changes, regenerate with `src/render_guia.py`. CAD only: clip and radio dimensions are estimated, not measured, and there is no load test.",
        figs=["Side view with dimensions (X points to the grip; radio on the −U side)", "End view (butt face)", "Clip plate and beam plan: %s mm at %s" % (N["placa"], N["ang"]),
              "Exploded view and numbered steps ①–④ (nut snaps in from Z−)", "Sections A-A (tunnel) and B-B (nut slot, 2 mm skin)", "Print orientations compared", "Clip insertion (position D: from the high free edge, parallel to the plate)"],
    h_fig="Graphics", h_bom="Bill of materials (BOM)", bom_h=["No.", "Qty", "Item", "Size / specification", "Note"],
    bom=[("1", "1", "Printed handle v6.2 (`stl/v6/*_v6_uvk5v3.stl` or `*_v6_rt950pro.stl`)", "Envelope %s mm (UV-K5 V3)" % N["bbox"], "PETG recommended"),
         ("2", "1", "Hex nut 1/4\"-20 UNC", "Across flats 11.1 mm, thickness 5.6 mm", "Pocket AF %s × %s mm" % (N["af"], N["esp"])),
         ("3", "1", "Boom (not included)", "Ø%s mm, tunnel %s mm (nominal clearance %s mm per side)" % (N["pluma"], N["tunel"], N["jgo"]), "Measure the real boom"),
         ("4", "0–1", "Tripod quick-release plate/screw (optional)", "1/4\"-20", "As needed"),
         ("5", "0–1", "Duplexer and EVA strip (optional)", "—", "Per radio")],
    nobear="This design has **no bearings or shafts**; the only hardware is the 1/4\"-20 nut.",
    h_ord="Assembly order", steps=["Check the part: remove burrs from the tunnel and hex pocket.", "Snap the nut in through the side channel on the Z− side, past the retention lips (%s mm skin toward the butt face; a screw of 6 mm or more engages about 4 mm)." % N["piel"], "Slide the Ø%s mm boom through the %s mm tunnel." % (N["pluma"], N["tunel"]), "Insert the clip tongue through the high free edge of the plate (%s at %s), parallel to it, and secure the radio on the −U side." % (N["placa"], N["ang"])],
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
    h_prof="Initial profiles", prof_h=["Parameter", "Initial value"], prof=[("Layer height", "0.20 mm"), ("Perimeters", "4"), ("Infill", "gyroid 40 % (60–100 % or extra walls in the beam and tripod zone)"), ("Brim", "5 mm (option A)"), ("Supports", "under the plate and the beam"), ("Dimensional adjustment", "0 until the coupon is measured")],
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
    title="SpaceQuad-Griff v6.2 — Bebilderte Montageanleitung",
    idx_title="SpaceQuad-Anleitungen (mehrsprachig)", idx_intro="Konsistente Dokumentation in 5 Sprachen. Alle Druckprofile und Belastungstests sind **Startwerte, DIE NOCH PHYSISCH ZU PRÜFEN SIND**.",
    d_mont="Bebilderte Montage, Stückliste, Spiel und Belastungstests", d_imp="Material, Ausrichtung und anfängliche Druckprofile", d_cal="Kalibrierung Anycubic Kobra S1 und Bambu Lab",
    pend="⚠ PHYSISCHE PRÜFUNG AUSSTEHEND",     geo="Basiert auf der Geometrie v6.2 (Position D) in `stl/v6/`. Bei Geometrieänderung mit `src/render_guia.py` neu erzeugen. Nur CAD: Die Maße von Clip und Funkgerät sind geschätzt, nicht gemessen; es gibt keinen Belastungstest.",
        figs=["Seitenansicht mit Maßen (X zeigt zum Griff; Funkgerät auf der −U-Seite)", "Stirnansicht (Griffende)", "Draufsicht der Clip-Platte und des Trägers: %s mm bei %s" % (N["placa"], N["ang"]),
              "Explosionsansicht und nummerierte Schritte ①–④ (Mutter rastet von Z− ein)", "Schnitte A-A (Tunnel) und B-B (Mutterntasche, 2 mm Haut)", "Druckausrichtungen im Vergleich", "Clip-Einschub (Position D: am oberen freien Rand, parallel zur Platte)"],
    h_fig="Grafiken", h_bom="Stückliste (BOM)", bom_h=["Nr.", "Menge", "Teil", "Maß / Spezifikation", "Hinweis"],
    bom=[("1", "1", "Gedruckter Griff v6.2 (`stl/v6/*_v6_uvk5v3.stl` oder `*_v6_rt950pro.stl`)", "Hüllmaß %s mm (UV-K5 V3)" % N["bbox"], "PETG empfohlen"),
         ("2", "1", "Sechskantmutter 1/4\"-20 UNC", "Schlüsselweite 11.1 mm, Dicke 5.6 mm", "Tasche SW %s × %s mm" % (N["af"], N["esp"])),
         ("3", "1", "Ausleger (nicht enthalten)", "Ø%s mm, Tunnel %s mm (Nennspiel %s mm je Seite)" % (N["pluma"], N["tunel"], N["jgo"]), "Echten Ausleger messen"),
         ("4", "0–1", "Stativ-Schnellwechselplatte/-schraube (optional)", "1/4\"-20", "Nach Bedarf"),
         ("5", "0–1", "Duplexer und EVA-Streifen (optional)", "—", "Je nach Funkgerät")],
    nobear="Dieses Design hat **keine Lager oder Wellen**; einziges Beschlagteil ist die 1/4\"-20-Mutter.",
    h_ord="Montagereihenfolge", steps=["Teil prüfen: Grate in Tunnel und Sechskanttasche entfernen.", "Mutter von der Z−-Seite durch den seitlichen Kanal einrasten, über die Haltelippen (%s mm Haut zum Griffende; eine Schraube ab 6 mm greift etwa 4 mm)." % N["piel"], "Ausleger Ø%s mm durch den %s-mm-Tunnel schieben." % (N["pluma"], N["tunel"]), "Clip-Zunge am oberen freien Rand der Platte (%s bei %s) parallel zu ihr einschieben und das Funkgerät auf der −U-Seite sichern." % (N["placa"], N["ang"])],
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
    h_prof="Anfängliche Profile", prof_h=["Parameter", "Startwert"], prof=[("Schichthöhe", "0.20 mm"), ("Perimeter", "4"), ("Füllung", "Gyroid 40 % (60–100 % oder zusätzliche Wände im Träger und im Stativbereich)"), ("Brim", "5 mm (Option A)"), ("Stützen", "unter Platte und Träger"), ("Maßkorrektur", "0 bis zur Messung des Prüfkörpers")],
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
    title="Poignée SpaceQuad v6.2 — Guide de montage illustré",
    idx_title="Guides SpaceQuad (multilingue)", idx_intro="Documentation cohérente en 5 langues. Tous les profils d'impression et essais de charge sont des **valeurs initiales EN ATTENTE D'ESSAI PHYSIQUE**.",
    d_mont="Montage illustré, nomenclature, jeux et essais de charge", d_imp="Matériau, orientation et profils d'impression initiaux", d_cal="Calibration Anycubic Kobra S1 et Bambu Lab",
    pend="⚠ ESSAI PHYSIQUE EN ATTENTE",     geo="Basé sur la géométrie v6.2 (position D) de `stl/v6/`. Si la géométrie change, régénérer avec `src/render_guia.py`. CAO uniquement : les dimensions du clip et de chaque radio sont estimées, non mesurées, et il n'y a pas d'essai de charge.",
        figs=["Vue latérale cotée (X pointe vers la prise ; radio côté −U)", "Vue de bout (culasse)", "Plan de la plaque du clip et de la poutre : %s mm à %s" % (N["placa"], N["ang"]),
              "Vue éclatée et étapes numérotées ①–④ (l'écrou se clipse par Z−)", "Coupes A-A (tunnel) et B-B (logement d'écrou, peau de 2 mm)", "Orientations d'impression comparées", "Insertion du clip (position D : par le bord libre haut, parallèle à la plaque)"],
    h_fig="Graphiques", h_bom="Nomenclature (BOM)", bom_h=["N°", "Qté", "Élément", "Dimension / spécification", "Remarque"],
    bom=[("1", "1", "Poignée imprimée v6.2 (`stl/v6/*_v6_uvk5v3.stl` ou `*_v6_rt950pro.stl`)", "Encombrement %s mm (UV-K5 V3)" % N["bbox"], "PETG recommandé"),
         ("2", "1", "Écrou hexagonal 1/4\"-20 UNC", "Sur plats 11.1 mm, épaisseur 5.6 mm", "Logement SP %s × %s mm" % (N["af"], N["esp"])),
         ("3", "1", "Mât / boom (non inclus)", "Ø%s mm, tunnel %s mm (jeu nominal %s mm par côté)" % (N["pluma"], N["tunel"], N["jgo"]), "Mesurer le mât réel"),
         ("4", "0–1", "Plaque/vis de déclenchement rapide trépied (option)", "1/4\"-20", "Selon usage"),
         ("5", "0–1", "Duplexeur et bande EVA (options)", "—", "Selon la radio")],
    nobear="Cette conception **n'a ni roulements ni arbres** ; la seule visserie est l'écrou 1/4\"-20.",
    h_ord="Ordre de montage", steps=["Vérifier la pièce : ébavurer le tunnel et le logement hexagonal.", "Clipser l'écrou par le canal latéral du côté Z−, en passant les lèvres de retenue (peau de %s mm vers la culasse ; une vis de 6 mm ou plus engage environ 4 mm)." % N["piel"], "Faire glisser le mât Ø%s mm dans le tunnel de %s mm." % (N["pluma"], N["tunel"]), "Introduire la languette du clip par le bord libre haut de la plaque (%s à %s), parallèlement à elle, et fixer la radio côté −U." % (N["placa"], N["ang"])],
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
    h_prof="Profils initiaux", prof_h=["Paramètre", "Valeur initiale"], prof=[("Hauteur de couche", "0.20 mm"), ("Périmètres", "4"), ("Remplissage", "gyroïde 40 % (60–100 % ou parois supplémentaires dans la poutre et la zone du trépied)"), ("Brim", "5 mm (option A)"), ("Supports", "sous la plaque et la poutre"), ("Ajustement dimensionnel", "0 jusqu'à mesure de l'éprouvette")],
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
    title="Impugnatura SpaceQuad v6.2 — Guida di montaggio illustrata",
    idx_title="Guide SpaceQuad (multilingue)", idx_intro="Documentazione coerente in 5 lingue. Tutti i profili di stampa e le prove di carico sono **valori iniziali IN ATTESA DI PROVA FISICA**.",
    d_mont="Montaggio illustrato, distinta, giochi e prove di carico", d_imp="Materiale, orientamento e profili di stampa iniziali", d_cal="Calibrazione Anycubic Kobra S1 e Bambu Lab",
    pend="⚠ PROVA FISICA IN SOSPESO",     geo="Basato sulla geometria v6.2 (posizione D) in `stl/v6/`. Se la geometria cambia, rigenerare con `src/render_guia.py`. Solo CAD: le dimensioni della clip e di ogni radio sono stimate, non misurate, e non c'è prova di carico.",
        figs=["Vista laterale quotata (X punta verso l'impugnatura; radio sul lato −U)", "Vista di testa (culatta)", "Pianta della piastra della clip e della trave: %s mm a %s" % (N["placa"], N["ang"]),
              "Vista esplosa e passi numerati ①–④ (il dado si inserisce a scatto da Z−)", "Sezioni A-A (tunnel) e B-B (sede del dado, pelle da 2 mm)", "Orientamenti di stampa a confronto", "Inserimento della clip (posizione D: dal bordo libero alto, parallelo alla piastra)"],
    h_fig="Grafici", h_bom="Distinta base (BOM)", bom_h=["N.", "Q.tà", "Elemento", "Misura / specifica", "Nota"],
    bom=[("1", "1", "Impugnatura stampata v6.2 (`stl/v6/*_v6_uvk5v3.stl` o `*_v6_rt950pro.stl`)", "Ingombro %s mm (UV-K5 V3)" % N["bbox"], "PETG consigliato"),
         ("2", "1", "Dado esagonale 1/4\"-20 UNC", "Chiave 11.1 mm, spessore 5.6 mm", "Sede CH %s × %s mm" % (N["af"], N["esp"])),
         ("3", "1", "Asta / boom (non inclusa)", "Ø%s mm, tunnel %s mm (gioco nominale %s mm per lato)" % (N["pluma"], N["tunel"], N["jgo"]), "Misurare l'asta reale"),
         ("4", "0–1", "Piastra/vite a sgancio rapido per treppiede (opzionale)", "1/4\"-20", "Secondo l'uso"),
         ("5", "0–1", "Duplexer e striscia EVA (opzionali)", "—", "Secondo la radio")],
    nobear="Questo progetto **non ha cuscinetti né alberi**; l'unica minuteria è il dado 1/4\"-20.",
    h_ord="Ordine di montaggio", steps=["Controllare il pezzo: sbavare tunnel e sede esagonale.", "Inserire a scatto il dado dal canale laterale del lato Z−, oltre i labbri di ritenzione (pelle di %s mm verso la culatta; una vite da 6 mm o più impegna circa 4 mm)." % N["piel"], "Far scorrere l'asta Ø%s mm nel tunnel di %s mm." % (N["pluma"], N["tunel"]), "Introdurre la linguetta della clip dal bordo libero alto della piastra (%s a %s), parallelamente ad essa, e fissare la radio sul lato −U." % (N["placa"], N["ang"])],
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
    h_prof="Profili iniziali", prof_h=["Parametro", "Valore iniziale"], prof=[("Altezza strato", "0.20 mm"), ("Perimetri", "4"), ("Riempimento", "gyroid 40 % (60–100 % o pareti extra nella trave e nella zona del treppiede)"), ("Brim", "5 mm (opzione A)"), ("Supporti", "sotto la piastra e la trave"), ("Correzione dimensionale", "0 fino alla misura del provino")],
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

# Contenido propio de v6.2 (posición D, tuerca reforzada, variantes por radio, impresión)
V6TXT = {
    "es": dict(
        h_posd="Posición D (v6.2)",
        posd=["Con la empuñadura en la mano, la radio queda en el lado del boom opuesto a la torre y al duplexor (lado −U) e inclinada %s hacia el operador (extremo superior hacia −V)." % N["ang"],
              "Una viga de %s mm une las dos cartelas de la placa con la torre y se empotra en ella; no toca el túnel del boom ni el duplexor." % N["viga"],
              "El clip entra paralelo a la placa por su borde libre alto y avanza hacia el fondo del hueco, donde está la ventana de retención (recorrido útil %s mm)." % N["rec"]],
        h_var="Variantes por radio", var_h=["Radio", "Archivo STL", "Envolvente de la radio (estimada, mm)", "Altura de la placa PH0 (mm)"],
        h_nut="Tuerca de trípode reforzada",
        nut=["Piel de la cara del culo de %s mm (antes 1.2 mm) y paredes de al menos 3 mm alrededor del alojamiento hexagonal." % N["piel"],
             "La tuerca entra a presión: se introduce por el canal lateral y encaja al pasar los labios de retención (apertura 10.6 mm frente a 11.1 mm de la tuerca). La interferencia es teórica.",
             "Un tornillo de trípode de 6 mm o más engrana unos 4 mm de la tuerca (nominal 5.6 mm).",
             "Cavidad del mango rellena %s mm con transición cónica y brida opcional en el culo." % N["rampa"]],
        h_print="Consejos de impresión",
        prn=["Soportes bajo la placa y bajo la viga.",
             "Relleno alto (60–100 %) o paredes extra en la viga y en la zona del trípode.",
             "Hacer una prueba de carga antes de fiarse de la pieza (ver la sección de verificación de resistencia)."],
        h_prev="Versiones anteriores",
        prev="Solo siguen v1 (entrada), v3 (generador base y referencia del Anytone) y el Anytone genérico (figuras en `docs/img/guia/anytone/`). v2, v4 y v5 se eliminaron; se recuperan desde el historial de git (commit anterior a la limpieza).",
        n_img="Figuras de la variante UV-K5 V3; la RT-950 Pro comparte la misma geometría salvo la altura de la placa.",
    ),
    "en": dict(
        h_posd="Position D (v6.2)",
        posd=["With the grip in hand, the radio sits on the side of the boom opposite the tower and the duplexer (−U side), leaning %s toward the operator (upper end toward −V)." % N["ang"],
              "A %s mm beam joins the two plate gussets to the tower and is embedded in it; it touches neither the boom tunnel nor the duplexer." % N["viga"],
              "The clip enters parallel to the plate through its high free edge and advances toward the bottom of the gap, where the retention window is (usable travel %s mm)." % N["rec"]],
        h_var="Per-radio variants", var_h=["Radio", "STL file", "Radio envelope (estimated, mm)", "Plate height PH0 (mm)"],
        h_nut="Reinforced tripod nut",
        nut=["%s mm skin on the butt face (was 1.2 mm) and walls of at least 3 mm around the hex pocket." % N["piel"],
             "The nut snaps in: insert it through the side channel and it seats once it passes the retention lips (10.6 mm opening versus the 11.1 mm nut). The interference is theoretical.",
             "A tripod screw of 6 mm or more engages about 4 mm of the nut (nominal 5.6 mm).",
             "Handle cavity filled %s mm with a tapered transition, and an optional butt flange." % N["rampa"]],
        h_print="Printing advice",
        prn=["Supports under the plate and under the beam.",
             "High infill (60–100 %) or extra walls in the beam and the tripod zone.",
             "Run a load test before trusting the part (see the strength verification section)."],
        h_prev="Earlier versions",
        prev="Only v1 (input), v3 (base generator and Anytone baseline) and the generic Anytone remain (figures in `docs/img/guia/anytone/`). v2, v4 and v5 were removed; recover them from git history (the commit before the cleanup).",
        n_img="Figures show the UV-K5 V3 variant; the RT-950 Pro shares the geometry except for the plate height.",
    ),
    "de": dict(
        h_posd="Position D (v6.2)",
        posd=["Mit dem Griff in der Hand sitzt das Funkgerät auf der dem Turm und dem Duplexer gegenüberliegenden Seite des Auslegers (−U-Seite) und ist um %s zum Bediener geneigt (oberes Ende zu −V)." % N["ang"],
              "Ein %s-mm-Träger verbindet die beiden Rippen der Platte mit dem Turm und ist in diesen eingelassen; er berührt weder den Auslegertunnel noch den Duplexer." % N["viga"],
              "Der Clip wird parallel zur Platte über deren oberen freien Rand eingeschoben und läuft zum Grund der Aussparung mit dem Haltefenster (nutzbarer Weg %s mm)." % N["rec"]],
        h_var="Varianten je Funkgerät", var_h=["Funkgerät", "STL-Datei", "Hüllmaß des Funkgeräts (geschätzt, mm)", "Plattenhöhe PH0 (mm)"],
        h_nut="Verstärkte Stativmutter",
        nut=["%s mm Haut an der Endfläche (vorher 1.2 mm) und Wände von mindestens 3 mm um die Sechskanttasche." % N["piel"],
             "Die Mutter rastet ein: Sie wird durch den seitlichen Kanal eingeführt und sitzt, sobald sie die Haltelippen passiert hat (Öffnung 10.6 mm gegenüber 11.1 mm Mutter). Die Überdeckung ist theoretisch.",
             "Eine Stativschraube ab 6 mm greift etwa 4 mm der Mutter (nominal 5.6 mm).",
             "Griffhohlraum auf %s mm gefüllt, mit konischem Übergang, und optionaler Flansch am Ende." % N["rampa"]],
        h_print="Druckhinweise",
        prn=["Stützen unter der Platte und unter dem Träger.",
             "Hohe Füllung (60–100 %) oder zusätzliche Wände im Träger und im Stativbereich.",
             "Vor dem Vertrauen in das Teil einen Belastungstest durchführen (siehe Abschnitt Festigkeitsprüfung)."],
        h_prev="Frühere Versionen",
        prev="Nur v1 (Eingabe), v3 (Basisgenerator und Anytone-Referenz) und das generische Anytone bleiben erhalten (Abbildungen in `docs/img/guia/anytone/`). v2, v4 und v5 wurden entfernt; sie lassen sich aus der Git-Historie wiederherstellen (Commit vor der Bereinigung).",
        n_img="Die Abbildungen zeigen die Variante UV-K5 V3; das RT-950 Pro hat dieselbe Geometrie bis auf die Plattenhöhe.",
    ),
    "fr": dict(
        h_posd="Position D (v6.2)",
        posd=["Poignée en main, la radio se trouve du côté de la flèche opposé à la tour et au duplexeur (côté −U), inclinée de %s vers l'opérateur (extrémité haute vers −V)." % N["ang"],
              "Une poutre de %s mm relie les deux goussets de la plaque à la tour et y est encastrée ; elle ne touche ni le tunnel de la flèche ni le duplexeur." % N["viga"],
              "Le clip entre parallèlement à la plaque par son bord libre haut et avance vers le fond du logement, où se trouve la fenêtre de retenue (course utile %s mm)." % N["rec"]],
        h_var="Variantes par radio", var_h=["Radio", "Fichier STL", "Encombrement de la radio (estimé, mm)", "Hauteur de plaque PH0 (mm)"],
        h_nut="Écrou de trépied renforcé",
        nut=["Peau de %s mm sur la face du talon (auparavant 1.2 mm) et parois d'au moins 3 mm autour du logement hexagonal." % N["piel"],
             "L'écrou se clipse : on l'introduit par le canal latéral et il s'engage en passant les lèvres de retenue (ouverture 10.6 mm pour un écrou de 11.1 mm). L'interférence est théorique.",
             "Une vis de trépied de 6 mm ou plus engage environ 4 mm de l'écrou (nominal 5.6 mm).",
             "Cavité de la poignée remplie sur %s mm avec transition conique, et bride optionnelle au talon." % N["rampa"]],
        h_print="Conseils d'impression",
        prn=["Supports sous la plaque et sous la poutre.",
             "Remplissage élevé (60–100 %) ou parois supplémentaires dans la poutre et la zone du trépied.",
             "Faire un essai de charge avant de se fier à la pièce (voir la section de vérification de résistance)."],
        h_prev="Versions antérieures",
        prev="Seuls restent v1 (entrée), v3 (générateur de base et référence Anytone) et l'Anytone générique (figures dans `docs/img/guia/anytone/`). v2, v4 et v5 ont été supprimées ; elles se récupèrent depuis l'historique git (commit précédant le nettoyage).",
        n_img="Les figures montrent la variante UV-K5 V3 ; la RT-950 Pro partage la même géométrie, sauf la hauteur de la plaque.",
    ),
    "it": dict(
        h_posd="Posizione D (v6.2)",
        posd=["Con l'impugnatura in mano, la radio si trova sul lato del braccio opposto alla torre e al duplexer (lato −U), inclinata di %s verso l'operatore (estremità superiore verso −V)." % N["ang"],
              "Una trave da %s mm collega le due nervature della piastra alla torre e vi è incastrata; non tocca né il tunnel del braccio né il duplexer." % N["viga"],
              "La clip entra parallela alla piastra dal suo bordo libero alto e avanza verso il fondo dell'alloggiamento, dove si trova la finestra di ritenzione (corsa utile %s mm)." % N["rec"]],
        h_var="Varianti per radio", var_h=["Radio", "File STL", "Ingombro della radio (stimato, mm)", "Altezza piastra PH0 (mm)"],
        h_nut="Dado da treppiede rinforzato",
        nut=["Pelle di %s mm sulla faccia del fondo (prima 1.2 mm) e pareti di almeno 3 mm attorno alla sede esagonale." % N["piel"],
             "Il dado si inserisce a scatto: lo si introduce dal canale laterale e si assesta superando i labbri di ritenzione (apertura 10.6 mm contro 11.1 mm del dado). L'interferenza è teorica.",
             "Una vite da treppiede da 6 mm o più impegna circa 4 mm del dado (nominale 5.6 mm).",
             "Cavità dell'impugnatura riempita per %s mm con transizione conica e flangia opzionale sul fondo." % N["rampa"]],
        h_print="Consigli di stampa",
        prn=["Supporti sotto la piastra e sotto la trave.",
             "Riempimento alto (60–100 %) o pareti extra nella trave e nella zona del treppiede.",
             "Eseguire una prova di carico prima di fidarsi del pezzo (vedere la sezione sulla verifica di resistenza)."],
        h_prev="Versioni precedenti",
        prev="Restano solo v1 (input), v3 (generatore di base e riferimento Anytone) e l'Anytone generico (figure in `docs/img/guia/anytone/`). v2, v4 e v5 sono state rimosse; si recuperano dalla cronologia git (commit precedente alla pulizia).",
        n_img="Le figure mostrano la variante UV-K5 V3; la RT-950 Pro condivide la stessa geometria tranne l'altezza della piastra.",
    ),
}

# Envolvente de cada radio (perfiles_radio.json, estimada) y altura PH0 nominal de la placa (docs/VARIANTES_V6.md)
RADIOS_V6 = [("UV-K5 V3", "uvk5v3", "115 × 60 × 37.5", "72.5"), ("RT-950 Pro", "rt950pro", "162 × 66 × 48", "88.5")]


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def nav(lang):
    return " · ".join("**%s**" % NAMES[l] if l == lang else "[%s](../%s/README.md)" % (NAMES[l], l) for l in LANGS)


# (carpeta de figuras, STL, envolvente mm, volumen mm3); medidos de los STL verificados
VARIANTES = [
    ("anytone", "stl/mango_spacequad_anytone_generico.stl + stl/anytone_calzos/*.stl", "195.2 × 93.7 × 79.0", "213099"),
]
VNAME = {
    "es": ("Anytone genérico ajustable (base ya reforzada; calzos opcionales)",),
    "en": ("Adjustable generic Anytone (base already reinforced; optional shims)",),
    "de": ("Anytone generisch einstellbar (Basis bereits verstärkt; optionale Keile)",),
    "fr": ("Anytone générique réglable (base déjà renforcée ; cales optionnelles)",),
    "it": ("Anytone generico regolabile (base già rinforzata; spessori opzionali)",),
}
VHEAD = {
    "es": ("Variantes (geometría final)", ["Variante", "Archivo STL", "Envolvente (mm)", "Volumen (mm³)"]),
    "en": ("Variants (final geometry)", ["Variant", "STL file", "Envelope (mm)", "Volume (mm³)"]),
    "de": ("Varianten (endgültige Geometrie)", ["Variante", "STL-Datei", "Hüllmaß (mm)", "Volumen (mm³)"]),
    "fr": ("Variantes (géométrie finale)", ["Variante", "Fichier STL", "Encombrement (mm)", "Volume (mm³)"]),
    "it": ("Varianti (geometria finale)", ["Variante", "File STL", "Ingombro (mm)", "Volume (mm³)"]),
}


def doc_mont(lang, t):
    x = V6TXT[lang]
    o = ["# " + t["title"], "", nav(lang), "", "> " + t["geo"], "", "## " + x["h_posd"], ""]
    o += ["- " + s for s in x["posd"]]
    o += ["", "## " + x["h_var"], "",
          table(x["var_h"], [[n, "`%s`" % V6_STL[k], e, ph] for n, k, e, ph in RADIOS_V6]), "",
          "## " + x["h_nut"], ""] + ["- " + s for s in x["nut"]]
    o += ["", "## " + x["h_print"], ""] + ["- " + s for s in x["prn"]]
    o += ["", "## " + t["h_fig"], "", "> " + x["n_img"], ""]
    for f, c in zip(FIGS, t["figs"]):
        o += ["![%s](%s%s/%s.png)" % (c, IMG, lang, f), "*%s*" % c, ""]
    o += ["## " + t["h_bom"], "", table(t["bom_h"], [list(r) for r in t["bom"]]), "", t["nobear"], "",
          "## " + t["h_ord"], ""] + ["%d. %s" % (i + 1, s) for i, s in enumerate(t["steps"])]
    o += ["", "## " + t["h_hol"], "", "> " + t["pend"], ""] + ["%d. %s" % (i + 1, s) for i, s in enumerate(t["hol"])]
    o += ["", "## " + t["h_car"], "", "> " + t["pend"], ""] + ["%d. %s" % (i + 1, s) for i, s in enumerate(t["car"])]
    o += ["", "## " + x["h_prev"], "", x["prev"], "",
          table(VHEAD[lang][1], [[VNAME[lang][i], "`%s`" % v[1], v[2], v[3]] for i, v in enumerate(VARIANTES)]), ""]
    o += ["## " + t["h_lic"], "", t["lic"], ""]
    return "\n".join(o)


def doc_imp(lang, t):
    import json
    ruta = os.path.join(ROOT, "docs", "img", "guia", "v6", lang, "orientaciones.json")
    filas = {}
    if os.path.isfile(ruta):   # métricas calculadas por render_guia.py sobre el STL v6
        filas = {f["cama"]: f for f in json.load(open(ruta, encoding="utf-8"))}
    metr = []
    for k in ("Y-", "X+", "Z+"):
        f = filas.get(k)
        metr.append((k.replace("-", "−"), "%s" % f["altura_mm"] if f else "—", "%s" % f["contacto_mm2"] if f else "—",
                     "%s" % f["voladizo_mm2"] if f else "—"))
    o = ["# " + t["h_mat"] + " — SpaceQuad v6.2", "", nav(lang), "", "> " + t["pend"], "", "## " + t["h_mat"], "",
         table(t["mat_h"], [list(r) for r in t["mat"]]), "",
         table(t["ori_h"], [[m[0], m[1] + " mm", m[2] + " mm²", m[3] + " mm²", c] for m, c in zip(metr, t["ori_c"])]), "",
         "![%s](%s%s/fig04_orientacion_impresion.png)" % (t["figs"][5], IMG, lang), "",
         "## " + t["h_prof"], "", table(t["prof_h"], [list(r) for r in t["prof"]]), "", t["prof_note"], "",
         "## " + V6TXT[lang]["h_print"], ""] + ["- " + s for s in V6TXT[lang]["prn"]] + ["",
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
