from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    youtube_url = Column(String, unique=True, nullable=False)
    mentor_email = Column(String, nullable=False)
    category = Column(String, nullable=False)
    stars = Column(Float, default=0.0)
    likes = Column(Integer, default=0)
    views = Column(Integer, default=0)
    publication_date = Column(DateTime)
    title = Column(String)
    description = Column(String)

class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, nullable=False)
    mentee_email = Column(String, nullable=False)
    watched = Column(Integer, default=0)