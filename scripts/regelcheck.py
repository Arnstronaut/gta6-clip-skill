"""Regel-Check: prueft einen fertigen Clip und seine .meta.json. Meldet OK/FEHLER, Exit-Code 1 bei Fehler.

Beispiel: python regelcheck.py clip.mp4 [--kampagne kampagne.json]
kampagne.json (alles optional): {"min_dauer": 15, "max_dauer": 45, "pflicht_hashtags": ["#gta6"],
                                 "pflicht_text": ["@kanal"], "verboten": ["Giveaway"]}
Die Kampagnenregeln muessen aus der Kampagnenseite abgeschrieben sein, hier wird nichts geraten.
"""
import argparse
import json
import os
import sys

import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # noetig bei python -I
import gemeinsam

SHORTS_TITEL_MAX = 100  # YouTube-Limit fuer Titel


def pruefe(info, meta, kampagne=None):
    """Gibt Liste (ok, text) zurueck."""
    k = kampagne or {}
    r = []

    def ok(bed, gut, schlecht):
        r.append((bool(bed), gut if bed else schlecht))

    ok((info["breite"], info["hoehe"]) == (1080, 1920), "Format 1080x1920",
       f"Format {info['breite']}x{info['hoehe']}, erwartet 1080x1920")
    lo, hi = k.get("min_dauer", 15), k.get("max_dauer", 45)
    ok(lo <= info["dauer"] <= hi + 0.5, f"Laenge {info['dauer']:.1f}s (erlaubt {lo}-{hi}s)",
       f"Laenge {info['dauer']:.1f}s ausserhalb {lo}-{hi}s")
    ok(info["codec"] == "h264", "Codec h264", f"Codec {info['codec']}, erwartet h264")
    ok(info["ton"], "Ton vorhanden", "kein Ton")
    ok(str(meta.get("erlaubt_durch", "")).strip(), f"Erlaubnis: {meta.get('erlaubt_durch')}",
       "erlaubt_durch fehlt: ohne Kampagne oder Rechteinhaber wird nicht geschnitten")
    ok(str(meta.get("hook", "")).strip(), "Hook vorhanden", "Hook fehlt")
    titel = meta.get("titel") or {}
    ok(isinstance(titel, dict) and titel, "Titel vorhanden", "Titel fehlt")
    if isinstance(titel, dict) and titel.get("shorts"):
        ok(len(titel["shorts"]) <= SHORTS_TITEL_MAX, "Shorts-Titel kurz genug",
           f"Shorts-Titel {len(titel['shorts'])} Zeichen, max {SHORTS_TITEL_MAX}")
    tags = meta.get("hashtags") or []
    ok(tags and all(t.startswith("#") and " " not in t for t in tags), f"{len(tags)} Hashtags",
       "Hashtags fehlen oder sind falsch geschrieben (#ohneLeerzeichen)")
    alles = (str(meta.get("hook", "")) + " " + json.dumps(titel, ensure_ascii=False) + " " + " ".join(tags)).lower()
    for t in k.get("pflicht_hashtags", []):
        ok(t.lower() in alles, f"Pflicht-Hashtag {t}", f"Pflicht-Hashtag {t} fehlt")
    for t in k.get("pflicht_text", []):
        ok(t.lower() in alles, f"Pflicht-Text {t}", f"Pflicht-Text {t} fehlt")
    for t in k.get("verboten", []):
        ok(t.lower() not in alles, f"'{t}' nicht verwendet", f"verbotenes Wort '{t}' kommt vor")
    return r


def main():
    p = argparse.ArgumentParser()
    p.add_argument("clip")
    p.add_argument("--kampagne")
    a = p.parse_args()
    mp = os.path.splitext(a.clip)[0] + ".meta.json"
    meta = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else {}
    kam = json.load(open(a.kampagne, encoding="utf-8")) if a.kampagne else None
    erg = pruefe(gemeinsam.ffprobe(a.clip), meta, kam)
    for gut, t in erg:
        print(("OK     " if gut else "FEHLER ") + t)
    schlecht = sum(1 for g, _ in erg if not g)
    print(f"\nErgebnis: {'ALLES OK' if not schlecht else str(schlecht) + ' Fehler'} - {os.path.basename(a.clip)}")
    return 1 if schlecht else 0


if __name__ == "__main__":
    sys.exit(main())
