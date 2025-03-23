from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

# ==============================================================================
# Schéma de création d'une vidéo
# ==============================================================================
class VideoCreate(BaseModel):
    # URL de la vidéo YouTube à créer
    youtube_url: str
    # Email du mentor associé à la vidéo
    mentor_email: str
    # Catégorie à laquelle appartient la vidéo
    category: str
    # Ordre de la vidéo dans une liste ou séquence (optionnel, calculé dynamiquement si non fourni)
    order: Optional[int] = None

# ==============================================================================
# Schéma de réponse pour une vidéo
# Ce modèle hérite de VideoCreate pour réutiliser les champs de base,
# et ajoute des informations supplémentaires gérées par la base de données.
# ==============================================================================
class VideoResponse(VideoCreate):
    # Identifiant unique de la vidéo
    id: int
    # Titre de la vidéo
    title: str
    # Description de la vidéo
    description: str
    # Date de publication de la vidéo
    publication_date: datetime
    # Nombre de vues de la vidéo
    views: int
    # Nombre de likes de la vidéo
    likes: int
    order: Optional[int] = None  # Optionnel, calculé dynamiquement si non fourni
    # Liste de progressions liées à la vidéo
    progresses: List["ProgressResponse"] = []
    # Liste des avis (reviews) liés à la vidéo
    reviews: List["ReviewResponse"] = []

    class Config:
        # Permet de travailler avec des objets ORM (ex : SQLAlchemy) sans conversion explicite
        orm_mode = True

# ==============================================================================
# Schéma de mise à jour d'une vidéo
# Chaque champ est optionnel pour permettre une mise à jour partielle
# ==============================================================================
class VideoUpdate(BaseModel):
    # Nouveau titre (optionnel)
    title: Optional[str] = None
    # Nouvelle description (optionnel)
    description: Optional[str] = None
    # Nouvelle catégorie (optionnel)
    category: Optional[str] = None
    # Nouvel ordre (optionnel)
    order: Optional[int] = None

# ==============================================================================
# Schéma de création d'une progression de visionnage
# ==============================================================================
class ProgressCreate(BaseModel):
    # Identifiant de la vidéo pour laquelle la progression est enregistrée
    video_id: int
    # Email du mentee (utilisateur) pour lequel la progression est suivie
    mentee_email: str

# ==============================================================================
# Schéma de réponse pour une progression de visionnage
# ==============================================================================
class ProgressResponse(BaseModel):
    # Identifiant unique de la progression
    id: int
    # Identifiant de la vidéo associée à cette progression
    video_id: int
    # Email du mentee (utilisateur)
    mentee_email: str
    # Temps ou nombre de secondes regardées (ou autre métrique de suivi)
    watched: int

    class Config:
        # Active le mode ORM pour faciliter la conversion des objets SQLAlchemy
        orm_mode = True

# ==============================================================================
# Schéma de création d'une review (avis)
# ==============================================================================
class ReviewCreate(BaseModel):
    video_id: int
    mentee_email: str
    stars: int = Field(..., ge=1, le=5)  # Entre 1 et 5 étoiles
    comment: Optional[str] = None

# ==============================================================================
# Schéma de réponse pour une review
# ==============================================================================
class ReviewResponse(BaseModel):
    id: int
    video_id: int
    mentee_email: str
    stars: int
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

# ==============================================================================
# Schéma de création d'un utilisateur
# ==============================================================================
class UserCreate(BaseModel):
    # Nom de l'utilisateur
    name: str
    # Email de l'utilisateur
    email: str
    # Indique si l'utilisateur est connecté (optionnel, par défaut False)
    is_logged_in: Optional[bool] = False
    # URL de la photo de profil (optionnel)
    profile_picture_uri: Optional[str] = ""
    # Track ou parcours de l'utilisateur
    track: str
    # Mentor associé à l'utilisateur
    mentor: str

# ==============================================================================
# Schéma de réponse pour un utilisateur
# ==============================================================================
class UserResponse(BaseModel):
    # Identifiant unique de l'utilisateur
    id: int
    # Nom de l'utilisateur
    name: str
    # Email de l'utilisateur
    email: str
    # Indicateur de connexion
    is_logged_in: bool
    # URL de la photo de profil
    profile_picture_uri: str
    # Track ou parcours de l'utilisateur
    track: str
    # Mentor associé à l'utilisateur
    mentor: str
    # Date de création du compte
    created_at: datetime

    class Config:
        orm_mode = True

# Mise à jour des références en avant pour résoudre "ProgressResponse" et "ReviewResponse"
VideoResponse.update_forward_refs()
