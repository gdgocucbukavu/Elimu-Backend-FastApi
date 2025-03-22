from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, database, schemas, models

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def track_progress(progress: schemas.ProgressCreate, db: Session = Depends(get_db)):
    """
    Enregistre la progression d'une vidéo pour un utilisateur.

    Étapes :
    1. Vérifie si la vidéo existe dans la base de données.
    2. Si la vidéo n'existe pas, lève une exception HTTP 404 avec un message d'erreur approprié.
    3. Si la vidéo existe, appelle la fonction CRUD pour enregistrer la progression et retourne le résultat.

    Args:
        progress (schemas.ProgressCreate): Objet contenant les informations sur la progression (ID de la vidéo, email du mentee, etc.).
        db (Session, optionnel): Session de base de données injectée par la dépendance get_db.

    Returns:
        Le résultat de l'opération de suivi de progression, tel que défini dans la couche CRUD.

    Raises:
        HTTPException: Si la vidéo correspondant à progress.video_id n'est pas trouvée.
    """
    # Vérification de l'existence de la vidéo en interrogeant la base de données
    video = db.query(models.Video).filter(models.Video.id == progress.video_id).first()

    # Si la vidéo n'existe pas, on lève une exception HTTP 404
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")

    # Enregistrement de la progression via la fonction CRUD et retour du résultat
    return crud.track_progress(db, progress.video_id, progress.mentee_email)
