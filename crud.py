from sqlalchemy.orm import Session
from models import Video, Progress
from youtube_api import get_youtube_video_data
from datetime import datetime


def create_video(db: Session, youtube_url: str, mentor_email: str, category: str):
    video_id = youtube_url.split("v=")[-1]
    video_data = get_youtube_video_data(video_id)
    print(video_data)
    video = Video(
        youtube_url=youtube_url,
        mentor_email=mentor_email,
        category=category,
        title=video_data["title"],
        description=video_data["description"],
        publication_date=datetime.fromisoformat(video_data["publication_date"].replace("Z", "+00:00")),
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

