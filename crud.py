from sqlalchemy.orm import Session
from models import Video, Progress
from youtube_api import get_youtube_video_data
from datetime import datetime
from urllib.parse import urlparse, parse_qs
# essaie de gérer les erreurs, Donc appel du module HttpException

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

def create_video(db: Session, youtube_input: str, mentor_email: str, category: str): # ajouter la variable ordre
    """
    Crée une entrée vidéo dans la base de données à partir d'une URL YouTube ou d'un ID.
    La fonction extrait l'ID de la vidéo et récupère les informations associées.
    """
    # Vérifier si l'entrée est une URL et extraire l'ID
    if "youtu" in youtube_input:
        video_id = extract_video_id(youtube_input)
    else:
        video_id = youtube_input  # On considère que c'est déjà un ID
    # Gestion d'erreur en cas not video_id ca raise status_code 400
    # et aussi vérifier si la vidéo existe déjà
    """
    existing_video = db.query(Video).filter(Video.youtube_url == youtube_input).first()
    if existing_video : 
        raise HTTPException(status_code = 400, detail = "Crtte video est déjà enregistré")

        """"
    # Récupérer les données de la vidéo en utilisant l'ID
    video_data = get_youtube_video_data(video_id)
    if video_data is None:
        print("Impossible de récupérer les données de la vidéo.")
        return None
    #Gerer ici l'erreur aussi une fois ca arrive d'etre impossible de récupérer les données de la vidéo.

    video = Video(
        youtube_url=video_data["video_id"],  # Stocke uniquement l'ID de la vidéo
        mentor_email=mentor_email,
        category=category,
        # ordre = ordre
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
    # la progression doit se faire si la vidéo existe. on peut vérifier avant si la vidéo existe et puis si la progression existe aussi
    progress = db.query(Progress).filter(Progress.video_id == video_id, Progress.mentee_email == mentee_email).first()
    if progress:
        progress.watched += 1
    else:
        progress = Progress(video_id=video_id, mentee_email=mentee_email, watched=1)
        db.add(progress)
    db.commit()
    return progress

def update_video(db: Session, video_id: int, title: str = None, description: str = None, category: str = None): # ajout de la variable ordre ( ordre : int | None)
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        return None

    if title:
        video.title = title
    if description:
        video.description = description
    if category:
        video.category = category
    """ 
    une mise en jour de l'ordre
    if ordre is not None : 
        video.ordre = ordre
    """

    db.commit()
    db.refresh(video)
    return video

def delete_video(db: Session, video_id: int):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        return None
    #Gestion d'erreur pour des vidéos si qui seront non trouvées au lieu de None

    db.delete(video)
    db.commit()
    return video
""" 

une fonction pour récupérer toutes les vidéos triées 
def get_all_videos(db: Session):
    return db.query(models.Video).order_by(models.Video.ordre).all()
    """
