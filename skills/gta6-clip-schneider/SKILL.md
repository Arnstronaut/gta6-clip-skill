---
name: gta6-clip-schneider
description: Lädt einen Ausschnitt eines Videos und schneidet ihn mit ffmpeg ins Hochformat 9:16 (1080x1920), 15 bis 45 Sekunden. Mit Facecam oben und Spiel unten, ohne Facecam mit unscharf aufgefülltem Rand. Nutzen bei "schneide den Clip", "Hochformat", "9:16", "Clip aus diesem Video".
---

# Clip-Schneider (GTA 6)

Nur Material schneiden, das eine Kampagne oder der Rechteinhaber erlaubt. Der Befehl braucht deshalb immer `--erlaubt` mit einer Begründung.

## Ganze Kette bis zum fertigen Clip (empfohlen)
```
python scripts/gta6_los.py --url <Link oder Datei> --start 1:20 --dauer 30 --erlaubt "<Kampagne/Rechteinhaber, Datum>" --arbeitsordner gta6
```
Das lädt nur den Ausschnitt (`yt-dlp --download-sections`), schneidet 9:16, brennt Untertitel ein und legt `gta6/morgen/<id>.mp4` plus `<id>.meta.json` an.

## Nur schneiden
```
python scripts/clip_schneider.py --eingabe quelle.mp4 --start 0:12 --dauer 30 --ausgabe clip.mp4
```
- Mit Facecam: `--facecam x:y:w:h` = der Facecam-Bereich im Originalbild in Pixeln. Dann liegt die Facecam oben (1080x720), das Spiel unten (1080x1200).
  Facecam-Position herausfinden: ein Standbild ziehen (`ffmpeg -ss 5 -i quelle.mp4 -frames:v 1 bild.png`), ansehen, Rechteck ablesen.
- `--spiel-mitte 0.5` verschiebt den Bildausschnitt des Spiels (0 = links, 1 = rechts).
- Länge: 15 bis 45 Sekunden. Länger als 45 wird abgelehnt.

## Gute Stelle wählen
Anfang = die Sekunde, in der etwas passiert (kein Vorlauf), Ende = nach dem Höhepunkt, nicht mitten im Satz.

## Prüfen
`ffprobe` muss 1080x1920, h264 und Ton zeigen, dazu ein Standbild ansehen (`ffmpeg -ss 5 -i clip.mp4 -frames:v 1 stand.png`). Erst dann weiter.
