---
description: Die ganze GTA-6-Kette in einem Durchgang - Trend finden, schneiden, Untertitel, Hook, Titel, Regel-Check. Lädt nie hoch.
argument-hint: [optional: Video-Link und Startzeit, sonst sucht der Befehl selbst]
---

Mach einen kompletten Durchgang der GTA-6-Clip-Kette. Arbeitsordner ist `gta6/` im aktuellen Projekt. Sprich mit dem Menschen ganz einfach auf Deutsch.

Skript-Ordner: `${CLAUDE_PLUGIN_ROOT}/scripts` (bei Handinstallation der Ordner `scripts` des Pakets). Auf Mac `python3` statt `python`.

Eingabe des Menschen: $ARGUMENTS

## Schritte
1. **Quelle bestimmen.**
   - Hat der Mensch einen Link (und Startzeit) mitgegeben, nimm den.
   - Sonst: Skill `gta6-trend-jaeger` mit `--erlaubt gta6/erlaubt.txt --stand gta6/nacht-stand.json`. Gibt es `gta6/erlaubt.txt` nicht oder keinen Treffer: **hier stoppen**, melden "nichts erlaubt oder nichts Neues", keine Clips machen.
   - Nimm das beste Video, dessen Kanal erlaubt ist. Die Stelle (Startzeit) muss belegt sein (Kapitel, Beschreibung, Transkript). Sonst Protokollzeile "Stelle offen" in `gta6/nacht-protokoll.txt` und stoppen.
2. **Erlaubnis festhalten.** Schreibe in einem Satz auf, wer das Material freigibt (Kampagne oder Rechteinhaber, mit Datum). Kannst du das nicht belegen: stoppen und den Menschen fragen.
3. **Schneiden und Untertitel** (Skills `gta6-clip-schneider`, `gta6-untertitel`):
   `python scripts/gta6_los.py --url <Link> --start <Zeit> --dauer 30 --erlaubt "<Satz aus Schritt 2>" --arbeitsordner gta6 --stand gta6/nacht-stand.json`
   (Facecam-Videos zusätzlich `--facecam x:y:w:h`.)
4. **Hook** (Skill `gta6-hook-schreiber`): 5 Vorschläge aus echtem Inhalt (Transkript/Standbild), Favorit in `gta6/morgen/<id>.meta.json`. Optional mit `hook_einblenden.py` ins Bild.
5. **Titel und Hashtags** (Skill `gta6-titel-hashtags`) in dieselbe `.meta.json`.
6. **Regel-Check** (Skill `gta6-regel-check`): `python scripts/regelcheck.py gta6/morgen/<id>.mp4 [--kampagne gta6/kampagne-<name>.json]`. Bei Fehlern beheben und wiederholen; bleibt es rot, den Clip in `gta6/morgen/PROBLEME.txt` eintragen.
7. **Protokoll:** eine Zeile in `gta6/nacht-protokoll.txt` (Uhrzeit, Video-Link, Ergebnis).
8. **Abschluss an den Menschen:** Pfad des Clips, Hook, Titel, Hashtags, Ergebnis des Regel-Checks, was offen ist.

## Nie
Hochladen, einreichen, irgendwo anmelden, Aufrufzahlen oder Verdienste erfinden, Material ohne Erlaubnis schneiden. Der Mensch lädt selbst hoch.
