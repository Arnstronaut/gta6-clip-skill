---
name: gta6-untertitel
description: Erkennt gesprochene Sprache Wort für Wort mit faster-whisper und brennt die Untertitel groß ins Video ein (ein Wort auf einmal, Großbuchstaben, unten in der Bildmitte). Nutzen bei "Untertitel", "Captions", "Wort für Wort", "Text einbrennen".
---

# Untertitel (GTA 6)

```
python scripts/untertitel.py --eingabe clip.mp4 --ausgabe clip_sub.mp4 --sprache de
```
- `--sprache` weglassen = automatisch erkennen. `--modell small` ist der Standard, für bessere Qualität `medium`.
- Läuft auf der Grafikkarte, wenn möglich, sonst automatisch auf dem Prozessor.
- Das Skript schreibt auch `clip_sub.ass`. Falsch erkannte Wörter kann man in dieser Textdatei ändern und mit
  `ffmpeg -i clip.mp4 -vf ass=clip_sub.ass clip_sub.mp4` neu einbrennen (im selben Ordner ausführen).

## Wenn keine Sprache da ist
Reine Spielgeräusche oder Musik: das Skript sagt "KEINE SPRACHE erkannt" und kopiert das Video unverändert. Keine Untertitel erfinden. Der Hook-Text oben im Bild reicht dann.

## Prüfen
Standbild bei einer Stelle mit Sprache ziehen und ansehen: Wort lesbar, nicht am Rand abgeschnitten. Namen und Spielbegriffe (z. B. Vice City, Lucia) in der `.ass` kontrollieren: Whisper verhört sich dort oft.
