from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, database, schemas, models

# router = APIRouter(prefix="/videos", tags=["Videos"]
router = APIRouter()

# Comme ceci j'ai déjà ajouté dans database.py tu peux l'appeler simplement
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.VideoResponse) #status_code = 201
def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    """
    on n'est des developpeurs il faut toujours une vérification si la vidéo existe déjà bien qu'il est.
    existing_video = db.query(models.Video).filter(models.Video.youtube_url == video.youtube_url).first()
    if existing_video :
        raise HTTPException(status_code = 400, détail = " Une Vidéo avec cette URL existe déjà")
    puis 👇🏾👇🏾
    """
    
    return crud.create_video(db, video.youtube_url, video.mentor_email, video.category) # (vidéo.ordre ) pour s'assurer que la vidéo est créée par ord

@router.get("/{video_id}", response_model=schemas.VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")
    return video
@router.put("/{video_id}", response_model=schemas.VideoResponse)
def update_video(video_id: int, video_update: schemas.VideoUpdate, db: Session = Depends(get_db)):
    video = crud.update_video(db, video_id, video_update.title, video_update.description, video_update.category)
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")
    return video


@router.delete("/{video_id}") #Status_code = 204
def delete_video(video_id: int, db: Session = Depends(get_db)):
    video = crud.delete_video(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")
    return {"message": "Vidéo supprimée avec succès"}
# Pour éviter le doublons uje fois du route écrit router.get("/")
@router.get("/videos/", response_model=list[schemas.VideoResponse])
def get_all_videos(db: Session = Depends(get_db)):
    videos = db.query(models.Video).all()
    return videos

