# GTA-6-Skill

Ein kostenloses Paket für Claude Code, auf Deutsch. Es hilft dir bei GTA-6-Clipping: Kampagnen finden, Trends finden, Clips schneiden, Untertitel, Hook, Titel, Prüfung. Und der **Nacht-Modus** macht das alles über Nacht, damit am Morgen fertige Clips bereitliegen.

**Wichtig:** Das Paket lädt nie etwas hoch, reicht nie etwas ein und meldet sich nirgends an. Hochladen machst du selbst. Es erfindet auch keine Aufrufzahlen oder Verdienste. Und es schneidet nur Material, das eine Kampagne oder der Rechteinhaber erlaubt.

## Was drin ist (8 Skills und 1 Befehl)

| Name | Was er macht |
|---|---|
| `gta6-kampagnen-finder` | Sucht Clipping-Kampagnen zu GTA 6 (Satz, Regeln, Link, Restbudget). Unbekanntes heißt "offen". |
| `gta6-trend-jaeger` | Zeigt GTA-6-Videos der letzten 24 Stunden von YouTube, nach Aufrufen sortiert. |
| `gta6-clip-schneider` | Schneidet 15 bis 45 Sekunden ins Hochformat 1080x1920 (Facecam oben, Spiel unten). |
| `gta6-untertitel` | Untertitel Wort für Wort, groß, ins Video eingebrannt. |
| `gta6-hook-schreiber` | 5 Hook-Vorschläge für den Text oben im Bild. |
| `gta6-titel-hashtags` | Titel und Hashtags für TikTok, Shorts und Reels. |
| `gta6-regel-check` | Prüft Format, Länge, Ton, Hook, Titel, Hashtags, Kampagnenregeln und Erlaubnis. |
| `gta6-nacht-modus` | Wiederholt die Kette über Nacht. Morgens liegen Clips in `gta6/morgen/`. |
| Befehl `gta6-los` | Die ganze Kette in einem Durchgang. |

## Was du vorher brauchst (einmal)

Du brauchst Claude Code und diese vier Programme.

**Windows** (in der PowerShell):
```
winget install Python.Python.3.12
winget install Gyan.FFmpeg
pip install yt-dlp faster-whisper
```
**Mac** (im Terminal, mit Homebrew):
```
brew install python ffmpeg yt-dlp
pip3 install faster-whisper
```
Danach Terminal neu öffnen. Test: `ffmpeg -version` und `yt-dlp --version` müssen eine Version zeigen.
Auf dem Mac heißt Python im Alltag `python3`: überall, wo hier `python` steht, `python3` schreiben.

## Installation

**Weg 1, am einfachsten (nur für eine Sitzung):**
1. Lade den Ordner `gta6-skill` auf deinen Rechner, zum Beispiel nach `C:\gta6-skill` (Windows) oder `~/gta6-skill` (Mac).
2. Starte Claude Code so:
   ```
   claude --plugin-dir C:\gta6-skill
   ```
   (Mac: `claude --plugin-dir ~/gta6-skill`)

**Weg 2, dauerhaft über den Plugin-Katalog:**
In Claude Code:
```
/plugin marketplace add C:\gta6-skill
/plugin install gta6-clip-skill@gta6-clip-skill
```
(Mac: den Pfad `~/gta6-skill` nehmen.) Danach Claude Code neu starten.

Bei beiden Wegen heißt der Befehl `/gta6-clip-skill:gta6-los`. Die Skills findet Claude von selbst, wenn du sagst, was du willst ("Finde mir GTA-6-Trends").

## So benutzt du es

1. Öffne Claude Code in einem leeren Ordner für dein Clipping-Projekt.
2. **Kampagnen suchen:** "Finde laufende GTA-6-Clipping-Kampagnen."
   Ergebnis: `gta6/kampagnen.md`.
3. **Erlaubnis festhalten:** Schreibe in `gta6/erlaubt.txt` die Kanäle, deren Videos eine Kampagne oder der Rechteinhaber zum Schneiden freigibt (eine Zeile pro Kanal, voller Kanalname wie auf YouTube; Teilstücke zählen nicht).
4. **Ein Clip:** `/gta6-clip-skill:gta6-los` (oder mit Link: `/gta6-clip-skill:gta6-los https://youtube.com/watch?v=... ab 1:20`).
   Ergebnis in `gta6/morgen/`: der Clip als `.mp4`, dazu eine `.meta.json` mit Hook, Titel und Hashtags.
5. Sieh dir den Clip an. Wenn er passt, lädst **du** ihn hoch oder reichst ihn ein.

## Nacht-Modus

Vor dem Schlafengehen:
1. `gta6/erlaubt.txt` ausfüllen (ohne diese Datei macht der Nacht-Modus nichts).
2. Rechner an den Strom, Ruhezustand aus, Claude Code offen lassen.
3. In Claude Code eingeben:
   ```
   /loop 30m /gta6-clip-skill:gta6-los
   ```
   Alle 30 Minuten läuft ein Durchgang. Pro Durchgang entsteht höchstens ein Clip.
4. Am Morgen: Ordner `gta6/morgen/` öffnen. Dort liegen die fertigen Clips. Was nicht durch den Regel-Check kam, steht in `PROBLEME.txt`. Was gelaufen ist, steht in `gta6/nacht-protokoll.txt`.

Alternative ohne offenes Claude Code: eine geplante Aufgabe (Windows Aufgabenplanung oder Mac `launchd`), die `claude -p "/gta6-clip-skill:gta6-los"` aufruft. Mit `/schedule` in Claude Code geht das auch.

## Wenn etwas nicht geht

| Problem | Lösung |
|---|---|
| `yt-dlp` lädt nicht / YouTube meldet Fehler | `pip install -U yt-dlp` und installiere Node.js (`winget install OpenJS.NodeJS` bzw. `brew install node`). |
| "Library cublas ... not found" | Egal. Das Paket schaltet dann selbst auf den Prozessor um. |
| Untertitel falsch geschrieben | Die `.ass`-Datei im Texteditor ändern und neu einbrennen (siehe Skill `gta6-untertitel`). |
| "KEINE SPRACHE erkannt" | Der Clip hat keine Sprache. Das ist normal bei reinem Spielgeräusch. Der Hook oben reicht. |
| Schwarze Balken im Spiel-Teil | Das Original hat selbst Balken (Trailer sind oft Kino-Format). Für andere Quellen entfällt das. |
| Der Befehl wird nicht gefunden | Claude Code mit `--plugin-dir` neu starten oder `/plugin` prüfen. |

## Ordner

```
gta6/                 dein Arbeitsordner (entsteht beim ersten Lauf)
  kampagnen.md        gefundene Kampagnen
  erlaubt.txt         Kanäle, die du schneiden darfst
  trends.txt          Ergebnisliste des Trend-Jägers
  quelle/             heruntergeladene Ausschnitte
  morgen/             fertige Clips + .meta.json + PROBLEME.txt
```

## Für Entwickler

Skripte liegen in `scripts/`, Tests in `tests/`: `python -m pytest tests`.
Lizenz: MIT.
