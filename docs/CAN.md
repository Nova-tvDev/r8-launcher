# docs/CAN.md — protocole et astuces CAN

## Ce qui est lu, et d'où

| Info | Source | Direct ? |
|---|---|---|
| Portes, coffre, clignotants, vitesse | Propriétés système Junsun `hcn.*` (firmware « hcn » : MT8163, RK3326…) | Oui, < 1 s |
| Portes (secours) | Fenêtre « display door info » de CarCan, lue par accessibilité | Oui, quelques s de retard |
| Carburant, batterie, température, km | Appli CarCan (ouverture éclair au démarrage) | Au démarrage |
| Ordinateur de bord en direct | Journal système Android (`READ_LOGS`, trames CAN recopiées par le MCU) | Oui, après `adb` |

## Propriétés Junsun « hcn » (lues par `CanBridge.java`, par réflexion sur `android.os.SystemProperties`)

```
hcn.door.fl / hcn.door.fr / hcn.door.rl / hcn.door.rr   0/1 (R8 : rl/rr toujours 0 — 2 portes)
hcn.door.trunk / hcn.door.hood                          0/1 (R8 : trunk = coffre AVANT)
hcn.light.turn_l / hcn.light.turn_r                     0/1
hcn.car.speed                                           km/h (entier)
```

Si ton poste n'a pas ces clés : exporte le journal et cherche les tiennes —
`CanBridge.java` a une table `PROP_FALLBACKS` prévue pour ça.

## CarCan + SimpleSoft (profil VW) — testé

- Profil CAN = marque du **boîtier** derrière l'autoradio, pas de la voiture.
  SimpleSoft + profil **VW SimpleSoft** : portes, coffre, clignotants, vitesse OK.
- Dans CarCan : laisser **display door info** sur **Open** (la fenêtre portes sert de
  2e source : `CarText.java` la lit via le service d'accessibilité).
- Ordinateur de bord : `CarText.java` parse la page infos véhicule ; le service
  `CanWatchService.java` garde une notification persistante pour ne pas être tué.

## Journal de diagnostic (`r8_diag.txt`)

Réglages › Diagnostic CAN › Vider le journal, puis moteur allumé : chaque porte une par
une (3 s entre gestes), coffre avant, clignotants G/D 5 s, feux, marche AR si radars,
puis **Exporter le journal** → `Android/data/fr.r8.launcher/files/r8_diag.txt`.
`LogCan.java` écrit aussi tout ce qui précède le dernier redémarrage (utile écran noir).

## Commandes utiles (PC, SDK Platform-Tools)

```
adb devices
adb shell pm grant fr.r8.launcher android.permission.READ_LOGS
adb push image.png /sdcard/Android/data/fr.r8.launcher/files/icons/
```

Accès refusé en accessibilité sur Android 13+ : Paramètres › Applis › R8 Launcher ›
menu ⋮ › **Autoriser les paramètres restreints**, puis réactiver le service.
