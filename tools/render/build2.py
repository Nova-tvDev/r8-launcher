#!/usr/bin/env python3
"""build2.py — rendus Audi R8 pour le pack voiture « audi-r8 » (Blender 3.6+, à lancer en CLI).

Usage :
    blender -b -P tools/render/build2.py -- --fbx ./r8.fbx --out ./www/img/car --test
    blender -b -P tools/render/build2.py -- --fbx ./r8.fbx --out ./www/img/car

--test : rend 4 vues basse résolution pour validation AVANT le rendu complet.
Sans --test : 48 vues hero_XX.webp (720x402, fond transparent) + 6 étapes par
ouvrant (porte AVG, porte AVD, coffre avant).

Adapte les motifs OBJ_* ci-dessous à la hiérarchie de TON import (noms KeyShot/FBX
variables). Le script affiche toute la hiérarchie trouvée pour t'aider.
"""
import argparse
import os
import sys

# ---- À adapter à ton import ----
OBJ_PORTE_AVG = ("door_l", "porte_avg", "door_fl", "left_door")
OBJ_PORTE_AVD = ("door_r", "porte_avd", "door_fr", "right_door")
OBJ_COFFRE_AV = ("hood", "bonnet", "frunk", "capot")
BODY_MATS = ("paint", "carrosserie", "body")
R8_GREY = (0.827, 0.843, 0.867, 1.0)  # gris cool métallisé du pack par défaut

VIEWS = 48
STEPS = 6


def log_tree(obj, depth=0):
    print("  " * depth + obj.name + " (" + obj.type + ")")
    for c in obj.children:
        log_tree(c, depth + 1)


def find_by_names(root_objs, names):
    lowered = [n.lower() for n in names]
    for o in root_objs:
        n = o.name.lower()
        if any(k in n for k in lowered):
            return o
    return None


def all_objects():
    import bpy
    return list(bpy.data.objects)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--fbx", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--test", action="store_true")
    args = ap.parse_args(argv)

    import bpy
    import math

    for o in all_objects():
        bpy.data.objects.remove(o, do_unlink=True)

    bpy.ops.import_scene.fbx(filepath=args.fbx)
    print("=== Hiérarchie importée ===")
    for o in bpy.context.scene.objects:
        if o.parent is None:
            log_tree(o)

    imported = all_objects()
    porte_avg = find_by_names(imported, OBJ_PORTE_AVG)
    porte_avd = find_by_names(imported, OBJ_PORTE_AVD)
    coffre = find_by_names(imported, OBJ_COFFRE_AV)
    print("Porte AVG :", porte_avg.name if porte_avg else "NON TROUVÉE")
    print("Porte AVD :", porte_avd.name if porte_avd else "NON TROUVÉE")
    print("Coffre av:", coffre.name if coffre else "NON TROUVÉ")

    # Peinture R8 : teinte gris cool métallisé sur les matériaux de carrosserie
    for m in bpy.data.materials:
        if any(k in m.name.lower() for k in BODY_MATS) and m.use_nodes:
            for node in m.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    node.inputs["Base Color"].default_value = R8_GREY
                    if "Metallic" in node.inputs:
                        node.inputs["Metallic"].default_value = 0.9
                    if "Roughness" in node.inputs:
                        node.inputs["Roughness"].default_value = 0.35

    sc = bpy.context.scene
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "WEBP"
    sc.render.image_settings.color_mode = "RGBA"
    os.makedirs(args.out, exist_ok=True)

    cam_data = bpy.data.cameras.new("R8Cam")
    cam = bpy.data.objects.new("R8Cam", cam_data)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.location = (4.6, 0.0, 2.1)
    track = cam.constraints.new("TRACK_TO")
    track.target = next((o for o in imported if o.type == "MESH"), None)
    track.track_axis = "TRACK_NEGATIVE_Z"
    track.up_axis = "UP_Y"

    steps = 4 if args.test else VIEWS
    sc.render.resolution_x = 480 if args.test else 720
    sc.render.resolution_y = 268 if args.test else 402
    sc.render.resolution_percentage = 100

    movers = [(o, "porte_avg") for o in (porte_avg,) if o]
    movers += [(o, "porte_avd") for o in (porte_avd,) if o]
    movers += [(o, "frunk") for o in (coffre,) if o]

    # D'abord les étapes d'ouvrants (charnière = rotation Z progressive)
    for obj, tag in movers:
        rx, ry, rz = obj.rotation_euler
        for s in range(STEPS):
            obj.rotation_euler = (rx, ry, rz + (s / (STEPS - 1)) * 0.6)
            bpy.context.view_layer.update()
            sc.render.filepath = os.path.join(args.out, "%s_%d.webp" % (tag, s))
            bpy.ops.render.render(write_still=True)
        obj.rotation_euler = (rx, ry, rz)

    # Puis le plateau tournant (caméra orbite autour de la voiture)
    for i in range(steps):
        a = 2 * math.pi * i / steps
        cam.location = (4.6 * math.cos(a), 4.6 * math.sin(a), 2.1)
        bpy.context.view_layer.update()
        sc.render.filepath = os.path.join(args.out, "hero_%02d.webp" % i)
        bpy.ops.render.render(write_still=True)

    print("OK — images dans", args.out)


if __name__ == "__main__":
    main()
