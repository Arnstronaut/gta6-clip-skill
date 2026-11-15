"""Hook-Text oben ins Bild einblenden (erste Sekunden), mit ffmpeg drawtext.

Beispiel: python hook_einblenden.py --eingabe clip.mp4 --text "HAST DU DAS GESEHEN?" --ausgabe clip_hook.mp4 [--sekunden 3]
"""
import argparse
import os
import subprocess
import sys
import tempfile
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # noetig bei python -I
import gemeinsam

SCHRIFTEN = ["C:/Windows/Fonts/arialbd.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def umbrechen(text, breite=18):
    return "\n".join(textwrap.wrap(text.strip(), breite))


def filter_text(textdatei, schrift, sekunden):
    f = schrift.replace(":", "\\:")
    return (f"drawtext=fontfile='{f}':textfile='{textdatei}':fontsize=76:fontcolor=white:borderw=7:bordercolor=black:"
            f"line_spacing=10:x=(w-text_w)/2:y=150:enable='lt(t,{sekunden})'")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--eingabe", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--ausgabe", required=True)
    p.add_argument("--sekunden", type=float, default=3)
    a = p.parse_args()
    schrift = next((s for s in SCHRIFTEN if os.path.exists(s)), None)
    if not schrift:
        print("FEHLER: keine Schriftdatei gefunden (Arial/DejaVu). Pfad in SCHRIFTEN ergaenzen.")
        return 1
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "hook.txt"), "w", encoding="utf-8").write(umbrechen(a.text))
        subprocess.run([gemeinsam.finde("ffmpeg", "GTA6_FFMPEG"), "-y", "-i", os.path.abspath(a.eingabe),
                        "-vf", filter_text("hook.txt", schrift, a.sekunden), "-c:v", "libx264", "-crf", "20",
                        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", os.path.abspath(a.ausgabe)],
                       cwd=d, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    print(f"fertig: {a.ausgabe}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
