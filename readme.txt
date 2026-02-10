Das Blender (5.0.1) Addon „SnapSplit“ automatisiert das Zerlegen komplexer 3D‑Modelle in druckbare Einzelteile und generiert präzise, passgenaue Steckverbindungen ohne Kleber. Es integriert sich in einen 3D‑Druck‑Workflow (Toleranzen, Ausrichtung, Bauraum, Stützvermeidung) und nutzt robuste Booleans, adaptive Toleranzmodelle und Drucker-/Materialprofile.

Das Addon enthält:

    Panel im 3D‑View (N‑Panel → „SnapSplit“)
    Property‑Gruppe mit:
        Teileanzahl (z. B. 2–8)
        Verbindungsart (Zylinder‑Pin, Rechteck‑Zapfen)
        Material-/Druckerprofil (PLA, PETG, ABS, ASA, TPU, SLA)
        daraus abgeleitete Toleranzen (pro Seite)
    Operatoren:
        Planar Split entlang globaler Achse, auf die angegebene Teileanzahl
        Automatische Platzierung und Erzeugung der Steckverbindungen entlang der Naht
        Exporthilfe (optional im Skeleton als Stub)
    QA‑Checks (leichtgewichtig) und best‑practice Addon-Struktur

Bitte beachte: Dies ist ein solides Startgerüst. Die Geometriealgorithmen sind auf Robustheit ausgelegt, aber minimal gehalten. Du kannst später Freiform‑Nähte, Bajonett, Schwalbenschwanz, Magnettaschen, Support‑Aware Features usw. ergänzen.

Installation

    Lege die unten gezeigte Ordnerstruktur an und ziple den Ordner „snapsplit“ (nicht den Inhalt, sondern den Ordner selbst).
    In Blender: Edit → Preferences → Add-ons → Install… → ZIP auswählen → aktivieren.
    N‑Panel öffnen (Taste N) → Tab „SnapSplit“.

Ordnerstruktur (für die ZIP):

    snapsplit/
        init.py
        ops_split.py
        ops_connectors.py
        ui.py
        prefs.py
        utils.py
        profiles.py

Toleranzprofile (Richtwerte, anpassbar)

    PLA: 0.15–0.25 mm pro Seite
    PETG: 0.25–0.35 mm pro Seite
    ABS/ASA: 0.20–0.30 mm pro Seite
    TPU: 0.30–0.45 mm pro Seite
    SLA: 0.05–0.15 mm pro Seite

Diese werden im Addon als Presets vorgegeben und können vom Nutzer übersteuert werden. Ein künftiger Kalibrier‑Wizard kann Messwerte rückkoppeln.

Hinweise zur Verwendung

    Wähle ein geschlossenes Mesh (manifold). Skala anwenden (Ctrl+A → Scale). Einheit mm optional in Scene Settings.
    N‑Panel → SnapSplit:
        Teileanzahl und Schnittachse wählen.
        Planar Split ausführen. Es entstehen mehrere Teile in der Sammlung „_SnapSplit_Parts“.
    Wähle zwei oder mehr benachbarte Teile aus (Reihenfolge egal).
    Wähle Verbindungsart und Toleranzprofil (optional Override).
    „Verbinder hinzufügen“ klicken. Pins/Zapfen werden auf einer gedachten Nahtlinie verteilt:
        Pin/Zapfen wird an Teil A vereinigt, in Teil B eine Buchse mit Toleranz geschnitten.
    Exportiere Teile wie gewohnt (STL/OBJ/3MF). Tipp: für 3MF bitte Skala/Einheiten prüfen.

Grenzen und nächste Schritte

    Der aktuelle „Planar Split“ nutzt Heuristiken und große Cutter-Körper. Für hochkomplexe Geometrien sind gelegentlich manuelle Nacharbeiten sinnvoll.
    Verbinder werden aktuell entlang einer groben Mittellinie platziert; spätere Versionen können:
        Nahtkurve exakt bestimmen,
        Überhang-/Wandstärke‑Aware Platzierung,
        Anti‑Verdreh-Kombinationen automatisch setzen,
        Freiform‑/Krümmungsbasierte Nähte,
        Kalibrier‑Wizard für präzisere Toleranzen.
    SLA‑Modelle benötigen ggf. Entlüftungsbohrungen in Buchsen (geplant).

Qualitätssicherung und Fehlervermeidung

    Vor Split: 3D‑Printing Toolbox nutzen (Manifold, Thin Walls, Intersections).
    Nach Split: Sichtprüfung, ob alle Teile Polygone enthalten.
    Wenn Booleans fehlschlagen: Remesh (Voxel, moderat), Doppelte Vertices entfernen, Normals rücksetzen.
    Skalierung: Arbeite in mm‑Werten, das Addon rechnet korrekt nach Blender‑Metern um.

Wenn du möchtest, erweitere ich dir als Nächstes:

    einen Export‑Operator (3MF mit Metadaten),
    ein QA‑Panel (Manifold-/Wandstärke‑Checks),
    Bajonett/Schwalbenschwanz‑Verbinder,
    einen Kalibrier‑Wizard für Toleranzen.

