"""Trend-Jaeger (nur Titel mit GTA 6 / GTA VI, mit --alle alles): oeffentliche YouTube-Videos zu GTA 6 der letzten 24 Stunden, nach Aufrufen sortiert.

Beispiel:
  python trend_jaeger.py --suche "GTA 6 clip" --suche "GTA 6 stream" --anzahl 10 --ausgabe gta6/trends.txt
Nur Kanaele aus einer Erlaubt-Liste (ein Name pro Zeile):  --erlaubt gta6/erlaubt.txt
Schon bearbeitete ueberspringen:                            --stand gta6/nacht-stand.json
Die Aufrufzahlen kommen direkt von YouTube. Es wird nichts geschaetzt oder erfunden.
"""
import argparse
import json
import re
import subprocess
import sys
from urllib.parse import quote_plus

import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # noetig bei python -I
import gemeinsam

# YouTube-Suchfilter: sortiert nach Aufrufen, hochgeladen heute (= letzte 24 Stunden)
FILTER_24H = "CAMSBAgCEAE%253D"


def suche(begriff, n):
    url = f"https://www.youtube.com/results?search_query={quote_plus(begriff)}&sp={FILTER_24H}"
    cmd = gemeinsam.ytdlp_basis() + ["--flat-playlist", "--playlist-end", str(n), "--dump-json", url]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    treffer = []
    for zeile in r.stdout.splitlines():
        try:
            d = json.loads(zeile)
        except ValueError:
            continue
        treffer.append({
            "id": d.get("id"), "titel": d.get("title") or "", "kanal": d.get("channel") or "",
            "aufrufe": d.get("view_count"), "dauer": d.get("duration"),
            "url": d.get("url") or f"https://www.youtube.com/watch?v={d.get('id')}",
        })
    return treffer


BEZUG = re.compile(r"gta\s?(6|vi)\b|grand theft auto (6|vi)\b", re.I)


def sortiere(treffer, erlaubt=(), schon=(), nur_gta6=True):
    """Doppelte raus, bearbeitete raus, optional nur erlaubte Kanaele, absteigend nach Aufrufen."""
    gesehen, aus = set(), []
    erl = [e.lower() for e in erlaubt]
    for t in treffer:
        if not t["id"] or t["id"] in gesehen or t["id"] in schon:
            continue
        if nur_gta6 and not BEZUG.search(t["titel"]):
            continue
        if erl and not any(e in t["kanal"].lower() for e in erl):
            continue
        gesehen.add(t["id"])
        aus.append(t)
    return sorted(aus, key=lambda t: t["aufrufe"] or 0, reverse=True)


def als_text(treffer):
    zeilen = ["# Trend-Jaeger: GTA 6, YouTube, hochgeladen in den letzten 24 Stunden", ""]
    for i, t in enumerate(treffer, 1):
        auf = f"{t['aufrufe']:,}".replace(",", ".") if t["aufrufe"] is not None else "offen"
        dauer = f"{int(t.get('dauer') // 60)}:{int(t.get('dauer') % 60):02d}" if t.get("dauer") else "offen"
        zeilen.append(f"{i:2d}. {auf:>10} Aufrufe | {dauer:>6} | {t['kanal']} | {t['titel']}")
        zeilen.append(f"    {t.get('url')}")
    zeilen += ["", "Hinweis: Aufrufe = Stand von YouTube beim Abruf. 'offen' = YouTube hat keine Zahl geliefert.",
               "Twitch-Clips: URL von Hand einfuegen, yt-dlp kann sie laden (Twitch-Suche gibt es hier nicht).",
               "Vor dem Schneiden pruefen: Darf ich diesen Kanal laut Kampagne verwenden?"]
    return "\n".join(zeilen)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--suche", action="append", help="Suchbegriff, mehrfach moeglich")
    p.add_argument("--anzahl", type=int, default=10)
    p.add_argument("--erlaubt", help="Datei mit erlaubten Kanalnamen")
    p.add_argument("--stand", help="JSON-Datei mit schon bearbeiteten IDs")
    p.add_argument("--alle", action="store_true", help="auch Titel ohne GTA 6")
    p.add_argument("--ausgabe")
    a = p.parse_args()
    begriffe = a.suche or ["GTA 6 clip"]
    alle = [t for b in begriffe for t in suche(b, a.anzahl)]
    erlaubt = [z.strip() for z in open(a.erlaubt, encoding="utf-8")] if a.erlaubt else []
    erlaubt = [e for e in erlaubt if e and not e.startswith("#")]
    schon = json.load(open(a.stand, encoding="utf-8")) if a.stand else []
    text = als_text(sortiere(alle, erlaubt, schon, not a.alle)[: a.anzahl])
    print(text)
    if a.ausgabe:
        import os
        os.makedirs(os.path.dirname(os.path.abspath(a.ausgabe)), exist_ok=True)
        open(a.ausgabe, "w", encoding="utf-8").write(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
