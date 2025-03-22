from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, database, schemas, models

# Création du routeur FastAPI. Vous pouvez ajouter un préfixe et des tags si nécessaire,
# par exemple : APIRouter(prefix="/videos", tags=["Videos"])
router = APIRouter()


# Dépendance pour obtenir une session de base de données
def get_db():
    """
    Générateur de sessions de base de données.
    Récupère une session depuis database.SessionLocal et s'assure de sa fermeture après utilisation.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.VideoResponse, status_code=201)
def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle vidéo dans la base de données.

    Étapes :
    1. Vérifie si une vidéo avec la même URL YouTube existe déjà.
       Si c'est le cas, renvoie une erreur HTTP 400 pour éviter les doublons.
    2. Si aucune vidéo existante n'est trouvée, appelle la fonction CRUD pour créer la vidéo.

    Args:
        video (schemas.VideoCreate): Schéma contenant les informations de création de la vidéo
                                     (youtube_url, mentor_email, category, [optionnellement order]).
        db (Session): Session de base de données fournie par la dépendance get_db.

    Returns:
        schemas.VideoResponse: La vidéo nouvellement créée.

    Raises:
        HTTPException: Si une vidéo avec la même URL existe déjà.
    """
    # Vérification si la vidéo existe déjà dans la base de données
    existing_video = db.query(models.Video).filter(models.Video.youtube_url == video.youtube_url).first()
    if existing_video:
        raise HTTPException(status_code=400, detail="Une vidéo avec cette URL existe déjà")

    # Appel à la couche CRUD pour créer la vidéo
    return crud.create_video(db, video.youtube_url, video.mentor_email, video.category, video.order)


@router.get("/{video_id}", response_model=schemas.VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """
    Récupère une vidéo en fonction de son ID.

    Args:
        video_id (int): L'identifiant de la vidéo.
        db (Session): Session de base de données.

    Returns:
        schemas.VideoResponse: La vidéo correspondante.

    Raises:
        HTTPException: Si la vidéo n'est pas trouvée (erreur 404).
    """
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")
    return video


@router.put("/{video_id}", response_model=schemas.VideoResponse)
def update_video(video_id: int, video_update: schemas.VideoUpdate, db: Session = Depends(get_db)):
    """
    Met à jour les informations d'une vidéo.

    Args:
        video_id (int): L'identifiant de la vidéo à mettre à jour.
        video_update (schemas.VideoUpdate): Schéma contenant les nouvelles valeurs (title, description, category).
        db (Session): Session de base de données.

    Returns:
        schemas.VideoResponse: La vidéo mise à jour.

    Raises:
        HTTPException: Si la vidéo n'est pas trouvée.
    """
    video = crud.update_video(db, video_id, video_update.title, video_update.description, video_update.category)
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")
    return video


@router.put("/{video_id}/update_order", response_model=schemas.VideoResponse)
def update_video_order(video_id: int, new_order: int, db: Session = Depends(get_db)):
    """
    Met à jour l'ordre d'une vidéo.

    Args:
        video_id (int): L'identifiant de la vidéo.
        new_order (int): La nouvelle valeur de l'ordre.
        db (Session): Session de base de données.

    Returns:
        schemas.VideoResponse: La vidéo avec l'ordre mis à jour.

    Raises:
        HTTPException: Si la vidéo n'est pas trouvée.
    """
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")

    # Mise à jour de l'ordre de la vidéo
    video.order = new_order
    db.commit()  # Validation des modifications en base
    db.refresh(video)  # Rafraîchit l'objet vidéo avec les données mises à jour
    return video


@router.delete("/{video_id}", status_code=204)
def delete_video(video_id: int, db: Session = Depends(get_db)):
    """
    Supprime une vidéo en fonction de son ID.

    Args:
        video_id (int): L'identifiant de la vidéo à supprimer.
        db (Session): Session de base de données.

    Returns:
        dict: Message de succès en cas de suppression.

    Raises:
        HTTPException: Si la vidéo n'est pas trouvée.
    """
    video = crud.delete_video(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")

    # On retourne un message de succès. Le code de status 204 (No Content) signifie généralement
    # qu'il n'y a pas de contenu retourné, mais ici nous renvoyons un message explicatif.
    return {"message": "Vidéo supprimée avec succès"}


@router.get("/videos/", response_model=list[schemas.VideoResponse])
def get_all_videos(db: Session = Depends(get_db)):
    """
    Récupère l'ensemble des vidéos de la base de données.

    Trie les vidéos par catégorie, puis par ordre défini dans chaque catégorie.

    Args:
        db (Session): Session de base de données.

    Returns:
        list[schemas.VideoResponse]: Liste des vidéos.
    """
    videos = db.query(models.Video).order_by(models.Video.category, models.Video.order).all()
    return videos
