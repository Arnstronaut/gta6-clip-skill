---
name: gta6-nacht-modus
description: Lässt die ganze GTA-6-Kette über Nacht wiederholt laufen (Trend finden, schneiden, Untertitel, Hook, Titel, Regel-Check), sodass am Morgen fertige Clips in gta6/morgen/ liegen. Einrichtung mit /loop 30m /gta6-los oder mit einer geplanten Aufgabe. Nutzen bei "Nacht-Modus", "über Nacht laufen lassen", "automatisch Clips machen".
---

# Nacht-Modus (GTA 6)

Der Nacht-Modus ruft den Befehl `gta6-los` immer wieder auf. Er lädt nie hoch und reicht nie ein. Am Morgen liegen die Clips in `gta6/morgen/`, du prüfst und lädst selbst hoch.

## Vorbereitung (einmal, vor dem Schlafengehen)
1. `gta6/erlaubt.txt` anlegen: eine Zeile pro Kanal, dessen Videos eine Kampagne oder der Rechteinhaber zum Schneiden erlaubt. **Ohne diese Datei macht der Nacht-Modus nichts.**
2. Optional `gta6/kampagne-<name>.json` (Regeln, siehe `gta6-regel-check`).
3. Rechner an Strom, Ruhezustand aus, Claude Code geöffnet lassen.

## Starten
- In Claude Code: `/loop 30m /gta6-los` (alle 30 Minuten ein Durchgang). Bei der Plugin-Installation heißt der Befehl `/gta6-clip-skill:gta6-los`.
- Oder als geplante Aufgabe (Claude Code `/schedule`, Windows-Aufgabenplanung oder Mac `launchd`), die `claude -p "/gta6-los"` aufruft.
- Beenden: `/loop` stoppen oder die Aufgabe löschen.

## Was ein Durchgang tut
1. Trend-Jäger mit `--erlaubt gta6/erlaubt.txt --stand gta6/nacht-stand.json`. Keine Treffer = Durchgang endet, nichts passiert.
2. Das beste Video nehmen, das noch nicht im Stand steht. Pro Durchgang höchstens 1 Clip.
3. Clip-Schneider und Untertitel (`gta6_los.py ... --stand gta6/nacht-stand.json`), damit dasselbe Video nicht doppelt kommt.
4. Hook-Schreiber und Titel-Hashtags füllen die `.meta.json`.
5. Regel-Check. Bei Fehlern bleibt der Clip liegen und wird in `gta6/morgen/PROBLEME.txt` vermerkt.
6. Eine Zeile in `gta6/nacht-protokoll.txt` (Uhrzeit, Video, Ergebnis).

## Grenzen
- Den Zeitpunkt der besten Stelle kann der Rechner nicht sicher wissen. Ohne belegten Zeitpunkt (Kapitel oder Transkript) wird das Video übersprungen und im Protokoll als "Stelle offen" vermerkt.
- Nichts wird gepostet. Das Paket hat keine Zugänge und braucht keine.
- Speicherplatz: Ordner `gta6/quelle/` ab und zu leeren.
