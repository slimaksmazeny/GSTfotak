"""Zpracování snímku pro Waveshare 4" Spectra 6 (600 x 400 px)."""
import numpy as np
from PIL import Image, ImageEnhance, ImageOps

W, H = 600, 400
# Ideální barvy palety = barvy, které očekává ovladač epd4in0e (getbuffer).
# Skutečné pigmenty jsou tlumenější, proto před ditheringem zvyšujeme sytost.
PALETTE_S6 = [(0, 0, 0), (255, 255, 255), (255, 255, 0),
              (255, 0, 0), (0, 0, 255), (0, 255, 0)]

def prepare(img, saturation=1.4, contrast=1.2, gamma=0.9):
    img = ImageOps.exif_transpose(img).convert("RGB")
    img = ImageOps.fit(img, (W, H), Image.LANCZOS)          # ořez na střed 3:2
    img = ImageEnhance.Color(img).enhance(saturation)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    lut = [round(255 * (i / 255) ** gamma) for i in range(256)] * 3
    return img.point(lut)

def dither_fs(img, palette=PALETTE_S6):
    """Vlastní Floyd–Steinberg (chybová difuze) – srozumitelná verze do dokumentace.
    Pozor: čistý Python je na Pi Zero pomalý (desítky s) -> v produkci dither_fast()."""
    a = np.asarray(img, dtype=np.float32).copy()
    P = np.array(palette, dtype=np.float32)
    h, w, _ = a.shape
    out = np.zeros((h, w), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            old = a[y, x]
            i = int(np.argmin(((P - old) ** 2).sum(axis=1)))   # nejbližší barva
            out[y, x] = i
            err = old - P[i]                                     # chyba kvantizace
            if x + 1 < w:      a[y, x + 1]     += err * 7 / 16
            if y + 1 < h:
                if x > 0:      a[y + 1, x - 1] += err * 3 / 16
                a[y + 1, x]                    += err * 5 / 16
                if x + 1 < w:  a[y + 1, x + 1] += err * 1 / 16
    return Image.fromarray(np.array(palette, dtype=np.uint8)[out])

def dither_fast(img, palette=PALETTE_S6):
    """Stejný algoritmus v C uvnitř Pillow – rychlé (~1 s na Pi Zero 2 W)."""
    pal = Image.new("P", (1, 1))
    flat = [c for rgb in palette for c in rgb]
    pal.putpalette(flat + flat[:3] * (256 - len(palette)))
    return img.quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
