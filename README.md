# Elimu Backend

Ce dépôt contient le backend de la plateforme **Elimu**, qui permet de gérer des vidéos YouTube via une API FastAPI et de stocker leurs informations dans une base de données MySQL. Le projet inclut également des exemples d'API CRUD (création, lecture, mise à jour et suppression) ainsi qu'une fonction pour récupérer les données d'une vidéo YouTube à partir de son URL.

## Table des matières

- [Prérequis](#prérequis)
- [Installation](#installation)
  - [1. Cloner le dépôt](#1-cloner-le-dépôt)
  - [2. Configurer l'environnement Python](#2-configurer-lenvironnement-python)
  - [3. Installer les dépendances](#3-installer-les-dépendances)
  - [4. Configurer les variables d'environnement](#4-configurer-les-variables-denvironnement)
  - [5. Configurer la base de données avec XAMPP](#5-configurer-la-base-de-données-avec-xampp)
- [Lancement de l'application](#lancement-de-lapplication)
- [Structure du projet](#structure-du-projet)
- [Utilisation des endpoints](#utilisation-des-endpoints)
- [Licence](#licence)

## Prérequis

- **Python 3.8+**
- **pip**
- **Virtualenv** (optionnel, mais recommandé)
- **XAMPP** (pour MySQL)
- Une clé API YouTube

## Installation

### 1. Cloner le dépôt

Clone le dépôt sur ta machine locale :

```bash
git clone https://github.com/babekaja/elimu-backend.git
cd elimu-backend
```

### 2. Configurer l'environnement Python

Crée un environnement virtuel :

#### Sous Windows :

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Sous Linux/Mac :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

Installe toutes les dépendances via le fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

#### Contenu minimal du `requirements.txt` :

```txt
fastapi
uvicorn
sqlalchemy
mysql-connector-python
python-dotenv
requests
```

### 4. Configurer les variables d'environnement

Crée un fichier `.env` à la racine du projet et ajoute-y les variables suivantes :

```ini
DATABASE_URL=mysql+mysqlconnector://root:@localhost/elimu
YOUTUBE_API_KEY=VOTRE_CLE_API_YOUTUBE
```

Ce fichier sera chargé automatiquement par `python-dotenv` (assure-toi d'appeler `load_dotenv()` dans ton code, par exemple dans `config.py`).

### 5. Configurer la base de données avec XAMPP

#### Installer et lancer XAMPP :

- Télécharge et installe XAMPP.
- Lance le panneau de contrôle XAMPP et démarre le service MySQL.

#### Créer la base de données :

- Connecte-toi à phpMyAdmin via [http://localhost/phpmyadmin](http://localhost/phpmyadmin) et crée une base de données nommée `elimu` (ou utilise le script SQL fourni dans le répertoire `sql/` si présent).

## Lancement de l'application

Lancer le backend FastAPI :

Depuis la racine du projet, exécute :

```bash
uvicorn main:app --reload
```

L'application sera accessible à [http://127.0.0.1:8000](http://127.0.0.1:8000).

La documentation interactive se trouve à [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Tester les endpoints :

Utilise un outil comme **Postman** ou la documentation interactive de **FastAPI** pour tester les endpoints (création, lecture, mise à jour et suppression de vidéos).

## Structure du projet

```
elimu-backend/
├── main.py               # Point d'entrée de l'application FastAPI
├── config.py             # Configuration (variables d'environnement, etc.)
├── database.py           # Connexion à la base de données via SQLAlchemy
├── models.py             # Définition des modèles SQLAlchemy (Video, Progress, etc.)
├── schemas.py            # Schémas Pydantic pour validation des données
├── crud.py               # Fonctions CRUD pour la gestion des vidéos et progression
├── youtube_api.py        # Intégration avec l'API YouTube (extraction de l'ID, récupération des données)
├── routers/
│   ├── video.py          # Routes FastAPI pour la gestion des vidéos
│   └── progress.py       # Routes FastAPI pour la gestion de la progression
├── requirements.txt      # Liste des dépendances Python
├── .env                  # Fichier de variables d'environnement (non versionné)
└── README.md             # Ce fichier README
```

## Utilisation des endpoints

### Créer une vidéo

**Endpoint** : `POST /videos/`

**Body JSON** :

```json
{
  "youtube_url": "https://youtu.be/dQw4w9WgXcQ",
  "mentor_email": "mentor@example.com",
  "category": "Flutter"
}
```

### Récupérer une vidéo

**Endpoint** : `GET /videos/{video_id}`

### Mettre à jour une vidéo

**Endpoint** : `PUT /videos/{video_id}`

**Body JSON (exemple)** :

```json
{
  "title": "Nouveau titre",
  "description": "Nouvelle description",
  "category": "Nouvelle Catégorie"
}
```

### Supprimer une vidéo

**Endpoint** : `DELETE /videos/{video_id}`



**Remarques** :

- **XAMPP & MySQL** : Assure-toi que le service MySQL est lancé via XAMPP avant de démarrer l'application.
- **Variables d'environnement** : Ne partage pas ta clé API publiquement. Utilise un fichier `.env` et ajoute-le à ton fichier `.gitignore`.

N'hésite pas à contribuer ou à signaler des problèmes via les Issues du dépôt.

**Happy coding! 🚀**

# Elimu-backend-FastApi
# Elimu-Backend-FastApi
