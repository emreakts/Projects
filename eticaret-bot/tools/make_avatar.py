"""EA Shopping bot profil animasyonu üretir.

E'nin orta çizgisi ve A'nın yatay çizgisi tek bir EKG (kalp atışı) hattıdır; parlak bir sinyal
bu hattın üzerinden soldan sağa geçer, harflerin arasında kalp atışı zirvesi yapar.

Çıktılar (eticaret-bot/assets/):
  avatar.mp4  Telegram animasyonlu profil fotoğrafı (640x640, 30 fps, 4 sn, H.264)
  avatar.gif  Önizleme
  avatar.jpg  Statik yedek (sinyalin zirvede olduğu kare)

Kullanım: python tools/make_avatar.py   (Pillow ve ffmpeg gerekir)
"""

from __future__ import annotations

import math
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent.parent / "assets"

SIZE = 640
SS = 2  # süper örnekleme: 2x çizip küçültünce kenarlar yumuşar
C = SIZE * SS
FPS = 30
DURATION = 4.0
FRAMES = int(FPS * DURATION)
SWEEP = 3.0  # sinyalin baştan sona geçiş süresi (sn); kalan süre sakin bekleme

BG_CENTER = (24, 33, 62)
BG_EDGE = (8, 11, 24)
LETTER = (245, 247, 252)
PULSE = (255, 59, 92)
GOLD = (245, 194, 107)

# Geometri (2x koordinatlar)
STROKE = 72
TOP, BOTTOM = 330, 760
MID = 575  # E orta çizgisi = A yatay çizgisi = EKG taban hattı
E_LEFT, E_RIGHT = 250, 520
A_LEFT, A_RIGHT = 650, 1030
A_APEX = (A_LEFT + A_RIGHT) / 2
LINE_W = 46
TRAIL = 520  # parlak kuyruk uzunluğu (px)

