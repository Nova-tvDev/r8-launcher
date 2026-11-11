#!/usr/bin/env python3
"""make_pack.py — assemble un pack voiture .zip installable sans recompiler.

Usage :
    python3 tools/pack/make_pack.py --www app/src/main/assets/www --id audi-r8 --name "Audi R8"
Produit : <id>.zip (pack.json + img/car + img/top + img/toph + img/cockpit si présent).
Installation : zip à la racine d'une clé USB → Réglages › Voiture 3D › Pack voiture › Clé USB.
"""
import argparse
import json
import os
import zipfile

IMG_DIRS = ("img/car", "img/top", "img/toph", "img/cockpit")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--www", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--name", required=True)
    args = ap.parse_args()

    files = []
    for d in IMG_DIRS:
        full = os.path.join(args.www, d)
        if not os.path.isdir(full):
            continue
        for f in sorted(os.listdir(full)):
            if f.startswith("."):
                continue
            files.append(d + "/" + f)

    if not any(f.startswith("img/car/hero_") for f in files):
        raise SystemExit("aucune vue hero_XX dans img/car — lance build2.py d'abord")

    pack = {"id": args.id, "name": args.name, "version": 1, "files": files}
    out = args.id + ".zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("pack.json", json.dumps(pack, indent=2))
        for f in files:
            z.write(os.path.join(args.www, f), f)
    print("pack écrit :", out, "(%d fichiers)" % len(files))


if __name__ == "__main__":
    main()
