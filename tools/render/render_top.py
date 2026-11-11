#!/usr/bin/env python3
"""render_top.py — vue du dessus R8 (radars + ouvrants), Blender 3.6+ en CLI.

Usage : blender -b -P tools/render/render_top.py -- --fbx ./r8.fbx --out ./www/img
Écrit top/top_XX.webp (fond transparent) + toph/toph_XX.webp (fond sombre radar)
et affiche topBox (voiture basse et large : BOX plus large que la berline d'exemple).

États rendus par combinaison : fermé, avg, avd, avg+avd, frunk, tout ouvert.
"""
import argparse
import os
import sys

COMBOS = {
    "closed": (),
    "avg": ("avg",),
    "avd": ("avd",),
    "avg_avd": ("avg", "avd"),
    "frunk": ("frunk",),
    "all": ("avg", "avd", "frunk"),
}


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--fbx", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    import bpy

    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.import_scene.fbx(filepath=args.fbx)
    imported = list(bpy.data.objects)

    def pick(*keys):
        for o in imported:
            if any(k in o.name.lower() for k in keys):
                return o
        return None

    parts = {
        "avg": pick("door_l", "porte_avg", "door_fl", "left_door"),
        "avd": pick("door_r", "porte_avd", "door_fr", "right_door"),
        "frunk": pick("hood", "bonnet", "frunk", "capot"),
    }
    base_rot = {k: (o.rotation_euler[:] if o else None) for k, o in parts.items()}

    sc = bpy.context.scene
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "WEBP"
    sc.render.resolution_x, sc.render.resolution_y = 512, 512

    cam = bpy.data.objects.new("TopCam", bpy.data.cameras.new("TopCam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.location = (0, 0, 7.5)
    cam.rotation_euler = (0, 0, 0)
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 5.2  # R8 basse et large : cadrer large

    top = os.path.join(args.out, "top")
    toph = os.path.join(args.out, "toph")
    os.makedirs(top, exist_ok=True)
    os.makedirs(toph, exist_ok=True)

    for name, openers in COMBOS.items():
        for k, o in parts.items():
            if o and base_rot[k]:
                rx, ry, rz = base_rot[k]
                o.rotation_euler = (rx, ry, rz + (0.6 if k in openers else 0.0))
        bpy.context.view_layer.update()
        sc.render.filepath = os.path.join(top, "top_%s.webp" % name)
        bpy.ops.render.render(write_still=True)
        sc.render.filepath = os.path.join(toph, "toph_%s.webp" % name)
        bpy.ops.render.render(write_still=True)

    print("OK — top/ + toph/ dans", args.out)
    print('config.js → "topView": true, "topBox": [0.10, 0.06, 0.90, 0.94]')


if __name__ == "__main__":
    main()
