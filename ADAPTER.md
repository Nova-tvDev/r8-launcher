# ADAPTER.md — prompt « adapte-le à ma voiture » + marche à suivre

## Le prompt à donner à l'IA

Remplis les crochets, joins **ce dossier complet**, ton modèle 3D (ici : `r8.fbx` + textures),
ton journal et tes captures, puis envoie :

```
Tu vas adapter le projet Android « Car Launcher » (dossier joint) à ma voiture et à mon autoradio.
Lis d'abord README.md, ADAPTER.md, docs/CAN.md, CHANGELOG.txt et tools/render/README.md.

Mon autoradio : [marque, modèle, puce, Android, captures « À propos »]
Ma voiture : [Audi R8, année, 2 portes, couleur + code peinture, essence]
Boîtier / appli CAN : [nom de l'appli, profil choisi]
Fichiers joints : [journal exporté, APK CAN copiés, captures, modèle 3D]

Ce que je veux :
1. Réglages du véhicule dans app/src/main/assets/www/js/config.js (car.name, car.model,
   car.fuel) et nom de l'appli dans app/src/main/res/values/strings.xml.
2. Lecture CAN : analyse mon journal et les APK CAN (méthode décrite dans docs/CAN.md)
   pour lire portes, clignotants, vitesse et ordinateur de bord sur MON autoradio ;
   adapte CanBridge.java, CarText.java, LogCan.java et CanWatchService.java si le format
   diffère. Explique-moi ce qui est lu en direct et ce qui ne l'est pas.
3. Pack 3D (modèle fourni) : adapte tools/render/build2.py à mon modèle (pièces, découpage
   des portes, charnières, couleur de peinture), envoie-moi des images test et attends ma
   validation avant le rendu complet ; puis convertis en webp dans img/car ; génère les flux
   de rotation continue avec tools/render/flows.py (img/car/flow_XX.png, valeur flowMax) ;
   génère la vue du dessus avec tools/render/render_top.py (img/top, img/toph, valeur topBox) ;
   img/cockpit si je veux la vue poste de conduite ; puis règle config.js : carPack, topView,
   topBox, cockpit, hiView, comboAnim, doorViews, homeView, flowMax.
4. Vérifie que le JavaScript et le Java n'ont pas d'erreur, teste l'interface dans un
   navigateur, puis donne-moi le projet complet en zip et la liste de ce qui a changé.
Pose-moi une question à la fois si une info manque.
```

## Marche à suivre (résumé)

1. **config.js** : `car.name` (nom court, ex. « R8 »), `car.model` (ex. « Audi R8 coupé »),
   `car.fuel` (`"essence"` — les opérations d'entretien proposées en dépendent).
   `carPack` reste à `false` tant que le pack R8 n'est pas installé.
2. **CAN** : profil du boîtier dans l'autoradio, appli CAN choisie dans le lanceur
   (Réglages › Applis par défaut), `display door info` sur Open dans CarCan,
   autorisation accessibilité + `adb shell pm grant … READ_LOGS` pour le direct.
3. **Pack R8** : voir `tools/render/README.md`. Ordre : build2 → validation images test →
   rendu 48 vues → flows → render_top → `make_pack.py` → zip sur clé USB →
   Réglages › Voiture 3D › Pack voiture › Clé USB.
4. **Mise à jour** : nouveau dossier, reporter `config.js` + `img/car,top,toph,cockpit` +
   `keystore.properties`, compiler **avec la même clé**, installer par-dessus
   (Mettre à jour, jamais désinstaller — sinon carnet d'entretien perdu).
