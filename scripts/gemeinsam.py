"""Kleine gemeinsame Helfer fuer das GTA-6-Skill-Paket."""
import json
import os
import shutil
import subprocess
import sys

# Windows-Konsole kann sonst keine Emojis aus Titeln drucken.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def finde(name, env=None):
    """Pfad eines Programms: Umgebungsvariable, sonst PATH."""
    p = os.environ.get(env or "") if env else None
    return p or shutil.which(name) or name


def ytdlp_basis():
    cmd = [finde("yt-dlp", "GTA6_YTDLP")]
    if shutil.which("node"):
        cmd += ["--js-runtimes", "node"]
    return cmd


def sekunden(text):
    """'1:05', '00:01:05' oder '65' -> 65.0"""
    teile = [float(t) for t in str(text).split(":")]
    s = 0.0
    for t in teile:
        s = s * 60 + t
    return s


def hms(sek):
    sek = int(sek)
    return f"{sek // 3600:02d}:{sek % 3600 // 60:02d}:{sek % 60:02d}"


def ffprobe(datei):
    """Gibt Breite, Hoehe, Dauer, Ton (bool) und Codec zurueck."""
    out = subprocess.run(
        [finde("ffprobe", "GTA6_FFPROBE"), "-v", "error", "-print_format", "json",
         "-show_format", "-show_streams", str(datei)],
        capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), {})
    return {
        "breite": v.get("width"), "hoehe": v.get("height"),
        "dauer": float(d["format"].get("duration", 0)),
        "ton": any(s["codec_type"] == "audio" for s in d["streams"]),
        "codec": v.get("codec_name"),
    }
