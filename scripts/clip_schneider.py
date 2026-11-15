"""Clip-Schneider: Video ins Hochformat 1080x1920 (9:16) schneiden.

Mit Facecam:  --facecam x:y:w:h  (Bereich der Facecam im Original, in Pixeln) -> Facecam oben, Spiel unten.
Ohne Facecam: Spiel in der Mitte, Rand unscharf aufgefuellt.
Beispiel: python clip_schneider.py --eingabe quelle.mp4 --start 0:12 --dauer 30 --ausgabe clip.mp4
"""
import argparse
import subprocess
import sys

import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # noetig bei python -I
import gemeinsam

MAX_DAUER = 45.0


def filtergraph(facecam=None, spiel_mitte=0.5):
    if facecam:
        x, y, w, h = [int(v) for v in facecam.split(":")]
        return (f"[0:v]split=2[a][b];"
                f"[a]crop={w}:{h}:{x}:{y},scale=1080:720:force_original_aspect_ratio=increase,crop=1080:720[oben];"
                f"[b]scale=-2:1200,crop=1080:1200:(in_w-1080)*{spiel_mitte}:0[unten];"
                f"[oben][unten]vstack,setsar=1[v]")
    return ("[0:v]split=2[a][b];"
            "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5[bg];"
            "[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[v]")


def baue_befehl(eingabe, ausgabe, start, dauer, facecam=None, spiel_mitte=0.5):
    return [gemeinsam.finde("ffmpeg", "GTA6_FFMPEG"), "-y", "-ss", str(start), "-t", str(dauer), "-i", str(eingabe),
            "-filter_complex", filtergraph(facecam, spiel_mitte), "-map", "[v]", "-map", "0:a?",
            "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(ausgabe)]


def schneide(eingabe, ausgabe, start=0, dauer=30, facecam=None, spiel_mitte=0.5):
    dauer = float(dauer)
    if dauer > MAX_DAUER:
        raise ValueError(f"Dauer {dauer}s ist laenger als {MAX_DAUER:.0f}s")
    subprocess.run(baue_befehl(eingabe, ausgabe, start, dauer, facecam, spiel_mitte), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return ausgabe


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--eingabe", required=True)
    p.add_argument("--ausgabe", required=True)
    p.add_argument("--start", default="0")
    p.add_argument("--dauer", default="30")
    p.add_argument("--facecam")
    p.add_argument("--spiel-mitte", type=float, default=0.5, help="0 = links, 1 = rechts")
    a = p.parse_args()
    schneide(a.eingabe, a.ausgabe, gemeinsam.sekunden(a.start), a.dauer, a.facecam, a.spiel_mitte)
    print(f"fertig: {a.ausgabe}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
