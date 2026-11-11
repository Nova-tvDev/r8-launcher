/* config.js — ★ LE FICHIER À RÉGLER (nom, modèle, carburant, pack R8).
   R8 d'origine : 2 portes, essence, pack « audi-r8 » dès qu'il est installé. */
window.R8_CONFIG = {
  "car": {"name": "R8", "model": "Audi R8 coupé", "fuel": "essence"},
  "carPack": false,          // true dès que le pack audi-r8 est installé (ne pas forcer avant)
  "topView": true,           // vue du dessus (radars + ouvrants)
  "topBox": [0.10, 0.06, 0.90, 0.94],  // R8 basse et large : boîte large
  "cockpit": false,          // true si img/cockpit présent (vidéo d'entrée habitacle)
  "hiView": false,
  "comboAnim": ["avg", "avd", "frunk"],  // pas de portes arrière sur la R8
  "doorViews": {"avg": "door_avg", "avd": "door_avd", "frunk": "frunk"},
  "homeView": "hero",
  "flowMax": 0,              // renseigné par tools/render/flows.py (rotation fluide)
  "unit": {"speed": "km/h", "temp": "°C", "fuel": "%"},
  "entretien": [
    {"titre": "Vidange + filtre à huile", "quand": "tous les 15 000 km"},
    {"titre": "Filtres air / habitacle", "quand": "tous les 2 ans"},
    {"titre": "Plaquettes + disques", "quand": "contrôle annuel"},
    {"titre": "Liquide de frein", "quand": "tous les 2 ans"},
    {"titre": "CT", "quand": "selon date"}
  ]
};