FONT_PATHS = [
    "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def ecg_points() -> list[tuple[float, float]]:
    """EKG hattı: E'nin içinden düz, harfler arasında QRS zirvesi, A'dan geçip T dalgası."""
    gap_l, gap_r = E_RIGHT + 10, A_LEFT + 20
    w = gap_r - gap_l
    pts = [(140, MID), (gap_l, MID)]
    pts += [
        (gap_l + w * 0.15, MID + 45),  # Q
        (gap_l + w * 0.40, MID - 300),  # R zirvesi
        (gap_l + w * 0.65, MID + 130),  # S
        (gap_l + w * 0.85, MID),
    ]
    pts.append((A_RIGHT + 30, MID))
    # T dalgası
    for i in range(1, 13):
        x = A_RIGHT + 30 + i * 8
        pts.append((x, MID - 55 * math.sin(math.pi * i / 12)))
    pts.append((1150, MID))
    return pts


def cumulative(pts: list[tuple[float, float]]) -> list[float]:
    dist = [0.0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dist.append(dist[-1] + math.hypot(x1 - x0, y1 - y0))
    return dist


def point_at(pts, dist, s: float) -> tuple[float, float]:
    s = max(0.0, min(dist[-1], s))
    for i in range(1, len(pts)):
        if dist[i] >= s:
            t = (s - dist[i - 1]) / ((dist[i] - dist[i - 1]) or 1)
            (x0, y0), (x1, y1) = pts[i - 1], pts[i]
            return (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
    return pts[-1]


def subpath(pts, dist, s0: float, s1: float) -> list[tuple[float, float]]:
    """Hattın [s0, s1] uzaklık aralığındaki parçası; ara köşeleri korur (az ve uzun segment)."""
    s0, s1 = max(0.0, s0), min(dist[-1], s1)
    if s1 <= s0:
        return []
    inner = [p for p, d in zip(pts, dist) if s0 < d < s1]
    return [point_at(pts, dist, s0), *inner, point_at(pts, dist, s1)]


def background() -> Image.Image:
    small = 160
    img = Image.new("RGB", (small, small))
    px = img.load()
    for y in range(small):
        for x in range(small):
            d = min(1.0, math.hypot(x - small / 2, y - small / 2) / (small * 0.62))
            px[x, y] = tuple(int(c + (e - c) * d) for c, e in zip(BG_CENTER, BG_EDGE))
    return img.resize((C, C), Image.BICUBIC)


def letters_mask() -> Image.Image:
    """E ve A'nın orta çizgileri hariç gövdeleri (orta çizgiyi EKG hattı çizer)."""
    m = Image.new("L", (C, C), 0)
    d = ImageDraw.Draw(m)
    # E
    d.rectangle([E_LEFT, TOP, E_LEFT + STROKE, BOTTOM], fill=255)
    d.rectangle([E_LEFT, TOP, E_RIGHT, TOP + STROKE], fill=255)
    d.rectangle([E_LEFT, BOTTOM - STROKE, E_RIGHT, BOTTOM], fill=255)
    # A: dış yamuk eksi iç üçgen (tek parça, tepesi düz)
    apex_w = STROKE * 0.95
    leg = STROKE * 1.2  # bacakların tabandaki yatay kalınlığı
    d.polygon([(A_LEFT, BOTTOM), (A_APEX - apex_w / 2, TOP), (A_APEX + apex_w / 2, TOP), (A_RIGHT, BOTTOM)], fill=255)
    slope = (A_APEX - apex_w / 2 - A_LEFT) / (BOTTOM - TOP)  # sol kenarın dx/dy oranı
    inner_apex_y = BOTTOM - (A_APEX - A_LEFT - leg) / slope
    d.polygon([(A_LEFT + leg, BOTTOM + 1), (A_APEX, inner_apex_y), (A_RIGHT - leg, BOTTOM + 1)], fill=0)
    return m


def shopping_text() -> Image.Image:
    font = next((ImageFont.truetype(p, 104) for p in FONT_PATHS if Path(p).exists()), ImageFont.load_default())
    text, spacing = "SHOPPING", 26
    widths = [font.getbbox(ch)[2] - font.getbbox(ch)[0] for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    layer = Image.new("RGBA", (C, C), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = (C - total) / 2, 845
    for ch, w in zip(text, widths):
        d.text((x - font.getbbox(ch)[0], y), ch, font=font, fill=GOLD + (255,))
        x += w + spacing
    return layer


def draw_polyline(d: ImageDraw.ImageDraw, pts, color, width) -> None:
    d.line(pts, fill=color, width=width, joint="curve")
    r = width / 2
    for x, y in (pts[0], pts[-1]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def render(head: float, beat: float, static: dict) -> Image.Image:
    """head: sinyal başının hattaki konumu (px); beat: 0-1 kalp atışı parlaklığı."""
    pts, dist = static["pts"], static["dist"]
    img = static["bg"].copy().convert("RGBA")

    # Harfler: atışta hafif parıltı
    glow_alpha = int(70 + 110 * beat)
    glow = Image.new("RGBA", (C, C), LETTER + (0,))
    glow.putalpha(static["letters_blur"].point(lambda v: v * glow_alpha // 255))
    img.alpha_composite(glow)
    letters = Image.new("RGBA", (C, C), LETTER + (255,))
    letters.putalpha(static["letters"])
    img.alpha_composite(letters)

    # Sönük taban hattı (harfler her an E ve A olarak okunsun)
    base = Image.new("RGBA", (C, C), (0, 0, 0, 0))
    draw_polyline(ImageDraw.Draw(base), pts, PULSE + (110,), LINE_W)
    img.alpha_composite(base)

    # Parlak sinyal: kuyruktan başa doğru parçalar halinde, giderek parlaklaşan
    sig = Image.new("RGBA", (C, C), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sig)
    chunks = 24
    drawn = False
    for k in range(chunks):
        s0 = head - TRAIL + TRAIL * k / chunks
        part = subpath(pts, dist, s0, s0 + TRAIL / chunks + 2)
        if len(part) < 2:
            continue
        a = (k + 1) / chunks
        col = tuple(int(c + (255 - c) * a * 0.55) for c in PULSE) + (int(255 * a),)
        draw_polyline(sd, part, col, LINE_W + 4)
        drawn = True
    if drawn and head <= dist[-1]:
        hx, hy = point_at(pts, dist, head)
        r = LINE_W * 0.85
        sd.ellipse([hx - r, hy - r, hx + r, hy + r], fill=(255, 235, 240, 255))
    halo = sig.filter(ImageFilter.GaussianBlur(26))
    img.alpha_composite(halo)
    img.alpha_composite(halo)
    img.alpha_composite(sig)

    img.alpha_composite(static["text"])
    return img.convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)


def main() -> None:
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg bulunamadı")
    OUT.mkdir(parents=True, exist_ok=True)

    pts = ecg_points()
    dist = cumulative(pts)
    total = dist[-1]
    peak_s = dist[min(range(len(pts)), key=lambda i: pts[i][1])]
    letters = letters_mask()
    static = {
        "pts": pts,
        "dist": dist,
        "bg": background(),
        "letters": letters,
        "letters_blur": letters.filter(ImageFilter.GaussianBlur(22)),
        "text": shopping_text(),
    }

    peak_frame = 0
    with tempfile.TemporaryDirectory() as tmp:
        for f in range(FRAMES):
            t = f / FPS
            head = (t / SWEEP) * (total + TRAIL) if t < SWEEP else total + TRAIL + 1
            # Atış: sinyal zirveyi geçtikten sonra kısa süre parlayıp söner
            since_peak = (head - peak_s) / (total + TRAIL) * SWEEP
            beat = math.exp(-((since_peak - 0.08) / 0.12) ** 2) if 0 <= since_peak < 0.6 else 0.0
            if beat > 0.95 and not peak_frame:
                peak_frame = f
            render(head, beat, static).save(f"{tmp}/f{f:03d}.png")

        ff = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/f%03d.png"]
        subprocess.run(
            ff + ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", str(OUT / "avatar.mp4")],
            check=True,
        )
        subprocess.run(
            ff
            + [
                "-vf",
                "fps=20,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=4",
                "-loop",
                "0",
                str(OUT / "avatar.gif"),
            ],
            check=True,
        )
        Image.open(f"{tmp}/f{peak_frame:03d}.png").save(OUT / "avatar.jpg", quality=92)

    (OUT / "avatar_main_frame.txt").write_text(f"{peak_frame / FPS:.2f}\n")
    print(f"Tamam: {OUT} (zirve karesi {peak_frame / FPS:.2f} sn)")


if __name__ == "__main__":
    main()
