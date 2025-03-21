from typing import Optional #, List

from pydantic import BaseModel
from datetime import datetime

class VideoCreate(BaseModel):
    youtube_url: str
    mentor_email: str
    category: str
    # ordre : int 

class VideoResponse(VideoCreate):
    id: int
    title: str #Optional[str] = None
    description: str #Optional[str] = None
    publication_date: datetime #Optional[str] = None
    views: int
    likes: int
    # une liset de progressions liées à la vidéo
    # progresses : List["ProgressResponse"] = []

    class Config:
        orm_mode = True



class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    # ordre : int |None = None


class ProgressCreate(BaseModel):
    video_id: int
    mentee_email: str
# le schéma de réponse pour une progression 
"""
class ProgressResponse(BaseModel):
    id : int
    video_id : int
    mentee_email : str
    watched : int

    class Config : 
        orm_mode = True

        """
