# Gestion de l’environnement virtuel Python

Un **environnement virtuel Python** est un espace isolé dans lequel tu peux installer des bibliothèques **sans impacter ton système** ni les autres projets.
Chaque projet peut ainsi avoir **ses propres versions** de packages, ce qui évite les conflits (par exemple : un projet nécessite Flask 2.0 et un autre Flask 3.0).

C’est une bonne pratique **indispensable** pour tous les projets Python.

---

## Création de l'environnement virtuel

### 1) Créer un environnement virtuel

```bash
python -m venv .venv
```

### 2) L’activer

**Linux / Mac :**

```bash
source .venv/bin/activate
```

**Windows :**

```bash
.venv\Scripts\activate
```

Une fois activé, ton terminal affichera généralement `(.venv)` au début de la ligne, preuve que l’environnement est actif.

---

## Installation des packages du projet

```bash
pip install pandas openpyxl requests python-dotenv
pip install jupyter  # Optionnel, pour les notebooks
```

---

## Enregistrer les dépendances – `requirements.txt`

Une fois que toutes les dépendances sont installées dans l'environnement virtuel, **enregistre-les dans un fichier** pour que quelqu’un d’autre (ou toi plus tard) puisse recréer le même environnement.

### Générer le fichier :

```bash
pip freeze > requirements.txt
```

Ce fichier liste précisément les **versions** installées (ex : `pandas==2.2.0`, etc.).

---

## Réinstaller les dépendances depuis `requirements.txt`

Quand quelqu’un récupère le projet (ou toi sur un autre poste), il suffit de :

1️⃣ Créer l’environnement virtuel :

```bash
python -m venv .venv
```

2️⃣ L’activer :

**Linux / Mac :**

```bash
source .venv/bin/activate
```

**Windows :**

```bash
.venv\Scripts\activate
```

3️⃣ Installer **toutes les dépendances en une seule commande** :

```bash
pip install -r requirements.txt
```

---

## Utilisation de l’environnement virtuel avec VS Code

Pour que VS Code travaille correctement avec ton environnement virtuel, le plus simple est :

1. **Avoir le dossier `.venv` à la racine du projet**
2. **Ouvrir le projet dans VS Code** (`Fichier > Ouvrir un dossier...`)
3. **Installer l’extension "Python" de Microsoft** (si ce n’est pas déjà fait)


### Activer automatiquement le venv dans le terminal intégré

VS Code peut activer automatiquement l’environnement virtuel quand tu ouvres un nouveau terminal.

Vérifie dans les paramètres que l’option suivante est activée :

* **Python › Terminal: Activate Environment** → `true`

Tu peux aussi forcer ces réglages au niveau du projet via un dossier `.vscode`.

Crée le fichier :
`/.vscode/settings.json`

Avec par exemple (pour **Windows**) :

```json
{
  "python.defaultInterpreterPath": ".venv\\Scripts\\python.exe",
  "python.terminal.activateEnvironment": true
}
```

Pour **Linux / Mac** :

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.terminal.activateEnvironment": true
}
```

---

## Ne jamais pousser `.venv` dans Git (très important)

Ton environnement virtuel peut peser des **centaines de Mo**.
Il dépend aussi de ton OS (Linux, Windows, Mac) → inutilisable pour quelqu’un d’autre.

Il **ne doit jamais être versionné**.

Ajoute donc un **`.gitignore`** à la racine du projet :

### `.gitignore`

```gitignore
.venv/
__pycache__/
```

Tu peux ajouter d’autres règles si nécessaire, mais ces deux-là sont indispensables.