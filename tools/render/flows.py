#!/usr/bin/env python3
"""flows.py — rotation fluide : génère flow_XX.png entre les vues hero (Farnebäck / PIL).

Usage : python3 tools/render/flows.py --img ./www/img/car [--max 47]
Écrit flow_00.png … flow_47.png + affiche la valeur flowMax pour config.js.
Sans OpenCV : mode dégradé (copie hero suivante) — le lanceur fera un fondu.
"""
import argparse
import os
import shutil

try:
    import cv2
    import numpy as np
    HAVE_CV2 = True
except ImportError:
    HAVE_CV2 = False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--img", required=True, help="dossier avec hero_XX.webp")
    ap.add_argument("--max", type=int, default=47)
    args = ap.parse_args()

    flows = 0
    for i in range(args.max + 1):
        a = os.path.join(args.img, "hero_%02d.webp" % i)
        b = os.path.join(args.img, "hero_%02d.webp" % ((i + 1) % (args.max + 1)))
        out = os.path.join(args.img, "flow_%02d.png" % i)
        if not (os.path.exists(a) and os.path.exists(b)):
            continue
        if HAVE_CV2:
            ia = cv2.imread(a, cv2.IMREAD_GRAYSCALE)
            ib = cv2.imread(b, cv2.IMREAD_GRAYSCALE)
            if ia is None or ib is None:
                continue
            if ia.shape != ib.shape:
                ib = cv2.resize(ib, (ia.shape[1], ia.shape[0]))
            flow = cv2.calcOpticalFlowFarneback(ia, ib, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            cv2.imwrite(out, (255 * mag / max(mag.max(), 1e-6)).astype("uint8"))
        else:
            shutil.copy(b, out)
        flows += 1

    print("flows écrits :", flows)
    print('config.js → "flowMax": %d (mode %s)' % (flows, "optique" if HAVE_CV2 else "dégradé/fondu"))


if __name__ == "__main__":
    main()
