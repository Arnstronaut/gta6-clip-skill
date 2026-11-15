import json
import os
import re
import subprocess
import sys

import pytest

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "scripts"))

import clip_schneider  # noqa: E402
import gemeinsam  # noqa: E402
import hook_einblenden  # noqa: E402
import regelcheck  # noqa: E402
import trend_jaeger  # noqa: E402
import untertitel  # noqa: E402

SKILLS = ["kampagnen-finder", "trend-jaeger", "clip-schneider", "untertitel", "hook-schreiber",
          "titel-hashtags", "regel-check", "nacht-modus"]


def test_manifeste():
    p = json.load(open(os.path.join(WURZEL, ".claude-plugin", "plugin.json"), encoding="utf-8"))
    m = json.load(open(os.path.join(WURZEL, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
    assert p["name"] == "gta6-clip-skill" and m["name"] == "gta6-clip-skill"
    assert m["plugins"][0]["name"] == "gta6-clip-skill"


@pytest.mark.parametrize("name", SKILLS)
def test_skill_datei(name):
    text = open(os.path.join(WURZEL, "skills", "gta6-" + name, "SKILL.md"), encoding="utf-8").read()
    kopf = re.match(r"---\n(.*?)\n---\n", text, re.S).group(1)
    assert f"name: gta6-{name}" in kopf
    assert re.search(r"^description: .{40,}", kopf, re.M)


def test_genau_acht_skills_und_befehl():
    ordner = [d for d in os.listdir(os.path.join(WURZEL, "skills"))]
    assert len(ordner) == 8
    assert os.path.exists(os.path.join(WURZEL, "commands", "gta6-los.md"))


def test_trend_filter_sortierung_und_stand():
    t = [
        {"id": "a", "titel": "GTA 6 Clip", "kanal": "Eins", "aufrufe": 10, "dauer": 60, "url": "u"},
        {"id": "b", "titel": "GTA 5 Clip", "kanal": "Zwei", "aufrufe": 999},
        {"id": "c", "titel": "Grand Theft Auto VI leak", "kanal": "Drei", "aufrufe": 500},
        {"id": "c", "titel": "Grand Theft Auto VI leak", "kanal": "Drei", "aufrufe": 500},
        {"id": "d", "titel": "gta vi", "kanal": "Vier", "aufrufe": None, "dauer": None, "url": "u"},
    ]
    assert [x["id"] for x in trend_jaeger.sortiere(t)] == ["c", "a", "d"]
    assert [x["id"] for x in trend_jaeger.sortiere(t, schon=["c"])] == ["a", "d"]
    assert [x["id"] for x in trend_jaeger.sortiere(t, erlaubt=["eins"])] == ["a"]
    assert [x["id"] for x in trend_jaeger.sortiere(t, erlaubt=["  EINS "])] == ["a"]
    # leere Liste erlaubt nichts (frueher: alles)
    assert trend_jaeger.sortiere(t, erlaubt=[]) == []
    # Teilstuecke reichen nicht (frueher: "ei" passte auf "Eins" und "Drei")
    assert trend_jaeger.sortiere(t, erlaubt=["ei"]) == []
    assert "offen" in trend_jaeger.als_text(trend_jaeger.sortiere(t))  # fehlende Zahl bleibt "offen"


def test_untertitel_ass_wort_fuer_wort():
    ass = untertitel.woerter_zu_ass([(0.0, 0.4, "Hello"), (0.5, 0.9, "world"), (5.0, 5.3, "end")])
    zeilen = [z for z in ass.splitlines() if z.startswith("Dialogue")]
    assert len(zeilen) == 3 and zeilen[0].endswith(",HELLO") and "0:00:00.00,0:00:00.50" in zeilen[0]
    assert "0:00:05.30" in zeilen[2]
    assert untertitel.ass_zeit(3725.5) == "1:02:05.50"


def test_filtergraph_und_dauergrenze(tmp_path):
    assert "vstack" in clip_schneider.filtergraph("0:0:400:300")
    assert "boxblur" in clip_schneider.filtergraph()
    with pytest.raises(ValueError):
        clip_schneider.schneide("x.mp4", tmp_path / "y.mp4", 0, 46)


def test_schnitt_echt_1080x1920(tmp_path):
    quelle = tmp_path / "q.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc=size=1280x720:rate=30:duration=3",
                    "-f", "lavfi", "-i", "sine=frequency=440:duration=3", "-shortest", "-pix_fmt", "yuv420p",
                    str(quelle)], check=True, capture_output=True)
    for fc in (None, "0:0:320:180"):
        ziel = tmp_path / f"z{bool(fc)}.mp4"
        clip_schneider.schneide(quelle, ziel, 0, 2, fc)
        i = gemeinsam.ffprobe(ziel)
        assert (i["breite"], i["hoehe"], i["codec"], i["ton"]) == (1080, 1920, "h264", True)


def test_regelcheck():
    gut = {"breite": 1080, "hoehe": 1920, "dauer": 30.0, "codec": "h264", "ton": True}
    meta = {"erlaubt_durch": "Kampagne X", "hook": "Hook", "titel": {"shorts": "GTA 6 Test"}, "hashtags": ["#gta6"]}
    assert all(ok for ok, _ in regelcheck.pruefe(gut, meta))
    # ohne Erlaubnis, falsches Format, zu lang, zu langer Shorts-Titel, Pflicht-Hashtag fehlt
    schlecht = dict(gut, breite=1920, hoehe=1080, dauer=60.0)
    meta2 = dict(meta, erlaubt_durch="", titel={"shorts": "x" * 101})
    texte = [t for ok, t in regelcheck.pruefe(schlecht, meta2, {"pflicht_hashtags": ["#kampagne"]}) if not ok]
    assert len(texte) == 5
    assert any("erlaubt_durch" in t for t in texte)


def test_hook_einblenden_uebernimmt_meta(tmp_path):
    quelle = tmp_path / "c.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc=size=1080x1920:rate=30:duration=2",
                    "-f", "lavfi", "-i", "sine=frequency=440:duration=2", "-shortest", "-pix_fmt", "yuv420p",
                    str(quelle)], check=True, capture_output=True)
    meta = {"erlaubt_durch": "Kampagne X", "hook": "", "titel": {"shorts": "GTA 6 Test"}, "hashtags": ["#gta6"]}
    (tmp_path / "c.meta.json").write_text(json.dumps(meta), encoding="utf-8")
    ziel = tmp_path / "c_hook.mp4"
    r = subprocess.run([sys.executable, os.path.join(WURZEL, "scripts", "hook_einblenden.py"), "--eingabe", str(quelle),
                        "--text", "Warte bis zum Ende", "--ausgabe", str(ziel)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    neu = json.loads((tmp_path / "c_hook.meta.json").read_text(encoding="utf-8"))
    assert neu["hook"] == "Warte bis zum Ende" and neu["hook_im_bild"] is True
    assert neu["erlaubt_durch"] == "Kampagne X"
    gut = {"breite": 1080, "hoehe": 1920, "dauer": 30.0, "codec": "h264", "ton": True}
    assert all(ok for ok, _ in regelcheck.pruefe(gut, neu))
    assert gemeinsam.ffprobe(ziel)["hoehe"] == 1920
    # vorhandener Hook bleibt stehen; ohne Quell-meta passiert nichts
    (tmp_path / "c.meta.json").write_text(json.dumps(dict(meta, hook="Alt")), encoding="utf-8")
    assert json.load(open(hook_einblenden.meta_uebernehmen(str(quelle), str(ziel), "Neu")))["hook"] == "Alt"
    assert hook_einblenden.meta_uebernehmen(str(tmp_path / "x.mp4"), str(ziel), "Neu") is None


def test_trend_jaeger_erlaubt_datei(tmp_path):
    skript = os.path.join(WURZEL, "scripts", "trend_jaeger.py")
    nur_kommentar = tmp_path / "erlaubt.txt"
    nur_kommentar.write_text("# nur ein Kommentar\n\n", encoding="utf-8")
    r = subprocess.run([sys.executable, skript, "--erlaubt", str(nur_kommentar)], capture_output=True, text=True)
    assert r.returncode == 0 and "Nichts erlaubt" in r.stdout and "watch?v=" not in r.stdout
    r = subprocess.run([sys.executable, skript, "--erlaubt", str(tmp_path / "fehlt.txt")], capture_output=True, text=True)
    assert r.returncode == 1 and "ABBRUCH" in r.stdout
