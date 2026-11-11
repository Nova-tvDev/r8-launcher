# Car Launcher — édition Audi R8

Launcher façon CarPlay pour autoradio Android : voiture 3D qui ouvre ses portes en direct,
ordinateur de bord, carnet d'entretien en PDF, alertes de sécurité.

Réglé d'origine pour : **Audi R8 coupé, 2 portes, essence** (au lieu de la voiture de la vidéo).
Interface, applis, musique et entretien marchent sur **tout autoradio Android 6+**.
Portes / clignotants / vitesse / ordinateur de bord : voir `docs/CAN.md` (matériel testé :
Junsun firmware « hcn », appli CarCan, boîtier SimpleSoft profil VW — sinon adaptation via IA).

## Contenu du dossier

```
CarLauncher-R8/
├── README.md                  — ce fichier
├── ADAPTER.md                 — le prompt + la marche à suivre (donne-le à une IA avec ce dossier)
├── CHANGELOG.txt              — historique des versions
├── docs/CAN.md                — protocole et astuces CAN
├── tools/render/              — pipeline Blender 3D (R8) : build2.py, flows.py, render_top.py, recolor.py
├── tools/pack/make_pack.py    — fabrique un pack voiture .zip installable sans recompiler
└── app/                       — le lanceur (Android Studio : Java + interface web)
    └── src/main/assets/www/
        ├── index.html          — l'interface (autonome, zéro dépendance en roulage)
        ├── js/config.js        — ★ LE FICHIER À RÉGLER : nom, modèle, carburant, pack R8
        └── img/                — pack voiture R8 (rendus) + aperçu
```

## Démarrage rapide

1. Ouvre `app/` dans Android Studio (dossier avec `settings.gradle`), laisse Gradle synchroniser.
2. Règle `app/src/main/assets/www/js/config.js` (nom, modèle, `fuel: "essence"`).
3. Sans pack R8 : le lanceur marche, la carte Véhicule affiche « Pack voiture non installé ».
   Avec pack : voir `tools/render/README.md` puis `make_pack.py`.
4. Compile l'APK (Build › Generate APKs), copie sur clé USB, installe sur l'autoradio,
   choisis **R8 Launcher** comme écran d'accueil (HOME).
5. Autorisations : lanceur par défaut, accès notifications (média), lecture CAN
   (accessibilité), fenêtre par-dessus les apps.
