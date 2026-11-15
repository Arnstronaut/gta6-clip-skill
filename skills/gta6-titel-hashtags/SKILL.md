---
name: gta6-titel-hashtags
description: Schreibt Titel und Hashtags für einen GTA-6-Clip je Plattform (TikTok, YouTube Shorts, Instagram Reels). Nutzen bei "Titel", "Beschreibung", "Hashtags", "Caption für den Clip".
---

# Titel und Hashtags (GTA 6)

## Ablauf
1. Lies `.meta.json` und das Transkript des Clips: Titel müssen zum Inhalt passen.
2. Schreibe pro Plattform einen Titel:
   - `tiktok`: kurze Caption, Hook-Gedanke, höchstens ein Satz
   - `shorts`: höchstens 100 Zeichen (YouTube-Grenze), "GTA 6" vorn
   - `reels`: ein bis zwei Sätze, am Ende eine Frage an die Zuschauer
3. Hashtags: 3 bis 5 je Clip, ohne Leerzeichen. Immer dabei: `#gta6`. Dazu themenpassend (`#gta6trailer`, `#vicecity`, `#gaming`). Für Shorts zusätzlich `#shorts`. Das ist ein Richtwert, die Kampagnenregeln gehen vor.
4. Verlangt die Kampagne Pflicht-Hashtags oder einen Pflichttext (z. B. Namen des Streamers), genau so übernehmen.
5. Eintragen in die `.meta.json`:
   ```
   "titel": {"tiktok": "...", "shorts": "...", "reels": "..."},
   "hashtags": ["#gta6", "#gaming", "#shorts"]
   ```

## Regeln
- Kein Clickbait, das der Clip nicht einlöst. Keine erfundenen Aufrufzahlen, Verdienste oder Releasetermine.
- Quelle und Streamer nennen, wenn die Kampagne es verlangt.
