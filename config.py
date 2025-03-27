import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

# URL de la base de données avec une valeur par défaut pour le développement local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

if not DATABASE_URL:
    raise ValueError("La variable d'environnement DATABASE_URL doit être définie.")

# Clé API YouTube : essentielle pour les appels à l'API YouTube
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise ValueError("La variable d'environnement YOUTUBE_API_KEY doit être définie")
