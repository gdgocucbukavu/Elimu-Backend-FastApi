

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# ==============================================================================
# Classe représentant une vidéo dans la base de données
# ==============================================================================
class Video(Base):
    __tablename__ = "videos"  # Nom de la table dans la base de données

    # --------------------------------------------------------------------------
    # Définition des colonnes
    # --------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)
    # URL unique de la vidéo YouTube
    youtube_url = Column(String, unique=True, nullable=False)
    # Email du mentor associé à la vidéo
    mentor_email = Column(String, nullable=False)
    # Catégorie de la vidéo (ex: tutoriel, entretien, etc.)
    category = Column(String, nullable=False)
    # Évaluation par étoiles, valeur par défaut 0.0
    stars = Column(Float, default=0.0)
    # Nombre de likes
    likes = Column(Integer, default=0)
    # Nombre de vues
    views = Column(Integer, default=0)
    # Date de publication, ici par défaut la date et l'heure actuelles
    publication_date = Column(DateTime, default=datetime.utcnow)
    # Titre de la vidéo (peut être optionnel)
    title = Column(String, nullable=True)
    # Description de la vidéo (peut être optionnel)
    description = Column(String, nullable=True)
    # Champ pour l'ordre d'affichage. Le nom "order" est un mot réservé,
    # donc il est explicitement défini dans la base avec des guillemets.
    order = Column("order", Integer, nullable=False)


    reviews = relationship("Review", back_populates="video",
                           cascade="all, delete-orphan")  # Ajout de la relation reviews

    # --------------------------------------------------------------------------
    # Définition de la relation avec la table Progress
    # --------------------------------------------------------------------------
    # 'progresses' sera un attribut list contenant toutes les entrées de progression associées à cette vidéo.
    # cascade="all, delete-orphan" permet de supprimer toutes les progressions associées si la vidéo est supprimée.
    progresses = relationship("Progress", back_populates="video", cascade="all, delete-orphan")


# ==============================================================================
# Classe représentant la progression du visionnage d'une vidéo
# ==============================================================================
class Progress(Base):
    __tablename__ = "progress"  # Nom de la table dans la base de données

    # --------------------------------------------------------------------------
    # Définition des colonnes
    # --------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)
    # Clé étrangère liant la progression à une vidéo spécifique.
    # ondelete="CASCADE" assure que la progression sera supprimée si la vidéo associée est supprimée.
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    # Email du mentee pour lequel la progression est enregistrée
    mentee_email = Column(String, nullable=False)
    # Quantité de la vidéo regardée (par exemple, en secondes ou en pourcentage)
    watched = Column(Integer, default=0)

    # --------------------------------------------------------------------------
    # Définition de la relation avec la table Video
    # --------------------------------------------------------------------------
    # Cet attribut permet d'accéder facilement à l'objet Video associé à cette progression.
    video = relationship("Video", back_populates="progresses")


class Review(Base):

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    mentee_email = Column(String, nullable=False)
    stars = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video", back_populates="reviews")