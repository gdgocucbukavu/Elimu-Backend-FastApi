from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()



"""
Je suis entrain de comprendre petit à petit le code donc avant de 
prendre en compte ceci je dois parcours les tous pour savoir si 
c'est pas répèter.
Je copie oe même code d'haut avec un peu d'ajustage 


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Création du moteur SQLAlchemy avec support du pooling
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},  # Spécifique à SQLite
    pool_size=10,  # Nombre max de connexions en pool
    max_overflow=20,  # Nombre max de connexions supplémentaires en cas de charge élevée
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dépendance pour obtenir une session de base de données (suggestion Meschack)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
