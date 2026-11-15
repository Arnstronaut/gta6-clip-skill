---
name: gta6-kampagnen-finder
description: Findet laufende Clipping-Kampagnen zu GTA 6 oder zu Streamern, die pro 1.000 Aufrufe zahlen, und schreibt Satz, Regeln, Link und Restbudget in eine Liste. Nutzen, wenn jemand "Kampagne finden", "wo kann ich GTA 6 Clips einreichen", "Clipping-Kampagnen" oder "wer zahlt pro 1000 Aufrufe" sagt. Erfindet nichts, Lücken heißen "offen".
---

# Kampagnen-Finder (GTA 6)

Ziel: eine ehrliche Liste laufender Kampagnen. Du suchst nur, du meldest dich nirgends an und reichst nichts ein.

## Ablauf
1. Suche mit WebSearch nach öffentlichen Kampagnenseiten, zum Beispiel: `GTA 6 clipping campaign`, `clipping campaign pay per 1000 views GTA`, `Streamer Clipping Kampagne GTA 6`, `Whop clipping GTA 6`. Öffne die gefundenen Seiten mit WebFetch.
2. Nimm nur Seiten, die ohne Anmeldung lesbar sind. Steht etwas hinter einem Login: Eintrag mit "Regeln: offen (Login nötig)".
3. Schreibe pro Kampagne diese Felder, und zwar nur, was wörtlich auf der Seite steht:
   - Name und Link
   - Satz (z. B. 1,00 USD pro 1.000 Aufrufe)
   - Erlaubtes Material (welche Streamer/Quellen dürfen geschnitten werden)
   - Regeln (Länge, Hashtags, Pflichttext, verbotene Dinge)
   - Restbudget (so wie angezeigt) und Stand-Datum (heute)
   - Plattformen
4. Speichere alles in `gta6/kampagnen.md` (Ordner anlegen, falls er fehlt) als Tabelle plus je Kampagne ein Absatz Regeln.
5. Schreibe für jede Kampagne mit klaren Regeln eine `gta6/kampagne-<name>.json` im Format für den Regel-Check (siehe Skill `gta6-regel-check`): nur Felder, die auf der Seite stehen.

## Eiserne Regeln
- Nichts erfinden: kein Satz, kein Budget, keine Verdienstzahl, die nicht auf der Seite steht. Unbekanntes heißt `offen`.
- Keine Verdienstversprechen schreiben ("damit verdienst du ...").
- Nicht anmelden, nicht einreichen, keine Konten anlegen. Das macht der Mensch selbst.
- Quelle (Link) bei jeder Zeile.

## Am Ende melden
Wie viele Kampagnen gefunden, wie viele mit vollständigen Regeln, was offen ist.
