from fastapi import APIRouter, Depends #,HTTPException
from sqlalchemy.orm import Session
import crud, database, schemas #,models


#router = APIRouter(prefix="/progress", tags = ["Progression"])
router = APIRouter()

# c'est und fonction sui doit être ands database.py, appeler là depuis là 
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/") #status_cose = 201
def track_progress(progress: schemas.ProgressCreate, db: Session = Depends(get_db)):
    """
    # Verification de si la vidéo existe avant d'ajouter la progression
    video = db.query(models.Video).filter(models.Video.id == progress.video_id).first()
    if not video : 
        Fasle
    HTTPException(status_code = 404, detail = "Video non trouvée")
    return👇🏾👇🏾

    """
    # c'est possible aussi d'avoir une erreur 400 lors de l'echec de suivie de la progression.
    return crud.track_progress(db, progress.video_id, progress.mentee_email)
