---
name: gta6-trend-jaeger
description: Sucht GTA-6-Videos von großen Streamern und Kanälen, die in den letzten 24 Stunden auf YouTube hochgeladen wurden, und sortiert sie nach Aufrufen. Nutzen bei "was ist gerade viral", "Trends GTA 6", "welche Stelle clippen". Twitch-Clips kommen per Link dazu.
---

# Trend-Jäger (GTA 6)

Das Skript fragt YouTube öffentlich über `yt-dlp` ab (kein Login) und liefert Titel, Kanal, Länge, Link und die echte Aufrufzahl. Es zeigt nur Titel mit "GTA 6" oder "GTA VI" (mit `--alle` auch den Rest).

## Ablauf
1. Ordner `gta6/` im aktuellen Projekt anlegen, falls er fehlt.
2. Ausführen (Skript-Ordner: `${CLAUDE_PLUGIN_ROOT}/scripts`, bei Handinstallation der Ordner `scripts` des Pakets):
   ```
   python scripts/trend_jaeger.py --suche "GTA 6 clip" --suche "GTA 6 stream" --suche "GTA 6 reaction" --anzahl 10 --ausgabe gta6/trends.txt
   ```
   - Nur erlaubte Kanäle: `--erlaubt gta6/erlaubt.txt` (eine Zeile = ein Kanalname, `#` = Kommentar)
   - Schon bearbeitete weglassen: `--stand gta6/nacht-stand.json`
   - Auf Mac `python3` statt `python`.
3. Lies die Liste und sortiere von Hand aus: Livestream-Marathons (mehrere Stunden), reine Trailer-Neuuploads und Treffer ohne echtes Spiel-Material sind kein Clip-Futter.
4. Schlage die 3 besten Stellen vor. Für jede: Link, Kanal, Aufrufe laut Liste, und die Frage "Darf ich das laut Kampagne verwenden?" (siehe `gta6-regel-check`).
5. Für den genauen Zeitpunkt der Stelle: Kapitel oder Beschreibung des Videos lesen oder bei Bedarf Untertitel/Transkript holen (`yt-dlp --skip-download --write-auto-subs`). Zeitpunkte nie raten, bei Unsicherheit den Menschen fragen.

## Regeln
- Aufrufzahlen stehen so da, wie YouTube sie liefert. Nie schätzen, nie aufhübschen.
- Twitch: Suche geht hier nicht. Der Mensch gibt Clip-Links, `yt-dlp` kann sie laden.
- Kein Video ohne Erlaubnis weiterverwenden. Die Liste ist nur eine Ideenliste.
