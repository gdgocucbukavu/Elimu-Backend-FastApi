from sqlalchemy.orm import Session
from models import Video, Progress
from youtube_api import get_youtube_video_data
from datetime import datetime
from urllib.parse import urlparse, parse_qs

def extract_video_id(youtube_url: str) -> str:
    """
    Extrait l'ID de la vidéo depuis une URL YouTube.
    Fonctionne pour les formats suivants :
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    """
    parsed_url = urlparse(youtube_url)
    # Si l'URL est de type youtu.be
    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")
    # Si l'URL est de type youtube.com
    if "youtube.com" in parsed_url.netloc:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    return None

def create_video(db: Session, youtube_input: str, mentor_email: str, category: str):
    """
    Crée une entrée vidéo dans la base de données à partir d'une URL YouTube ou d'un ID.
    La fonction extrait l'ID de la vidéo et récupère les informations associées.
    """
    # Vérifier si l'entrée est une URL et extraire l'ID
    if "youtu" in youtube_input:
        video_id = extract_video_id(youtube_input)
    else:
        video_id = youtube_input  # On considère que c'est déjà un ID

    # Récupérer les données de la vidéo en utilisant l'ID
    video_data = get_youtube_video_data(video_id)
    if video_data is None:
        print("Impossible de récupérer les données de la vidéo.")
        return None

    video = Video(
        youtube_url=video_data["video_id"],  # Stocke uniquement l'ID de la vidéo
        mentor_email=mentor_email,
        category=category,
        title=video_data["title"],
        description=video_data["description"],
        publication_date=datetime.fromisoformat(
            video_data["publication_date"].replace("Z", "+00:00")
        ),
        views=video_data["views"],
        likes=video_data["likes"]
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    return video

def track_progress(db: Session, video_id: int, mentee_email: str):
    progress = db.query(Progress).filter(Progress.video_id == video_id, Progress.mentee_email == mentee_email).first()
    if progress:
        progress.watched += 1
    else:
        progress = Progress(video_id=video_id, mentee_email=mentee_email, watched=1)
        db.add(progress)
    db.commit()
    return progress

def update_video(db: Session, video_id: int, title: str = None, description: str = None, category: str = None):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        return None

    if title:
        video.title = title
    if description:
        video.description = description
    if category:
        video.category = category

    db.commit()
    db.refresh(video)
    return video

def delete_video(db: Session, video_id: int):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        return None

    db.delete(video)
    db.commit()
    return video
