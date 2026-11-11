#!/usr/bin/env python3
"""recolor.py — repeint un pack existant sans refaire les rendus.

Usage : python3 tools/render/recolor.py --pack ./pack-audi-r8 --color "#ffffff" --out ./pack-audi-r8-blanche
Teinte les hero_XX.webp + top/toph en conservant la luminance (la R8 de démo est grise,
donc la recolorisation est fidèle ; sur peinture d'origine colorée, convertir d'abord
en niveaux de gris lumineux).
"""
import argparse
import os

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def reteint(src, dst, rgb):
    im = Image.open(src).convert("RGBA")
    lum = im.convert("L").convert("RGB")
    teinte = Image.new("RGB", im.size, rgb)
    out = Image.blend(lum, teinte, 0.55)
    out.putalpha(im.split()[3])
    out.save(dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--color", required=True, help='ex. "#ffffff"')
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if not HAVE_PIL:
        raise SystemExit("pip install pillow")

    rgb = hex_rgb(args.color)
    n = 0
    for root, _, files in os.walk(args.pack):
        for f in files:
            if not f.endswith(".webp"):
                continue
            src = os.path.join(root, f)
            rel = os.path.relpath(src, args.pack)
            dst = os.path.join(args.out, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            reteint(src, dst, rgb)
            n += 1
    print("images repeintes :", n, "→", args.out)


if __name__ == "__main__":
    main()
