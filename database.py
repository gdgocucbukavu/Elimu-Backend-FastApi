# Importation des fonctions nécessaires depuis SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Importation de l'URL de la base de données depuis le fichier de configuration
from config import DATABASE_URL

# ======================================================================
# Configuration du moteur SQLAlchemy en fonction du type de base de données
# ======================================================================

# Vérification si l'URL de la base de données concerne SQLite.
# SQLite nécessite un argument spécifique "check_same_thread" pour permettre
# l'utilisation de la base de données dans un contexte multi-thread.
if "sqlite" in DATABASE_URL.lower():
    engine = create_engine(
        DATABASE_URL,  # URL de connexion à la base de données SQLite
        connect_args={"check_same_thread": False}  # Permet l'accès multi-thread
    )
else:
    # Pour les autres SGBD (ex : PostgreSQL, MySQL, etc.), on configure le pooling
    engine = create_engine(
        DATABASE_URL,  # URL de connexion à la base de données
        pool_size=10,  # Nombre maximum de connexions à maintenir dans le pool
        max_overflow=20  # Nombre maximum de connexions supplémentaires en cas de charge élevée
    )

# ======================================================================
# Création d'une instance de session pour interagir avec la base de données
# ======================================================================

# SessionLocal est une usine (factory) qui crée de nouvelles sessions
# SQLAlchemy configurées avec le moteur ci-dessus.
SessionLocal = sessionmaker(
    autocommit=False,  # Désactive l'autocommit, il faut explicitement valider les transactions
    autoflush=False,  # Désactive l'autoflush pour un meilleur contrôle sur la synchronisation des objets avec la base
    bind=engine  # Lie la session au moteur configuré
)

# ======================================================================
# Définition de la base de déclaration pour les modèles
# ======================================================================

# 'Base' est la classe de base que toutes les classes de modèle doivent hériter.
# Elle est utilisée pour enregistrer les métadonnées et permettre la création des tables.
Base = declarative_base()


# ======================================================================
# Définition d'une fonction génératrice pour la gestion de sessions de base de données
# ======================================================================

def get_db():
    """
    Générateur de sessions de base de données.

    Ce générateur est utile dans un contexte d'injection de dépendances,
    par exemple dans des applications FastAPI, afin de fournir une session
    pour chaque requête et de garantir sa fermeture après utilisation.

    Yields:
        db: Une instance de session SQLAlchemy.
    """
    # Création d'une nouvelle session
    db = SessionLocal()
    try:
        # Fournit la session au contexte appelant
        yield db
    finally:
        # Assure la fermeture de la session même en cas d'exception
        db.close()
