"""gta6-los (Technik-Teil): Stelle laden -> 9:16 schneiden -> Untertitel -> meta.json anlegen.
Hook, Titel und Hashtags schreibt Claude danach in die meta.json (siehe Befehl gta6-los), dann Regel-Check.
LAEDT NICHTS HOCH und meldet sich nirgends an.

Beispiel:
  python gta6_los.py --url https://www.youtube.com/watch?v=ID --start 1:20 --dauer 30 \
      --erlaubt "Kampagne XY, Regeln am 15.11. gelesen" --arbeitsordner gta6
Lokale Datei statt URL geht auch (--url C:\\pfad\\video.mp4).
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # noetig bei python -I
import clip_schneider
import gemeinsam
import untertitel


def lade(url, start, dauer, quelle_dir):
    """Laedt nur den Ausschnitt. Gibt (Datei, id) zurueck. Lokale Dateien werden nicht geladen."""
    if os.path.exists(url):
        return os.path.abspath(url), os.path.splitext(os.path.basename(url))[0], start
    os.makedirs(quelle_dir, exist_ok=True)
    abschnitt = f"*{gemeinsam.hms(start)}-{gemeinsam.hms(start + dauer)}"
    cmd = gemeinsam.ytdlp_basis() + [
        "--download-sections", abschnitt,
        "-f", "bv*[height<=1080]+ba/b", "--merge-output-format", "mp4", "--no-playlist",
        "-o", os.path.join(quelle_dir, "%(id)s.%(ext)s"), "--print", "after_move:filepath", url]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    pfad = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    if r.returncode or not os.path.exists(pfad):
        raise RuntimeError("Download fehlgeschlagen:\n" + r.stderr[-800:])
    return pfad, os.path.splitext(os.path.basename(pfad))[0], 0.0  # Ausschnitt beginnt bei 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    p.add_argument("--start", default="0")
    p.add_argument("--dauer", type=float, default=30)
    p.add_argument("--erlaubt", required=True, help="Wer erlaubt das? (Kampagne/Rechteinhaber). Pflicht.")
    p.add_argument("--facecam")
    p.add_argument("--sprache")
    p.add_argument("--modell", default="small")
    p.add_argument("--arbeitsordner", default="gta6")
    p.add_argument("--ziel", help="Standard: <arbeitsordner>/morgen")
    p.add_argument("--stand", help="JSON mit bearbeiteten IDs (Nacht-Modus)")
    a = p.parse_args()
    if not a.erlaubt.strip():
        print("ABBRUCH: --erlaubt darf nicht leer sein.")
        return 2
    ziel = a.ziel or os.path.join(a.arbeitsordner, "morgen")
    os.makedirs(ziel, exist_ok=True)
    start = gemeinsam.sekunden(a.start)
    datei, vid, schnitt_start = lade(a.url, start, a.dauer, os.path.join(a.arbeitsordner, "quelle"))
    if os.path.exists(a.url):
        schnitt_start = start
    name = re.sub(r"[^A-Za-z0-9_-]", "", vid)[:40] or "clip"
    roh = os.path.join(ziel, name + "_roh.mp4")
    clip_schneider.schneide(datei, roh, schnitt_start, a.dauer, a.facecam)
    fertig = os.path.join(ziel, name + ".mp4")
    sprache = untertitel.erkenne(roh, a.sprache, a.modell) if gemeinsam.ffprobe(roh)["ton"] else []
    if sprache:
        ass = os.path.join(ziel, name + ".ass")
        open(ass, "w", encoding="utf-8").write(untertitel.woerter_zu_ass(sprache))
        untertitel.brenne(roh, fertig, ass)
    else:
        os.replace(roh, fertig)
        print("Hinweis: keine Sprache erkannt, Clip ohne Untertitel.")
    if os.path.exists(roh):
        os.remove(roh)
    meta = {"quelle": a.url, "ausschnitt": f"{gemeinsam.hms(start)} + {a.dauer:.0f}s", "erlaubt_durch": a.erlaubt,
            "untertitel": bool(sprache), "hook": "", "hook_vorschlaege": [], "titel": {}, "hashtags": []}
    open(os.path.join(ziel, name + ".meta.json"), "w", encoding="utf-8").write(
        json.dumps(meta, ensure_ascii=False, indent=2))
    if a.stand:
        alt = json.load(open(a.stand, encoding="utf-8")) if os.path.exists(a.stand) else []
        json.dump(alt + [vid], open(a.stand, "w", encoding="utf-8"))
    print(f"FERTIG: {fertig}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
