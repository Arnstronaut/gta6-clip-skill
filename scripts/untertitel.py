"""Untertitel: Wort fuer Wort mit faster-whisper erkennen und ins Video einbrennen.

Beispiel: python untertitel.py --eingabe clip.mp4 --ausgabe clip_sub.mp4 [--sprache de] [--modell small]
Ohne erkannte Sprache wird das Video unveraendert kopiert und das klar gemeldet.
"""
import argparse
import os
import shutil
import subprocess
import sys

import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # noetig bei python -I
import gemeinsam

KOPF = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Wort,Arial,96,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,7,2,2,40,40,{margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ass_zeit(s):
    cs = int(round(s * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def woerter_zu_ass(woerter, margin_v=620):
    """woerter: Liste (start, ende, text). Jedes Wort ein eigener Eintrag, gross, in Grossbuchstaben.
    Ein Wort bleibt sichtbar, bis das naechste beginnt (maximal 0,8 s Luecke)."""
    zeilen = [KOPF.format(margin=margin_v)]
    for i, (s, e, t) in enumerate(woerter):
        t = t.strip().upper().replace("{", "").replace("}", "")
        if not t:
            continue
        ende = min(woerter[i + 1][0], e + 0.8) if i + 1 < len(woerter) else e
        ende = max(ende, e)
        zeilen.append(f"Dialogue: 0,{ass_zeit(s)},{ass_zeit(ende)},Wort,,0,0,0,,{t}\n")
    return "".join(zeilen)


def _audio(datei):
    """Ton per ffmpeg als 16-kHz-Mono-Zahlenfeld holen (unabhaengig von der PyAV-Version)."""
    import numpy as np
    roh = subprocess.run([gemeinsam.finde("ffmpeg", "GTA6_FFMPEG"), "-v", "error", "-i", str(datei), "-vn", "-ac", "1",
                          "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(roh, dtype=np.int16).astype(np.float32) / 32768.0


def erkenne(datei, sprache=None, modell="small"):
    from faster_whisper import WhisperModel  # erst hier, damit Tests ohne Whisper laufen
    audio = _audio(datei)
    for geraet, typ in (("auto", "auto"), ("cpu", "int8")):  # Grafikkarte kaputt/fehlt -> Prozessor
        try:
            m = WhisperModel(modell, device=geraet, compute_type=typ)
            segs, _ = m.transcribe(audio, language=sprache, word_timestamps=True, vad_filter=True)
            return [(w.start, w.end, w.word) for s in segs for w in (s.words or [])]
        except RuntimeError:
            if geraet == "cpu":
                raise


def brenne(eingabe, ausgabe, ass_datei):
    ordner, name = os.path.split(os.path.abspath(ass_datei))
    # relativer Dateiname + cwd, damit Windows-Pfade (C:\) im Filter nicht stoeren
    subprocess.run([gemeinsam.finde("ffmpeg", "GTA6_FFMPEG"), "-y", "-i", os.path.abspath(eingabe),
                    "-vf", f"ass={name}", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "copy", "-movflags", "+faststart", os.path.abspath(ausgabe)],
                   cwd=ordner, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--eingabe", required=True)
    p.add_argument("--ausgabe", required=True)
    p.add_argument("--sprache")
    p.add_argument("--modell", default="small")
    a = p.parse_args()
    if not gemeinsam.ffprobe(a.eingabe)["ton"]:
        woerter = []
    else:
        woerter = erkenne(a.eingabe, a.sprache, a.modell)
    if not woerter:
        shutil.copyfile(a.eingabe, a.ausgabe)
        print(f"KEINE SPRACHE erkannt - Video ohne Untertitel kopiert: {a.ausgabe}")
        return 0
    ass = os.path.splitext(a.ausgabe)[0] + ".ass"
    open(ass, "w", encoding="utf-8").write(woerter_zu_ass(woerter))
    brenne(a.eingabe, a.ausgabe, ass)
    print(f"fertig: {a.ausgabe} ({len(woerter)} Woerter)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
