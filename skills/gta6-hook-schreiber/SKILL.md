---
name: gta6-hook-schreiber
description: Schreibt 5 Hook-Vorschläge (kurzer Text oben im Bild) für einen GTA-6-Clip und wählt einen aus. Nutzen bei "Hook", "Text oben", "erste Sekunde", "wie fange ich den Clip an".
---

# Hook-Schreiber (GTA 6)

Der Hook ist der Text oben im Bild in den ersten Sekunden. Er soll neugierig machen, ohne zu lügen.

## Ablauf
1. Sieh dir an, was im Clip wirklich passiert: Transkript (`.ass` oder Whisper-Text) und mindestens ein Standbild. Ohne das keine Hooks schreiben.
2. Schreibe genau 5 Vorschläge, jeder in einer anderen Form:
   - Frage ("Hast du das gesehen?")
   - Behauptung, die der Clip belegt
   - Zahl, nur wenn sie im Clip vorkommt
   - Reaktion ("Das hat keiner erwartet")
   - Aufforderung ("Warte auf das Ende")
3. Regeln für jeden Hook: höchstens 8 Wörter, höchstens 2 Zeilen, keine erfundenen Fakten (kein Releasedatum, kein Name, keine Zahl, die der Clip nicht zeigt), keine Aufrufzahlen und keine Verdienstversprechen.
4. Nenne deinen Favoriten mit einem Satz Begründung.
5. Trage in die `.meta.json` des Clips ein: `"hook_vorschlaege": [5 Texte]` und `"hook": "<Favorit>"`.

## Hook ins Bild bringen
Mit dem Skript (setzt den Text in den ersten 3 Sekunden oben ins Bild, Umlaute gehen):
```
python scripts/hook_einblenden.py --eingabe clip.mp4 --text "DEIN HOOK" --ausgabe clip_hook.mp4
```
Alternativ blendet der Mensch den Text in seiner Schnitt-App ein.
