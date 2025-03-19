from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, database, schemas

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def track_progress(progress: schemas.ProgressCreate, db: Session = Depends(get_db)):
    return crud.track_progress(db, progress.video_id, progress.mentee_email)
