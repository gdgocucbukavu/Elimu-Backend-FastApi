from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class VideoCreate(BaseModel):
    youtube_url: str
    mentor_email: str
    category: str

class VideoResponse(VideoCreate):
    id: int
    title: str
    description: str
    publication_date: datetime
    views: int
    likes: int

    class Config:
        orm_mode = True



class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None


class ProgressCreate(BaseModel):
    video_id: int
    mentee_email: str
