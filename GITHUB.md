# GITHUB.md — pousser le projet sur GitHub et le déployer (APK + démo web)

Le dossier `CarLauncher-R8/` **est** la racine du futur repo : pousse son **contenu**
(pas le dossier lui-même) à la racine d'un repo GitHub. Deux workflows YAML compilent
et déploient tout le projet à chaque push.

## 1. Créer le repo et pousser

```bash
cd CarLauncher-R8
git init
git add .
git commit -m "R8 Launcher 1.0"
git branch -M main
git remote add origin https://github.com/TON-COMPTE/TON-REPO.git
git push -u origin main
```

## 2. Activer les workflows (OBLIGATOIRE, une fois)

GitHub n'exécute que `.github/workflows/*.yml`. Les fichiers sont fournis dans
`github-workflows/` (repli : les dossiers pointés sont interdits dans l'éditeur).
Déplace-les — Windows (PowerShell) :

```powershell
mkdir .github\workflows
copy github-workflows\build-apk.yml .github\workflows\build-apk.yml
copy github-workflows\deploy-pages.yml .github\workflows\deploy-pages.yml
git add .github
git commit -m "active workflows"
git push
```

Linux / macOS :

```bash
mkdir -p .github/workflows
cp github-workflows/build-apk.yml .github/workflows/build-apk.yml
cp github-workflows/deploy-pages.yml .github/workflows/deploy-pages.yml
git add .github
git commit -m "active workflows"
git push
```

## 3. Activer GitHub Pages (une fois)

Repo → **Settings → Pages** → **Source : GitHub Actions**. La démo web
(`app/src/main/assets/www`, pilotée par `js/config.js`) se publie à chaque push.

## 4. Récupérer l'APK

Repo → onglet **Actions** → run **Build APK (R8 Launcher)** → en bas,
artefact **R8-Launcher-APK** → `app-debug.apk`. Si le run est rouge, ouvre-le :
l'étape **Contrôle du projet** dit quel fichier manque à la racine.

## 5. Installer

APK sur clé USB → autoradio : gestionnaire de fichiers → **Installer** →
bouton Accueil → **R8 Launcher / Toujours**. Détail + Android Auto :
voir `src/android/README_APK.md` du projet vitrine et `docs/CAN.md`.

## Dépannage

- **Le workflow ne se lance pas** : vérifie que les fichiers sont bien en
  `.github/workflows/` (avec le point), pas dans `github-workflows/`.
- **Pages : 404** : Settings → Pages → Source = GitHub Actions, puis relance le run.
- **Build : erreur SDK** : l'étape Android SDK l'installe ; en local (Android Studio),
  ouvre le dossier qui contient `settings.gradle`.
- **Clé de signature** : l'APK debug suffit pour tester. Pour les mises à jour sans
  perdre le carnet d'entretien, signe toujours avec la même clé (voir ADAPTER.md §4).
