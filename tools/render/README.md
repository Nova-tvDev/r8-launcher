# tools/render — pipeline 3D Audi R8 (Blender 3.6+)

Fabrique les images du **pack voiture « audi-r8 »** à partir de ton modèle
(`r8.fbx` + `r8.mtl` + textures décompressées à côté).

## Ordre de travail

1. `build2.py` — importe le FBX, sépare **porte AVG / porte AVD / coffre avant**,
   pose les pivots de charnière, peinture gris cool métallisé, plateau tournant,
   rend les **48 vues** `hero_XX.webp` (720×402, fond transparent) + **6 étapes**
   par ouvrant (`door_avg_0..5`, `door_avd_0..5`, `frunk_0..5`).
   → Envoie les images test à l'utilisateur, attends sa validation.
2. `flows.py` — flux optique entre vues → `flow_00.png … flow_47.png` + valeur `flowMax`
   (rotation fluide ; sans eux le lanceur fait un simple fondu).
3. `render_top.py` — vue du dessus radars/ouvrants → `img/top`, `img/toph` + `topBox`.
4. `recolor.py` — repeint un pack existant (ex. gris → blanc) sans refaire les rendus.
5. `../pack/make_pack.py` — assemble le `.zip` installable par clé USB.

## Spécificités R8 (2 portes, moteur central arrière)

- Pas de portes arrière : `comboAnim` ne combine que AVG + AVD + coffre avant.
- Le « coffre » logique = le **coffre avant** ; la vitre moteur arrière ne s'anime pas.
- Voiture basse et large : `topBox` plus large que la berline d'exemple (voir render_top.py).
- Adapte les noms d'objets (`OBJ_PORTE_AVG`, … en tête de build2.py) à TON import —
  les noms KeyShot/FBX varient ; le script loggue la hiérarchie trouvée.
- Vérifie la **licence de ton modèle 3D** avant de diffuser les rendus.
