---
name: gta6-regel-check
description: Prüft einen fertigen GTA-6-Clip gegen Format, Länge, Ton, Hook, Titel, Hashtags und Kampagnenregeln und prüft, ob das Material erlaubt ist. Nutzen bei "Regel-Check", "ist der Clip okay", "vor dem Einreichen prüfen".
---

# Regel-Check (GTA 6)

```
python scripts/regelcheck.py gta6/morgen/<id>.mp4 --kampagne gta6/kampagne-<name>.json
```
Ausgabe: je Prüfpunkt `OK` oder `FEHLER`, am Ende das Ergebnis. Exit-Code 1 bei mindestens einem Fehler.

## Was geprüft wird
Format 1080x1920, Länge (Standard 15 bis 45 s), Codec h264, Ton vorhanden, `erlaubt_durch` ausgefüllt, Hook, Titel, Hashtags, Shorts-Titel höchstens 100 Zeichen, plus alles aus der Kampagnendatei.

## Kampagnendatei (alles optional, nur abschreiben, was die Kampagne wörtlich verlangt)
```
{"min_dauer": 15, "max_dauer": 45, "pflicht_hashtags": ["#gta6"], "pflicht_text": ["@streamer"], "verboten": ["giveaway"]}
```

## Erlaubnis, das Wichtigste
- Geschnitten und weitergegeben wird nur Material, das eine Kampagne ausdrücklich freigibt oder das der Rechteinhaber erlaubt. "Liegt öffentlich auf YouTube" ist keine Erlaubnis.
- Fehlt die Erlaubnis: Clip nicht freigeben und dem Menschen sagen, welche Kampagne oder Zusage fehlt.
- Bei Fehlern: Ursache beheben (neu schneiden, Hook kürzen, ...) und den Check wiederholen. Die Prüfung nicht lockern.

## Danach
Der Mensch lädt selbst hoch oder reicht selbst ein. Dieses Paket macht das nie.
