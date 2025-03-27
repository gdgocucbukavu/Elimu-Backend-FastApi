from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
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
    # URL unique de la vidéo YouTube (ici, on stocke l'ID de la vidéo)
    youtube_url = Column(String, unique=True, nullable=False)
    # Email du mentor associé à la vidéo
    mentor_email = Column(String, nullable=False)
    # Catégorie de la vidéo (ex: tutoriel, entretien, etc.)
    category = Column(String, nullable=False)
    # Note moyenne calculée à partir des avis (stars), initialisée à 0.0
    stars = Column(Float, default=0.0)
    # Nombre de likes
    likes = Column(Integer, default=0)
    # Nombre de vues
    views = Column(Integer, default=0)
    # Date de publication ; par défaut, la date et l'heure actuelles
    publication_date = Column(DateTime, default=datetime.utcnow)
    # Titre de la vidéo (optionnel)
    title = Column(String, nullable=True)
    # Description de la vidéo (optionnel)
    description = Column(String, nullable=True)
    # Ordre d'affichage de la vidéo (le nom "order" étant un mot réservé, on le définit explicitement)
    order = Column("order", Integer, nullable=False)

    # --------------------------------------------------------------------------
    # Relations avec d'autres tables
    # --------------------------------------------------------------------------
    # Relation avec la table Review pour accéder aux avis de la vidéo.
    reviews = relationship("Review", back_populates="video", cascade="all, delete-orphan")
    # Relation avec la table Progress pour accéder aux progressions de visionnage.
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
    # ondelete="CASCADE" permet de supprimer la progression si la vidéo associée est supprimée.
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    # Email du mentee pour lequel la progression est enregistrée.
    mentee_email = Column(String, nullable=False)
    # Indique la quantité de la vidéo regardée (par exemple en secondes ou en pourcentage).
    watched = Column(Integer, default=0)

    # --------------------------------------------------------------------------
    # Relation avec la table Video
    # --------------------------------------------------------------------------
    # Permet d'accéder à l'objet Video associé à cette progression.
    video = relationship("Video", back_populates="progresses")


# ==============================================================================
# Classe représentant un avis sur une vidéo
# ==============================================================================
class Review(Base):
    __tablename__ = "reviews"  # Nom de la table dans la base de données

    # --------------------------------------------------------------------------
    # Définition des colonnes
    # --------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)
    # Clé étrangère liant l'avis à une vidéo spécifique.
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    # Email du mentee qui a laissé l'avis.
    mentee_email = Column(String, nullable=False)
    # Évaluation par étoiles donnée dans l'avis (valeur attendue entre 1 et 5).
    stars = Column(Integer, nullable=False)
    # Commentaire associé à l'avis (optionnel).
    comment = Column(Text, nullable=True)
    # Date de création de l'avis ; par défaut, la date et l'heure actuelles.
    created_at = Column(DateTime, default=datetime.utcnow)

    # --------------------------------------------------------------------------
    # Relation avec la table Video
    # --------------------------------------------------------------------------
    # Permet d'accéder à l'objet Video associé à cet avis.
    video = relationship("Video", back_populates="reviews")


# ==============================================================================
# Classe représentant un utilisateur dans la base de données
# ==============================================================================
class User(Base):
    __tablename__ = "users"  # Nom de la table dans la base de données

    # --------------------------------------------------------------------------
    # Définition des colonnes
    # --------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)
    # Nom de l'utilisateur.
    name = Column(String, nullable=False)
    # Email unique de l'utilisateur.
    email = Column(String, unique=True, index=True, nullable=False)
    # Indique si l'utilisateur est connecté.
    is_logged_in = Column(Boolean, default=False)
    # URL de la photo de profil de l'utilisateur.
    profile_picture_uri = Column(String, default="")
    # Track ou parcours de l'utilisateur.
    track = Column(String, nullable=False)
    # Mentor associé à l'utilisateur.
    mentor = Column(String, nullable=False)
    # Date de création du compte ; par défaut, la date et l'heure actuelles.
    created_at = Column(DateTime, default=datetime.utcnow)
